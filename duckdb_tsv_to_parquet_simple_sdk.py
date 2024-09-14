# pylint: disable=missing-module-docstring, missing-function-docstring, line-too-long
import duckdb

FILE = 'name.basics.tsv'

with duckdb.connect(':memory:') as con:
    duckdb \
        .read_csv(f'data/{FILE}', all_varchar=True, quotechar='', sep='\t') \
        .to_parquet(f'data/{FILE[:-4]}.parquet')
