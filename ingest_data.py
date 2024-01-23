import argparse
import os
import pandas as pd
from sqlalchemy import create_engine
from time import time

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    csv_file = params.csv_file # 'yellow_tripdata_2021-01.csv'
    
    # create egine # connect to db
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # insert data into dv
    df_iter = pd.read_csv(csv_file, iterator=True, chunksize=100000)
    df = next(df_iter)

    # changing the type this columns
    df['tpep_pickup_datetime'] = pd.to_datetime(df.tpep_pickup_datetime)
    df['tpep_dropoff_datetime'] = pd.to_datetime(df.tpep_dropoff_datetime)

    # insert the headers in the db table 
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')


    while True:
        t_start = time()
        df = next(df_iter)
        df['tpep_pickup_datetime'] = pd.to_datetime(df.tpep_pickup_datetime)
        df['tpep_dropoff_datetime'] = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name=table_name, con=engine, if_exists='append')
        t_end = time()
        print(f'inserted another chunk ...., took {t_end - t_start} seconds')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ingest csv data to Postgres")
    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table  for postgres')
    parser.add_argument('--csv_file', required=True, help='csv file')
    # parser.add_argument('--url', required=True, help='url of the csv file')

    args = parser.parse_args()

    main(args)