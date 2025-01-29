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
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import matplotlib.pyplot as plt


nltk.download('stopwords')
nltk.download('punkt')
nltk.download('vader_lexicon')


# Clean and preprocess text
# def clean_text(text):
#     # Remove special characters (but keep numbers)
#     text = re.sub(r'[^\w\s]', '', text)
#
#     # Convert to lowercase
#     text = text.lower()
#
#     # Remove stopwords
#     stop_words = set(stopwords.words('english'))
#     word_tokens = word_tokenize(text)
#     filtered_text = [word for word in word_tokens if word not in stop_words]
#
#     return ' '.join(filtered_text)


# Perform sentiment analysis using textblob
def get_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity  # Returns a polarity score between -1 (negative) and 1 (positive)


url_site = 'https://www.forbes.com/'

# response = requests.get(url=url_site)
# soup = BeautifulSoup(response.text, 'html.parser')

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
print(df.columns)  # Check the structure

# clean title if needed
# df["cleaned_title"] = df["title"].apply(clean_text)


# Initialize VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Apply sentiment analysis
df["sentiment"] = df["title"].apply(lambda x: sia.polarity_scores(x)["compound"])

# Classify as Positive, Neutral, or Negative
df["sentiment_label"] = df["sentiment"].apply(lambda x: "Positive" if x > 0.05 else ("Negative" if x < -0.05 else "Neutral"))

print(df['sentiment_label'])

# Count sentiment categories
sentiment_counts = df["sentiment_label"].value_counts()

# Create a pie chart
plt.figure(figsize=(6, 6))
plt.pie(
    sentiment_counts,
    labels=sentiment_counts.index,
    autopct='%1.1f%%',
    startangle=140,
    wedgeprops={'edgecolor': 'black'}
)
plt.title("Sentiment Analysis of Forbes News Titles")
plt.show()

# Create a bar chart
plt.figure(figsize=(8, 5))
plt.bar(sentiment_counts.index, sentiment_counts.values, color=["green", "gray", "red"])
plt.xlabel("Sentiment")
plt.ylabel("Count")
plt.title("Sentiment Distribution of Forbes News Titles")
plt.show()