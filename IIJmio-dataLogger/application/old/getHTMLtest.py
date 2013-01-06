# -*- coding: utf-8 -*-

import urllib
import urllib2
import cookielib
from lxml import etree
import lxml.html

name = 'MA7251610'
password = 'k7n4203i'


def main():
    #url = 'https://www.iijmio.jp/service/setup/hdd/couponstatus/'
    #html = download(url)
    #save(html, 'file1.html')
    html = open('file1.html').read()
    #data = get_data(html)

    #url = 'https://www.iijmio.jp/service/setup/hdd/viewdata/'
    #html = download(url)
    #save(html, 'file2.html')

    html = open('file2.html').read()
    data = get_data2(html)


def get_data(html):

    
    root = lxml.html.fromstring(html.decode('shift_jis'))
    
    data = root.xpath('//table[@class="base2"]/tr/td')#.encode('utf-8').strip()
    print u"総容量:" + lxml.html.tostring(data[2], method='text', encoding="shift_jis").strip()
    print u"クーポン残量:" + lxml.html.tostring(data[4], method='text', encoding="shift_jis").strip()

    data2 = data[14].xpath('table/tr[position() >= 2]')

    for x in data2:
        x2 = x.xpath('td/text()')
        print u"番号   :" + x2[0]
        print u"ICCID  :" + x2[1]
        print u"SIMtype:" + x2[2]
        print u"coupon :" + x2[3]

    #print lxml.html.tostring(y, method='text', encoding="shift_jis").strip()
    #print lxml.html.tostring(data[14], method='html', encoding="shift_jis").strip()
    #print lxml.html.tostring(data2[1], method='html', encoding="shift_jis").strip()

def get_data2(html):
    root = lxml.html.fromstring(html.decode('shift_jis'))

    data = root.xpath('//table[@class="base2"]/tr')
    print lxml.html.tostring(data[1], method='text', encoding="shift_jis").strip()
    data2 = data[0].xpath('tr[position() >= 3]')

    #print lxml.html.tostring(data2[0], method='text', encoding="shift_jis").strip()

    print data[2].xpath('td/text()')[0]
    for i in range(3,6):
        print i
        x2 = data[i].xpath('td[@class="data2-c"]/text()')
        print u"番号   :" + x2[0].strip()
        print u"ICCID  :" + x2[1].strip()
        print u"SIMtype:" + x2[2].strip()
        print u"coupon :" + x2[3].strip()


def download(url):
    opener = login()
    
    req = urllib2.Request(url)
    conn = opener.open(req)
    cont = conn.read()
    return cont


def save(html, filename):
    f = open(filename, 'w')
    f.write(html)
    f.close()


def login():
    url = 'https://www.iijmio.jp/j_security_check'
    values = {'type': 'id',
              'j_uri': '/auth/message/welcome.jsp',
              'j_username':  name,
              'j_password': password}

    data = urllib.urlencode(values)

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.26 Safari/537.4'
    }

    cj = cookielib.CookieJar()

    #opener = urllib2.build_opener()
    #opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    urllib2.install_opener(opener)

    req = urllib2.Request(url, data, header)
    conn = opener.open(req)
    #print cj

    return opener

main()