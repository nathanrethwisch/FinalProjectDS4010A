from datalake import Datalake

if __name__ == "__main__":
    data = Datalake('../data')
    data.process_states()
