import random
import datetime
import psycopg2
from psycopg2 import sql
import pandas as pd

# Function to generate random timestamps
def random_timestamp(start, end):
    return start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

# PostgreSQL connection details
conn = psycopg2.connect(
    host="localhost",    # Change this to your PostgreSQL host
    database="exampledb",  # Change to your database
    user="docker",  # Change to your PostgreSQL username
    password="docker" , # Change to your PostgreSQL password
    port = 5432
)
cursor = conn.cursor()

# Function to generate dummy data and insert into purchase_trends table
def generate_and_insert_purchase_trends(num_rows):
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2023, 1, 1)
    start_datetime = datetime.datetime(2020, 1, 1)
    end_datetime = datetime.datetime(2023, 1, 1)
    
    for _ in range(num_rows):
        date = random.choice(pd.date_range(start_date, end_date))
        number_of_concert_tickets = random.randint(0, 10)
        number_of_comedy_shows = random.randint(0, 10)
        number_of_sport_events = random.randint(0, 10)
        number_of_online_txns = random.randint(0, 50)
        home_mortgage_purchased_ts = random.randint(1609459200, 1672531199)  # Random Unix timestamp
        customer_id = random.randint(1, 500)
        datetime_created = random_timestamp(start_datetime, end_datetime)
        datetime_updated = random_timestamp(start_datetime, end_datetime)

        # Insert data into purchase_trends table
        insert_query = sql.SQL("""
            INSERT INTO purchase_trends (
                date, number_of_concert_tickets, number_of_comedy_shows,
                number_of_sport_events, number_of_online_txns, 
                home_mortgage_purchased_ts, customer_id, 
                datetime_created, datetime_updated
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """)
        cursor.execute(insert_query, (
            date, number_of_concert_tickets, number_of_comedy_shows,
            number_of_sport_events, number_of_online_txns,
            home_mortgage_purchased_ts, customer_id,
            datetime_created, datetime_updated
        ))

# Function to generate dummy data and insert into checking_account table
def generate_and_insert_checking_account(num_rows):
    start_datetime = datetime.datetime(2020, 1, 1)
    end_datetime = datetime.datetime(2023, 1, 1)
    
    for _ in range(num_rows):
        customer_id = random.randint(1, 500)
        scheduled_payment = random.randint(0, 10000)
        txn_amount = round(random.uniform(100.0, 10000.0), 2)
        debit_or_credit = random.choice([0, 1])  # 0 for debit, 1 for credit
        updt_ts = random_timestamp(start_datetime, end_datetime)
        initial_balance = round(random.uniform(1000.0, 50000.0), 2)

        # Insert data into checking_account table
        insert_query = sql.SQL("""
            INSERT INTO checking_account (
                customer_id, scheduled_payment, txn_amount,
                debit_or_credit, updt_ts, initial_balance
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """)
        cursor.execute(insert_query, (
            customer_id, scheduled_payment, txn_amount,
            debit_or_credit, updt_ts, initial_balance
        ))

# Generate and insert data
num_rows = 1000
#generate_and_insert_purchase_trends(num_rows)
generate_and_insert_checking_account(num_rows)

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()

print(f"Inserted {num_rows} rows into both tables.")
