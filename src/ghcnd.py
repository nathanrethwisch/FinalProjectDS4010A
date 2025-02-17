from pathlib import Path

import pyarrow as pa
from pyarrow import csv
import pyarrow.parquet as pq
import pyarrow.dataset as ds



def convert_csv_to_parquet(csv_path, parquet_path):
    writer = None
    with csv.open_csv(csv_path) as reader:
        for next_chunk in reader:
            if next_chunk is None:
                break
            if writer is None:
                writer = pq.ParquetWriter(parquet_path, next_chunk.schema)
            next_table = pa.Table.from_batches([next_chunk])
            writer.write_table(next_table)
    writer.close()


def convert_csv_to_dataset(csv_path, dataset_path):
    dataset = ds.dataset(csv_path, format="csv")
    return dataset

if __name__ == "__main__":
    base_path = Path("C:/Users/dhruv/Downloads/capstone")
    csv_path = base_path / "superghcnd_full_20250212.csv.gz"
    dataset_path = base_path / "superghcnd_full_20250212"
    data = convert_csv_to_dataset(csv_path, dataset_path)
    data.to_table().head()
