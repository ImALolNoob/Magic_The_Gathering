import sqlite3

import requests
from colorama import Fore


def delete_later():
    temp = {'object': 'list', 'not_found': [], 'data': [{'object': 'card', 'id': '3dfb8817-ca3c-44ba-92f2-e9d6294cd25d',
                                                         'oracle_id': '467e22c3-6107-40ff-afc7-5960710c970b',
                                                         'multiverse_ids': [442890], 'mtgo_id': 67469,
                                                         'arena_id': 67108,
                                                         'tcgplayer_id': 164696, 'cardmarket_id': 355395,
                                                         'name': 'Adamant Will', 'lang': 'en',
                                                         'released_at': '2018-04-27',
                                                         'uri': 'https://api.scryfall.com/cards/3dfb8817-ca3c-44ba-92f2-e9d6294cd25d',
                                                         'scryfall_uri': 'https://scryfall.com/card/dom/2/adamant-will?utm_source=api',
                                                         'layout': 'normal', 'highres_image': True,
                                                         'image_status': 'highres_scan', 'image_uris': {
            'small': 'https://cards.scryfall.io/small/front/3/d/3dfb8817-ca3c-44ba-92f2-e9d6294cd25d.jpg?1562734428',
            'normal': 'https://cards.scryfall.io/normal/front/3/d/3dfb8817-ca3c-44ba-92f2-e9d6294cd25d.jpg?1562734428',
            'large': 'https://cards.scryfall.io/large/front/3/d/3dfb8817-ca3c-44ba-92f2-e9d6294cd25d.jpg?1562734428',
            'png': 'https://cards.scryfall.io/png/front/3/d/3dfb8817-ca3c-44ba-92f2-e9d6294cd25d.png?1562734428',
            'art_crop': 'https://cards.scryfall.io/art_crop/front/3/d/3dfb8817-ca3c-44ba-92f2-e9d6294cd25d.jpg?1562734428',
            'border_crop': 'https://cards.scryfall.io/border_crop/front/3/d/3dfb8817-ca3c-44ba-92f2-e9d6294cd25d.jpg?1562734428'},
                                                         'mana_cost': '{1}{W}', 'cmc': 2.0, 'type_line': 'Instant',
                                                         'oracle_text': 'Target creature gets +2/+2 and gains indestructible until end of turn. (Damage and effects that say "destroy" don\'t destroy it.)',
                                                         'colors': ['W'], 'color_identity': ['W'], 'keywords': [],
                                                         'legalities': {'standard': 'legal', 'future': 'legal',
                                                                        'historic': 'legal', 'timeless': 'legal',
                                                                        'gladiator': 'legal', 'pioneer': 'legal',
                                                                        'explorer': 'legal', 'modern': 'legal',
                                                                        'legacy': 'legal', 'pauper': 'legal',
                                                                        'vintage': 'legal', 'penny': 'legal',
                                                                        'commander': 'legal', 'oathbreaker': 'legal',
                                                                        'standardbrawl': 'legal', 'brawl': 'legal',
                                                                        'alchemy': 'not_legal',
                                                                        'paupercommander': 'legal',
                                                                        'duel': 'legal', 'oldschool': 'not_legal',
                                                                        'premodern': 'not_legal', 'predh': 'not_legal'},
                                                         'games': ['arena', 'paper', 'mtgo'], 'reserved': False,
                                                         'foil': True, 'nonfoil': True, 'finishes': ['nonfoil', 'foil'],
                                                         'oversized': False, 'promo': False, 'reprint': False,
                                                         'variation': False,
                                                         'set_id': 'be1daba3-51c9-4e7e-9212-36e68addc26c', 'set': 'dom',
                                                         'set_name': 'Dominaria', 'set_type': 'expansion',
                                                         'set_uri': 'https://api.scryfall.com/sets/be1daba3-51c9-4e7e-9212-36e68addc26c',
                                                         'set_search_uri': 'https://api.scryfall.com/cards/search?order=set&q=e%3Adom&unique=prints',
                                                         'scryfall_set_uri': 'https://scryfall.com/sets/dom?utm_source=api',
                                                         'rulings_uri': 'https://api.scryfall.com/cards/3dfb8817-ca3c-44ba-92f2-e9d6294cd25d/rulings',
                                                         'prints_search_uri': 'https://api.scryfall.com/cards/search?order=released&q=oracleid%3A467e22c3-6107-40ff-afc7-5960710c970b&unique=prints',
                                                         'collector_number': '2', 'digital': False, 'rarity': 'common',
                                                         'flavor_text': 'The shield took a year to craft, a month to enchant, and a decade to master—all for one glorious moment.',
                                                         'card_back_id': '0aeebaf5-8c7d-4636-9e82-8c27447861f7',
                                                         'artist': 'Alex Konstad',
                                                         'artist_ids': ['58b2a57c-50ca-4047-b4e7-efb28cb22851'],
                                                         'illustration_id': '8783d8d3-9c2b-45c6-b611-262d2fe4da54',
                                                         'border_color': 'black', 'frame': '2015', 'full_art': False,
                                                         'textless': False, 'booster': True, 'story_spotlight': False,
                                                         'edhrec_rank': 7603, 'penny_rank': 6612,
                                                         'prices': {'usd': '0.02', 'usd_foil': '0.30',
                                                                    'usd_etched': None,
                                                                    'eur': '0.08', 'eur_foil': '0.19', 'tix': '0.03'},
                                                         'related_uris': {
                                                             'gatherer': 'https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=442890&printed=false',
                                                             'tcgplayer_infinite_articles': 'https://tcgplayer.pxf.io/c/4931599/1830156/21018?subId1=api&trafcat=infinite&u=https%3A%2F%2Finfinite.tcgplayer.com%2Fsearch%3FcontentMode%3Darticle%26game%3Dmagic%26partner%3Dscryfall%26q%3DAdamant%2BWill',
                                                             'tcgplayer_infinite_decks': 'https://tcgplayer.pxf.io/c/4931599/1830156/21018?subId1=api&trafcat=infinite&u=https%3A%2F%2Finfinite.tcgplayer.com%2Fsearch%3FcontentMode%3Ddeck%26game%3Dmagic%26partner%3Dscryfall%26q%3DAdamant%2BWill',
                                                             'edhrec': 'https://edhrec.com/route/?cc=Adamant+Will'},
                                                         'purchase_uris': {
                                                             'tcgplayer': 'https://tcgplayer.pxf.io/c/4931599/1830156/21018?subId1=api&u=https%3A%2F%2Fwww.tcgplayer.com%2Fproduct%2F164696%3Fpage%3D1',
                                                             'cardmarket': 'https://www.cardmarket.com/en/Magic/Products/Search?referrer=scryfall&searchString=Adamant+Will&utm_campaign=card_prices&utm_medium=text&utm_source=scryfall',
                                                             'cardhoarder': 'https://www.cardhoarder.com/cards/67469?affiliate_id=scryfall&ref=card-profile&utm_campaign=affiliate&utm_medium=card&utm_source=scryfall'}}]}


