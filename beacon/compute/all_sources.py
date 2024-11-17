import os
import json
import requests
import logging
import requests
from tavily import TavilyClient
from datetime import datetime, timezone, timedelta
from datetime import datetime, timedelta, timezone
import requests
from dateutil import parser
import logging

# If you plan to use NLP features, uncomment the following lines:
import spacy

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# If you plan to use NLP features, load the spaCy model
# python3 -m spacy download en_core_web_sm
# this model is giving us a warning that
# UserWarning: [W007] The model you're using has no word vectors loaded, so the result of the Token.similarity method will be based on the tagger, parser and NER, which may not give useful similarity judgements. This may happen if you're using one of the small models, e.g. `en_core_web_sm`, which don't ship with word vectors and only use context-sensitive tensors. You can always add your own word vectors, or use one of the larger models instead if available.
#   token.similarity(nlp(term)[0]) > 0.75 for term in DISASTER_KEYWORDS

# python3 -m spacy download en_core_web_md


nlp = spacy.load("en_core_web_md")

# Disaster-related keywords (used only if NLP is enabled)
DISASTER_KEYWORDS = [
    "hurricane",
    "storm",
    "flood",
    "earthquake",
    "tornado",
    "wildfire",
    "tsunami",
    "landslide",
    "volcano",
    "eruption",
    "disaster",
    "emergency",
    "alert",
    "warning",
    "evacuation",
    "crisis",
    "cyclone",
    "typhoon",
]

# Disaster-related keywords
DISASTER_CONTEXT = {
    "hurricane": ["category", "wind", "storm", "damage", "mph", "tropical"],
    "flood": ["water", "level", "rising", "submerged", "evacuation", "rain"],
    "earthquake": ["magnitude", "richter", "seismic", "tremor", "aftershock"],
    "tornado": ["funnel", "wind", "damage", "warning", "touchdown", "mph"],
    "wildfire": ["acres", "burning", "spread", "containment", "evacuation"],
    "tsunami": ["wave", "coastal", "warning", "evacuation", "surge"],
    "landslide": ["debris", "mud", "slope", "warning", "damage"],
    "volcano": ["eruption", "ash", "lava", "magma", "activity"],
    "disaster": ["emergency", "damage", "impact", "affected", "relief"],
}

ALL_DISASTER_KEYWORDS = [
    keyword for keywords in DISASTER_CONTEXT.values() for keyword in keywords
]


