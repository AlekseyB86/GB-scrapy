import re

import scrapy
from scrapy.http import HtmlResponse


class InstaSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'Alekseyb86'
    inst_password = '#PWD_INSTAGRAM_BROWSER:10:1645011472:AY5QAGDLHBY29czWEzT9dd2J6DnKWsW5+8ud1Zf5PSRdU4Vq9ey6S0gfOikY0gapUrokrqnD3W/1q9XGwsfW3InJGfsXFTHC48fie90n3mp18pVeYcMN2urU/BpMpmnWbJMlDrlNHsNM4tZ8qBM='
    user_parse = 'techskills_2022'

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.inst_login_link,
                                 method='POST',
                                 callback=self.login,
                                 formdata={'username': self.inst_login,
                                           'enc_password': self.inst_password},
                                 headers={'X-CSRFToken': csrf})

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data.get('authenticated'):
            yield response.follow(
                f'/{self.user_parse}/',
                callback=self.user_data_parse,
                cb_kwargs={'username': self.user_parse}
            )

    def user_data_parse(self, response: HtmlResponse, username):
        print()

    @staticmethod
    def fetch_csrf_token(text):
        return re.search(r'\"csrf_token\":\"(\w+)\"', text).group(1)
