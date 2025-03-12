from datalake import Datalake

if __name__ == '__main__':
    lake = Datalake('../lake')
    lake.process_fire_perimeter()
