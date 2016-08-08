import requests
import re
from scrapy.selector import Selector
from config import ArborBlackholeParams,ArborSettings

ARBOR_IP = ArborSettings['ip']
ARBOR_URL = "https://" + ARBOR_IP + "/"
ARBOR_KEY = ArborSettings['api_key']
VERIFY = ArborSettings['verifyssl']

LOGIN_URI = 'index'
LOGIN_USER = ArborSettings['user']
LOGIN_PASS = ArborSettings['password']
LOGIN_PARAMS = {'username': LOGIN_USER, 'password': LOGIN_PASS}

ALERTS_URI = 'arborws/alerts'
ALERTS_PARAMS = {
    'api_key': ARBOR_KEY,
    'format': 'json'
}

MITIGATION_URI = 'mitigation/offramp/index'
BLACKHOLE_URI = 'mitigation/offramp/edit?ip_version=4'
BLACKHOLE_PARAMS = ArborBlackholeParams

START_BLACKHOLE_PARAMS = {
    'sort_field': '',
    '__start_panel': '',
    'start_one':'Start'
}


STOP_BLACKHOLE_PARAMS = {
        'sort_field': '',
    '__start_panel': '',
    'stop_one': 'Stop'
}

def arbor_login():
    login = requests.post(ARBOR_URL + LOGIN_URI, params=LOGIN_PARAMS, verify=VERIFY)
    session_id = login.headers['Set-Cookie'].split(';')[0]
    cookie = {'Cookie': session_id}
    return cookie


def get_mitigation(cookie):
    mitigations = requests.get(ARBOR_URL + MITIGATION_URI, headers=cookie, verify=VERIFY)
    return mitigations.text


def get_mitigation_id_by_ip(cookie, check_ip):
    mitigations_html = get_mitigation(cookie)
    sel = Selector(text=mitigations_html)
    for tr in sel.xpath('//table[@class="sptable"]/tr'):
        ip = tr.xpath('td[4]//text()').extract()
        status = tr.xpath('td[6]//text()').extract()
        miti_id = tr.xpath('td[7]/button/attribute::onclick').extract()
        if len(status) > 0:
            status = status[0]
            ip = ip[2].split('/')[0]
            miti_id = miti_id[0].split('=')[1]
            miti_id = re.sub('\'','', miti_id)
            if check_ip == ip:
                return miti_id, status
    return False, False


def add_mitigation(cookie, ip, alert_id):
    blackhole_params = BLACKHOLE_PARAMS
    blackhole_params['name'] = 'auto-blackhole-' + str(alert_id)
    blackhole_params['alert_id'] = alert_id
    blackhole_params['offramp_prefix'] = ip + '/32'
    post = requests.post(ARBOR_URL + BLACKHOLE_URI, headers=cookie, params=blackhole_params, verify=VERIFY)
    return post.text


def start_blackhole(miti_id, cookie=None):
    if not cookie:
        cookie = arbor_login()
    params = START_BLACKHOLE_PARAMS
    params['id'] = miti_id
    post = requests.post(ARBOR_URL + MITIGATION_URI, headers=cookie, params=params, verify=VERIFY)
    return post.text


def stop_blackhole(miti_id, cookie=None):
    if not cookie:
        cookie = arbor_login()
    params = STOP_BLACKHOLE_PARAMS
    params['id'] = miti_id
    post = requests.post(ARBOR_URL + MITIGATION_URI, headers=cookie, params=params, verify=VERIFY)
    return post.text


def blackhole(ip, alert_id):
    cookie = arbor_login()
    miti_id, status = get_mitigation_id_by_ip(cookie, ip)
    if not miti_id:
        add_mitigation(cookie, ip, alert_id)
        miti_id, status = get_mitigation_id_by_ip(cookie, ip)
        if not miti_id:
            print "Error!!"
            exit(1)
    if status == 'Stopped':
        start_blackhole(miti_id, cookie)


def pretty_alert(alert):
    id = alert['id']
    mbps = int(alert['max_impact_bps']) / 1024 /1024
    if 'cidr' in alert['resource']:
        resource_cidr = alert['resource']['cidr']
    else:
        resource_cidr = "???"
    resource_name = alert['resource']['managedObjects'][0]['name']
    type = alert['type']
    string = "ID: {} Attack: {} mbps: {} IP: {} Name: {}".format(id, type, mbps, resource_cidr, resource_name)
    alert_data = str(id) + '|' + resource_cidr
    return string, alert_data


def get_last_alert():
    alerts = requests.get(ARBOR_URL + ALERTS_URI, params=ALERTS_PARAMS, verify=VERIFY)
    alerts = alerts.json()
    return alerts[-1]


def get_ongoig_alerts():
    alert_params = ALERTS_PARAMS
    alert_params['filter'] = 'sts:ongoing'
    alerts = requests.get(ARBOR_URL + ALERTS_URI, params=ALERTS_PARAMS, verify=VERIFY)
    alerts = alerts.json()
    return alerts


def get_alert_by_id(alert_id):
    alert_params = ALERTS_PARAMS
    alert_params['filter'] = alert_id
    alerts = requests.get(ARBOR_URL + ALERTS_URI, params=ALERTS_PARAMS, verify=VERIFY)
    alerts = alerts.json()
    for alert in alerts:
        if alert['id'] == alert_id:
            return alert
    return None