def get_tavily_data(query):
    """
    Fetches data from Tavily API.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        logger.error("TAVILY_API_KEY environment variable not set.")
        raise ValueError("TAVILY_API_KEY environment variable not set.")

    tavily_client = TavilyClient(api_key=api_key)
    try:
        search_response = tavily_client.search(query)
        qna_answer = tavily_client.qna_search(query=query)
    except Exception as e:
        logger.error(f"Error fetching data from Tavily: {e}")
        return {}

    return {"search_response": search_response, "qna_answer": qna_answer}


def google_search(query, serpapi_key, num_results=5):
    """
    Performs a Google Search using SerpAPI.
    """
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google",
        "q": query,
        "api_key": serpapi_key,
        "num": num_results,
    }
    response = requests.get(url, params=params)
    print("Audit: Querying google search.")
    if response.status_code == 200:
        results = response.json().get("organic_results", [])
        return [
            {
                "title": result.get("title", ""),
                "link": result.get("link", ""),
                "snippet": result.get("snippet", ""),
            }
            for result in results
        ]
    else:
        logger.error(
            f"Error with Google Search: {response.status_code} {response.text}"
        )
        return []



def google_news(query, serpapi_key, num_results=5, date_cutoff=None):
    """
    Fetches Google News results using SerpAPI and filters them by a date cutoff.

    Args:
        query (str): The search query.
        serpapi_key (str): SerpAPI key.
        num_results (int): Number of results to return.
        date_cutoff (datetime, optional): The cutoff date to filter results. Only articles published
                                          on or after this date will be included. Defaults to 5 days ago.

    Returns:
        list: A list of dictionaries containing filtered news results.
    """
    # Set default cutoff date to 5 days ago if no date_cutoff is provided
    if date_cutoff is None:
        date_cutoff = datetime.now(timezone.utc) - timedelta(days=5)

    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_news",
        "q": query,
        "api_key": serpapi_key,
        "num": num_results,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get("news_results", [])

        # List to store filtered results
        filtered_results = []

        for result in results:
            published_str = result.get("date", "")

            # Clean up the date string
            published_str = published_str.strip().rstrip(',')

            # Remove '+0000 UTC' or similar timezone info if present
            if 'UTC' in published_str:
                published_str = published_str.split('UTC')[0].strip()

            try:
                # Use dateutil parser to handle various date formats flexibly
                published_date = parser.parse(published_str)

                # Only include articles published on or after the cutoff date
                if published_date >= date_cutoff:
                    filtered_results.append({
                        "title": result.get("title", ""),
                        "link": result.get("link", ""),
                        "published": published_str,
                        "snippet": result.get("snippet", ""),
                    })
            except (ValueError, TypeError, parser.ParserError) as e:
                # Log or skip if date parsing fails
                logger.warning(f"Skipping entry with unrecognized date format: {published_str}")

        return filtered_results
    else:
        logger.error(f"Error with Google News: {response.status_code} {response.text}")
        return []



def get_serpapi_data(query, num_results=5):
    """
    Fetches data from SerpAPI for both Google Search and News.
    """
    serpapi_key = os.getenv("SERPAPI_KEY")
    if not serpapi_key:
        logger.error("SERPAPI_KEY environment variable not set.")
        raise ValueError("SERPAPI_KEY environment variable not set.")

    search_results = google_search(query, serpapi_key, num_results)
    news_results = google_news(query, serpapi_key, num_results)
    return {"search_results": search_results, "news_results": news_results}


def extract_disaster_mentions(text):
    """
    Detects disaster-related mentions using spaCy's NLP processing.

    Args:
        text (str): The text to search within.

    Returns:
        list: A list of sentences containing disaster-related mentions.
    """
    disaster_mentions = []
    doc = nlp(text)  # Process the text with spaCy NLP

    # Iterate through each sentence in the processed document
    for sent in doc.sents:
        sentence_lower = (
            sent.text.lower()
        )  # Convert sentence to lowercase for case-insensitive matching
        found_disaster = False  # Flag to track if disaster-related content is found

        # Check for each disaster keyword and its context
        for keyword, context_words in DISASTER_CONTEXT.items():
            # Check if the disaster keyword is in the sentence
            if keyword in sentence_lower:
                # Verify context by checking if any context word is present in the sentence
                has_context = any(
                    context in sentence_lower for context in context_words
                )

                # Filter out non-disaster references by checking for:
                # 1. Historical or entertainment context
                # 2. Metaphorical usage
                is_historical = any(
                    term in sentence_lower
                    for term in ["movie", "game", "fiction", "novel"]
                )
                is_metaphorical = any(
                    term in sentence_lower
                    for term in ["economic", "political", "financial"]
                )

                # Only include sentence if:
                # 1. It has relevant context words
                # 2. It's not historical or entertainment
                # 3. It's not metaphorical
                if has_context and not (is_historical or is_metaphorical):
                    found_disaster = True
                    break  # Stop further checks if a disaster mention is confirmed

        # Check token similarity with disaster keywords as a secondary approach
        if not found_disaster:
            for token in sent:
                # If any token has a high similarity with a disaster term, consider it a mention
                if any(
                    token.similarity(nlp(term)[0]) > 0.75 for term in DISASTER_KEYWORDS
                ):
                    found_disaster = True
                    break  # Stop further checks if a disaster mention is confirmed

        # If a disaster-related mention is confirmed, add the sentence to the list
        if found_disaster:
            disaster_mentions.append(sent.text.strip())

    return disaster_mentions


def analyze_data_for_disasters(data):
    """
    Analyzes the collected data to find mentions of disasters.
    Used only if NLP is enabled.
    """
    disaster_findings = {"tavily": [], "serpapi_search": [], "serpapi_news": []}

    # Analyze Tavily QnA Answer
    tavily_answer = data["tavily"].get("qna_answer", "")
    if tavily_answer:
        mentions = extract_disaster_mentions(tavily_answer)
        disaster_findings["tavily"].extend(mentions)

    # Analyze Tavily Search Results
    for result in data["tavily"].get("search_response", {}).get("results", []):
        content = result.get("content", "")
        if content:
            mentions = extract_disaster_mentions(content)
            disaster_findings["tavily"].extend(mentions)

    # Analyze SerpAPI Search Results
    for result in data["serpapi"].get("search_results", []):
        snippet = result.get("snippet", "")
        if snippet:
            mentions = extract_disaster_mentions(snippet)
            disaster_findings["serpapi_search"].extend(mentions)

    # Analyze SerpAPI News Results
    for result in data["serpapi"].get("news_results", []):
        title = result.get("title", "")
        snippet = result.get("snippet", "")
        combined_text = f"{title}. {snippet}"
        mentions = extract_disaster_mentions(combined_text)
        disaster_findings["serpapi_news"].extend(mentions)

    return disaster_findings


def prepare_data_for_llm(data, use_nlp=False):
    """
    Prepares the combined data for ingestion into an LLM.
    If use_nlp is True, includes disaster analysis.
    """
    if use_nlp:
        # Perform disaster analysis
        disaster_findings = analyze_data_for_disasters(data)
        llm_input = "Disaster Analysis Report:\n\n"

        if disaster_findings["tavily"]:
            llm_input += "Tavily Findings:\n"
            for mention in set(disaster_findings["tavily"]):
                llm_input += f"- {mention}\n"
            llm_input += "\n"

        if disaster_findings["serpapi_search"]:
            llm_input += "Google Search Findings:\n"
            for mention in set(disaster_findings["serpapi_search"]):
                llm_input += f"- {mention}\n"
            llm_input += "\n"

        if disaster_findings["serpapi_news"]:
            llm_input += "Google News Findings:\n"
            for mention in set(disaster_findings["serpapi_news"]):
                llm_input += f"- {mention}\n"
            llm_input += "\n"

        if not any(disaster_findings.values()):
            llm_input += "No disaster-related mentions found in the collected data."
    else:
        # Output raw data without analysis
        llm_input = {
            "tavily": {
                "search_response": data["tavily"].get("search_response", {}),
                "qna_answer": data["tavily"].get("qna_answer", ""),
            },
            "serpapi": {
                "search_results": data["serpapi"].get("search_results", []),
                "news_results": data["serpapi"].get("news_results", []),
            },
        }
        llm_input = json.dumps(llm_input, indent=2)

    return llm_input
