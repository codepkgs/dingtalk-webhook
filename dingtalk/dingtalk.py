import base64
import hashlib
import hmac
import json
import time
from typing import List

import requests


class DingTalk:
    """
    send message to dingding webhook robot
    """

    def __init__(self, access_token: str, secret: str = None):
        """
        :param access_token: dingtalk webhook access_token
        :param secret: dingtalk webhook secret
        """
        self.access_token = self.__parse_token(access_token)
        self.secret = secret
        self.__headers = {"Content-Type": "application/json; charset=utf-8"}

    @staticmethod
    def __parse_token(access_token):
        """
        parse access token, access token must be 64 characters
        :param access_token: dingtalk webhook access_token
        :return: access_token
        """

        if len(access_token) != 64:
            raise ValueError('invalid access token')
        return access_token

    def __get_timestamp_secret(self):
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = requests.utils.quote(base64.b64encode(hmac_code))
        return timestamp, sign

    def __do_request(self, data):
        """
        send request
        :param data: data
        :return: like {"errcode":0,"errmsg":"ok"}
        """

        dingtalk_webhook = 'https://oapi.dingtalk.com/robot/send?access_token={}'.format(self.access_token)
        if self.secret:
            timestamp, sign = self.__get_timestamp_secret()
            dingtalk_webhook += '&timestamp={}&sign={}'.format(timestamp, sign)

        resp = requests.post(url=dingtalk_webhook, data=json.dumps(data), headers=self.__headers)
        return resp.json()

    @staticmethod
    def check_mobiles(mobiles):
        """检查手机号
        :param mobiles: mobiles
        :return: True or False
        """

        if mobiles is None:
            mobiles = []
        elif isinstance(mobiles, str):
            mobiles = mobiles.split(',')
        elif isinstance(mobiles, (list, tuple)):
            mobiles = list(mobiles)
        else:
            raise TypeError('{} is invalid, it must be list, tuple, or comma-separated str'.format(mobiles))

        return mobiles

    def send_text(self, text: str, at_mobiles: [str, list, tuple] = None, at_all: bool = False):
        """发送文本消息
        :param text: 发送的文本消息的内容
        :param at_mobiles: 需要@人的手机号
        :param at_all: 是否@所有人
        :return:
        """

        at_mobiles = self.check_mobiles(at_mobiles)

        data = {
            "msgtype": "text",
            "text": {
                "content": text
            },
            "at": {
                "atMobiles": at_mobiles,
                "isAtAll": at_all
            }
        }

        return self.__do_request(data=data)

    def send_link(self, title: str, text: str, message_url: str, picture_url=''):
        """发送link消息
        :param title: 消息标题
        :param text: 消息的文本内容
        :param message_url: 点击消息跳转到urlL
        :param picture_url: 引用的图片的url
        :return:
        """

        data = {
            "msgtype": "link",
            "link": {
                "text": text,
                "title": title,
                "picUrl": picture_url,
                "messageUrl": message_url
            }
        }

        return self.__do_request(data)

    def send_markdown(self, title: str, text: str, at_mobiles: [str, list, tuple] = None, at_all: bool = False):
        """发送markdown消息
        :param title: 首屏会话展示的标题内容
        :param text: markdown格式的文本
        :param at_mobiles: 需要@人的手机号
        :param at_all: 是否@所有人
        :return:
        """

        at_mobiles = self.check_mobiles(at_mobiles)

        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text,
            },
            "at": {
                "atMobiles": at_mobiles,
                "isAtAll": at_all
            }
        }

        return self.__do_request(data=data)

    def send_single_action_card(self, title: str, text: str, single_title: str, single_url: str, hide_avatar: int = 0,
                                button_orientation: int = 0):
        """整体跳转的action card
        :param title: 首屏会话展示的内容
        :param text: markdown 格式的文本
        :param single_title: 单个按钮显示的title。如: 阅读全文
        :param single_url: 跳转到的URL
        :param hide_avatar: 0 显示发送者的头像, 1 隐藏发送者的头像
        :param button_orientation: 按钮方向。0按钮竖直排列, 1按钮水平排列
        :return:
        """

        data = {
            "msgtype": "actionCard",
            "actionCard": {
                "title": title,
                "text": text,
                "hideAvatar": hide_avatar,
                "btnOrientation": button_orientation,
                "singleTitle": single_title,
                "singleURL": single_url
            }
        }

        return self.__do_request(data)

    def send_action_card(self, title: str, text: str, buttons: List[dict], hide_avatar: int = 0,
                         button_orientation: int = 0):
        """发送独立跳转的action card
        :param title: 首屏会话展示的标题内容
        :param text: markdown格式的文本内容
        :param hide_avatar: 0 显示发送消息者头像, 1 隐藏发送消息者头像
        :param button_orientation: 0 按钮竖直排列, 1 按钮水平排列
        :param buttons: list。每个列表的元素都是一个dict，单个按钮的跳转，需要传递title和actionUrl字段。
        :return:
        """

        if not isinstance(buttons, list):
            raise TypeError('buttons is invalid type, it must be a list')

        if len(buttons) == 0:
            raise ValueError('buttons can not empty')

        for button in buttons:
            if not isinstance(button, dict):
                raise TypeError('element {} is invalid type, it must be dict'.format(button))
            else:
                if 'title' not in button or 'actionURL' not in button:
                    raise KeyError('key title or actionURL not in {}'.format(button))

        data = {
            "msgtype": "actionCard",
            "actionCard": {
                "title": title,
                "text": text,
                "hideAvatar": hide_avatar,
                "btnOrientation": button_orientation,
                "btns": buttons
            }
        }

        return self.__do_request(data=data)

    def send_feed_card(self, links: List[dict]):
        """发送feed card消息
        :param links: list。列表中的每个元素为dict，每个dict需要包含title、messageURL以及picURL字段。
        :return:
        """

        if not isinstance(links, list):
            raise TypeError('links is invalid type, it must be a list')

        if len(links) == 0:
            raise ValueError('links can not empty')

        for link in links:
            if not isinstance(link, dict):
                raise TypeError('element {} is invalid type, it must be dict'.format(link))
            else:
                if 'title' not in link:
                    raise KeyError('title field not in {}'.format(link))

                if 'messageURL' not in link:
                    raise KeyError('messageURL field not in {}'.format(link))

                if 'picURL' not in link:
                    raise KeyError('picURL field not in {}'.format(link))

        data = {
            "msgtype": "feedCard",
            "feedCard": {
                "links": links
            }
        }

        return self.__do_request(data=data)
