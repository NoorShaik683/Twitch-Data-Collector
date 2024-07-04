import os
import aiohttp
import asyncio
import logging
from fastapi import FastAPI, HTTPException, BackgroundTasks
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# MongoDB setup
MONGO_DETAILS = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.twitch
chat_collection = database.get_collection("chats")

# Twitch API credentials
TWITCH_CLIENT_ID = "<TWITCH_CLIENT_ID>"
TWITCH_SECRET = "<TWITCH_SECRET>"
TWITCH_OAUTH_TOKEN = "<TWITCH_OAUTH_TOKEN>"

logging.basicConfig(level=logging.INFO)

async def get_twitch_oauth_token():
    global TWITCH_OAUTH_TOKEN
    async with aiohttp.ClientSession() as session:
        async with session.post('https://id.twitch.tv/oauth2/token', params={
            'client_id': TWITCH_CLIENT_ID,
            'client_secret': TWITCH_SECRET,
            'grant_type': 'authorization_code',
            'code':'<AUTHORIZATION_CODE>',
            'redirect_uri':'<REDIRECT_URI>'
            
        }) as response:
            if response.status == 200:
                data = await response.json()
                print('data =>',data)
                TWITCH_OAUTH_TOKEN = data['access_token']
                logging.info(f"Obtained Twitch OAuth token: {TWITCH_OAUTH_TOKEN}")
            else:
                error_detail = await response.text()
                logging.error(f"Failed to get Twitch OAuth token: {error_detail}")
                raise HTTPException(status_code=response.status, detail=error_detail)

async def collect_chat_data():
   
    server = 'irc.chat.twitch.tv'
    port = 6667
    nickname = '<NICKNAME>'
    token = f'oauth:{TWITCH_OAUTH_TOKEN}'
    channel = '#CHANNEL'

    logging.info(f"Connecting to {server}:{port} as {nickname} and token {token}")
    
    try:
        reader, writer = await asyncio.open_connection(server, port)

        writer.write(f"PASS {token}\r\n".encode('utf-8'))
        writer.write(f"NICK {nickname}\r\n".encode('utf-8'))
        writer.write(f"JOIN {channel}\r\n".encode('utf-8'))
        await writer.drain()

        logging.info(f"Joined channel {channel}")

        while True:
            data = await reader.read(2048)
            message = data.decode('utf-8')
            logging.info(f"Received message: {message} - {data}")
           
            if 'PRIVMSG' in message:
                chat_message = {
                    "channel": channel,
                    "message": message.split('PRIVMSG')[1].split(':')[1].strip()
                }
                await chat_collection.insert_one(chat_message)
                logging.info(f"Inserted chat message: {chat_message}")

                # Example threshold for alerts
                if await chat_collection.count_documents({"channel": channel}) > 10:
                    logging.warning(f"Alert: High chat volume in channel {channel}")

            # Respond to PING messages to keep the connection alive
            if message.startswith('PING'):
                writer.write("PONG :tmi.twitch.tv\r\n".encode('utf-8'))
                await writer.drain()
                logging.info("Responded to PING with PONG")

    except Exception as e:
        logging.error(f"Error in collect_chat_data: {e}")
@app.on_event("startup")
async def startup_event():
    await get_twitch_oauth_token()
    asyncio.create_task(collect_chat_data())

@app.get("/")
async def read_root():
    return {"message": "Twitch Data Collector"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)

