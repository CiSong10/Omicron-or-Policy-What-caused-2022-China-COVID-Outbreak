# Author: Ci Song
# Date: 2022-12-03
# Reference: https://juejin.cn/post/6996985734854869000
# Data Source: National Health Commission PRC

import asyncio
from bs4 import BeautifulSoup
import re
import csv
import json
from pyppeteer import launcher
launcher.DEFAULT_ARGS.remove('--enable-automation')  # prevent server from monitoring webdriver
from pyppeteer import launch


async def pyppteer_fetch_url(url):
    brower = await launch({'headless': False, 'dumpio': True, 'autoClose': False})
    page = await brower.newPage()

    await page.goto(url)
    await asyncio.wait([page.waitForNavigation()])
    str = await page.content()
    await brower.close()
    return str


def get_html(url):
    """
    :param url: (str) The URL of CDC webpage.
    :return: the html of webpage.
    """
    return asyncio.get_event_loop().run_until_complete(pyppteer_fetch_url(url))


def get_page_url(startpage, endpage):
    for page in range(startpage, endpage+1):
        if page == 1:
            url = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml'
        else:
            url = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd_' + str(page) + '.shtml'
        yield url


def get_daily_urls(html):
    soup = BeautifulSoup(html, 'html.parser')
    li = soup.find('div', attrs={"class": "list"}).ul.find_all("li")
    for item in li:
        try:
            link = 'http://www.nhc.gov.cn' + item.a['href']
            date = item.span.text
        except:
            print('Failed to crawl:' + item)
            continue
        # print((link, date))
        yield link, date


def get_content(html, date):
    soup = BeautifulSoup(html, 'html.parser')
    text_list = soup.find_all(name='p')
    try:
        if text_list[0].get_text():
            text = text_list[0].get_text()
        elif text_list[1].get_text():
            text = text_list[1].get_text()
        else:
            text = text_list[2].get_text()
    except:
        text = ''

    try:
        total_case = re.search('新增确诊病例(\d+)例', text).group(1)
    except:
        total_case = None
    try:
        import_case = re.search('境外输入病例(\d+)例', text).group(1)
    except:
        import_case = None
    try:
        local_case = re.search('本土病例(\d+)例', text).group(1)
    except:
        local_case = None

    if import_case is None:
        if re.search('均为境外输入病例', text):
            import_case = total_case
            local_case = 0

    daily_dict = {'date': date,
                  'total': total_case,
                  'import': import_case,
                  'local': local_case}

    return daily_dict


def write_dicts_to_csv(filepath, data, fieldnames, encoding='utf-8', newline=''):
    """
    Uses csv.DictWriter() to write a list of dictionaries to a target CSV file as row data.
    The passed in fieldnames list is used by the DictWriter() to determine the order
    in which each dictionary's key-value pairs are written to the row.

    Parameters:
        filepath (str): path to target file (if file does not exist it will be created)
        data (list): dictionary content to be written to the target file
        fieldnames (seq): sequence specifing order in which key-value pairs are written to each row
        encoding (str): name of encoding used to encode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences

    Returns:
        None
    """

    with open(filepath, 'w', encoding=encoding, newline=newline) as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()  # first row
        writer.writerows(data)


def read_json(filepath, encoding='utf-8'):
    """Reads a JSON document, decodes the file content, and returns a list or dictionary if
    provided with a valid filepath.

    Parameters:
        filepath (str): path to file
        encoding (str): name of encoding used to decode the file

    Returns:
        dict/list: dict or list representations of the decoded JSON document
    """

    with open(filepath, 'r', encoding=encoding) as file_obj:
        return json.load(file_obj)


if __name__ == "__main__":
    cases = []
    for url in get_page_url(33, 33):
        html = get_html(url)
        for link, date in get_daily_urls(html):
            daily_html = get_html(link)
            daily_dict = get_content(daily_html, date)
            cases.append(daily_dict)

    # print(cases)
        fieldnames = cases[0].keys()

    write_dicts_to_csv('china_covid_cases_33.csv', cases, fieldnames)