def connect_to_database():
    """Connect to SQLite DB"""
    conn = sqlite3.connect('AllPrintings.sqlite')
    return conn

def get_card_info(set_code, collector_number):
    """Get card info via API request"""
    print(f"API REQUESTING {type(set_code), set_code, type(collector_number), collector_number}")
    url = "https://api.scryfall.com/cards/collection"

    # Define the JSON payload
    json_payload = {
        "identifiers": [
            {
                "set": set_code,
                "collector_number": collector_number
            }
        ]
    }

    # Make the API request
    response = requests.post(url, json=json_payload)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Return the response JSON
        return response.json()
    # Return None if there's an error
    print("Error:", response.status_code)
    return None


def search_cards_by_scryfall_id(conn, scryfall_id):
    cursor = conn.cursor()
    query = "SELECT uuid FROM cardIdentifiers WHERE scryfallId = ?"
    cursor.execute(query, (scryfall_id,))
    uuid = cursor.fetchone()
    return uuid

def search_cards(conn, pattern):
    """Find cards where the pattern exists in one of multiple fields"""
    cursor = conn.cursor()
    query = """SELECT artistIds, name, flavorText, text 
               FROM cards
               WHERE flavorText LIKE ? OR name LIKE ? OR text LIKE ? OR originalText LIKE ?"""
    cursor.execute(query, ('%' + pattern + '%', '%' + pattern + '%', '%' + pattern + '%', '%' + pattern + '%'))
    results = cursor.fetchall()
    return results


def get_unique_set_codes(conn):
    cursor = conn.cursor()
    query = """SELECT DISTINCT setCode
               FROM cards"""
    cursor.execute(query)
    unique_set_codes = [row[0] for row in cursor.fetchall()]
    return unique_set_codes
