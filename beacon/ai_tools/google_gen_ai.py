import os
import google.generativeai as genai
import backoff
from google.api_core import exceptions
from beacon.util.logger import logger

# Initialize API keys
api_keys = []
current_key_index = 0


def set_api_keys(keys):
    global api_keys
    api_keys = keys.split(",") if keys else []


def configure_api_key():
    global current_key_index
    api_key = api_keys[current_key_index]
    genai.configure(api_key=api_key)
    # logger.info(f"Configured API key: {api_key}") #strictly debugging purpose only, api key should not be exposed as it is sensitive info


@backoff.on_exception(
    backoff.constant, exceptions.ResourceExhausted, max_tries=max(len(api_keys), 3)
)
async def generate_content_gemini(prompt, text):
    configure_api_key()
    global current_key_index
    try:
        response = genai.GenerativeModel("gemini-pro").generate_content(
            f"{prompt} : {text}"
        )
        return response.text.strip()
    except exceptions.ResourceExhausted:
        current_key_index = (current_key_index + 1) % max(len(api_keys), 3)
        configure_api_key()
        raise  # Re-raise the exception to trigger backoff
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        raise


async def screen_tweets_gemini(tweet):
    prompt = (
        "Classify the following tweet into two categories: disaster-related or noise. Disaster-related tweets "
        "contain information about natural disasters such as hurricanes, earthquakes, floods, tornadoes, "
        "or landslides, along with details about the location, damage, severity, and urgency. Noise tweets are "
        "not related to disasters and cover various topics such as vacations, events, business meetings, or"
        " personal activities. After classification if the tweet is of disaster nature share response with "
        "relevant disaster details like location, impact, and whatever other crucial information is in the tweet,"
        "this will be directly communicated with impacted users. finally format your response as "
        "Disaster: <Your message>;  for disaster related messages and"
        "just 'Noise:' for noise messages"
    )

    try:
        tweet_category = await generate_content_gemini(prompt, tweet)
        tweet = tweet.replace("\n", " ").strip()
        logger.info(
            f"\n Tweet text = {tweet},"
            f" \n Google LLM generated response = "
            + tweet_category.replace("\n", " ").strip()
            + "\n"
        )
        return tweet_category

    except Exception as e:
        logger.exception(f"Error occurred while screening tweets: {e}")
        return None
