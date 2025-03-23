#dependencies
#streamlit, pandas, tweepy, textblob, matplotlib, seaborn
import streamlit as st
import pandas as pd
import tweepy
import textblob as TextBlob
import matplotlib.pyplot as plt
import seaborn as sns


#authorisation details
API_KEY = "M4nU9MH3Z6pvipJatd9kCLDaI"
API_SECRET = "2LLtpobF0hhv4xYpAEJ9U31tUK4f5lkddch4mqmyeaquHHWLIp"
ACCESS_TOKEN = "1759664880964005888-PyTE7KEhRfHJzZcAXKJliXW5Y35cYH"
ACCESS_SECRET = "ao3auzXRltZwFM51Ghbo8eJM7CNEGoPblEbjDARfWZu52"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAABPIyQEAAAAA5E7hTNYMYmhZQC9m4ESXhTUgNFQ%3DuIj4l1mWXgWWaWGGdMQJvqeWjBEa4V4IAaMk7xkvTS3ANuOXdI"


#authentication
auth = tweepy.OAuth1UserHandler(API_KEY,API_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_SECRET)
api = tweepy.API(auth,wait_on_rate_limit=True)


#function to fetch tweets using tweepy
def fetch_tweets(keyword,count = 100):
    tweets_list = []
    try:
        for tweet in tweepy.Cursor(api.search_tweets,q=keyword, lang = "en", tweet_mode = "extended").items(count):
            tweets_list.append([tweet.created_at, tweet.full_text, tweet.user.screen_name])

            df = pd.DataFrame(tweets_list, columns = ["Date","Tweet","User"])
            return df
    except tweepy.errors.TweepyException as e:
        st.error(f"Error fetching tweets {e}")
        return pd.DataFrame(tweets_list, columns = ["Date","Tweet","User"])
    
def analyze_sentiment(tweet):
    analysis = TextBlob(tweet)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return "positive"
    elif polarity < 0:
        return "negative"
    else:
        return "netural"
    
#streamlit dashboard
st.title("Twitter Sentiment Analysis Dashboard")
keyword = st.text_input("Enter a keyword to search tweets", "AI")

if st.button("analyze sentiment"):
    with st.spinner("fetching tweets..."):
        tweets_df = fetch_tweets(keyword, count=100)

    if not tweets_df.empty:
        tweets_df["sentiment"] = tweets_df["Tweet"].apply(analyze_sentiment)

        st.write("### Sample Tweets with Sentiment")
        st.dataframe(tweets_df.head(10))

        sentiment_counts = tweets_df["Sentiment"].value_counts()

        st.write("### Sentiment Distribution")
        pif, ax = plt.subplots()
        ax.pie(sentiment_counts, labels = sentiment_counts.index,autopct='%1.1f%', colors=['red','blue','green'])

        st.write("### Top Tweets per sentiment")
        for sentiment in ["positive", "negative", "neutral"]:
            st.write(f"### {sentiment} tweets")
            top_tweets = tweets_df[tweets_df["sentiment"] == sentiment].head(5)
            for tweet in top_tweets["Tweet"]:
                st.write(f" - {tweet}")