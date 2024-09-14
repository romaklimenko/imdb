# pylint: disable=missing-module-docstring, missing-function-docstring, line-too-long
import os
import time

import duckdb


def main():
    con = duckdb.connect(':memory:')

    con.execute("""
        CREATE OR REPLACE TABLE df_stats (
            file VARCHAR,
            rows INTEGER,
            time_to_load_tsv FLOAT,
            time_to_write_parquet FLOAT
        )
    """)

    for file in sorted(os.listdir('data')):
        if file.endswith('.tsv'):

            # Arrange

            file_path = f'data/{file}'

            # Load from TSV

            start_time = time.time()

            con.execute(f"""
                CREATE OR REPLACE TABLE temp_table AS
                SELECT * FROM read_csv('{file_path}', delim='\t', all_varchar=true, quote='')
            """)

            time_to_load_tsv = time.time() - start_time

            row_count = con.execute(
                'SELECT COUNT(*) FROM temp_table').fetchone()[0]

            # Write to Parquet

            start_time = time.time()

            con.execute(f"""
                COPY temp_table TO 'data/{file[:-4]}.parquet' (FORMAT PARQUET)
            """)

            time_to_write_parquet = time.time() - start_time

            con.execute("""
                INSERT INTO df_stats VALUES (?, ?, ?, ?)
            """, [file, row_count, time_to_load_tsv, time_to_write_parquet])

            print(f'{file}: load tsv: {time_to_load_tsv:.2f}s, write parquet: {
                  time_to_write_parquet:.2f}s')

    df_stats = con.execute('SELECT * FROM df_stats').df()
    print(df_stats)

    con.close()


if __name__ == '__main__':
    total_start_time = time.time()
    main()
    print(f'Total time: {time.time() - total_start_time:.2f}s')

# for run in {1..5}; do python duckdb_tsv_to_parquet_sql.py; done

#                    file      rows  time_to_load_tsv  time_to_write_parquet
# 0       name.basics.tsv  13774705          1.379998               3.659557
# 1        title.akas.tsv  49666209          4.727510              16.042751
# 2      title.basics.tsv  11054773          3.358746               3.559898
# 3        title.crew.tsv  10396598          0.551299               1.160159
# 4     title.episode.tsv   8476451          0.484668               0.621722
# 5  title.principals.tsv  87769634          6.795673              22.900936
# 6     title.ratings.tsv   1473482          0.949025               0.126737
# Total time: 66.87s

#                    file      rows  time_to_load_tsv  time_to_write_parquet
# 0       name.basics.tsv  13774705          1.273344               2.772715
# 1        title.akas.tsv  49666209          5.063885              13.920846
# 2      title.basics.tsv  11054773          2.679705               3.307260
# 3        title.crew.tsv  10396598          0.547847               1.104008
# 4     title.episode.tsv   8476451          0.482873               0.678877
# 5  title.principals.tsv  87769634          6.649331              21.747505
# 6     title.ratings.tsv   1473482          0.957212               0.112975
# Total time: 61.79s

#                    file      rows  time_to_load_tsv  time_to_write_parquet
# 0       name.basics.tsv  13774705          1.314882               2.662638
# 1        title.akas.tsv  49666209          4.702453              13.884505
# 2      title.basics.tsv  11054773          2.515679               3.439650
# 3        title.crew.tsv  10396598          0.526245               1.176139
# 4     title.episode.tsv   8476451          0.495987               0.590272
# 5  title.principals.tsv  87769634          6.843617              24.783892
# 6     title.ratings.tsv   1473482          0.883216               0.112614
# Total time: 64.39s

#                    file      rows  time_to_load_tsv  time_to_write_parquet
# 0       name.basics.tsv  13774705          1.204235               2.745026
# 1        title.akas.tsv  49666209          4.595074              14.176809
# 2      title.basics.tsv  11054773          2.434611               3.225452
# 3        title.crew.tsv  10396598          0.582064               1.462299
# 4     title.episode.tsv   8476451          0.417020               0.665635
# 5  title.principals.tsv  87769634          6.676824              22.080299
# 6     title.ratings.tsv   1473482          0.959504               0.115386
# Total time: 61.78s

#                    file      rows  time_to_load_tsv  time_to_write_parquet
# 0       name.basics.tsv  13774705          1.284649               2.656536
# 1        title.akas.tsv  49666209          4.559265              13.942426
# 2      title.basics.tsv  11054773          2.462919               3.376270
# 3        title.crew.tsv  10396598          0.504721               1.220647
# 4     title.episode.tsv   8476451          0.479378               0.620194
# 5  title.principals.tsv  87769634          6.635607              24.119877
# 6     title.ratings.tsv   1473482          0.984407               0.127887
# Total time: 63.48s
