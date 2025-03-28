import argparse
from pathlib import Path

from utils import GHCND

if __name__ == '__main__':
    ghcnd = GHCND()
    ghcnd.clean_stations()
    ghcnd.clean_daily()
