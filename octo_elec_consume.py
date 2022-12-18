import requests
import json
from datetime import datetime, timedelta

#
# DATES & TIMES
# Consumption API accepts earliest/latest snapped to half hour increments (HH:00 - HH:30 & HH:30 - HH:00).
# This is where we calculate those values to be passed to the API
#

# Get the current system time.
timenow = datetime.now()
#timenow = "2022-11-12 14:29:15.535784"
# Print timenow
#print(timenow)

# Testing - Only needed if timenow is manually set.  Turns from string to datetime format.
#datetime_time = datetime.strptime(timenow, "%Y-%m-%d %H:%M:%S.%f")
#print(datetime_time)

# Create our rounded time, snaps down to the nearest 30 mins.  
# Mins 01-29 = 00
# Mins 31-59 = 30
rounded = timenow - (timenow - datetime.min) % timedelta(minutes=30)
# Print rounded time.
#print(rounded)

# Octopus API wants period_from & period_to values in ISO 8601 Format.
iso_timenow = rounded.isoformat()

# I get errors here about string & datetime values not gelling, so I'm going to force it into a format that can be manipulated.
date_format = '%Y-%m-%dT%H:%M:%S'
provided_time = datetime.strptime(iso_timenow, date_format)
#print(provided_time)

# period_to value.  Take our rounded time, subtract a minute for our 29 or 59 value.
#latest = "{}Z".format(provided_time - timedelta(minutes=1)).replace(" ", "T")
#print(latest)

# period_from value.  Take our rounded time, subtract 30 mins for our 00 or 30 value.
#earliest = "{}Z".format(provided_time - timedelta(minutes=30)).replace(" ", "T")
#print(earliest)

# Testing Specific Periods
earliest = "2022-11-15T00:00:00Z"
latest = "2022-11-15T23:59:00Z"



time_period = f"?period_from={earliest}&period_to={latest}"
#print(time_period)

# Testing we've got the right formats
#print(time_now.isoformat())
#print(time_earliest.isoformat())
#print(time_latest.isoformat())

# Variables

# https://octopus.energy/dashboard/developer/
base_url = "https://api.octopus.energy"
api_key = XXXXX

# https://www.base64encode.org/
enc_api_key = XXXXX

# https://octopus.energy/dashboard/developer/
elec_mpan = XXXXX
elec_serial = XXXXX

# https://octopus.energy/dashboard/developer/
gas_mprn = XXXXX
gas_serial = XXXXX

# Build Header
# Basic Auth as per https://developer.octopus.energy/docs/api/
header = {"Authorization": f"Basic {enc_api_key}"}

url = f"{base_url}/v1/electricity-meter-points/{elec_mpan}/meters/{elec_serial}/consumption/{time_period}"

# Get a list of products
response_elec_consume = requests.get(url, headers=header)

# Get current Electricity Consumption
# response_elec_consumption = requests.get(f"{base_url}/v1/electricity-meter-points/{elec_mpan}/meters/{elec_serial}/consumption", headers=header)

# get response body as json. If the body text is not a json string, raise a ValueError
rp_json = response_elec_consume.json()

# get response status code
rp_status = response_elec_consume.status_code

# check the response status, if the status is not sucessful, raise requests.HTTPError
response_elec_consume.raise_for_status()

# Strip the header - Print only the contents of the Results dictionary.
rec_json_string = json.dumps(rp_json["results"])

# Let's just double-check this is actually JSON before it hits Splunk.
# I have been burned before.
json.loads(rec_json_string)

# Let's output our JSON payload.
# For now we'll print and output to a file via the CLI for manual ingestion into Splunk.
print(rec_json_string)
#print(rp_status)
#print(url)