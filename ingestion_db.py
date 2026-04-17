import pandas as pd
import os
import logging
import time
import sqlite3

def ingest_db(df, table_name, conn):
    df.to_sql(table_name, con=conn, if_exists='replace', index=False)

def run_ingestion():
    conn = sqlite3.connect('inventory.db')
    start = time.time()

    first_chunk = True  

    for file in os.listdir():
        if file.endswith('.csv'):
            print("Processing:", file)

            if file == 'sales.csv':
                for chunk in pd.read_csv(file, chunksize=200000):
                    if first_chunk:
                        chunk.to_sql('sales', con=conn, if_exists='replace', index=False)
                        first_chunk = False
                    else:
                        chunk.to_sql('sales', con=conn, if_exists='append', index=False)
            else:
                df = pd.read_csv(file)
                ingest_db(df, file[:-4], conn)

    end = time.time()
    total_time = (end - start) / 60
    logging.info('----------Ingestion Complete---------')
    logging.info(f'Total Time Taken: {total_time:.2f} minutes')
    conn.close()
    return conn  # return fresh conn reference is not needed, caller should make their own

if __name__ == '__main__':
    logging.basicConfig(       
        filename="logs/ingestion_db.log",
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filemode="a"
    )
    run_ingestion()