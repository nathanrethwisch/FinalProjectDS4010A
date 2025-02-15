from pathlib import Path

import pyarrow as pa
from pyarrow import csv, parquet

if __name__ == "__main__":
    source_path = Path("C:/Users/dhruv/OneDrive - Iowa State University/DS4010/superghcnd_full_20250212.csv.gz")
    dest_path = Path("C:/Users/dhruv/Downloads/capstone/superghcnd_full_20250212.parquet")

    writer = None
    with csv.open_csv(source_path) as reader:
        for next_chunk in reader:
            if next_chunk is None:
                break
            if writer is None:
                writer = parquet.ParquetWriter(dest_path, next_chunk.schema)
            next_table = pa.Table.from_batches([next_chunk])
            writer.write_table(next_table)
    writer.close()
