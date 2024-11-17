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
                    'content': "An approaching Category 4 hurricane is expected to make landfall in Belize within the next 24 hours. Authorities are urging residents to evacuate from coastal areas. Wind speeds are anticipated to reach 140 mph with potential for significant flooding and damage in low-lying areas.",
                    'score': 0.995236,
                    'raw_content': None
                },
                {
                    'title': 'Emergency Weather Warning - Belize',
                    'url': 'https://www.accuweather.com/',
                    'content': "A tropical storm in the region is intensifying. Forecasts predict heavy rainfall, severe winds, and flooding across Belize. The National Meteorological Service has issued an emergency evacuation order for affected areas.",
                    'score': 0.98589,
                    'raw_content': None
                }
            ],
            'response_time': 4.16
        },
        'qna_answer': 'A Category 4 hurricane is approaching Belize with wind speeds of 140 mph and severe rainfall expected. Evacuation orders have been issued for coastal and flood-prone areas as local authorities prepare for potentially catastrophic impacts.'
    }
    return mock_response
