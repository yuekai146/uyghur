from sklearn.manifold import TSNE
import argparse
import matplotlib.pyplot as plt
import numpy as np


def tsne_plot(filename, start, end):
    f = open(filename, 'r')
    lines = f.readlines()[1:]
    f.close()

    words = []
    vecs = []
    for l in lines:
        w, v = l.strip().split(' ', 1)
        v = np.fromstring(v, sep=' ')
        words.append(w)
        vecs.append(v)

    "Creates and TSNE model and plots it"
    
    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(vecs[start:end])

    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])

    x_arr = np.array(x)
    x_mean = np.mean(x_arr)
    x_sd = np.std(x_arr)

    y_arr = np.array(y)
    y_mean = np.mean(y_arr)
    y_sd = np.std(y_arr)

    plt.figure(figsize=(16, 16)) 
    for i in range(len(x)):
        if check_inlier(x[i], y[i], x_mean, x_sd, y_mean, y_sd):
            plt.scatter(x[i],y[i])
            plt.annotate(words[start+i],
                         xy=(x[i], y[i]),
                         xytext=(5, 2),
                         textcoords='offset points',
                         ha='right',
                         va='bottom')
    plt.show()


def check_inlier(x, y, x_mean, x_sd, y_mean, y_sd):
    if (x > x_mean - 2 * x_sd) and (x < x_mean + 2 * x_sd) and (y > y_mean - 2 * y_sd) and (y < y_mean + 2 * y_sd):
        return True
    else:
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str, required=True)
    parser.add_argument('-s', '--start', type=int, default=0)
    parser.add_argument('-e', '--end', type=int, default=200)
    args = parser.parse_args()

    tsne_plot(args.filename, args.start, args.end)


if __name__ == '__main__':
    main()