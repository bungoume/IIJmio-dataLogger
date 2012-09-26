# -*- coding: utf-8 -*-
"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""


from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from google.appengine.ext import db

from flask import render_template, flash, url_for, redirect

from decorators import login_required, admin_required

import datetime
import time
import re
import urllib
import urllib2
import cookielib
import models
import lxml.html
import codecs


def home():
    return redirect(url_for('list_examples'))


def say_hello(username):
    return 'Hello %s' % username


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

    for i in range(3, 6):
        x2 = data[i].xpath('td[@class="data2-c"]/text()')

        iccid = x2[1].strip()
        key_name = 'DATE=' + str(date) + '&ICCID=' + str(iccid)
        usage = int(re.search('[0-9]+', x2[3].strip()).group(0)) * 1024 * 1024

        item = models.SimLogModel(
            key_name=key_name,
            iccid=iccid,
            usage=usage,
            date=date
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
    name = ''
    password = ''
    opener = login_iij(name, password)

    req = urllib2.Request(url)
    conn = opener.open(req)
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
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.26 Safari/537.4'
    }

    cj = cookielib.CookieJar()

    #opener = urllib2.build_opener()
    #opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    urllib2.install_opener(opener)

    req = urllib2.Request(url, data, header)
    opener.open(req)
    #print cj

    return opener


@login_required
def list_examples():
    """List all examples"""
    examples = ""
    return render_template('list_examples.html', examples=examples, form=form)


@login_required
def delete_example(example_id):
    """Delete an example object"""


@admin_required
def admin_only():
    """This view requires an admin account"""
    return 'Super-seekrit admin page.'


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''
