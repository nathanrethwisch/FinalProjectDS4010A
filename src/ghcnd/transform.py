import argparse
from pathlib import Path

from utils import GHCND

if __name__ == '__main__':

    ghcnd = GHCND()
    ghcnd.create_element_tables()
    ghcnd.join_element_tables()
