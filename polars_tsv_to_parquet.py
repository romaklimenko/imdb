# pylint: disable=missing-module-docstring, missing-function-docstring
import os
import time

import polars as pl


def get_column_names(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        header = f.readline().strip()
    return header.split('\t')


def main():

    df_stats = pl.DataFrame(schema={
                            'file': pl.Utf8,
                            'rows': pl.Int64,
                            'time_to_load_tsv': pl.Float64,
                            'time_to_write_parquet': pl.Float64})

    for file in sorted(os.listdir('data')):
        if file.endswith('.tsv'):

            # Arrange

            file_path = f'data/{file}'
            column_names = get_column_names(file_path)
            schema_overrides = {col: pl.Utf8 for col in column_names}

            # Load from TSV

            start_time = time.time()

            df = pl.read_csv(file_path,
                             encoding='utf-8',
                             quote_char=None,
                             schema_overrides=schema_overrides,
                             separator='\t')

            time_to_load_tsv = time.time() - start_time

            # Write to Parquet

            start_time = time.time()

            df.write_parquet(f'data/{file[:-4]}.parquet')

            time_to_write_parquet = time.time() - start_time

            df_stats = df_stats.vstack(
                pl.DataFrame(
                    {
                        'file': [file],
                        'rows': [df.height],
                        'time_to_load_tsv': [time_to_load_tsv],
                        'time_to_write_parquet': [time_to_write_parquet]
                    }))

            print(f'{file}: load tsv: {time_to_load_tsv:.2f}s, write parquet: {
                  time_to_write_parquet:.2f}s')

    print(df_stats)


if __name__ == '__main__':
    total_start_time = time.time()
    main()
    print(f'Total time: {time.time() - total_start_time:.2f}s')

# for run in {1..5}; do python pola.rs/convert_tsv_to_parquet.py; done

# ┌──────────────────────┬──────────┬──────────────────┬───────────────────────┐
# │ file                 ┆ rows     ┆ time_to_load_tsv ┆ time_to_write_parquet │
# │ ---                  ┆ ---      ┆ ---              ┆ ---                   │
# │ str                  ┆ i64      ┆ f64              ┆ f64                   │
# ╞══════════════════════╪══════════╪══════════════════╪═══════════════════════╡
# │ name.basics.tsv      ┆ 13774705 ┆ 9.443366         ┆ 4.696756              │
# │ title.akas.tsv       ┆ 49666209 ┆ 91.645905        ┆ 6.774255              │
# │ title.basics.tsv     ┆ 11054773 ┆ 6.756502         ┆ 4.177063              │
# │ title.crew.tsv       ┆ 10396598 ┆ 0.446132         ┆ 1.6185                │
# │ title.episode.tsv    ┆ 8476451  ┆ 0.331534         ┆ 1.033456              │
# │ title.principals.tsv ┆ 87769634 ┆ 145.931527       ┆ 10.909271             │
# │ title.ratings.tsv    ┆ 1473482  ┆ 0.366551         ┆ 0.161006              │
# └──────────────────────┴──────────┴──────────────────┴───────────────────────┘
# Total time: 284.35s

# ┌──────────────────────┬──────────┬──────────────────┬───────────────────────┐
# │ file                 ┆ rows     ┆ time_to_load_tsv ┆ time_to_write_parquet │
# │ ---                  ┆ ---      ┆ ---              ┆ ---                   │
# │ str                  ┆ i64      ┆ f64              ┆ f64                   │
# ╞══════════════════════╪══════════╪══════════════════╪═══════════════════════╡
# │ name.basics.tsv      ┆ 13774705 ┆ 6.927027         ┆ 4.767558              │
# │ title.akas.tsv       ┆ 49666209 ┆ 75.379274        ┆ 7.16669               │
# │ title.basics.tsv     ┆ 11054773 ┆ 6.865432         ┆ 3.65374               │
# │ title.crew.tsv       ┆ 10396598 ┆ 0.466211         ┆ 1.426351              │
# │ title.episode.tsv    ┆ 8476451  ┆ 0.31436          ┆ 1.015495              │
# │ title.principals.tsv ┆ 87769634 ┆ 141.14548        ┆ 10.792138             │
# │ title.ratings.tsv    ┆ 1473482  ┆ 0.309603         ┆ 0.167109              │
# └──────────────────────┴──────────┴──────────────────┴───────────────────────┘
# Total time: 260.43s

# ┌──────────────────────┬──────────┬──────────────────┬───────────────────────┐
# │ file                 ┆ rows     ┆ time_to_load_tsv ┆ time_to_write_parquet │
# │ ---                  ┆ ---      ┆ ---              ┆ ---                   │
# │ str                  ┆ i64      ┆ f64              ┆ f64                   │
# ╞══════════════════════╪══════════╪══════════════════╪═══════════════════════╡
# │ name.basics.tsv      ┆ 13774705 ┆ 5.963979         ┆ 4.525079              │
# │ title.akas.tsv       ┆ 49666209 ┆ 82.458508        ┆ 7.052599              │
# │ title.basics.tsv     ┆ 11054773 ┆ 6.567031         ┆ 4.356904              │
# │ title.crew.tsv       ┆ 10396598 ┆ 0.666655         ┆ 1.472071              │
# │ title.episode.tsv    ┆ 8476451  ┆ 0.292067         ┆ 0.970062              │
# │ title.principals.tsv ┆ 87769634 ┆ 138.215462       ┆ 10.504346             │
# │ title.ratings.tsv    ┆ 1473482  ┆ 0.271147         ┆ 0.165711              │
# └──────────────────────┴──────────┴──────────────────┴───────────────────────┘
# Total time: 263.51s

# ┌──────────────────────┬──────────┬──────────────────┬───────────────────────┐
# │ file                 ┆ rows     ┆ time_to_load_tsv ┆ time_to_write_parquet │
# │ ---                  ┆ ---      ┆ ---              ┆ ---                   │
# │ str                  ┆ i64      ┆ f64              ┆ f64                   │
# ╞══════════════════════╪══════════╪══════════════════╪═══════════════════════╡
# │ name.basics.tsv      ┆ 13774705 ┆ 5.799583         ┆ 4.446162              │
# │ title.akas.tsv       ┆ 49666209 ┆ 70.754341        ┆ 6.624542              │
# │ title.basics.tsv     ┆ 11054773 ┆ 6.309861         ┆ 3.995834              │
# │ title.crew.tsv       ┆ 10396598 ┆ 0.421842         ┆ 1.475031              │
# │ title.episode.tsv    ┆ 8476451  ┆ 0.305577         ┆ 0.940387              │
# │ title.principals.tsv ┆ 87769634 ┆ 120.401568       ┆ 10.47416              │
# │ title.ratings.tsv    ┆ 1473482  ┆ 0.251861         ┆ 0.174039              │
# └──────────────────────┴──────────┴──────────────────┴───────────────────────┘
# Total time: 232.40s

# ┌──────────────────────┬──────────┬──────────────────┬───────────────────────┐
# │ file                 ┆ rows     ┆ time_to_load_tsv ┆ time_to_write_parquet │
# │ ---                  ┆ ---      ┆ ---              ┆ ---                   │
# │ str                  ┆ i64      ┆ f64              ┆ f64                   │
# ╞══════════════════════╪══════════╪══════════════════╪═══════════════════════╡
# │ name.basics.tsv      ┆ 13774705 ┆ 5.620352         ┆ 4.736117              │
# │ title.akas.tsv       ┆ 49666209 ┆ 69.939147        ┆ 6.362878              │
# │ title.basics.tsv     ┆ 11054773 ┆ 6.286102         ┆ 3.834926              │
# │ title.crew.tsv       ┆ 10396598 ┆ 0.413587         ┆ 1.530933              │
# │ title.episode.tsv    ┆ 8476451  ┆ 0.284025         ┆ 0.946205              │
# │ title.principals.tsv ┆ 87769634 ┆ 135.559501       ┆ 10.098989             │
# │ title.ratings.tsv    ┆ 1473482  ┆ 0.252147         ┆ 0.174029              │
# └──────────────────────┴──────────┴──────────────────┴───────────────────────┘
# Total time: 246.06s
