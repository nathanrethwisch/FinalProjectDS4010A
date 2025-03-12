from datalake import Datalake

if __name__ == "__main__":
    data = Datalake('../lake')
    data.process_states()
