# -*- coding: utf-8 -*-
#!/usr/bin/python
import sys
import random
import string
import hashlib
import urllib2
import xml.etree.cElementTree as XML

reload(sys)
sys.setdefaultencoding('utf8')

UNIFIEDORDER_URL = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
QUERYORDER_URL = 'https://api.mch.weixin.qq.com/pay/orderquery'


class WeixinPay():
    def __init__(self):
        pass

    @staticmethod
    def unifiedorder(key, **kwargs):
        """
        统一下单接口
        :param key: API密钥
        :param kwargs:
            详见 https://pay.weixin.qq.com/wiki/doc/api/native.php?chapter=9_1
            appid: 应用id
            mch_id: 商户id
            api_key: 微信支付 api_key
            notify_url: 通知加调地址
            openid: 客户标识，trade_type='JSAPI'时必传
            spbill_create_ip: 客户端ip地址 或 web页面ip地址
            trade_type: JSAPI 或 NATIVE
            body: 标题
            attach: 附加数据
            out_trade_no: 业务端号
            total_fee: 金额,单位为:分
            示例 unifiedorder(appid='appid', mch_id='mch_id')
        :return:
        """
        nonce_str = WeixinPay.generate_random_string()
        kwargs['nonce_str'] = nonce_str
        sign = WeixinPay.generate_sign_for_dict(kwargs, key)
        kwargs['sign'] = sign
        xml = WeixinPay.generate_xml_for_dict(kwargs)
        return WeixinPay.send_data(UNIFIEDORDER_URL, xml)

    @staticmethod
    def order_query(appid, mch_id, key, out_trade_no):
        """
        查询订单
        :param appid: 应用id
        :param mch_id: 商户id
        :param key: API密钥
        :param out_trade_no: 商户订单号
        :return:
        """
        nonce_str = WeixinPay.generate_random_string()  # 随机字符串
        params = {
            'appid': str(appid),
            'mch_id': str(mch_id),
            'out_trade_no': out_trade_no,
            'nonce_str': nonce_str
        }
        sign = WeixinPay.generate_sign_for_dict(params, key)
        params['sign'] = sign
        xml = WeixinPay.generate_xml_for_dict(params)
        return WeixinPay.send_data(QUERYORDER_URL, xml)

    @staticmethod
    def generate_random_string(length=16):
        """
        生成随机字符串
        :param length:
        :return:
        """
        return ''.join(random.sample(string.letters + string.digits, length))

    @staticmethod
    def generate_xml_for_dict(params):
        """
        根据参数生成XML
        :param params: 参数字典 {key1: value1, key2: value2}
        :return:
        """
        sorted_params = sorted([(key, value) for key, value in params.iteritems()])
        data = ''.join(['<%(key)s>%(value)s</%(key)s>' % {'key': x[0], 'value': x[1]} for x in sorted_params])
        return '<xml>' + data + '</xml>'

    @staticmethod
    def generate_sign_for_dict(params, sign_key):
        """
        生成签名
        :param params: 参数字典 {key1: value1, key2: value2}
        :param sign_key: api_key 或 secret
        :return:
        """
        sorted_params = sorted([(key, str(value)) for key, value in params.iteritems()])
        sign_data = '&'.join(['='.join(x) for x in sorted_params])
        sign_data += '&key=' + sign_key
        return WeixinPay.generate_sign_for_string(sign_data)

    @staticmethod
    def generate_sign_for_string(data):
        md5 = hashlib.md5()
        md5.update(data)
        sign = md5.hexdigest().upper()
        return sign

    @staticmethod
    def send_data(url, data):
        """
        POST数据
        :param url: URL地址
        :param data: 数据
        :return:
        """
        send_data = data.encode('utf-8')
        req = urllib2.Request(url, send_data)
        response = urllib2.urlopen(req)
        result = response.read()
        return result

    @staticmethod
    def validate_sign_for_xml(xml, sign_key):
        """
        验证签名
        :param xml: xml 字符串
        :param key: api_key 或 secret
        :return:
        """
        root = XML.fromstring(xml)
        sign_to_check = root.find('sign').text

        sorted_params = sorted([(child.tag, child.text) for child in root if child.tag != 'sign'])
        sign_data = '&'.join(['='.join(x) for x in sorted_params])
        sign_data += '&key=' + sign_key

        sign = WeixinPay.generate_sign_for_string(sign_data)

        if sign == sign_to_check:
            return True
        return False
