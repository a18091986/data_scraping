import scrapy
import re
import json
from scrapy.http import HtmlResponse
from Instagram.items import InstagramItem
import hashlib
from Instagram.auth import log, pas

class InstagramSpider(scrapy.Spider):

    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    insta_login = log
    insta_pass = pas
    insta_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    graphql_url = 'https://i.instagram.com/api/v1/friendships/'
    users = ['ai_machine_learning', 'cloudyml.akash']

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.insta_login_link,
                                 method='POST',
                                 callback=self.user_login,
                                 formdata={'username': self.insta_login,
                                           'enc_password': self.insta_pass},
                                 headers={'X-CSRFToken': csrf}
                                 )

    def user_login(self, response: HtmlResponse):
        resp = response.json()
        if resp['authenticated']:
            for user in self.users:
                yield response.follow(f'/{user}/',
                                      callback=self.user_data_parse,
                                      cb_kwargs={'username': user})

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        url_following = f'{self.graphql_url}{user_id}/following/?count=12'
        yield response.follow(url_following,
                              callback=self.follow_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'fol_list': 'following'},
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'})
        url_followers = f'{self.graphql_url}{user_id}/followers/?count=12'
        yield response.follow(url_followers,
                              callback=self.follow_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'fol_list': 'followers'},
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'})

    def follow_parse(self, response: HtmlResponse, username, user_id, fol_list):
        data = response.json()
        if data['next_max_id']:
            max_id = data['next_max_id']
            url_following = f'{self.graphql_url}{user_id}/{fol_list}/?count=12&max_id={max_id}'
            yield response.follow(url_following,
                                    callback=self.follow_parse,
                                    cb_kwargs={ 'username': username,
                                                'user_id': user_id,
                                                'fol_list': fol_list},
                                    headers={'User-Agent': 'Instagram 155.0.0.37.107'})

        for user in data['users']:
            yield InstagramItem(_id=hashlib.sha1(str(user).encode()).hexdigest(),
                                follow_list=fol_list,
                                fol_username=user['username'],
                                fol_user_id=user['pk'],
                                pic_url=user['profile_pic_url'],
                                body=user,
                                username=username,
                                user_id=user_id
                                )

    def fetch_csrf_token(self, text: str) -> str:
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search('{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text).group()
        return json.loads(matched).get('id')