# -*- coding: utf-8 -*-
import requests
import time
import re
import json
from pyzbar.pyzbar import decode
from PIL import Image
import qrcode 



 
def loads_jsonp(_jsonp):
    try:
        return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
    except:
        raise ValueError('Invalid Input')
 
def p_qr():
    barcode_url = ''
    barcodes = decode(Image.open('./wc.png'))
    for barcode in barcodes:
        barcode_url = barcode.data.decode("utf-8")
    print(barcode_url)

    qr = qrcode.QRCode()
    qr.add_data(barcode_url)
    #invert=True白底黑块,有些app不识别黑底白块.
    qr.print_ascii(invert=True) 


class jdthor:
    def qrcode(self):      # 保存二维码
        url = "https://qr.m.jd.com/show?appid=133&size=147"
        req = requests.get(url)
        with open("wc.png", mode="wb") as f1:
            f1.write(req.content)
        p_qr() # 终端打印二维码
        # print(req.headers)
        self.state(req.cookies.get_dict())
 
    def state(self, h):   # 查看扫码情况
        while True:
            smdl = h.get('wlfstk_smdl')
            codekey = h.get('QRCodeKey')
            headers = {
                "Referer": "https://union.jd.com/index",
                "Cookie": f"QRCodeKey={codekey}; wlfstk_smdl={smdl}"
            }
            url = f'https://qr.m.jd.com/check?appid=133&token={smdl}&callback=jsonp'
            req = requests.get(url, headers=headers)
            data = loads_jsonp(req.text)
            if data.get('code') == 201:
                print('\t还没扫描呢亲~')  # 未扫描
            elif data.get('code') == 202:
                print('\t\t请确认登陆')  # 请再手机端确认登陆
            elif data.get('code') == 205:
                print('\t\t\t干嘛取消登陆了')
                break  # 取消登陆
            elif data.get('code') == 203:
                print('已经过期了')
                break
            elif data.get('code') == 200:
                self.get(data.get('ticket'), smdl)
                break
            else:
                print(data)
                break
            time.sleep(1)
 
    def get(self, ticket, smdl):      # 获取Ck
        global ckdict
        url = f'https://passport.jd.com/uc/qrCodeTicketValidation?t={ticket}&ReturnUrl=https://union.jd.com/index&callback=jsonp'
        headers = {
            "Referer": "https://union.jd.com/index",
            "Cookie": f"wlfstk_smdl={smdl}"
        }
        req = requests.get(url, headers=headers)
        ckdict = req.cookies.get_dict()
        

def dict2s(d):
    r = ''
    for i in d:
        s = i + '=' + d.get(i) + ';'
        r+=s
    return r



def getcookie():
    jd = jdthor()
    jd.qrcode()
    ds = dict2s(ckdict)
    return ds