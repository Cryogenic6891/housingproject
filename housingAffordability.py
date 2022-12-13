import time
import pandas as pd

from sqlalchemy import create_engine
from selenium import webdriver
from bs4 import BeautifulSoup
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
# driver = webdriver.Chrome(ChromeDriverManager().install())
Path = "/Python/ChromeDriver/"
File = 'chromedriver.exe'
URL = "https://vancouver.craigslist.org/search/apa"
browser = webdriver.Chrome(service=Service(Path+File))
browser.get(URL)

# Give the browser time to load all content.
time.sleep(1)

SEARCH_TERM = "2 bedroom"
search = browser.find_element(By.CSS_SELECTOR,"#query")

search.send_keys(SEARCH_TERM)

# Find the search button - this is only enabled when a search query is entered
button = browser.find_element(By.CSS_SELECTOR,".icon-search")
button.click()  # Click the button.
time.sleep(3)

# content = browser.find_elements_by_css_selector(".cp-search-result-item-content")
cleanStringTitle = []
cleanStringPrice = []
cleanStringLoc = []
pageNum = 1;
for i in range(0, 10):

    titleContent = browser.find_elements(By.CSS_SELECTOR, ".hdrlnk")
    priceContent = browser.find_elements(By.CSS_SELECTOR, ".result-meta .result-price")
    locContent = browser.find_elements(By.CSS_SELECTOR, ".result-hood")

    for e in titleContent:
        textContent = e.get_attribute('innerHTML')

        # Beautiful soup removes HTML tags from our content if it exists.
        soup = BeautifulSoup(textContent, features="lxml")
        rawString = soup.get_text().strip()

        cleanStringTitle.append(rawString)

    for e in priceContent:
        textContent = e.get_attribute('innerHTML')

        soup = BeautifulSoup(textContent, features="lxml")
        rawString = soup.get_text().strip()
        rawString = rawString.replace("$","")
        rawString = rawString.replace(",", "")
        cleanStringPrice.append(rawString)

    for e in locContent:
        textContent = e.get_attribute('innerHTML')

        soup = BeautifulSoup(textContent, features="lxml")
        rawString = soup.get_text().strip()
        rawString = rawString.replace("(","")
        rawString = rawString.replace(" ", "")
        rawString = rawString.replace(")", "")
        rawString = rawString.replace("Ave", "")
        rawString = rawString.replace("ave", "")
        rawString = rawString.replace("nue", "")
        rawString = rawString.replace("Street", "")
        rawString = rawString.replace(" A ", "")
        rawString = rawString.replace(" B ", "")
        rawString = rawString.replace("B ", "")
        rawString = rawString.replace("layton", "")
        rawString = rawString.replace(",", "")
        rawString = rawString.replace("Kingsway", "")
        rawString = rawString.replace("BC", "")
        rawString = rawString.replace(" C ", "")
        rawString = rawString.replace("Sureey", "Surrey")
        rawString = rawString.replace("surrey", "Surrey")
        rawString = rawString.replace("-", "")
        rawString = rawString.replace("vancouver", "Vancouver")
        rawString = rawString.replace("richmond", "Richmond")
        rawString = rawString.replace("BURNABY", "Burnaby")
        rawString = rawString.replace("newwestminster", "NewWestminster")
        rawString = rawString.replace("westVancouver", "WestVancouver")
        rawString = rawString.replace("Bayview", "")
        rawString = rawString.replace("BLangley", "Langley")
        rawString = rawString.replace("SURREY", "Surrey")
        rawString = rawString.replace("Kitsilano", "Vancouver")

        rawString = re.sub(r'[0-9]+','',rawString)
        cleanStringLoc.append(rawString)

    pageNum += 1
    nbutton = browser.find_element(By.CSS_SELECTOR, ".next")
    nbutton.click()  # Click the button.

    time.sleep(3)

dataSetTitle = { 'Title' : cleanStringTitle, 'Price' : cleanStringPrice, 'Location' : cleanStringLoc}

df = pd.DataFrame(dataSetTitle, columns=['Title','Price','Location'])
# Show all columns.
pd.set_option('display.max_columns', None)
# Increase number of columns that display on one line.
pd.set_option('display.width', 1000)

outPath = "C:/Python/DataSets/"
csvFile = "2bedApa.csv"
df.to_csv(outPath+csvFile, sep='\t')

dfIN = pd.read_csv(outPath+csvFile, sep='\t')


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

addResults = showQueryResult(SQL2)
print(addResults)