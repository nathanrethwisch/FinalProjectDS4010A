import argparse
from pathlib import Path

from utils import GHCND

if __name__ == '__main__':
    ghcnd = GHCND()
    ghcnd.init_datalake()
    ghcnd.download_metadata()
    ghcnd.download_stations()
    ghcnd.download_daily_data()
