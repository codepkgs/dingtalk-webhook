# coding: utf-8
import json

import requests


class DingTalk(object):
    """
    send message to dingding webhook robot
    """

    def __init__(self, access_token):
        """
        :param access_token: dingtalk webhook access_token
        """
        self.access_token = self.__parse_token(access_token)
        self.__headers = {"Content-Type": "application/json; charset=utf-8"}
        self.dingtalk_webhook = 'https://oapi.dingtalk.com/robot/send?access_token=%s' % self.access_token

    def __parse_token(self, access_token):
        """
        parse access token, access token must be 64 characters
        :param access_token: dingtalk webhook access_token
        :return: access_token
        """
        if len(access_token) != 64:
            raise ValueError('invalid access token')
        return access_token

    def __do_request(self, data):
        """
        send request
        :param data: data
        :return: like {"errcode":0,"errmsg":"ok"}
        """
        try:
            response = requests.post(url=self.dingtalk_webhook, data=json.dumps(data), headers=self.__headers)
            return response.text
        except Exception:
            raise

    def send_text(self, text, at_mobiles=[], at_all=False):
        """
        发送文本消息
        :param text: 发送的文本消息的内容
        :param at_mobiles: 需要@人的手机号
        :param at_all: 是否@所有人
        :return:
        """

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

    def send_link(self, title, text, message_url, picture_url=''):
        """
        发送link消息
        :param title: 消息标题
        :param text: 消息的文本内容
        :param message_url: 点击消息跳转到的URL
        :param picture_url: 引用的图片的URL
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

    def send_markdown(self, title, text, at_mobiles=[], at_all=False):
        """
        发送markdown消息
        :param title: 首屏会话展示的标题内容
        :param text: markdown格式的文本
        :param at_mobiles: 需要@人的手机号
        :param at_all: 是否@所有人
        :return:
        """

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

    def send_single_action_card(self, title, text, single_title, single_url, hide_avatar=0, button_orientation=0):
        """
        整体跳转的action card
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

    def send_action_card(self, title, text, buttons, hide_avatar=0, button_orientation=0):
        """
        发送独立跳转的action card
        :param title: 首屏会话展示的标题内容
        :param text: markdown格式的文本内容
        :param hide_avatar: 0 显示发送消息者头像, 1 隐藏发送消息者头像
        :param button_orientation: 0 按钮竖直排列, 1 按钮水平排列
        :param buttons: list。每个列表的元素都是一个dict，单个按钮的跳转，需要传递title和actionURL字段。
        :return:
        """

        if not isinstance(buttons, list):
            raise TypeError('buttons must be a list')

        if len(buttons) == 0:
            raise ValueError('buttons can not empty')

        for d in buttons:
            if not isinstance(d, dict):
                raise TypeError('element {} must be dict'.format(d))
            else:
                if 'title' not in d:
                    raise ValueError('title field not in {}'.format(d))

                if 'actionURL' not in d:
                    raise ValueError('messageURL field not in {}'.format(d))

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

    def send_feed_card(self, links):
        """
        发送feed card消息
        :param links: 列表。列表中的每个元素为dict，每个dict需要包含title、messageURL以及picURL字段。
        :return:
        """

        if not isinstance(links, list):
            raise TypeError('links must be a list')

        if len(links) == 0:
            raise ValueError('links can not empty')

        for d in links:
            if not isinstance(d, dict):
                raise TypeError('element {} must be dict'.format(d))
            else:
                if 'title' not in d:
                    raise ValueError('title field not in {}'.format(d))

                if 'messageURL' not in d:
                    raise ValueError('messageURL field not in {}'.format(d))

                if 'picURL' not in d:
                    raise ValueError('picURL field not in {}'.format(d))

        data = {
            "msgtype": "feedCard",
            "feedCard": {
                "links": links
            }
        }

        return self.__do_request(data=data)
