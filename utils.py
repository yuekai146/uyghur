import argparse

def remove_dup(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    lines = list(set([l.strip() for l in lines]))
    f = open('filtered_'+filename, 'w')
    f.write('\n'.join(lines) + '\n')
    f.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', default='remove_dup')
    parser.add_argument('-f', '--filename', default=None)
    args = parser.parse_args()

    if args.type == 'remove_dup':
        remove_dup(args.filename)


if __name__ == '__main__':
    main()
