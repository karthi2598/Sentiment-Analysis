import streamlit as st
import tweepy
import re
import pandas as pd
from textblob import TextBlob
import time


consumer_key = "lF0O2phF3sW7u145zVRu0ngFN"
consumer_key_secret = "1w9yrHjKRGtDm9F3RUE0ptKw3mDmmJyhFGs9ej4uLNRzq9ilCE"
bearer_token = "AAAAAAAAAAAAAAAAAAAAADq4tAEAAAAAw2LzGDUMwJHTaUvXvNoeyg4lYyg%3DVupztXPXxl3oRsmD33ZPiJfqE7obwa2L5q3JAmnrPJPqU56GYb"
access_key = "1775947963476402176-kcpLKYpQddR0gc9N7DKWtEnFkDS018"
access_key_secret = "k077vmUmpPzYHeNOBUsY47tZiARH6kj4w7RpoxzEbBUqM"

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
        response = client.search_recent_tweets(query=query, max_results=100)
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
