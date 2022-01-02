import json, requests, sys

_json_configuration_file = "conf.json"
_unspecified_json_warning = "No JSON config was specified. Defaulting to"
_request_decode_format = "utf-8"
_request_not_found_continue_code = 429

config = False

def get_json (location):
	try:
		return json.load(open(location))
	except FileNotFoundError:
		request = requests.get(location)
		while request.status_code == _request_not_found_continue_code:
			request = requests.get(location)
		return json.loads(request.content.decode(_request_decode_format))

try:
	_json_configuration_file = sys.argv[1]
except:
	print(_unspecified_json_warning, _json_configuration_file)

config = get_json("https://api.scryfall.com/cards/named?exact=boompile")
print(config)
