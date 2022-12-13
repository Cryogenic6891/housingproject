import time
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine



outPath = "C:/Python/DataSets/"
csvFile = "2bedApa.csv"
df = pd.read_csv(outPath+csvFile, sep='\t')


def showQueryResult(sql):
# This code creates an in-memory table called 'Inventory'.
    engine = create_engine('sqlite://', echo=False)
    connection = engine.connect()
    df.to_sql(name='database', con=connection, if_exists='replace', index=False)
    # This code performs the query.
    queryResult = pd.read_sql(sql, connection)
    return queryResult
# Read all rows from the table.
SQL = "SELECT AVG(Price) AS AveragePrice,Location FROM database WHERE Location = 'Vancouver' OR Location = 'Coquitlam' OR Location = 'Burnaby' OR Location = 'Surrey' GROUP BY Location "
results = showQueryResult(SQL)
print(results)

SQL2 = "SELECT Count(Price) AS SampleSize,Location FROM database WHERE Location = 'Vancouver' OR Location = 'Coquitlam' OR Location = 'Burnaby' OR Location = 'Surrey' GROUP BY Location "
sampleSize = showQueryResult(SQL2)
print(sampleSize)



plt.bar(results['Location'],results['AveragePrice'],color='green')
plt.xlabel("Location")
plt.ylabel("Price per Month ($)")
plt.title("Average Monthly Price of 2 Bedroom Apartment")
plt.show()