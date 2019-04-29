import argparse
import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.common.exceptions import TimeoutException


THRESHOULD=0.7
MIN_LENGTH=100

def get_content(url, threshould, min_length, driver=None):
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
    content = BeautifulSoup(content, "html.parser")
    part = content.get_text().split("\n")
    part = [p for p in part if len(p) > 0]
    text = []

    for paragraph in part:
        arabic_status = count_arabic(str(paragraph))
        length = arabic_status[0]
        possible = arabic_status[1]
        if possible > threshould and length >= min_length:
                text.append(str(paragraph))
    text = list(set(text))
    return text


def count_arabic(string):
    pattern = re.compile(u'[\u0600-\u06FF]+?')
    result = pattern.findall(string)
    arabic_num = len(result)
    possible = arabic_num / len(str(string))
    return (arabic_num, possible)


def test_url(url):
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(20)

    content1 = get_content(url, 20, 0.7, driver)
    content2 = get_content(url, 20, 0.7)

    driver.close()

    num1 = 0
    num2 = 0
    for c in content1:
        num1 += len(c.split())
    
    for c in content2:
        num2 += len(c.split())

    print(num1)
    print(num2)

    if num1 <= num2:
        return 'requests'
    else:
        return 'selenium'


def test_method(urls):
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str, default='urls.txt')
    parser.add_argument('-l', '--min_length', type=int, default=100)
    parser.add_argument('-t', '--threshould', type=float, default=0.7)
    args = parser.parse_args()

    f = open(args.filename, 'r')
    urls = f.readlines()
    f.close()

    urls = [u.strip() for u in urls]
    if os.path.exists("./crawl_method"):
        f_crawl_m = open("./crawl_method", 'r')
        crawl_method = f_crawl_m.readline().strip()
        f_crawl_m.close()
    else:
        crawl_method = test_method(urls)
        f_crawl_m = open("./crawl_method", 'w')
        f_crawl_m.write(crawl_method + "\n")
        f_crawl_m.close()


    print("Use {} for crawling.".format(crawl_method))

    f = open("./texts.txt", 'a')

    if os.path.exists("./extracted_urls.txt"):
        f_finished = open("./extracted_urls.txt", 'r')
        extracted_urls = f_finished.readlines()
        if len(extracted_urls) == 0:
            extracted_urls = []
        else:
            extracted_urls = [u.strip() for u in extracted_urls]
        f_finished.close()
    else:
        extracted_urls = []
    
    f_finished = open("./extracted_urls.txt", 'a')

    if crawl_method == 'selenium':
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
        driver.set_page_load_timeout(20)
    else:
        driver = None
    
    unextracted_urls = set(urls) - set(extracted_urls)
    unextracted_urls = list(unextracted_urls)
    for i, u in enumerate(unextracted_urls):
        if u not in extracted_urls:
            print(u)

            if crawl_method == 'selenium':
                text = get_content(u, args.threshould, args.min_length, driver)
            elif crawl_method == 'requests':
                text = get_content(u, args.threshould, args.min_length, driver)

            for paragraph in text:
                f.writelines(paragraph)
                f.write("\n")
                f.flush()
            f_finished.writelines(u)
            f_finished.write("\n")
            f_finished.flush()
            extracted_urls.append(u)
        else:
            continue

    f_finished.close()
    f.close()
    if driver is not None:
        driver.close()

    # Post process
    f = open("./texts.txt", 'r')
    lines = f.readlines()
    f.close()
    
    lines = [l.strip() for l in lines]
    lines = list(set(lines))

    f = open("filtered_texts.txt", 'w')
    f.write("\n".join(lines) + "\n")
    f.close()


if __name__ == "__main__":
    main()
