import csv
import fileinput
import sys

reader = csv.reader(fileinput.input(), delimiter='\t')
writer = csv.writer(sys.stdout)
writer.writerows(reader)
