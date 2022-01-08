from PIL import Image
import json, math, os, requests, sys, time, urllib.request

# ----------------------------------------------------------------------------------------------------
# "Universal" variables

_deck_split_character = "\n"
_json_configuration_file = "conf.json"
_unspecified_json_warning = "No JSON config was specified. Defaulting to"
_request_decode_format = "utf-8"
_request_delay = 100 / 1000
_request_not_found_continue_code = 429

config = False
imagedb = []

dimensions = []

# ----------------------------------------------------------------------------------------------------
# Functions

def get_json (location):
	try:
		return json.load(open(location))
	except FileNotFoundError:
		request = requests.get(location)
		while request.status_code == _request_not_found_continue_code:
			request = requests.get(location)
		return json.loads(request.content.decode(_request_decode_format))

def get_image (location):
	try:
		return Image.open(location)
	except FileNotFoundError:
		urllib.request.urlretrieve(location, config["api"]["tmp"])
		return Image.open(config["api"]["tmp"])

def atoi (x):
	try:
		return int(x)
	except ValueError:
		return -1

def get_card_image_from_api (card_name, api_config = False):
	if api_config == False:
		api_config = config["api"]
	time.sleep(_request_delay)
	json_array = get_json(api_config["prefix"] + card_name.replace(api_config["infix_replace"], api_config["infix"]) + api_config["postfix"])["data"]
	for card_object in json_array:
		if card_object["image_status"] == api_config["image_status_text"]:
			return card_object["image_uris"]["large"]

def parse_deck_to_image_db (deck = False, ic = False, db = imagedb):
	if deck == False:
		deck = config["deck"]
	if ic == False:
		ic = config["image_character"]
	deck = open(deck).read().split(_deck_split_character)[:-1]
	db.clear()
	for card in deck:
		tmp_image_datum = []
		count = atoi(card.split(" ")[0])
		" ".join(card)
		tmp_image_datum.append(count if count > 0 else 1)
		if count > 0:
			card = " ".join(card.split(" ")[1:])
		print(card)
		if card.split(" ")[-1][0] == ic:
			" ".join(card)
			tmp_image_datum.append(card.split(" ")[-1][1:])
		else:
			" ".join(card)
			tmp_image_datum.append(get_card_image_from_api(card))
		db.append(tmp_image_datum)

def set_hard_maxes (set_dim = dimensions):
	width = math.floor((config["paper"]["width"] - config["paper"]["margin"]) / (config["card"]["width"] + config["paper"]["margin"]))
	height = math.floor((config["paper"]["height"] - config["paper"]["margin"]) / (config["card"]["height"] + config["paper"]["margin"]))
	if ((config["print"]["max_cols"] != -1) and (config["print"]["max_cols"] < width)):
		width = config["print"]["max_cols"]
	if ((config["print"]["max_rows"] != -1) and (config["print"]["max_rows"] < height)):
		height = config["print"]["max_cols"]
	cardsperpage = width * height
	set_dim.append(width)
	set_dim.append(height)
	set_dim.append(cardsperpage)

# ----------------------------------------------------------------------------------------------------

try:
	_json_configuration_file = sys.argv[1]
except:
	print(_unspecified_json_warning, _json_configuration_file)
config = get_json(_json_configuration_file)

parse_deck_to_image_db()
set_hard_maxes()
print(dimensions)

for card in imagedb:
	card[1] = get_image(card[1])

os.remove(config["api"]["tmp"])
