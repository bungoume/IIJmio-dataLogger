# -*- coding: utf-8 -*-
"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""


#from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from google.appengine.ext import db

from flask import render_template, flash, jsonify
#, redirect, url_for

from decorators import admin_required
#,login_required

from secret_keys import USERNAME, PASSWORD

import datetime
import time
import re
import urllib
import urllib2
import cookielib
import models
import lxml.html


def home():
    return render_template('index.html')
    #return redirect(url_for('list_log'))


def set_sim_info(html):
    "https://www.iijmio.jp/customer/contract/"

    sim_info_array = []

    for obj in sim_info_array:
        sim_info = models.SimInfoModel(
            service_code="",
            sim_service_code="",
            phone_number="",
            iccid="",
            sim_type="",
            status=""
            #added_by=users.get_current_user()
        )
        try:
            sim_info.put()
            sim_info_id = sim_info.key().id()
            flash(u'Example %s successfully saved.' % sim_info_id, 'success')
            return ""
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return ""


def set_log():
    html = download("https://www.iijmio.jp/service/setup/hdd/viewdata/")
    #html = open('test2.html').read()
    root = lxml.html.fromstring(html.decode('shift_jis'))
    #ここですでにunicodeになっている
    data = root.xpath('//table[@class="base2"]/tr')
    #print lxml.html.tostring(data[1], method='text', encoding="utf-8").strip()

    date = data[2].xpath('td/text()')[0]
    date = re.sub(u'[年月日今（）]', '-', date)
    date = datetime.datetime.strptime(date, '%Y-%m-%d-----')
    date = datetime.date(date.year, date.month, date.day)
    items = []
    d = datetime.datetime.utcnow()
    created_at = datetime.datetime(d.year, d.month, d.day, d.hour)

    range_list = range(3, 6)
    # 15時(JPN0時)台は前日のログを取得
    if created_at.hour == 15:
        range_list = range(7, 10)

    for i in range_list:
        x2 = data[i].xpath('td[@class="data2-c"]/text()')

        iccid = x2[1].strip()
        #key_name = 'DATE=' + str(date) + '&ICCID=' + str(iccid)
        usage = int(re.search('[0-9]+', x2[3].strip()).group(0)) * 1024 * 1024

        item = models.SimLogModel(
        #    key_name=key_name,
            iccid=iccid,
            usage=usage,
        #    created_at=created_at
        #    date=date
        )
        items.append(item)

    try:
        db.put(items)
        return ""
    except CapabilityDisabledError:
        flash(u'App Engine Datastore is currently in read-only mode.', 'info')
        return ""


def set_detail_log():
    html = download("https://www.iijmio.jp/service/setup/hdd/couponstatus/")
    #html = open('test1.html').read()
    root = lxml.html.fromstring(html.decode('shift_jis'))

    data = root.xpath('//table[@class="base2"]/tr/td')
    service_code = data[1].xpath('//b/text()')[0].strip().encode('utf_8')
    total_remaining_amount = lxml.html.tostring(data[2], method='text', encoding="unicode").strip()
    total_remaining_amount = int(re.search('[0-9]+', total_remaining_amount).group(0)) * 1024 * 1024
    remaining_coupons = lxml.html.tostring(data[4], method='text', encoding="unicode").strip()
    remaining_coupons = int(re.search('[0-9]+', remaining_coupons).group(0)) * 1024 * 1024

    service_detail_log = models.ServiceDetailLogModel(
        total_remaining_amount=total_remaining_amount,
        remaining_coupons=remaining_coupons,
        service_code=service_code
    )
    try:
        service_detail_log.put()
        service_detail_log_id = service_detail_log.key().id()
        flash(u'Example %s successfully saved.' % service_detail_log_id, 'success')
    except CapabilityDisabledError:
        flash(u'App Engine Datastore is currently in read-only mode.', 'info')

    data2 = data[14].xpath('table/tr[position() >= 2]')
    for x in data2:
        x2 = x.xpath('td/text()')
        iccid = x2[1].strip()
        remaining_coupons = int(re.search('[0-9]+', x2[3]).group(0)) * 1024 * 1024

        sim_info = models.SimDetailLogModel(
            iccid=iccid,
            remaining_coupons=remaining_coupons
        )
        try:
            sim_info.put()
            sim_info_id = sim_info.key().id()
            flash(u'Example %s successfully saved.' % sim_info_id, 'success')
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
    return ""


def download(url):
    opener = login_iij(USERNAME, PASSWORD)

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.45 Safari/537.17'
    }

    req = urllib2.Request(url, None, header)
    conn = opener.open(req, None, 30)
    cont = conn.read()
    return cont


def login_iij(name, password):
    url = 'https://www.iijmio.jp/j_security_check'
    values = {'type': 'id',
              'j_uri': '/auth/message/welcome.jsp',
              'j_username': name,
              'j_password': password}

    data = urllib.urlencode(values)

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.45 Safari/537.17'
    }

    cj = cookielib.CookieJar()

    #opener = urllib2.build_opener()
    #opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)

    req = urllib2.Request(url, data, header)
    opener.open(req, None, 30)
    #print cj

    return opener


@admin_required
def list_log():
    #query = models.SimLogModel.all()
    #logs = query.fetch(limit=50)
    data = {}
    logs = models.SimLogModel.gql("ORDER BY updated_at DESC LIMIT 3000")
    for x in logs:
        #時間ちょうど付近での誤差修正（+5することで四捨五入的な）
        d = x.updated_at + datetime.timedelta(minutes=5)
        d = datetime.datetime(d.year, d.month, d.day, d.hour)
        timestamp = time.mktime(d.timetuple())
        timestamp = str(int(timestamp))
        usage = int(x.usage) / (1024 * 1024)
        if not timestamp in data:
            data[timestamp] = {}
        data[str(timestamp)][x.iccid] = usage

    # logs = models.ServiceDetailLogModel.gql("ORDER BY updated_at ASC LIMIT 1000")
    # for x in logs:
    #     timestamp = time.mktime((x.updated_at + datetime.timedelta(hours=9)).timetuple())
    #     timestamp = int(timestamp) * 1000
    #     usage = 1000 - (int(x.total_remaining_amount) / (1024 * 1024))
    #     if not str(timestamp) in data:
    #         data[str(timestamp)] = {}
    #     data[str(timestamp)]["total"] = usage

    # dataList = []
    # for key, value in data.iteritems():
    #     temp = [int(key), value]
    #     dataList.append(temp)

    return jsonify(data=data)
    #return render_template('list_log.html', log=log)


@admin_required
def list_detail_log():
    query = models.SimDetailLogModel.all()

    logs = query.fetch(limit=50)
    log = []
    for x in logs:
        y = []
        y['iccid'] = x.iccid
        y['remaining_coupons'] = x.remaining_coupons
        y['updated_at'] = (x.updated_at + datetime.timedelta(hours=9)).isoformat(' ')
        log.append(y)
    print log
    return jsonify(log=log)
    #return render_template('list_log.html', log=log)


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''
