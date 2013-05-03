'''
Convenience script wrapping knowledge on how to import a csv
file to PostgreSQL.

Usage:
    csv_to_postgres name-of-table-to-create < file.csv |
        psql [connection options - NOT requiring password!]

This is working for at least PostgreSQL psql 9.1.
'''

import csv
import sys


SQL_TEMPLATE = '''\
-- exit if table already exists - avoids double population
\\set ON_ERROR_STOP on

CREATE TABLE {table} (
    {fielddefs}
);

\copy {table} from stdin with csv header force not null {notnullcolumns}
'''


def main():
    table, = sys.argv[1:]
    reader = csv.reader(sys.stdin)
    header = reader.next()
    notnullcolumns = header

    def field_def(field):
        return '{} VARCHAR NOT NULL'.format(field)

    fielddefs = ',\n    '.join(field_def(field) for field in header)

    create_and_import_sql = SQL_TEMPLATE.format(
        table=table,
        fielddefs=fielddefs,
        notnullcolumns=', '.join(notnullcolumns))

    sys.stdout.write(create_and_import_sql)

    writer = csv.writer(sys.stdout)
    writer.writerow(header)
    writer.writerows(reader)


if __name__ == '__main__':
    main()
