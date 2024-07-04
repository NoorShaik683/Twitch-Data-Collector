# Twitch-Data-Collector

This repository contains an example Python application demonstrating how to implement Twitch Data Collection using FastAPI.

## DEMO

[twitch-data-collector.webm](https://github.com/NoorShaik683/Twitch-Data-Collector/assets/106299708/95ad1639-50bb-4738-a840-00c7f0474fa7)



## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/NoorShaik683/Twitch-Data-Collector.git
   cd your_repository
   ```

2. Install dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Twitch Application Setup:**

   - Create a new application on the [Twitch Developer Portal](https://dev.twitch.tv/console).
   - Obtain your `CLIENT_ID` and `CLIENT_SECRET`.
   - Configure the `REDIRECT_URI` in your Twitch application settings. Ensure it matches the redirect URI in your Flask application (`http://localhost:3000/callback` in this example).
  
2. **Get the Code by Authorizing Your Application:**

   - Visit the [Twitch OAuth Authorization Documentation](https://dev.twitch.tv/docs/authentication/getting-tokens-oauth#oauth-authorization-code-flow) for detailed instructions on obtaining the authorization code by authorizing your application.


3. **Replace Twitch Data with Actual User Data:**

   - Open `main.py`.
   - Replace `CLIENT_ID`, `CLIENT_SECRET`, 'CODE'(You got in step2), 'SCOPES'(Scope for your access token) and `REDIRECT_URI` variables with your Twitch application credentials and redirect URI.
   - Update the `nickname` variable to your Twitch username or bot name.
   - Update the `channel` variable to the Twitch channel you want to monitor for chat messages.
     ```python
     nickname = 'your_twitch_nickname_or_botname'
     channel = '#your_twitch_channel'
     ```
. 
4. **MongoDB Setup:**

   - Install MongoDB on your local machine or set up a MongoDB server.
   - Update the MongoDB connection string (`MONGO_DETAILS`) in `main.py` to point to your MongoDB instance. Example:
     ```python
     MONGO_DETAILS = "mongodb://localhost:27017"
     ```


## Usage

1. Run the FASTAPI application:
   ```bash
   python main.py
   ```

   
## Additional Notes

- The application connects to Twitch IRC (`irc.chat.twitch.tv`) using an OAuth token for authorization (`oauth:{TWITCH_OAUTH_TOKEN}`).
- Chat messages are stored in MongoDB in the `twitch.chats` collection.
- Customize the application further based on your requirements, such as implementing additional Twitch API functionalities or enhancing error handling.

