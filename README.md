# codesnap
    ```python
    from WeixinPay import WeixinPay
    pay = WeixinPay()
    key = 'api_key'
    result = pay.unifiedorder(key, appid='appid', mch_id='mch_id', notify_url='notify_url', spbill_create_ip='spbill_create_ip', trade_type='NATIVE', body='测试', attach='codesnap',out_trade_no='10000', total_fee=1)
    print result
