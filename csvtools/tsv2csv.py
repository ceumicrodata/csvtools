import csv
import sys


def main():
    reader = csv.reader(sys.stdin, delimiter='\t')
    writer = csv.writer(sys.stdout)
    writer.writerows(reader)


if __name__ == '__main__':
    main()
