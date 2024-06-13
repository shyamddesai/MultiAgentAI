import pymysql
import pandas as pd
import requests
import yfinance as yf

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

def fetch_weather_data(api_key, location='Abu Dhabi'):
        url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}'
        response = requests.get(url)
        data = response.json()
        return data


def fetch_historical_prices():
    data = yf.download('NG=F', start='1960-01-01', end='2024-06-01')
    return data


def write_historical_prices_to_file(data, filename='historical_pricesNG.txt'):
    with open(filename, 'w') as file:
        # Write the header
        file.write("Date,Open,High,Low,Close,Volume,Adj Close\n")

        # Iterate over each row in the DataFrame and write to the file
        for date, row in data.iterrows():
            file.write(
                f"{date},{row['Open']},{row['High']},{row['Low']},{row['Close']},{row['Volume']},{row['Adj Close']}\n")


if __name__ == "__main__":
    def main():

        ##yfinance crude oil and natural gas
        historical_prices = fetch_historical_prices()
        print("Historical Prices:", historical_prices)
        # Write the historical prices to a file
        write_historical_prices_to_file(historical_prices)

        ##internal data with sample dataset
        internal_data = fetch_internal_data()
        if internal_data.empty:
            print("No internal data fetched.")
            return

        print("Internal Production Data:", internal_data)

        #Data cleaning and preprocessing
        internal_data.drop_duplicates(inplace=True)  # Remove duplicate entries
        internal_data.ffill(inplace=True)  # Fill missing values with forward fill method
        internal_data['date'] = pd.to_datetime(internal_data['date'])  # Convert date column to datetime format
        internal_data['production_rate'] = internal_data['production_rate'].astype(float)  # Ensure production_rate is of float type

         #Print cleaned data
        print("Cleaned Production Data:", internal_data)

        api_key = '4b43bb6a07214bcd85844122241306'  # Replace with your WeatherAPI key
        weather_data = fetch_weather_data(api_key)

        print("Weather Data:", weather_data)



if __name__ == "__main__":
    main()
