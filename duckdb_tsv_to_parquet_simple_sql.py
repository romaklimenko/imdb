# pylint: disable=missing-module-docstring, missing-function-docstring, line-too-long
import duckdb

FILE = 'name.basics.tsv'

con = duckdb.connect(':memory:')

con.execute(f"""
    CREATE TABLE temp_table AS
    SELECT * FROM read_csv('data/{FILE}', delim='\t', all_varchar=true, quote='')
""")

con.execute(f"""
    COPY temp_table TO 'data/{FILE[:-4]}.parquet' (FORMAT PARQUET)
""")

con.close()
