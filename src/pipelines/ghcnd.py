from datalake import Datalake

if __name__ == '__main__':
    lake = Datalake('../../data')
    lake.download_ghcnd()
    lake.process_ghcnd_stations()
    lake.process_ghcnd_daily()
