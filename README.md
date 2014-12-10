# Tools for transforming .csv files

Pipe friendly command line tools for processing CSV files with headers.

CSV files
- have a header row
- use `,` as field separator and `"` as quote character
- are well formatted according to [rfc 4180](https://tools.ietf.org/html/rfc4180)
- all rows have the same number of fields


------------------
## Installation

    pip install csvtools

Except, this works only internally @CEU, not released to PyPI: the csvtools package there is not this one (see #6).  This package will be rebranded to resolve this issue.


------------------
## Tools

### Structure manipulation

- `add_id`
- `add_fields`  (TODO: implement)
- `rmfields`  (TODO: rename to `drop_fields`?)
- `select` (TODO: rename to `cut`)
- `extract_map`
- `unzip`
- `zip`

### Map-reduce helpers
- `split`
- `concatenate`

### Conversion tools
- `csv_to_tsv`
- `tsv_to_csv`
- `to_postgres`
- `to_sqlite`  (TODO: implement)
- `from-sqlite`  (TODO: implement)

### Temporal CSV tools (dealing with dates)
- `normalize_date`  (TODO: implement)
- `drop_bad_date`  (TODO: implement)
- `snapshot`
- `snapshot_quality`  (TODO: implement)


------------------
## The design goals of the tools are

- ease of use
    - minimal no-nonsense interface (file a bug if something is non-obvious!)
    - exclusive use of standard input/output wherever possible
    - composability with pipes
    - fields are referenced by name instead of index
- speed - simplicity results in speed, pipes enable use of multiple CPUs
- python 3 compatibility

Please note, that not all of the goals are achieved for all tools, yet.


------------------
## Status

The tools are in production use.

This documentation is in need of some content and improvement.

The package will be rebranded as its name is taken on PyPI (#6).

Raise issues on [github](https://github.com/ceumicrodata/csvtools/issues) for questions, bugs, problems, or worthy alternatives not mentioned below.

You can also open pull requests.


------------------
## Projects having similar goals

Python's csv module is exceptionally good, thus CSV processing is a low hanging fruit in Python.

A lot of random tools can be found, but there is only few well maintained projects.

Probably the best known and most mature is [csvkit](https://github.com/onyxfish/csvkit).

There is an overlap between the tools between csvtools and csvkit, in those cases csvtools should be recognizably faster (probably due to csvkit supporting csv variants or more functionality???).
