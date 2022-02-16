import json
import os
import re

import scrapy
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()


class InstaSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = os.getenv('USERNAME')
    inst_password = os.getenv('PASSWORD')
    user_parse = 'techskills_2022'
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    post_hash = ''

    def parse(self, response: HtmlResponse, **kwargs):
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
        user_id = self.fetch_user_id(response.text, username)
        variables = {'id': user_id,
                     'first': 12}

        url_posts = f'{self.graphql_url}query_hash={self.post_hash}&{urlencode(variables)}'

        yield response.follow(url_posts,
                              callback=self.user_posts_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'variables': variables})

    def user_posts_parse(self, response: HtmlResponse, username, user_id, variables):
        print()

    @staticmethod
    def fetch_csrf_token(text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    @staticmethod
    def fetch_user_id(text, username):
        try:
            matched = re.search('{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text).group()
            return json.loads(matched).get('id')
        except:
            return re.findall('{\"id\":\"\\d+\"', text)[-1].split('"')[-2]
