import csv
import sys


def main():
    reader = csv.reader(sys.stdin)
    writer = csv.writer(sys.stdout, delimiter='\t')
    writer.writerows(reader)


if __name__ == '__main__':
    main()
