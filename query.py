import requests
import json

# Variables

# https://octopus.energy/dashboard/developer/
base_url = "https://api.octopus.energy"
api_key = "sk_live_sjFqMHi3PHCmQfGJyRKjEwPY"

# https://www.base64encode.org/
enc_api_key = "c2tfbGl2ZV9zakZxTUhpM1BIQ21RZkdKeVJLakV3UFk="

# https://octopus.energy/dashboard/developer/
elec_mpan = "3200000070992"
elec_serial = "21E5433813"

# https://octopus.energy/dashboard/developer/
gas_mprn = "7621831004"
gas_serial = "E6E06453952221"


# Build Header
# Basic Auth as per https://developer.octopus.energy/docs/api/
header = {"Authorization": f"Basic {enc_api_key}"}

# Get a list of products
response_products = requests.get(f"{base_url}/v1/products/", headers=header)

# Get current Electricity Consumption
response_elec_consumption = requests.get(f"{base_url}/v1/electricity-meter-points/{elec_mpan}/meters/{elec_serial}/consumption", headers=header)


# get response body as json. If the body text is not a json string, raise a ValueError
rp_json = response_products.json()

# get response status code
rp_status = response_products.status_code
# check the response status, if the status is not sucessful, raise requests.HTTPError
response_products.raise_for_status()

rec_json = response_elec_consumption.json()
rec_status = response_elec_consumption.status_code
response_elec_consumption.raise_for_status()


#print(rp_json)

rp_json_string = json.dumps(rp_json["results"])
json.loads(rp_json_string)

# rp_json_string_fixed = rp_json_string.replace("false", '"false"')
print(rp_json_string)

#print(rp_status)

#print(rec_json)
#print(rec_status)




#print(response.status_code)
#print(response.json())