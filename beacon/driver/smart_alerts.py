import asyncio
import logging
import uuid
from sys import audit

from charset_normalizer.cd import alpha_unicode_split

from beacon.ai_tools.local_ai import summarize_disaster_report
from beacon.compute.all_sources import (
    get_tavily_data,
    get_serpapi_data,
    prepare_data_for_llm,
)
from beacon.ai_tools.google_gen_ai import screen_tweets_gemini
from beacon.compute.persist import persist_disaster_event
from beacon.util.logger import logger
from beacon.util.mock_utils import get_mock_tavily_response

async def smart_alerts(query: str, mock_disaster: bool=False):

    # Fetch data from Tavily
    tavily_data = get_mock_tavily_response() if mock_disaster else get_tavily_data(query)
    logger.info("Fetched data from Tavily.")

    # Fetch data from SerpAPI (Google)
    serpapi_data = get_serpapi_data(query, num_results=50)
    logger.info("Fetched data from SerpAPI.")

    # Prepare data for LLM
    combined_data = {
        'tavily': tavily_data,
        'serpapi': serpapi_data,
    }

    # use nlp to pre-classify disaster events
    llm_input = prepare_data_for_llm(combined_data, use_nlp=True)
    print('Audit: LLM input ', llm_input)
    logger.info("Prepared data for LLM.")

    # Screen the combined data using the LLM
    screen_result = await screen_tweets_gemini(llm_input)
    print('Audit: Screen result ', screen_result)

    if screen_result and screen_result.lstrip("**").startswith("Disaster:"):
        logger.info("Disaster Event found, persisting")

        # Generate a unique ID for the event since it's not a tweet
        event_id = str(uuid.uuid4())

        logger.info(event_id, llm_input, screen_result, mock = False)
        # persist the disaster event
        persist_disaster_event(
           event_id, llm_input, screen_result, mock=False
        )

    else:
        logger.info("No disaster-related content found.")



