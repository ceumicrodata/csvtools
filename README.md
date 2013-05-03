# Tools for transforming .csv files

Pipe friendly command line tools for processing csv files with headers.
The design goals of the tools are

1. ease of use - fields are given by name instead of index
1. interoperability within package through pipes
1. minimal interface (i.e. exclusive use of standard input/output wherever possible)


------------------
## Tools

------------------
### select

    - select, reorder and rename fields in stream


------------------
### rmfields

    - remove fields from csv stream


------------------
### extract_map

    - extract a group of fields into a new file with an id
    - only distinct values are stored
    - the output will receive the id field


------------------
### csv2tsv
    convert csv to tsv stream


------------------
### tsv2csv
    convert tsv to csv stream


------------------
### to_postgres

    - create and populate postgres table


```sh
    csv... | csv_to_postgres new-table-name | psql -q [connection options]
```

All fields are created as VARCHAR NOT NULL.
Possible NULL values in csv (unquoted empty strings) are imported as empty
strings.

Possible future improvements:
 - serial primary key column
 - per field data types defined by a config file - field-data-type map
 - custom index/indices (including primary key, unique constraint)

------------------
### unzip
    split csv file into two by columns - in a reversible way

#### Input:

- standard input: csv stream with header
- parameters:
    1. fields
    2. file name to receive fields not explicitly specified
    3. (optional) zip-id field name: `--id=zip-id`, defaults to `id`

#### Output:

- standard output: csv stream with the zip-id and the specified fields
- file whose name was given as parameter: csv file with fields including
  zip-id and fields not on stdout

#### Example
    TBD


### zip
    join two csv files by a common sorted id field - reverse an unzip

Note: by default also removes the field to join on.

#### Input:

- standard input: csv stream with header
- parameters:
    1. other file name to join with
    2. (optional) `--keep-id`
    3. (optional) `--rm` to remove other file

The field to join with is implicitly given, as the only common field name.

#### Output:

- standard output: joined csv stream

#### Example
    TBD


------------------
## Planned tools


------------------
### split
    standard input into file chunks of given size

#### Input:

- standard input: csv stream with header
- parameters:
    1. output chunk size (in data rows)
    2. output file prefix

#### Output:

- standard output: nothing
- files named `output file prefix`.`file number`

Split csv stream with header to files.
Each file has the same header as the input and contain exactly the number of
data rows given.
The last output file might potentially contain less than the chunk size.


------------------
### divide
    into exactly the given number of equal sized files


------------------
### concatenate
    which is reverse of split

Concatenate the inputs, so that the headers are skipped: only the first
header is written.

#### Input:

- parameters:
    1. input file or input file prefix
    2. (optional) input file or input file prefix
    3. ...

The inputs are either file names or prefixes.
The input is a file if it exists.
The input is a prefix if it does not exist as a file, but `prefix` `0`
does exist.
When the input is a prefix the files to be concatenated are all of
the files with `prefix` + number, so that a file exists for every
non-negative integer less than this number.

Thus it is possible to give multiple explicit file names to concatenate
but it is also possible to give only a prefix for a series of files.

#### Output:

- standard output: concatenated csv stream


------------------
### weave
    which is reverse of divide


------------------
## Status

Planned tools are under development, existing tools are in production
use, even if used manually and rarely.

This documentation is in need of some content and improvement + formatting.

Currently tools can be invoked from anywhere by commands like

```sh
python -m csvtools.tool tool-arguments
```

where `tool` is the above tools: `select`, `rmfields`, ...

In the future tools will become console scripts, so that they can be invoked like

```sh
csv_select arguments
csv_rmfields arguments
csv_extract_map arguments
csv_split arguments
csv_divide arguments
csv_concatenate arguments
csv_cat arguments
csv_weave arguments
csv2tsv
tsv2csv
```

------------------
## Projects having similar goals

1. [csvfix](https://code.google.com/p/csvfix/)
   - feature rich, but by not restricting input to csv files with headers,
     *fields can not be given by name*
1. [tsvutils](https://github.com/brendano/tsvutils)
   - for TSV-s, *bunch of shell, python, ruby scripts, no tests, ...*
1. [csvkit](https://github.com/onyxfish/csvkit)
   - mature(!) but *small* set of tools, supports csv variants

