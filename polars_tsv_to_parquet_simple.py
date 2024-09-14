# pylint: disable=missing-module-docstring, missing-function-docstring
import polars as pl

FILE = 'name.basics.tsv'

file_path = f'data/{FILE}'

with open(file_path, 'r', encoding='utf-8') as f:
    header = f.readline().strip()
column_names = header.split('\t')

df = pl.read_csv(file_path,
                 encoding='utf-8',
                 quote_char=None,
                 schema_overrides={col: pl.Utf8 for col in column_names},
                 separator='\t')

df.write_parquet(f'data/{FILE[:-4]}.parquet')
