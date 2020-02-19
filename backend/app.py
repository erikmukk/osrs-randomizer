from flask import Flask, jsonify, request
from random import sample
import random
import requests
from bs4 import BeautifulSoup
import re
import lxml
from osrsbox import items_api, monsters_api
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

def get_random_monsters():
    all_db_monsters = monsters_api.load()
    monsters = []
    for monster in all_db_monsters:
        _monster = {
            'Name': monster.name,
            'wiki_url': monster.wiki_url
        }
        monsters.append(_monster)
    return monsters

def can_pick(item, att_lvl, def_lvl, str_lvl, ranged_lvl, magic_lvl):
    requirements = item.equipment.requirements
    if requirements == None:
        return True
    is_suitbale_array = []    
    for key in requirements: 
        if 'attack' == key:
            is_suitbale_array.append(int(att_lvl) >= requirements['attack'])
        if 'defence' == key:  
            is_suitbale_array.append(int(def_lvl) >= requirements['defence'])
        if 'strength' == key:  
            is_suitbale_array.append(int(str_lvl) >= requirements['strength'])
        if 'ranged' == key:  
            is_suitbale_array.append(int(ranged_lvl) >= requirements['ranged'])
        if 'magic' == key:  
            is_suitbale_array.append(int(magic_lvl) >= requirements['magic'])
    if False in is_suitbale_array:
        return False
    return True    

def get_all_in_slot(item_slot = None, att_lvl = 99, def_lvl = 99, str_lvl = 99, ranged_lvl = 99, magic_lvl = 99):
    all_db_items = items_api.load()
    items = []
    for item in all_db_items:
        if item.equipment:
            if (can_pick(item, att_lvl, def_lvl, str_lvl, ranged_lvl, magic_lvl)):
                if item.equipment.slot == item_slot:
                    item_object = {
                        'Name': item.wiki_name,
                        'URL': item.wiki_url,
                        'base64_icon': item.icon,
                        'slot': item.equipment.slot
                    }

                    items.append(item_object)
                elif item_slot == None:
                    item_object = {
                        'Name': item.wiki_name,
                        'URL': item.wiki_url,
                        'base64_icon': item.icon,
                        'slot': item.equipment.slot
                    }
                    items.append(item_object)
    return items

def get_full_gear(att_lvl = 99, def_lvl = 99, str_lvl = 99, ranged_lvl = 99, magic_lvl = 99):
    all_gear_slots = [
        "head", 
        "body", 
        "legs",
        "feet",
        "ammo",
        "ring",
        "cape",
        "neck",
        "hands"
        ]
    if random.uniform(0, 1) > 0.5:
        all_gear_slots = all_gear_slots + ['weapon', 'shield'] 
    else:   
        all_gear_slots = all_gear_slots + ['2h']  
    items = []
    for slot in all_gear_slots:
        item = sample(get_all_in_slot(slot, att_lvl, def_lvl, str_lvl, ranged_lvl, magic_lvl), 1)
        items.append(item)
    return items    

@app.route("/all_equipment")
def all_equipment():
    slot = request.args.get('slot')
    att_lvl = request.args.get('att')
    def_lvl = request.args.get('def')
    str_lvl = request.args.get('str')
    ranged_lvl = request.args.get('ranged')
    magic_lvl = request.args.get('magic')
    return jsonify(get_all_in_slot(slot, att_lvl=int(att_lvl), def_lvl=int(def_lvl), str_lvl=int(str_lvl), ranged_lvl=int(ranged_lvl), magic_lvl=int(magic_lvl)))

@app.route("/one_in_slot")
def one_in_slot():
    slot = request.args.get('slot')
    att_lvl = request.args.get('att')
    def_lvl = request.args.get('def')
    str_lvl = request.args.get('str')
    ranged_lvl = request.args.get('ranged')
    magic_lvl = request.args.get('magic')
    return jsonify(sample(get_all_in_slot(slot, att_lvl=int(att_lvl), def_lvl=int(def_lvl), str_lvl=int(str_lvl), ranged_lvl=int(ranged_lvl), magic_lvl=int(magic_lvl)), 1))

@app.route("/full_gear")
def full_gear():
    att_lvl = request.args.get('att')
    def_lvl = request.args.get('def')
    str_lvl = request.args.get('str')
    ranged_lvl = request.args.get('ranged')
    magic_lvl = request.args.get('magic')
    return jsonify(get_full_gear(att_lvl=int(att_lvl), def_lvl=int(def_lvl), str_lvl=int(str_lvl), ranged_lvl=int(ranged_lvl), magic_lvl=int(magic_lvl)))

@app.route("/one_monster")
def random_monsters():
    monster = sample(get_random_monsters(), 1)
    monster_wiki_url = monster[0]['wiki_url']
    page = requests.get(monster_wiki_url)
    soup = BeautifulSoup(page.content, "lxml")
    results = soup.find_all('td', class_='infobox-image infobox-full-width-content')
    string_result = str(results)
    r = re.compile("src=.*")
    result_list = list(filter(r.match, string_result.split(' ')))
    result = result_list[0][6:]
    monster[0]['wiki_image_url'] = f"https://oldschool.runescape.wiki/{result}"
    return jsonify(monster)

if __name__ == '__main__':
    app.debug = True
    app.run()  
