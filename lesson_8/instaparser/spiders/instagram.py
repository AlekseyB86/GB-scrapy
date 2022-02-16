import json
# import os
import re

import scrapy
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem
from urllib.parse import urlencode
# from dotenv import load_dotenv
from copy import deepcopy

# load_dotenv()


class InstaSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'Onliskill_udm'
    inst_password = '#PWD_INSTAGRAM_BROWSER:10:1644677079:AX1QAFsfSNcVaV94ohcAQgPEbgInWVmdhDQtD3X4Mn3b5aFlf0DLvP8n0h4wptBszm9uImjjVyUqeS3THd6sK8aR1KwvCr7OiR7vfHLATExBtX1+YcoCXNVoCA48Xjf9J2L7N4/hewUPutX/rQGS'
    user_parse = ['techskills_2022', 'muzkom22']
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    post_hash = '8c2a529969ee035a5063f2fc8602a0fd'
    friends_url = 'https://i.instagram.com/api/v1/friendships'

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
            for user in self.user_parse:
                yield response.follow(
                    f'/{user}/',
                    callback=self.user_data_parse,
                    cb_kwargs={'username': user}
                )

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response, username)
        variables_followers = {
            'count': 12,
            'search_surface': 'follow_list_page'
        }
        variables_following = {
            'count': 12
        }
        url_followers = f'{self.friends_url}/{user_id}/followers/?{urlencode(variables_followers)}'
        url_following = f'{self.friends_url}/{user_id}/following/?{urlencode(variables_following)}'
        yield response.follow(
            url_followers,
            callback=self.user_followers_pars,
            cb_kwargs={
                'username': username,
                'user_id': user_id,
                'variables_followers': deepcopy(variables_followers)
            },
            headers={
                'User-Agent': 'Instagram 155.0.0.37.107'
            }
        )
        yield response.follow(
            url_following,
            callback=self.user_following_pars,
            cb_kwargs={
                'username': username,
                'user_id': user_id,
                'variables_following': deepcopy(variables_following)
            },
            headers={
                'User-Agent': 'Instagram 155.0.0.37.107'
            }
        )

    def user_followers_pars(self, response: HtmlResponse, username, user_id, variables_followers):
        j_data = response.json()
        if j_data.get('big_list'):
            variables_followers['max_id'] = j_data.get('next_max_id')
            url_followers = f'{self.friends_url}/{user_id}/followers/?{urlencode(variables_followers)}'
            yield response.follow(
                url_followers,
                callback=self.user_followers_pars,
                cb_kwargs={
                    'username': username,
                    'user_id': user_id,
                    'variables_followers': deepcopy(variables_followers)
                },
                headers={
                    'User-Agent': 'Instagram 155.0.0.37.107'
                }
            )

        users = j_data.get('users')
        for user in users:
            yield InstaparserItem(
                _id=user.get('pk'),
                from_user=username,
                type='followers',
                username=user.get('username'),
                full_name=user.get('full_name'),
                profile_pic_url=user.get('profile_pic_url')
            )

    def user_following_pars(self, response: HtmlResponse, username, user_id, variables_following):
        j_data = response.json()
        if j_data.get('big_list'):
            variables_following['max_id'] = j_data.get('next_max_id')
            url_following = f'{self.friends_url}/{user_id}/following/?{urlencode(variables_following)}'
            yield response.follow(
                url_following,
                callback=self.user_following_pars,
                cb_kwargs={
                    'username': username,
                    'user_id': user_id,
                    'variables_following': deepcopy(variables_following)
                },
                headers={
                    'User-Agent': 'Instagram 155.0.0.37.107'
                }
            )

        users = j_data.get('users')
        for user in users:
            yield InstaparserItem(
                _id=user.get('pk'),
                from_user=username,
                type='following',
                username=user.get('username'),
                full_name=user.get('full_name'),
                profile_pic_url=user.get('profile_pic_url')
            )

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
