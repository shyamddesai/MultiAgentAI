import pymysql
import pandas as pd
from bs4 import BeautifulSoup
import requests
import tweepy
import yfinance as yf
import snscrape.modules.twitter as sntwitter
from textblob import TextBlob

def fetch_tweets(query, max_tweets=100):
    tweets_list = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= max_tweets:
            break
        tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.username])
    return pd.DataFrame(tweets_list, columns=['Date', 'Tweet Id', 'Content', 'Username'])

def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def fetch_market_trends(api_key, query=None, from_date=None, to_date=None, language='en', sort_by='relevance',
                        sources=None, domains=None):
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'apiKey': api_key,
        'language': language,
        'sortBy': sort_by,
        'from': from_date,
        'to': to_date,
        'sources': sources,
        'domains': domains
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == 'ok':
        articles = data['articles']
        headlines = [article['title'] for article in articles]
        return headlines
    else:
        print("Error fetching data:", data.get('message', 'Unknown error'))
        return []


def fetch_internal_data():
    # Define your database connection details
    db_config = {
        'host': 'localhost',
        'user': 'oil_user',
        'password': 'aqswde.62001',
        'database': 'oil_production',
        'port': 3306  # default MySQL port
    }

    # Establish the database connection
    try:
        connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            port=db_config.get('port', 3306)  # Use default port if not specified
        )
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return pd.DataFrame()  # Return an empty DataFrame if connection fails

    try:
        # Create a cursor object
        with connection.cursor() as cursor:
            # Define the SQL query to fetch production rates for the oil industry
            sql = "SELECT id, date, production_rate, industry FROM production_rates WHERE industry = 'oil'"
            # Execute the SQL query
            cursor.execute(sql)
            # Fetch all results from the executed query
            result = cursor.fetchall()
            # Convert the result to a pandas DataFrame
            df = pd.DataFrame(result, columns=['id', 'date', 'production_rate', 'industry'])
            return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame if query fails
    finally:
        # Close the database connection
        connection.close()


def fetch_sentiment_data():
    consumer_key = 'your_consumer_key'
    consumer_secret = 'your_consumer_secret'
    access_token = 'your_access_token'
    access_token_secret = 'your_access_token_secret'

    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    api = tweepy.API(auth)
    oil_keywords = ['oil market', 'crude oil', 'petroleum', 'OPEC', 'fossil fuel']
    query = ' OR '.join(oil_keywords)
    tweets = api.search(q=query, lang='en', count=100)
    return [tweet.text for tweet in tweets]


def fetch_historical_prices():
    data = yf.download('CL=F', start='2020-01-01', end='2020-12-31')
    return data



if __name__ == "__main__":
    def main():
        internal_data = fetch_internal_data()
        if internal_data.empty:
            print("No internal data fetched.")
            return

        #print("Internal Production Data:", internal_data)

        api_key = '34b2d0895c874d81b7c4e296d03f851d'  # Replace with your NewsAPI key
        # Example parameters
        queries = [
            "(oil prices OR gas prices OR crude oil OR natural gas OR fossil fuels)",
            "(OPEC OR oil market OR energy market OR petroleum market OR oil demand OR oil supply)",
            "(oil industry OR energy companies OR oil production OR energy sector OR ExxonMobil OR Chevron OR BP OR Shell)",
            "(oil sanctions OR oil tariffs OR energy policy OR oil regulations OR oil trade OR geopolitical tensions)",
            "(renewable energy OR oil exploration OR drilling technology OR energy transition OR carbon emissions)",
            "(SPE OR Society of Petroleum Engineers OR oil conference OR energy summit OR industry forum)"
        ]
        from_date = '2024-05-11'
        to_date = '2024-06-10'
        language = 'en'
        sort_by = 'relevancy'
        sources = 'reuters,bloomberg,bbc-news,cnn,the-wall-street-journal,the-new-york-times,financial-times,forbes,al-jazeera-english,business-insider,cnbc'
        domains = 'reuters.com,bloomberg.com,bbc.co.uk,cnn.com,wsj.com,nytimes.com,ft.com,forbes.com,aljazeera.com,businessinsider.com,cnbc.com'

        all_headlines=[]
        for query in queries:
            market_trends = fetch_market_trends(api_key, query, from_date, to_date, language, sort_by, sources, domains)
            all_headlines.extend(market_trends)

        print("Market Trends:")
        for headline in market_trends:
            print(headline)

        query = 'oil OR gas OR OPEC OR SPE'
        max_tweets = 100  # Adjust the number of tweets to fetch
        tweets_df = fetch_tweets(query, max_tweets)

        # Perform sentiment analysis
        tweets_df['Sentiment'] = tweets_df['Content'].apply(analyze_sentiment)

        print("Tweets with Sentiment Analysis:")
        print(tweets_df.head())

        #sentiment_data = fetch_sentiment_data()
        #print("Sentiment Data:")
        #for tweet in sentiment_data:
        #    print(tweet)

        historical_prices = fetch_historical_prices()
        #print("Historical Prices:", historical_prices)

        # Data cleaning and preprocessing
        internal_data.drop_duplicates(inplace=True)  # Remove duplicate entries
        internal_data.ffill(inplace=True)  # Fill missing values with forward fill method
        internal_data['date'] = pd.to_datetime(internal_data['date'])  # Convert date column to datetime format
        internal_data['production_rate'] = internal_data['production_rate'].astype(
            float)  # Ensure production_rate is of float type

        # Print cleaned data
        #print("Cleaned Production Data:", internal_data)

    main()
