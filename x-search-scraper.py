import subprocess
import sys

required_packages = ['twscrape', 'pandas', 'asyncio']

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level
import pandas as pd

L = 500

async def main():

    api = API()

    keywords = input("Enter the keywords you want to search for: ")
    user = input("Enter user you want to search for (or leave blank): ")
    since_date = input("Enter your query start date (YYYY-MM-DD): ")
    until_date = input("Enter your query end date (YYYY-MM-DD): ")

    query_parts = [keywords.strip()]
    if user.strip():
            query_parts.append(f"from:{user.strip()}")
    if since_date.strip():
            query_parts.append(f"since:{since_date.strip()}")
    if until_date.strip():
            query_parts.append(f"until:{until_date.strip()}")        

    query_parts.append("-grok") #filters grok AI prompts for a more efficient dataset

    query = " ".join(query_parts)
 
    tweets = []
    q = query
    async for tweet in api.search(q, limit = L):
        tweets.append([tweet.date, tweet.user.username, tweet.rawContent])

    print(f"Collected {len(tweets)} tweets.")    
    
    filename = f"{keywords}_{since_date}_{until_date}".strip()
    df = pd.DataFrame(tweets, columns=['Date', 'User', 'Tweet'])
    df.to_csv(f"{filename}.csv", index=False, encoding='utf-8')
    df.to_json(f"{filename}.json", orient='records', lines=True)

    print(f"EXPORTED TO {filename}.csv AND {filename}.json")

if __name__ == "__main__":
    asyncio.run(main())