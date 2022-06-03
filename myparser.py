import requests
from bs4 import BeautifulSoup

class AdvertisementParser():
      def __init__(self):
        self.soup = None
      @property
      def title(self):
          title_tags =self.soup.find('span', attrs={'id':'titletextonly'})
          if title_tags:
              return title_tags.text
          return None
      @property
      def price(self):
          price_tags = self.soup.find('span', attrs={'class':'price'})
          if price_tags:
            return price_tags.text
          return None
      @property
      def post_id(self):
          id_selector ="body > section > section > section > div.postinginfos > p:nth-child(1)"
          post_id_tags = self.soup.select_one(id_selector)
          if post_id_tags:
            return post_id_tags.text.replace('post id: ','')
          return None
      @property
      def post_time(self):
          time_selector ='body > section > section > section > div.postinginfos > p.postinginfo.reveal > time'
          post_time_tags = self.soup.select_one(time_selector)
          if post_time_tags:
            return post_time_tags.attrs['datetime']
          return None
      @property
      def images(self):
        images_list = self.soup.find_all('img')
        images_sources = set([img.attrs['src'].replace('50x50c', '600x450') for img in images_list])
        return [{
                  "url": src,
                  'flag': False
                } for src in images_sources]


      def parser(self, html_docs):
        self.soup = BeautifulSoup(html_docs, 'html.parser')
        data = dict(title=self.title,
          price=self.price,
          post_id=self.post_id,
          post_time=self.post_time,
           images = self.images)
        return data

