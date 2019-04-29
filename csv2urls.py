import argparse
import csv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=True)
    args = parser.parse_args()

    with open(args.name+'.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        for i, row in enumerate(reader):
            if i > 1:
                print(row[0])
    csvFile.close()


if __name__ == "__main__":
    main()
