import asyncio
from dotenv import load_dotenv
import os
from  beacon.util.logger import configure_warnings
from beacon.ai_tools.google_gen_ai import set_api_keys
from beacon.driver.smart_alerts import smart_alerts

async def main(query, mock_disaster=False):
    await configure_warnings()
    await smart_alerts(query,mock_disaster=mock_disaster)

if __name__ == "__main__":
    load_dotenv()
    set_api_keys(os.getenv("GOOGLE_API"))
    query = "What is the weather and the time in Belize?"
    debug = True
    asyncio.run(main(query, mock_disaster=debug))

