# pylint: disable=missing-module-docstring, missing-function-docstring
import csv

import pandas as pd

FILE = 'name.basics.tsv'

df = pd.read_csv(f'data/{FILE}',
                 dtype=str,
                 encoding='utf-8',
                 quoting=csv.QUOTE_NONE,
                 sep='\t')

df.to_parquet(f'data/{FILE[:-4]}.parquet', index=False)
