import requests

def summarize_disaster_report(message):
    user_query = (f'''You are a summarizing agent specializing in disaster-related information. You will receive a 
                report containing current weather conditions and other details. 

                Your task is to:
                Extract only the disaster-related information from the report.
                Ignore any content that is not directly related to disasters or severe weather conditions affecting safety.

                Focus exclusively on the following categories:
                Severe weather conditions posing immediate threats (e.g., hurricanes, floods, tornadoes).
                Official warnings, alerts, or emergency declarations issued by authorities.
                Impacts on infrastructure such as road closures, power outages, or communication disruptions.
                Evacuation orders, shelter locations, or safety instructions for the public.

                Do not include:
                General weather information not related to disasters.
                Seasonal weather patterns or tourist information.
                Activities unrelated to disaster events (e.g., birding, sunbathing).

                For each relevant category, provide a concise summary in one sentence, including all specific and key 
                details. It is crucial to stick to one sentence per category and exclude any irrelevant information. 
                Do not include any phrases that indicate you are summarizing or that you are an AI agent. Present the 
                information directly and without any introductory or concluding remarks.Below is the text to 
                analyze:\n\n {message}''')
    return query_llm(user_query)

def query_llm(prompt, model="llama-3.2-3b-instruct", temperature=0, max_tokens=20000):
    """
    Queries the locally hosted LLM and extracts the assistant's response.

    Parameters:
        prompt (str): The user's input query.
        model (str): The model to use for generating the response.
        temperature (float): Sampling temperature (default: 0.0).
        max_tokens (int): Maximum number of tokens to generate (default: 20000).

    Returns:
        str: The assistant's response content.
    """


    # Define the local server details
    base_url = "http://127.0.0.1:1234"
    chat_endpoint = f"{base_url}/v1/chat/completions"

    # Define headers and payload
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    # Make the POST request
    response = requests.post(chat_endpoint, headers=headers, json=data)

    # Check response and extract content
    if response.status_code == 200:
        response_json = response.json()
        assistant_message = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")
        return assistant_message.strip()
    else:
        return f"Error: {response.status_code}, {response.text}"