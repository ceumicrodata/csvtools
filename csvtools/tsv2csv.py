import csv
import sys

reader = csv.reader(sys.stdin, delimiter='\t')
writer = csv.writer(sys.stdout)
writer.writerows(reader)
