import json
import requests


SCRYFALL_URL = 'https://api.scryfall.com/'
DEFAULT_SEARCH_PARAMS = '?format=json&include_extras=false&include_multilingual=false&order=name&unique=cards&q='


def get_modern_cards():
    card_file = open('/var/projects/sbguide/data/scryfall-oracle-cards.json', 'r')
    cards_json = json.loads(card_file.read())
    modern_cards = []
    for card in cards_json: 
        if card['legalities']['modern'] == "legal": 
            modern_cards.append(card)
    return  modern_cards


def get_card_legalities(card):
    modern_legal = False
    standard_legal = False
    if card['legalities']['modern'] == 'legal': 
        modern_legal=True 
    if card['legalities']['standard'] == 'legal': 
        standard_legal=True
    return {'standard_legal': standard_legal, 'modern_legal': modern_legal}

def get_name_and_set(card):
    try:
        return {'name': card['name'], 'set_code': card['set']}
    except:
        pass
    return {'name': card['name'], 'set_code': 'NOT_FOUND'}

def get_image(card):
    image = ""
    if card.get('image_uris', None):
        image = card['image_uris']['normal']
    elif not image and card.get('card_faces', None):
        try:
            image = card['card_faces'][0]['image_uris']['normal']
        except:
            pass
    return {'image_link': image,}

def get_mana_cost(card):
    mana_cost = 0
    if card.get('mana_cost', None):
        mana_cost = card['mana_cost']
    if not mana_cost and card.get('card_faces', None):
        mana_cost = card['card_faces'][0]['mana_cost']
    return {'mana_cost': mana_cost}


def parse_card_json(card):
    legalities = get_card_legalities(card)
    name_and_set = get_name_and_set(card)
    mana_cost = get_mana_cost(card)
    image = get_image(card)
    return {**legalities, **name_and_set, **mana_cost, **image}

def scryfall_api_call_wrapper(url):
    response = requests.get(url)
    print(response)
    return response.content

def get_json(response):
    return json.loads(response)

def get_set(set_code, url=None):
    if not url:
        url = "{0}cards/search?q=set%3D{1}".format(SCRYFALL_URL, set_code)
    print(url)
    response = scryfall_api_call_wrapper(url)
    json_response = get_json(response)
    return json_response

    
