def stats(path):
    f = open(path, 'r')
    lines = f.readlines()
    lines = [l.strip() for l in lines]
    lens = [len(l.split()) for l in lines]
    return len([n for n in lens if n <= 250]) / len(lens)



def main():
    root = './finished/'
    websites = ['tianshan', 'uycnr','xinhua', 'xjdaily', 'xj_gov', 'xjkunlun', 'xj_people']
    file_name = 'texts.txt.latin.tok.splited.clean'

    files = [root+w+'/'+file_name for w in websites]

    for path in files:
        print(stats(path))


if __name__ == "__main__":
    main()
