# pylint: disable=missing-module-docstring, missing-function-docstring
import csv
import os
import time

import pandas as pd


def main():

    df_stats = pd.DataFrame({
        column: pd.Series(dtype=dtype)
        for column, dtype in {
            'file': 'str',
            'rows': 'int',
            'time_to_load_tsv': 'float',
            'time_to_write_parquet': 'float'
        }.items()})

    for file in sorted(os.listdir('data')):
        if file.endswith('.tsv'):

            # Load from TSV

            start_time = time.time()

            df = pd.read_csv(f'data/{file}',
                             dtype=str,
                             encoding='utf-8',
                             quoting=csv.QUOTE_NONE,
                             sep='\t')

            time_to_load_tsv = time.time() - start_time

            # Write to Parquet

            start_time = time.time()

            df.to_parquet(f'data/{file[:-4]}.parquet', index=False)

            time_to_write_parquet = time.time() - start_time

            df_stats = pd.concat([df_stats, pd.DataFrame({
                'file': [file],
                'rows': [df.shape[0]],
                'time_to_load_tsv': [time_to_load_tsv],
                'time_to_write_parquet': [time_to_write_parquet]
            })], ignore_index=True)

            print(f'{file}: load tsv: {time_to_load_tsv:.2f}s, write parquet: {
                  time_to_write_parquet:.2f}s')

    print(df_stats)


if __name__ == '__main__':
    total_start_time = time.time()
    main()
    print(f'Total time: {time.time() - total_start_time:.2f}s')

# for run in {1..5}; do python pandas/convert_tsv_to_parquet.py; done

#                    file      rows  time_to_load_tsv  time_to_write_parquet
# 0       name.basics.tsv  13774705         12.923379               6.239671
# 1        title.akas.tsv  49666209         36.687104              20.950299
# 2      title.basics.tsv  11054773         16.754648               7.258535
# 3        title.crew.tsv  10396598          5.697210               2.020425
# 4     title.episode.tsv   8476451          3.208245               1.666130
# 5  title.principals.tsv  87769634         49.737480              32.583021
# 6     title.ratings.tsv   1473482          3.497929               0.250126
# Total time: 199.61s

#                    file      rows  time_to_load_tsv  time_to_write_parquet
# 0       name.basics.tsv  13774705         10.876613               5.996732
# 1        title.akas.tsv  49666209         36.671038              21.406271
# 2      title.basics.tsv  11054773         15.348889               6.760190
# 3        title.crew.tsv  10396598          5.320761               2.011244
# 4     title.episode.tsv   8476451          3.133913               1.654060
# 5  title.principals.tsv  87769634         49.608677              33.603424
# 6     title.ratings.tsv   1473482          4.200313               0.284009
# Total time: 196.98s

#                    file      rows  time_to_load_tsv  time_to_write_parquet
# 0       name.basics.tsv  13774705         11.033738               5.352266
# 1        title.akas.tsv  49666209         35.874315              20.437549
# 2      title.basics.tsv  11054773         14.281258               6.185180
# 3        title.crew.tsv  10396598          5.120206               1.879804
# 4     title.episode.tsv   8476451          3.132300               1.645072
# 5  title.principals.tsv  87769634         49.896451              38.698039
# 6     title.ratings.tsv   1473482          6.000082               0.295731
# Total time: 199.96s

#                    file      rows  time_to_load_tsv  time_to_write_parquet
# 0       name.basics.tsv  13774705         10.932431               5.705916
# 1        title.akas.tsv  49666209         35.710339              19.583129
# 2      title.basics.tsv  11054773         14.212744               6.651926
# 3        title.crew.tsv  10396598          5.502447               1.899057
# 4     title.episode.tsv   8476451          3.172628               1.675552
# 5  title.principals.tsv  87769634         49.389034              34.459343
# 6     title.ratings.tsv   1473482          3.661552               0.279646
# Total time: 192.94s

#                    file      rows  time_to_load_tsv  time_to_write_parquet
# 0       name.basics.tsv  13774705         10.885691               5.547881
# 1        title.akas.tsv  49666209         35.891238              19.519282
# 2      title.basics.tsv  11054773         14.169542               6.390713
# 3        title.crew.tsv  10396598          5.194208               2.010986
# 4     title.episode.tsv   8476451          3.149721               1.649875
# 5  title.principals.tsv  87769634         50.263725              35.195315
# 6     title.ratings.tsv   1473482          4.652201               0.278642
# Total time: 194.90s
