from openai import AsyncOpenAI

from beacon.util.env_var_utils import extract_from_env
from beacon.util.logger import logger

"""
need to set OPENAI_API_KEY as env for this to work 
"""


async def generate_content_open_ai(prompt, text):
    try:
        client = AsyncOpenAI(api_key=extract_from_env("OPEN_AI_KEY"))
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt + text},
                    ],
                },
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.exception(f"Error occurred when using OpenAI model: {e}")
        raise


async def screen_tweets_openai(tweet):
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
        tweet_category = await generate_content_open_ai(prompt, tweet)
        tweet = tweet.replace("\n", " ").strip()
        logger.info(
            f"\n Tweet text = {tweet},"
            f" \n Open AI LLM generated response = "
            + tweet_category.replace("\n", " ").strip()
            + "\n"
        )
        return tweet_category

    except Exception as e:
        logger.exception(f"Error occurred while screening tweets: {e}")
        return None
