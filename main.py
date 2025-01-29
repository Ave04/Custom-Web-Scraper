from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from time import sleep
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from textblob import TextBlob

nltk.download('stopwords')
nltk.download('punkt')


# Clean and preprocess text
def clean_text(text):
    # Remove special characters (but keep numbers)
    text = re.sub(r'[^\w\s]', '', text)

    # Convert to lowercase
    text = text.lower()

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word not in stop_words]

    return ' '.join(filtered_text)


url_site = 'https://www.forbes.com/'

response = requests.get(url=url_site)
soup = BeautifulSoup(response.text, 'html.parser')

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
# driver.maximize_window()
driver.get(url_site)

# close cookie button
# cookie_button = driver.find_element(By.XPATH, value='//*[@id="ketch-consent-banner"]/div[2]/div[2]/button[2]')
# cookie_button.click()

articles = driver.find_elements(By.CLASS_NAME, "data-viz__title")
article_data = [article.get_attribute("title") for article in articles]

print(article_data)

driver.quit()

# Save scraped data to a DataFrame or file

df = pd.DataFrame(article_data)
df.to_csv('forbes_articles.csv', index=False)

df.columns = ["title"]  # Assign a proper column name
print(df.head())  # Check the structure

# df["cleaned_title"] = df["title"].apply(clean_text)

