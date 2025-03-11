from datalake import Datalake

if __name__ == '__main__':
    lake = Datalake()
    lake.initialize()
    lake.clean_fire_perimeter()
