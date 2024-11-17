import datetime

from beacon.ai_tools.local_ai import query_llm


def get_mock_tavily_response():
    mock_response = {
        'search_response': {
            'query': 'What is the weather and the time in Belize',
            'follow_up_questions': None,
            'answer': None,
            'images': [],
            'results': [
                {
                    'title': 'Hurricane Alert in Belize',
                    'url': 'https://www.weatherapi.com/',
                    'content': generate_disaster_alert("An approaching Category 4 hurricane is expected to make landfall in Belize within the next 24 hours. Authorities are urging residents to evacuate from coastal areas. Wind speeds are anticipated to reach 140 mph with potential for significant flooding and damage in low-lying areas."),
                    'score': 0.995236,
                    'raw_content': None
                },
                {
                    'title': 'Emergency Weather Warning - Belize',
                    'url': 'https://www.accuweather.com/',
                    'content': generate_disaster_alert("A tropical storm in the region is intensifying. Forecasts predict heavy rainfall, severe winds, and flooding across Belize. The National Meteorological Service has issued an emergency evacuation order for affected areas."),
                    'score': 0.98589,
                    'raw_content': None
                }
            ],
            'response_time': 4.16
        },
        'qna_answer': 'A Category 4 hurricane is approaching Belize with wind speeds of 140 mph and severe rainfall expected. Evacuation orders have been issued for coastal and flood-prone areas as local authorities prepare for potentially catastrophic impacts.'
    }
    return mock_response


def get_mock_serpapi_response():
    now = datetime.datetime.now(datetime.timezone.utc)
    date_format = '%m/%d/%Y, %I:%M %p, %z'

    dates = [
        (now - datetime.timedelta(hours=2)).strftime(date_format),
        (now - datetime.timedelta(hours=5)).strftime(date_format),
        (now - datetime.timedelta(hours=10)).strftime(date_format)
    ]

    mock_response = {
        'search_results': [
            {
                'title': 'Belize Issues Hurricane Warning as Storm Approaches',
                'link': 'https://www.weathernews.com/belize-hurricane-warning',
                'snippet': generate_disaster_alert('Belize government has issued a hurricane warning as a Category 4 storm approaches the coast.'),
            },
            {
                'title': 'Residents Evacuate Ahead of Category 4 Hurricane in Belize',
                'link': 'https://www.bbc.com/news/world-latin-america-12345678',
                'snippet': generate_disaster_alert('Thousands are evacuating as a powerful hurricane threatens Belize with heavy winds and rain.'),
            }
        ],
        'news_results': [
            {
                'title': 'Tropical Storm Sara Drenches Honduras',
                'link': f'https://www.nytimes.com/live/{now.strftime("%Y/%m/%d")}/weather/tropical-storm-sara-hurricane',
                'published': dates[0],
                'snippet': generate_disaster_alert('Heavy rainfall from Tropical Storm Sara has caused severe flooding in parts of Honduras.')
            },
            {
                'title': 'Tropical Storm Warning Extended to Entire Belize Coast',
                'link': 'https://lovefm.com/tropical-storm-warning-extended-to-entire-belize-coast/',
                'published': dates[1],
                'snippet': generate_disaster_alert('The National Meteorological Service of Belize has extended the tropical storm warning.')
            },
            {
                'title': 'Tropical Storm Sara Approaches Belize: Heavy Rainfall and Strong Winds Expected',
                'link': f'https://www.breakingbelizenews.com/{now.strftime("%Y/%m/%d")}/tropical-storm-sara-approaches-belize-heavy-rainfall-and-strong-winds-expected/',
                'published': dates[2],
                'snippet': generate_disaster_alert('Belize prepares for Tropical Storm Sara, anticipating heavy rainfall and strong winds.')
            }
        ]
    }
    return mock_response


def generate_alert_prompt(message):
    prompt = f"""
    You are a disaster alert assistant. Based on the following information, generate an alert for affected users.

    Information:
    {message}

    Instructions:
    - Summarize the key details.
    - Include the location, severity, and any evacuation orders.
    - Keep the alert concise and clear.
    - Do not include any additional information not present in the base message.
    - Only one message
    """

    return prompt

def generate_disaster_alert(base_message):
    prompt = generate_alert_prompt(base_message)
    alert_message = query_llm(prompt)
    return alert_message
