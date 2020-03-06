from flask import jsonify, request, Blueprint
from random import sample
import random
from api.database_helpers import OSRSBoxDatabase

# price api http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item=4151

api = Blueprint('api', __name__)

database = OSRSBoxDatabase()

@api.route("/", methods = ["GET"])
def hello():
    return "<h1>Hello</h1>"

@api.route("/one_in_slot", methods = ["GET"])
def one_in_slot():
    slot = request.args.get('slot')
    att_lvl = request.args.get('att') or 99
    def_lvl = request.args.get('def') or 99
    str_lvl = request.args.get('str') or 99
    ranged_lvl = request.args.get('ranged') or 99
    magic_lvl = request.args.get('magic') or 99
    max_price = request.args.get('maxPrice') or 100000
    allow_untradeables = False
    if (request.args.get('untradeables')  == 'true'):
        allow_untradeables = True
    return jsonify(database.get_one_in_slot(
        slot=slot, 
        att_lvl=int(att_lvl), 
        def_lvl=int(def_lvl), 
        str_lvl=int(str_lvl), 
        ranged_lvl=int(ranged_lvl), 
        magic_lvl=int(magic_lvl), 
        allow_untradeables=allow_untradeables, 
        max_price=int(max_price)))

@api.route("/full_gear", methods = ["GET"])
def full_gear():
    att_lvl = request.args.get('att') or 99
    def_lvl = request.args.get('def') or 99
    str_lvl = request.args.get('str') or 99
    ranged_lvl = request.args.get('ranged') or 99
    magic_lvl = request.args.get('magic')  or 99
    prayer_lvl = request.args.get('prayer')  or 99
    max_price = request.args.get('maxPrice') or 100000
    allow_untradeables = False
    if (request.args.get('untradeables')  == 'true'):
        allow_untradeables = True 
    return jsonify(database.get_full_gear(
        att_lvl=int(att_lvl), 
        def_lvl=int(def_lvl), 
        str_lvl=int(str_lvl), 
        ranged_lvl=int(ranged_lvl), 
        magic_lvl=int(magic_lvl), 
        prayer_lvl=int(prayer_lvl),
        allow_untradeables=allow_untradeables, 
        max_price=int(max_price)))

@api.route("/one_monster", methods = ["GET"])
def random_monsters():
    bosses_only = False
    slayer_only = False
    max_lvl = int(request.args.get('maxLvl'))
    if (request.args.get('monsterConstraint')  == 'bossesOnly'):
        bosses_only = True
    elif (request.args.get('monsterConstraint')  == 'slayerOnly'):
        slayer_only = True
    monster = database.get_one_monster(bosses_only=bosses_only, slayer_only=slayer_only, max_lvl=max_lvl)
    
    return jsonify(monster)

@api.route("/full_inventory", methods = ["GET"])
def full_inventory():
    nr_of_pots = int(request.args.get('nrOfPots'))
    nr_of_food = int(request.args.get('nrOfFood'))
    inv = database.get_full_inventory(nr_of_pots, nr_of_food)
    return jsonify(inv)    

