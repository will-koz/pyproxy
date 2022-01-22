# Pyproxy: A Python Script to create MTG proxy PDFs
# No libraries that aren't installed by default on Linux Mint
from PIL import Image
import json, math, os, requests, sys, time, urllib.request

# ----------------------------------------------------------------------------------------------------
# "Universal" variables
# I call these universal variables because these are the variables that are
# independent of the config.

_colp = (255, 255, 255)
_deck_split_character = "\n"
_json_configuration_file = "conf.json" # In this case, it actually is the config location
_unspecified_json_warning = "No JSON config was specified. Defaulting to"

_request_decode_format = "utf-8"
_request_delay = 100 / 1000 # The scryfall API docs recomend 50 milliseconds between requests.
# I give 100 milliseconds because I'm usually not in a rush to have a proxy finish.
_request_not_found_continue_code = 429
# This number is next to useless. Network requests only return this in my tests from Reddit, which
# would only be requested if an image from Reddit was specified.

config = False
imagedb = [] # Image database
dimensions = []

outputPDF = []

# ----------------------------------------------------------------------------------------------------
# Less universal variables

current_col = 0
current_row = 0
current_page = 0

# This is the two dimensional location of the image being rendered at any given moment, and the page.

# ----------------------------------------------------------------------------------------------------
# Functions

def get_json (location): # Get JSON from either local storage or the Internet
	try:
		return json.load(open(location)) # Most likely, the file will be a local one
	except FileNotFoundError: # If it isn't a local file, search the Internet for the JSON
		request = requests.get(location)
		while request.status_code == _request_not_found_continue_code: # A do-while block would be better suited, but this is more readable
			request = requests.get(location)                       # Oh yeah, and there isn't that in python
		return json.loads(request.content.decode(_request_decode_format))

def get_image (location): # This is basically the same algorithm as get_json, but for images
	try:
		return Image.open(location) # try to load image from local storage
	except FileNotFoundError: # I don't like doing this, but this is slightly different than JSON
		urllib.request.urlretrieve(location, config["api"]["tmp"]) # Put it into local storage
		return Image.open(config["api"]["tmp"]) # and then load it from local storage

# It's hard to believe this is the most readible way I figured out how to add an image to a pdf. In short, it
# checks to see if the current page is initialized. If it isn't, then generate it. The render width is then
# determined from the card size in inches multiplied by the pixels per inch. The position is calculated from
# the margin, current row/column and dpi. Finally, it pastes the passed image to the PDF to the last page.
# Another note: actual MTG cards are around 600 dpi, but 270 dpi is still an extraordinarily good image.

def add_card (image, pdf):
	if len(pdf) <= current_page:
		pdf.append(Image.new("RGB", (int(config["paper"]["width"] * config["print"]["dpi"]), int(config["paper"]["height"] * config["print"]["dpi"])), _colp))
	card_width_dpi = int(config["card"]["width"] * config["print"]["dpi"])
	card_height_dpi = int(config["card"]["height"] * config["print"]["dpi"])
	x_position = int(current_col * (card_width_dpi + config["paper"]["margin"] * config["print"]["dpi"]) + config["paper"]["margin"] * config["print"]["dpi"])
	y_position = int(current_row * (card_height_dpi + config["paper"]["margin"] * config["print"]["dpi"]) + config["paper"]["margin"] * config["print"]["dpi"])
	pdf[-1].paste(image.resize((card_width_dpi, card_height_dpi)), (x_position, y_position))

def atoi (x): # This converts strings to integers. The name comes from the C function which does roughly the same thing
	try: # try to cast x to an integer and return it.
		return int(x)
	except ValueError: # The important thing for this application is that if there is an error, it returns -1
		return -1

# Using the API configuration and a card name, get a URL to an image using the Scryfall REST API

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
	for i in range(card[0]):
		add_card(card[1], outputPDF)
		current_col += 1
		if current_col >= dimensions[0]:
			current_col = 0
			current_row += 1
			if current_row >= dimensions[1]:
				current_row = 0
				current_page += 1

print("Outputting to " + config["output"])
outputPDF[0].save(config["output"], save_all = True, append_images = outputPDF[1:])

os.remove(config["api"]["tmp"])
