import asyncio
from aiohttp import ClientSession
import pymyq
import json
import datetime
import dateutil.parser
import configparser

config = configparser.ConfigParser()
config.read('settings.conf')

async def handle_garage(device):
    max_minutes = int(config['Duration']['max_minutes_open'])
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
      email = config['Login']['email']
      password = config['Login']['password']
      myq = await pymyq.login(email, password, websession)
      # Return *all* devices:
      devices = myq.devices
      for key in devices:
          device = devices[key]
          if (device.device_family == 'garagedoor' and device.close_allowed):
              await handle_garage(device)



asyncio.get_event_loop().run_until_complete(main())
