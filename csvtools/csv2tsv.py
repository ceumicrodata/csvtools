import csv
import sys

reader = csv.reader(sys.stdin)
writer = csv.writer(sys.stdout, delimiter='\t')
writer.writerows(reader)
