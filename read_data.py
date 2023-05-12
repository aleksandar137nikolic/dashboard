import pandas as pd
import pymysql
#from sqlalchemy import create_engine
import json

# Specify the file path to your CSV file
file_path = '/Users/anikolic/Documents/Projects/R/stem-salareis/data/raw/Levels_Fyi_Salary_Data.csv'

# Load the CSV file
data = pd.read_csv(file_path)

# Get the column names
column_names = data.columns.tolist()
for i in column_names:
    print(i)


# Select specific columns by name
data = data[['company', 'level','title','totalyearlycompensation','location','Education','basesalary','gender']]

# Replace NaaN with -99
data.fillna(-99, inplace=True)

print(data.head(10))
print(data['gender'].unique())


# Check the data types
data_types = data.dtypes
#print(data_types)

# Load into the DB

# Create a new table
# SQL query to create a new table
create_table_query = '''
CREATE TABLE IF NOT EXISTS stem_salaries (
    id INT PRIMARY KEY AUTO_INCREMENT,
    company VARCHAR(255),
    level VARCHAR(255),
    title VARCHAR(255),
    totalyearlycompensation decimal(13,2),
    location varchar(255),
    education varchar(255),
    gender varchar(50)
);
'''

with open('mysql-cred.json') as json_file:
    credentials = json.load(json_file)

host = credentials['host']
user = credentials['user']
password = credentials['password']
database = credentials['database']


try:
    # Create a connection
    connection = pymysql.connect(host=host, user=user, password=password, database=database)
    print("Connection successful!")

    # Proceed with your database operations here

     # Create a cursor object
    cursor = connection.cursor()

    # Execute the create table query
    cursor.execute(create_table_query)

    # Commit the changes
    connection.commit()

    print("Table created successfully!")

    # SQL query to insert data into the table
    insert_query = f"INSERT INTO stem_salaries (company, level, title, totalyearlycompensation, location, education, gender) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    # Prepare the data as a list of tuples
    values = [(row['company'], row['level'], row['title'], row['totalyearlycompensation'], row['location'], row['Education'], row['gender']) for _, row in data.iterrows()]

    # Execute the query with multiple values
    cursor.executemany(insert_query, values)

    # Commit the changes
    connection.commit()

except pymysql.Error as e:
    error_message = str(e)
    print("Connection error:", error_message)




