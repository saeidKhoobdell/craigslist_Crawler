from myparser import AdvertisementParser
import json
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests
from config import STORAGE_TYPE
from storage import MongoStorage,FileStorage



class CrawlerBase(ABC):
    def __init__(self):
        self.storage = self.__set_storage()

    @staticmethod
    def __set_storage():
        if STORAGE_TYPE == 'mongo':
            return MongoStorage()
        return FileStorage()


    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def store(self,*args, **kwargs):
        pass

    @staticmethod
    def get(url):
        try:
            response = requests.get(url)
        except requests.HTTPError : return None

        return response


class LinkCrawler(CrawlerBase):
    def __init__(self, cities, link):
        self.link = link
        self.cities = cities
        super().__init__()

    def find_link(self,html_doc):
      soup = BeautifulSoup(html_doc, 'html.parser')
      links = soup.find_all('a', attrs={'class':'hdrlnk'})
      return links

    def get_pages(self, link):
        start = 0
        crawl = True
        adv_links = []
        while crawl:
          response = self.get(link+str(start))
          if response is None:
             crawl = False
             print('Ops')
             continue
          new_links = self.find_link(response.text)
          adv_links.extend(new_links)
          start += 120
          crawl = bool(len(new_links))
        return adv_links

    def get_cities(self):
        adv_links = []
        for city in self.cities:
          new_links = self.get_pages(self.link.format(city))
          print(f'{city} total: {len(new_links)}')
          adv_links.extend(new_links)
        return adv_links

    def start(self, store=False):
       adv_links = self.get_cities()
       if store :
         self.store([{'url': li.get('href') , 'flag': False} for li in adv_links])
       print(len(adv_links))
       return adv_links




    def store(self, data, *args):
        self.storage.store(data, 'advertisement_links')

class DataCrawler(CrawlerBase):
      def __init__(self):
        super().__init__()
        self.links = self.__load_links()
        self.parser = AdvertisementParser()


      def __load_links(self):
        return self.storage.load('advertisement_links',{'flag': False})


      def start(self, store=False):

        for link in self.links:
          response = requests.get(link["url"])
          data = self.parser.parser(response.text)

          if store :
            self.store(data,data.get('post_id', 'sample'))

          self.storage.update(link)

      def store(self, data, filename):
          self.storage.store(data,'advertisement_data')


class ImageCrawler(CrawlerBase):

    def __init__(self, *args, **kwargs):
      super().__init__()
      self.advertisement = self.__load_links()

    def __load_links(self):
        return self.storage.load('advertisement_data')


    @staticmethod
    def get(link):
      try:
        response = requests.get(link, stream=True)
      except:
        return None
      return response

    def start(self, store=True):
         for advertisement in self.advertisement:
          counter = 1
          for image in advertisement["images"]:
            response = self.get(image['url'])
            if store == True:
                self.store(response,advertisement['post_id'],counter)
            counter +=1

    def store(self,data, adv_id, counter):
        filename = f'{adv_id}-{counter}'
        return self.__save_to_disk(data,filename)


    def __save_to_disk(self,response, filename):
        with open(f'fixtures/images/{filename}.jpg', 'ab') as f:
           f.write(response.content)
           for _ in response.iter_content():
             f.write(response.content)
        print(filename)
        return filename