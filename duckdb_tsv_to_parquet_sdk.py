# pylint: disable=missing-module-docstring, missing-function-docstring, line-too-long
import os
import time

import duckdb


def main():
    with duckdb.connect(':memory:') as con:

        con.execute("""
            CREATE TABLE df_stats (
                file VARCHAR,
                rows INTEGER,
                time_to_load_tsv FLOAT,
                time_to_write_parquet FLOAT
            )
        """)

        for file in sorted(os.listdir('data')):
            if file.endswith('.tsv'):

                # Load from TSV

                start_time = time.time()

                table = duckdb.read_csv(f'data/{file}', all_varchar=True, quotechar='', sep='\t')

                time_to_load_tsv = time.time() - start_time

                # Write to Parquet

                start_time = time.time()

                table.to_parquet(f'data/{file[:-4]}.parquet')

                time_to_write_parquet = time.time() - start_time

                con.execute("""
                    INSERT INTO df_stats VALUES (?, ?, ?, ?)
                """, [file, table.shape[0], time_to_load_tsv, time_to_write_parquet])

                print(f'{file}: load tsv: {time_to_load_tsv:.2f}s, write parquet: {
                    time_to_write_parquet:.2f}s')

        df_stats = con.execute('SELECT * FROM df_stats').df()
        print(df_stats)


if __name__ == '__main__':
    total_start_time = time.time()
    main()
    print(f'Total time: {time.time() - total_start_time:.2f}s')

# for run in {1..5}; do python duckdb_tsv_to_parquet_sdk.py; done

#                    file      rows  time_to_load_tsv  time_to_write_parquet
# 0       name.basics.tsv  13774705          0.018348               3.624165
# 1        title.akas.tsv  49666209          0.016955              12.325043
# 2      title.basics.tsv  11054773          0.018713               3.907468
# 3        title.crew.tsv  10396598          0.016690               1.490942
# 4     title.episode.tsv   8476451          0.017295               0.857380
# 5  title.principals.tsv  87769634          0.018615              17.269178
# 6     title.ratings.tsv   1473482          0.006747               0.159984
# Total time: 46.72s

#                    file      rows  time_to_load_tsv  time_to_write_parquet
# 0       name.basics.tsv  13774705          0.016825               3.142907
# 1        title.akas.tsv  49666209          0.016909              13.943434
# 2      title.basics.tsv  11054773          0.018914               3.965890
# 3        title.crew.tsv  10396598          0.015652               1.452260
# 4     title.episode.tsv   8476451          0.015862               0.823993
# 5  title.principals.tsv  87769634          0.018483              17.823105
# 6     title.ratings.tsv   1473482          0.005402               0.221289
# Total time: 48.80s

#                    file      rows  time_to_load_tsv  time_to_write_parquet
# 0       name.basics.tsv  13774705          0.018385               3.245435
# 1        title.akas.tsv  49666209          0.016611              12.599939
# 2      title.basics.tsv  11054773          0.018996               4.008519
# 3        title.crew.tsv  10396598          0.015465               1.635101
# 4     title.episode.tsv   8476451          0.016333               0.895878
# 5  title.principals.tsv  87769634          0.037420              16.749037
# 6     title.ratings.tsv   1473482          0.005898               0.157998
# Total time: 46.83s

#                    file      rows  time_to_load_tsv  time_to_write_parquet
# 0       name.basics.tsv  13774705          0.017087               3.388999
# 1        title.akas.tsv  49666209          0.016937              12.931180
# 2      title.basics.tsv  11054773          0.018779               3.867118
# 3        title.crew.tsv  10396598          0.016405               1.403635
# 4     title.episode.tsv   8476451          0.016060               0.907175
# 5  title.principals.tsv  87769634          0.017978              17.177073
# 6     title.ratings.tsv   1473482          0.006077               0.163441
# Total time: 47.23s

#                    file      rows  time_to_load_tsv  time_to_write_parquet
# 0       name.basics.tsv  13774705          0.016668               2.959149
# 1        title.akas.tsv  49666209          0.016994              12.553131
# 2      title.basics.tsv  11054773          0.018798               3.895125
# 3        title.crew.tsv  10396598          0.017674               1.556504
# 4     title.episode.tsv   8476451          0.016591               0.794665
# 5  title.principals.tsv  87769634          0.017818              17.119040
# 6     title.ratings.tsv   1473482          0.005796               0.160659
# Total time: 46.20s
