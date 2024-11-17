import asyncio
from dotenv import load_dotenv
import os

from beacon.ai_tools.google_gen_ai import set_api_keys
from beacon.driver.smart_alerts import smart_alerts

async def main(query):
    await configure_warnings()
    await smart_alerts(query)

async def configure_warnings():
    import warnings
    warnings.filterwarnings("ignore", message=r"\[W008\]", category=UserWarning)

if __name__ == "__main__":
    load_dotenv()
    set_api_keys(os.getenv("GOOGLE_API"))
    query = "What is the weather and the time in Belize?"
    asyncio.run(main(query))

