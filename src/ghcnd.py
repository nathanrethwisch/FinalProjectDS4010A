from pathlib import Path
from pyarrow import csv, parquet
import pyarrow as pa

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

# def list_files_http(url) -> list[str]:
#     """Naively lists files from an HTTP server directory by grabbing all HTML hrefs
#     :param url: HTTP Server directory URL
#     :return: List of files in HTTP server directory
#     """
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, 'html.parser')
#         files = [a['href'] for a in soup.find_all('a') if a.has_attr('href')]
#         return files
#     except requests.exceptions.RequestException as e:
#         print(f"Error accessing {url}: {e}")
#         return []


# def download_large_file(url, destination):
#     """
#     Download large blobs by streaming direct to disk.
#     :param url: Valid HTTP URL file
#     :param destination: Path or Path-like object
#     """
#     try:
#         # Check if the file already exists and delete it
#         if os.path.exists(destination):
#             os.remove(destination)
#             print(f"Existing file '{destination}' deleted.")
#         # Send a GET request to the URL with streaming enabled
#         with requests.get(url, stream=True) as response:
#             response.raise_for_status()  # Check for HTTP errors
#
#             # Get the total file size from the response headers
#             total_size = int(response.headers.get('content-length', 0))
#             total_size_mb = total_size / (1024 * 1024)
#             print(f"File size: {total_size_mb:.2f} MB")
#
#             # Open the destination file in write-binary mode
#             with open(destination, 'wb') as f:
#                 # Initialize the progress bar
#                 with tqdm(total=total_size_mb, unit='MB', unit_scale=True, desc='Downloading', ncols=100) as pbar:
#                     start_time = time.time()
#                     # Write the file in chunks to avoid memory issues
#                     for chunk in response.iter_content(chunk_size=8192):
#                         if chunk:
#                             f.write(chunk)
#                             # Update the progress bar
#                             pbar.update(len(chunk) / (1024 * 1024))
#                             # Update the progress bar description with elapsed time
#                             elapsed_time = time.time() - start_time
#                             pbar.set_postfix(elapsed=f"{elapsed_time:.2f}s")
#         print("File downloaded successfully!")
#     except requests.exceptions.RequestException as e:
#         print("Error downloading the file:", e)


# if __name__ == "__main__":


# metadata_url = "https://www.ncei.noaa.gov/pub/data/ghcn/daily/readme.txt"
# root_url = "https://www.ncei.noaa.gov/pub/data/ghcn/daily/superghcnd"
# output_dir = Path("C:/Users/dhruv/Downloads/capstone")
#
# download_large_file(metadata_url, output_dir / 'readme.txt')
#
# files = list_files_http(root_url)
# superghcnd_url = f'{root_url}/{files[-1]}'
# print(f"Downloading {files[-1]} to {output_dir}")
# download_large_file(superghcnd_url, output_dir / files[-1])
