from utils import GHCND

if __name__ == '__main__':

    ghcnd = GHCND()
    ghcnd.filter_na_stations()
    ghcnd.create_element_tables()
    ghcnd.join_element_tables()
    ghcnd.join_stations_elements()
    ghcnd.clean_data()
    ghcnd.clean_disk()
