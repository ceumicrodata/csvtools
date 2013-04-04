# coding: utf-8

import csv
import sys

"""
Joins csv1 and csv2 .csv files on fields joinField. Left join.

Usage:
python simple_joiner.py csv1.csv csv2.csv out_csv.csv joinField1 [joinField2, ...]
"""

def get_header_index(header, fields):
    return [next((ix for ix, v in enumerate(header) if v == x), None) for 
            x in fields]

def create_join_header(header1, header2, onFields, suffix1='_1', 
        suffix2='_2'):
    # determine common fields
    commonFields = [field for field in header1 if field in header2]
    commonFieldsNoJoin = [field for field in commonFields if 
            field not in onFields]
    fieldsOnly1 = [field for field in header1 if field not in commonFields]
    fieldsOnly2 = [field for field in header2 if field not in commonFields]
    fieldsCommon1 = [field + suffix1 for field in commonFieldsNoJoin]
    fieldsCommon2 = [field + suffix2 for field in commonFieldsNoJoin]

    joinHeader = []
    for fields in [fieldsOnly1, fieldsCommon1, onFields,
            fieldsOnly2, fieldsCommon2] :
        joinHeader += [field for field in fields]

    # determine indices in the order of the header, separately
    fields1 = fieldsOnly1 + commonFieldsNoJoin + onFields
    fields2 = fieldsOnly2 + commonFieldsNoJoin
    indicesJoinHeader1 = get_header_index(header1, fields1)
    indicesJoinHeader2 = get_header_index(header2, fields2)
    return joinHeader, indicesJoinHeader1, indicesJoinHeader2

def join_lists(list1, list2, onFields):
    iter1 = iter(list1)
    iter2 = iter(list2)
    
    header1 = iter1.next()
    header2 = iter2.next()
    
    joinIndex1 = get_header_index(header1, onFields)
    joinIndex2 = get_header_index(header2, onFields)
    
    joinHeader, indices1, indices2 = create_join_header(header1, header2, 
            onFields)
    yield joinHeader
    for line1 in iter1 :
        joinFields1 = [x for ix, x in enumerate(line1) if ix in joinIndex1]
        matchFound = False
        for line2 in iter(list2):
            joinFields2 = [x for ix, x in enumerate(line2) if ix in joinIndex2]
            if joinFields1 == joinFields2 :
                matchFound = True
                yield ([line1[ix] for ix in indices1] + 
                        [line2[ix] for ix in indices2])
        if not matchFound :
            yield ([line1[ix] for ix in indices1] + 
                    ['' for ix in indices2])


def join_csvs(inCsv1path, inCsv2path, outCsvPath, onFields):
    csv1 = open(inCsv1path, 'rb')
    csv2 = open(inCsv2path, 'rb')
    outfile = open(outCsvPath, 'wb')
    readerCsv1 = csv.reader(csv1)
    readerCsv2 = csv.reader(csv2)
    outcsv = csv.writer(outfile)
    outcsv.writerows(join_lists(readerCsv1, readerCsv2, onFields))
    csv1.close()
    csv2.close()
    outfile.close()
            
if __name__ == "__main__":
    inCsv1path = sys.argv[1]
    inCsv2path = sys.argv[2]
    outCsvPath = sys.argv[3]
    onFields = sys.argv[4:]
    join_csvs(inCsv1path, inCsv2path, outCsvPath, onFields)
