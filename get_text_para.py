from bs4 import BeautifulSoup
from urllib.parse import urljoin
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

import argparse
import os
import re
import requests


def get_content(url, threshould, min_length):
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


def main():
	parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str, default='urls.txt')
    parser.add_argument('-l', '--min_length', type=int, default=100)
    parser.add_argument('-t', '--threshould', type=float, default=0.7)
    parser.add_argument('-nt', '--num_threads', type=int, default=4)
    parser.add_argument('-bs', '--batch_size', type=int, default=1000)
    args = parser.parse_args()

    f = open(args.filename, 'r')
    urls = f.readlines()
    urls = [u.strip() for u in urls]
    f.close()

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
    f = open("./texts.txt", 'a')


	pool = ThreadPool(13)

	results = pool.map(requests.get, urls)

	pool.close()
	pool.join()

print(len(results))