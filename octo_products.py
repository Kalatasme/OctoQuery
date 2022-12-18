import requests
import json

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

# Get a list of products
response_products = requests.get(f"{base_url}/v1/products/", headers=header)

# Get current Electricity Consumption
# response_elec_consumption = requests.get(f"{base_url}/v1/electricity-meter-points/{elec_mpan}/meters/{elec_serial}/consumption", headers=header)

# get response body as json. If the body text is not a json string, raise a ValueError
rp_json = response_products.json()

# get response status code
rp_status = response_products.status_code

# check the response status, if the status is not sucessful, raise requests.HTTPError
response_products.raise_for_status()

# Strip the header - Print only the contents of the Results dictionary.
rp_json_string = json.dumps(rp_json["results"])

# Let's just double-check this is actually JSON before it hits Splunk.
# I have been burned before.
json.loads(rp_json_string)

# Let's output our JSON payload.
# For now we'll print and output to a file via the CLI for manual ingestion into Splunk.
print(rp_json_string)