from sentence_splitter import SentenceSplitter, split_text_into_sentences
import argparse
import nltk

def post_proc(lines):
    import re
    new_lines = []
    for l in lines:
        new_l = nltk.sent_tokenize(l)
        new_l = [l for l in new_l if len(l) > 0]
        new_lines += new_l

    return new_lines


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', "--file", required=True)
    parser.add_argument("-t", '--target', default='./total.splited.latin.tok')
    args = parser.parse_args()

    f = open(args.file, 'r')
    lines = f.readlines()
    f.close()

    lines = [l.strip() for l in lines]
    splited_lines = []
    splitter = SentenceSplitter(language='en')

    for l in lines:
        splited_lines += post_proc(splitter.split(text=l))

    f = open(args.target, 'w')
    f.write("\n".join(splited_lines) + "\n")


if __name__ == "__main__":
    main()
