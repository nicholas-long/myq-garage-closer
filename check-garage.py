import asyncio
from aiohttp import ClientSession
import pymyq
import json
import datetime
import dateutil.parser
import configparser
import os
import dotenv

dotenv.load_dotenv('.env')
email = os.getenv('MYQ_EMAIL')
password = os.getenv('MYQ_PASSWORD')
duration = os.getenv('MYQ_MAX_MINUTES_OPEN')

environ_params = [x for x in [email, password, duration] if x is not None]
assert(len(environ_params) == 3)

async def handle_garage(device):
    max_minutes = int(duration)
    if (device.state == 'open' or device.state == 'stopped'):
      updateTime = device.device_json['state']['last_update']
      time = dateutil.parser.parse(updateTime)
      now = datetime.datetime.now(datetime.timezone.utc)
      difference = now - time
      print(f"Garage is {device.state} for {difference}")
      maxTime = datetime.timedelta(minutes=max_minutes)
      if (difference > maxTime):
        await device.close()
    else:
      print(f"Garage is {device.state}")


async def main() -> None:
    """Create the aiohttp session and run."""
    async with ClientSession() as websession:
      myq = await pymyq.login(email, password, websession)
      # Return *all* devices:
      devices = myq.devices
      for key in devices:
          device = devices[key]
          if (device.device_family == 'garagedoor' and device.close_allowed):
              await handle_garage(device)

asyncio.run(main())
