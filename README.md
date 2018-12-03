# Twitter-user-reports

## Creating twitter access tokens
If you already have access credentials, skip this section.
1. Go to https://apps.twitter.com/ and create a developer account.
2. Click on the "Create New App" button, fill in the details and agree the Terms of Service.
3. Navigate to "Keys and Access Tokens" section and take a note of your Consumer Key and Secret
4. In the same section click on "Create my access token" button
Take note of your Access Token and Access Token Secret

## twiiter_credentials.json

Add the aforementioned keys to a json file:

    import json
    
    credentials = {}  
    credentials['consumer_key'] = ...  
    credentials['consumer_secret''] = ...  
    credentials['access_key'] = ...  
    credentials['access_secret'] = ...

with open("twitter_credentials.json", "w") as file:  
    json.dump(credentials, file)
    
## Install dependencies
In terminal,

    pip install nltk
    pip install urlparse
    pip install twython

In Python console,

    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    
## Running the code

Run user_reports.py.