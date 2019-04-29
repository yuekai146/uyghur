from urllib.parse import urlparse
import argparse


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--filename', type=str, default='urls.txt')
	args = parser.parse_args()

	f = open(args.filename, 'r')
	urls = f.readlines()
	f.close()
	urls = list(set([u.strip() for u in urls]))
	root_urls = []

	for u in urls:
		parsed_uri = urlparse(u)
		result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
		if result not in root_urls and 'http' in result:
        		root_urls.append(result)

	assert len(root_urls) == len(set(root_urls))

	for u in root_urls:
		print(u)


if __name__ == "__main__":
	main()
