def check_num_words(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    lines = [l.strip() for l in lines]
    lines = list(set(lines))
    num = 0
    for l in lines:
        num += len(l.split())
    return num
