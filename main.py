import json, requests, sys

# ----------------------------------------------------------------------------------------------------
# "Universal" variables

_json_configuration_file = "conf.json"
_unspecified_json_warning = "No JSON config was specified. Defaulting to"
_request_decode_format = "utf-8"
_request_not_found_continue_code = 429

config = False

# ----------------------------------------------------------------------------------------------------
# Functions

def get_json (location):
	print(location)
	try:
		return json.load(open(location))
	except FileNotFoundError:
		request = requests.get(location)
		while request.status_code == _request_not_found_continue_code:
			request = requests.get(location)
		return json.loads(request.content.decode(_request_decode_format))

def get_card_image_from_api (card_name, api_config = False):
	if api_config == False:
		api_config = config["api"]
	json_array = get_json(api_config["prefix"] + card_name.replace(api_config["infix_replace"], api_config["infix"]) + api_config["postfix"])["data"]
	for card_object in json_array:
		if card_object["image_status"] == api_config["image_status_text"]:
			return card_object["image_uris"]["large"]

# ----------------------------------------------------------------------------------------------------

try:
	_json_configuration_file = sys.argv[1]
except:
	print(_unspecified_json_warning, _json_configuration_file)
config = get_json(_json_configuration_file)

get_card_image_from_api ("Sol Ring")
