import argparse
import os
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from urllib.parse import urljoin


def test_url(url):
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(20)

    content1 = get_urls(url, driver)
    content2 = get_urls(url)

    driver.close()

    num1 = len(content1)
    num2 = len(content2)

    if num1 <= num2:
        return 'requests', content2
    else:
        return 'selenium', content1


def test_method(root_url):
    _, urls = test_url(root_url)
    import random
    test_urls = random.choices(urls, k=11)
    res = []

    for url in test_urls:
        res.append(test_url(url))

    num_selenium = len([c for c in res if c == 'selenium'])
    num_requests = len([c for c in res if c == 'requests'])

    if num_selenium > num_requests:
        return 'selenium'
    else:
        return 'requests'

def get_urls(url, driver=None):
    if driver is not None:
        try:
            driver.get(url)
            content = driver.page_source
        except:
            return []
    else:
        try:
            content = requests.get(url).content
        except:
            return []

    content = BeautifulSoup(content, 'html.parser')
    res = content.find_all("a", href=True)
    res = [urljoin(url, h["href"]) for h in res]

    res = list(set(res))
    return res

def assert_root(urls, base_url):
    if len(urls) == 0:
        return []
    else:
        return [u for u in urls if u[:len(base_url)] == base_url]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str, required=True)
    parser.add_argument('--base_url', default=None)
    args = parser.parse_args()

    root_url = args.url
    if args.base_url is not None:
        base_url = args.base_url
    else:
        base_url = root_url
    base_len = len(base_url)

    if os.path.exists("./crawl_method"):
        f_crawl_m = open("./crawl_method", 'r')
        crawl_method = f_crawl_m.readline().strip()
        f_crawl_m.close()
    else:
        crawl_method = test_method(root_url)
        f_crawl_m = open("./crawl_method", 'w')
        f_crawl_m.write(crawl_method + "\n")
        f_crawl_m.close()

    print("Use {} for crawl".format(crawl_method))
    
    if crawl_method == 'selenium':
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
        driver.set_page_load_timeout(20)
    else:
        driver = None

    url_queue = assert_root(get_urls(root_url, driver), base_url)
    url_queue = list(set(url_queue))
    visited_urls = []
    total_urls = []

    while len(url_queue) > 0:
        # pop the first url and get all hrefs in it.
        cur_url = url_queue[0]

        if cur_url not in visited_urls:
            if cur_url not in total_urls:
                print(cur_url)
                total_urls.append(cur_url)
            cur_hrefs = assert_root(get_urls(cur_url, driver), base_url)
            cur_hrefs = [h for h in cur_hrefs if h not in total_urls]
            cur_hrefs = [h for h in cur_hrefs if len(h) > 0]

            for h in cur_hrefs:
                print(h)
            
            visited_urls.append(cur_url)
            url_queue = url_queue + cur_hrefs
            total_urls = total_urls + cur_hrefs
        del url_queue[0]


    assert len(total_urls) == len(list(set(total_urls)))
    if driver is not None:
        driver.close()

def test():
    options = webdriver.FirefoxOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    u = "http://www.uycnr.com/sp/gqsp/"
    driver = webdriver.Firefox(options=options)
    urls = get_urls(u, driver)
    for u in urls:
        print(u)

    driver.close()


if __name__ == "__main__":
    main()
    #test()
