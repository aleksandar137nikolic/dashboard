import panel as pn
import pandas as pd
import json
import pymysql
import matplotlib.pyplot as plt

# Load data

with open('mysql-cred.json') as my_json:
    credentials = json.load(my_json)

# MySQL connection settings
host = credentials['host']
user = credentials['user']
password = credentials['password']
database = credentials['database']

# Establish a connection
cnx = pymysql.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

# SQL query to fetch data
query = 'SELECT * FROM stem_salaries'

# Read data into a DataFrame
df = pd.read_sql(query, cnx)

# Close the connection
cnx.close()

# Display the DataFrame
print(df.head(10))

# Create a Panel table
table = pn.widgets.DataFrame(df, name='Data Table')


# Count # of employees per company

company_headcount = df.groupby('company').size().reset_index(name='Count').sort_values('Count', ascending=False).head(10)
print(company_headcount)

#company_headcount.plot(kind='bar')
plt.bar(company_headcount['company'], company_headcount['Count'])
plt.xlabel('Company')
plt.ylabel('Count')
plt.title('Bar Chart Example')
plt.xticks(rotation=45)
plt.show()
# plt.savefig('bar_chart.png')  # Save the chart to a file (optional)

# Create the bar chart
fig, ax = plt.subplots()
ax.bar(company_headcount['company'], company_headcount['Count'])
ax.set_xlabel('Company')
ax.set_ylabel('Count')
ax.set_title('Top 10 Companies')


# Create a Panel component for the matplotlib figure
mpl_pane = pn.pane.Matplotlib(fig, tight=True)

# Create a Panel dashboard
dashboard = pn.Column(
    '# Simple Dashboard',
    #table
    mpl_pane
)
dashboard.show()



