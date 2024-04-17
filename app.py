import streamlit as st
import tweepy
import re
import pandas as pd
from textblob import TextBlob
import time


consumer_key = "kprGTrSpOWVoATFDN8d8C5PA3"
consumer_key_secret = "aNtMpCQVsTAa8fJa0JrA5Ivitl7aCkY92Bkj43k6szEZUK7khf"
bearer_token = "AAAAAAAAAAAAAAAAAAAAADq4tAEAAAAA3c%2Fh1SWI%2FgI5Ccd%2F04J8Er5VT3w%3D5M7hx2hCSFl0L46CiBu7ZiGTKpwrQvW8rCNZZN4hCnZ9Flylpa"
access_key = "1775947963476402176-rL4zT6QEBxgoeAQPwwZ2YX2bk200Rh"
access_key_secret = "4wmFlJEOx0dUnSkGnUYVo7WcWR2bKltwpEIKiOLK33Kkx"

# Initialize Tweepy client
client = tweepy.Client(bearer_token=bearer_token)

# Function to preprocess text
def preprocess_text(text):
    # Convert to lower case
    text = text.lower()
    # Remove user handles
    text = re.sub("@[\w]*", "", text)
    # Remove links
    text = re.sub(r"http\S+|www\S+", "", text)
    # Remove digits and special characters
    text = re.sub("[^a-zA-Z#]", " ", text)
    # Remove additional spaces
    text = re.sub("\s+", " ", text)
    return text

# Function to get sentiment
def get_sentiment(tweet):
    analysis = TextBlob(tweet)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return 'POSITIVE'
    elif polarity < 0:
        return 'NEGATIVE'
    else:
        return 'NEUTRAL'

# Streamlit app
def main():
    # Set title
    st.title('Twitter Sentiment Analysis')

    # Get tweets
    query = st.text_input('Enter Twitter query (e.g., #iphone16)')
    if st.button('Get Tweets'):
        response = client.search_recent_tweets(query=query, max_results=10)
        tweets = response.data

        # Process tweets
        sentiment_values = []
        for tweet in tweets:
            original_tweet = tweet.text
            clean_tweet = preprocess_text(original_tweet)
            sentiment = get_sentiment(clean_tweet)
            sentiment_values.append(sentiment)

            # Display tweet and sentiment
            st.write('------------------------Tweet-------------------------------')
            st.write(original_tweet)
            st.write('------------------------------------------------------------')
            st.write('Sentiment:', sentiment)
            time.sleep(1)

        # Create DataFrame
        df = pd.DataFrame({'Sentiment': sentiment_values})

        # Plot sentiment distribution
        st.write('Sentiment Distribution:')
        st.bar_chart(df['Sentiment'].value_counts())

if __name__ == '__main__':
    main()
