from datalake import Datalake

if __name__ == '__main__':
    lake = Datalake()
    lake.initialize()
    lake.download_ghcnd()
    lake.clean_ghcnd_stations()
    lake.clean_daily()
