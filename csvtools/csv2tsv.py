import csv
import fileinput
import sys

reader = csv.reader(fileinput.input())
writer = csv.writer(sys.stdout, delimiter='\t')
writer.writerows(reader)
