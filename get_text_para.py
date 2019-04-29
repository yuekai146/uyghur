from bs4 import BeautifulSoup
from urllib.parse import urljoin
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

import argparse
import os
import re
import requests


def get_content(kwargs):
	url = kwargs['url']
	threshould = kwargs['threshould']
	min_length = kwargs['min_length']
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
	print(url)
	if len(text) == 0:
		print("Got nothing from {}".format(url))
	return text


def count_arabic(string):
	pattern = re.compile(u'[\u0600-\u06FF]+?')
	result = pattern.findall(string)
	arabic_num = len(result)
	possible = arabic_num / len(str(string))
	return (arabic_num, possible)

def get_input(urls_batch, threshould, min_length):
	res = []
	for u in urls_batch:
		res.append({"url":u, "threshould":threshould, "min_length":min_length})
	return res


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

	unextracted_urls = set(urls) - set(extracted_urls)
	unextracted_urls = list(unextracted_urls)

	pool = ThreadPool(args.num_threads)

	while len(unextracted_urls) > 0:
		urls_batch = unextracted_urls[:args.batch_size]
		text_batch = pool.map(
			get_content, get_input(urls_batch, args.threshould, args.min_length)
			)

		# Remove duplicate
		texts = []
		for t in text_batch:
			texts += t
		texts = list(set(texts))
		
		# Write to file
		for paragraph in texts:
			f.writelines(paragraph)
			f.write("\n")
			f.flush()

		for u in urls_batch:
			f_finished.writelines(u)
			f_finished.write("\n")
			f_finished.flush()

		if len(unextracted_urls) <= args.batch_size:
			unextracted_urls = []
		else:
			unextracted_urls = unextracted_urls[args.batch_size:]	
	
	pool.close()
	pool.join()


if __name__ == '__main__':
	main()
