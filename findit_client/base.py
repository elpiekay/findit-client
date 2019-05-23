# -*- coding:utf-8 -*-
import requests
import json
from logzero import logger


class FindItBaseClient(object):
    def __init__(self, host=None, port=None):
        host = host or '127.0.0.1'
        port = port or 9410
        self.url = 'http://{}:{}'.format(host, port)
        logger.info('client init finished, server url: {}'.format(self.url))

    def heartbeat(self):
        target_url = '{}/'.format(self.url)
        try:
            resp = requests.get(target_url)
            return resp.ok
        except requests.exceptions.ConnectionError:
            return False

    def _request(self, arg_dict, pic_data):
        resp = requests.post(
            '{}/analyse'.format(self.url),
            data=arg_dict,
            files={'file': pic_data}
        )
        resp_dict = resp.json()
        logger.info('request: {}'.format(json.dumps(arg_dict)))
        logger.info('response: {}'.format(json.dumps(resp_dict)))
        return resp_dict

    def analyse_with_path(self, target_pic_path, template_pic_name, **extra_args):
        with open(target_pic_path, 'rb') as f:
            pic_data = f.read()

        return self._request(
            arg_dict={
                'target_pic_path': target_pic_path,
                'template_name': template_pic_name,
                'extras': json.dumps(extra_args),
            },
            pic_data=pic_data,
        )

    def check_exist_with_path(self, target_pic_path, template_pic_name, threshold, **extra_args):
        result = self.analyse_with_path(target_pic_path, template_pic_name, pro_mode=True, **extra_args)
        match_result = list(result['response']['data'].values())[0]['TemplateEngine']['raw']['max_val']
        logger.info('matching result is: {}, and threshold is: {}'.format(match_result, threshold))
        return match_result > threshold
