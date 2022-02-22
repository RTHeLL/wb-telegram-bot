from typing import Union

import requests

from bs4 import BeautifulSoup
from classes.descriptors import RequestDataDescriptor, BSDescriptor, FullTitleDescriptor


class BaseParser:
    request_data = RequestDataDescriptor()

    def preparing_data(self, url: str) -> None:
        """
        Getting data from WB
        :param url:
        :return:
        """
        # try:
        self.request_data = requests.get(url)
        # except requests.exceptions.RequestException:
        #     self.request_data = None


class HTMLParser(BaseParser):
    __WB_URL = 'https://www.wildberries.ru/catalog/{article}/detail.aspx'

    bs = BSDescriptor()
    full_title_dict = FullTitleDescriptor()

    def preparing_data(self, article: Union[str, int], **kwargs) -> None:
        """
        Overriding the base method to prepare the required data
        :param article:
        :param kwargs:
        :return:
        """
        super().preparing_data(self.__WB_URL.format(article=article))
        self.bs = BeautifulSoup(self.request_data.text, 'lxml')
        try:
            __full_title_case = self.bs.find('h1', class_='same-part-kt__header').findAll('span')
            self.full_title_dict = dict([('brand', __full_title_case[0]), ('title', __full_title_case[1])])
        except AttributeError:
            self.full_title_dict = dict()

    def get_brand(self, article: Union[str, int]) -> str:
        """
        Getting a brand of product
        :param article:
        :return:
        """
        self.preparing_data(article)
        product_brand = self.full_title_dict.get('brand', 'No brand')
        return product_brand

    def get_title(self, article: Union[str, int]) -> str:
        """
        Getting a title of product
        :param article:
        :return:
        """
        self.preparing_data(article)
        product_title = self.full_title_dict.get('title', 'No title')
        return product_title


class JSONParser(BaseParser):
    __WB_URL = 'https://wbx-cosntent-v2.wbstatic.net/ru/{article}.json'

    def preparing_data(self, article: Union[str, int], **kwargs) -> None:
        super().preparing_data(self.__WB_URL.format(article=article))
        self.request_data = self.request_data.json()

    def get_brand(self, article: Union[str, int]) -> str:
        self.preparing_data(article)
        try:
            return self.request_data.get('selling').get('brand_name')
        except AttributeError:
            return 'No brand'

    def get_title(self, article: Union[str, int]) -> str:
        self.preparing_data(article)
        return self.request_data.get('imt_name', 'No title')
