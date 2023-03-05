import json

import requests
import http.client

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


# user_agent = UserAgent()


# def get_proxy_info(count):
#     url = 'https://hidemy.name/en/proxy-list/?type=hs&anon=34#list'
#     response = requests.get(url)
#
#     soup = BeautifulSoup(response.content, 'html.parser')
#     table = soup.find('table')
#
#     proxy_list = []
#     for row in table.tbody.find_all('tr'):
#         columns = row.find_all('td')
#         if columns:
#             ip = columns[0].text.strip()
#             port = columns[1].text.strip()
#             protocol = columns[4].text.strip().lower()
#             proxy_list.append({'ip': ip, 'port': port, 'protocol': protocol})
#             if len(proxy_list) == count:
#                 break
#     return proxy_list

# def get_proxy_info(count):
#     url = 'https://hidemy.name/en/proxy-list/?type=s&anon=34'
#     options = webdriver.ChromeOptions()
#     # user_agent.update(True)
#     # options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
#     # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0")
#     # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63")
#     # options.add_argument('--headless')
#     options.add_argument('cookie=cf_clearance=76YHMKbsvXpv9UcHbjd1o1vpkF8YQ5l_ARQp66E7gGQ-1677956234-0-160; _ym_uid=167795624013051281; _ym_d=1677956240; _ym_isad=1; _gid=GA1.2.618453944.1677956240; _tt_enable_cookie=1; _ttp=Q_OcDWcpOLRAQqrS-d6hq19jN7g; PAPVisitorId=b24807e1048f03dc754c93lIzRqjh9AQ; PAPVisitorId=b24807e1048f03dc754c93lIzRqjh9AQ; _ga_KJFZ3PJZP3=GS1.1.1677959665.2.1.1677959669.0.0.0; _ga=GA1.1.252897160.1677956240')
#     options.add_argument('authority=hidemy.name')
#     options.add_argument('accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
#     options.add_argument('accept-language=en-GB,en-US;q=0.9,en;q=0.8,ru;q=0.7')
#     options.add_argument('cache-control=max-age=0')
#     options.add_argument('sec-ch-ua="Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"')
#     options.add_argument('sec-ch-ua-mobile=?0')
#     options.add_argument('sec-ch-ua-platform="Windows"')
#     options.add_argument('sec-fetch-dest=document')
#     options.add_argument('sec-fetch-mode=navigate')
#     options.add_argument('sec-fetch-site=none')
#     options.add_argument('sec-fetch-user=?1')
#     options.add_argument('upgrade-insecure-requests=1')
#     options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36')
#
#     driver = webdriver.Chrome(options=options)
#     driver.set_window_size(990, 800)
#     driver.get(url)
#
#     # Wait for the table to load
#     table = WebDriverWait(driver, 15).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, 'table.proxy__t tbody'))
#     )
#
#     # Extract the data from the table using BeautifulSoup
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     proxy_list = []
#     for row in table.find_all('tr'):
#         columns = row.find_all('td')
#         if columns:
#             ip = columns[0].text.strip()
#             port = columns[1].text.strip()
#             protocol = columns[4].text.strip().lower()
#             proxy_list.append({'ip': ip, 'port': port, 'protocol': protocol})
#
#     # Only keep the first `count` proxies
#     proxy_list = proxy_list[:count]
#
#     # Close the browser
#     driver.quit()
#
#     # Return the proxy list
#     return proxy_list


def get_proxy_info(proxy_count=None):
    return read_from_json()
    conn = http.client.HTTPSConnection("hidemy.name")
    headers = {
        'cookie': "cf_clearance=76YHMKbsvXpv9UcHbjd1o1vpkF8YQ5l_ARQp66E7gGQ-1677956234-0-160; _ym_uid=167795624013051281; _ym_d=1677956240; _ym_isad=1; _gid=GA1.2.618453944.1677956240; _tt_enable_cookie=1; _ttp=Q_OcDWcpOLRAQqrS-d6hq19jN7g; PAPVisitorId=b24807e1048f03dc754c93lIzRqjh9AQ; PAPVisitorId=b24807e1048f03dc754c93lIzRqjh9AQ; _ga_KJFZ3PJZP3=GS1.1.1677959665.2.1.1677959669.0.0.0; _ga=GA1.1.252897160.1677956240",
        'authority': "hidemy.name",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        'accept-language': "en-GB,en-US;q=0.9,en;q=0.8,ru;q=0.7",
        'cache-control': "max-age=0",
        'sec-ch-ua': "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Google Chrome\";v=\"110\"",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "Windows",
        'sec-fetch-dest': "document",
        'sec-fetch-mode': "navigate",
        'sec-fetch-site': "none",
        'sec-fetch-user': "?1",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    url = "/en/proxy-list/?maxtime=1000&type=hs&anon=34"
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    html = res.read()
    soup = BeautifulSoup(html, "html.parser")

    proxies = []
    pagination = soup.find("div", {"class": "pagination"})
    pages = pagination.find_all("li", class_=lambda x: not x or 'is-active' in x.split() or 'active' in x.split())
                    # lambda x: x and 'prev_array' not in x.split() and 'next_array' not in x.split()
    for skip_proxy_count in range(0, len(pages)):
        if skip_proxy_count > 0:
            conn.request("GET", f"{url}&start={skip_proxy_count*64}", headers=headers)
            res = conn.getresponse()
            html = res.read()
            soup = BeautifulSoup(html, "html.parser")
        proxy_table = soup.find("table")
        for row in proxy_table.tbody.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) < 7:
                continue
            address = cells[0].text.strip()
            port = cells[1].text.strip()
            proxies.append({"address": address, "port": port})
            if proxy_count is not None and len(proxies) == proxy_count:
                break
    conn.close()
    return proxies


def write_as_json(proxies):
    with open('proxies.json', 'w') as f:
        json.dump(proxies, f)


def read_from_json():
    with open("proxies.json", "r") as f:
        return json.load(f)


# proxies = [{'address': '80.179.140.189', 'port': '80'},
#            {'address': '116.117.253.212', 'port': '9002'},
#            {'address': '58.18.223.212', 'port': '9002'}]
# proxies = get_proxy_info()
# write_as_json(proxies)
# proxies = read_from_json()
# i = 0
