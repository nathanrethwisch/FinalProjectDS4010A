import os
import pandas as pd
import pyarrow.parquet as pq

def get_memory_usage(directory):
    total_memory_usage = 0

    for filename in os.listdir(directory):
        if filename.endswith(".parquet"):
            file_path = os.path.join(directory, filename)
            df = pq.read_table(file_path).to_pandas()
            memory_usage = df.memory_usage(deep=True).sum()/10**9
            print(memory_usage)
            total_memory_usage += memory_usage
            print(total_memory_usage)

    return total_memory_usage

# Example usage
directory_path = 'C:\\Users\\dhruv\\IdeaProjects\\FinalProjectDS4010A\\data\\curated\\ModelOutput'
total_memory = get_memory_usage(directory_path)
print(f"Total memory usage: {total_memory} gb")

## OUTPUT:
# Total memory usage: 0.4524759160000015 gb
