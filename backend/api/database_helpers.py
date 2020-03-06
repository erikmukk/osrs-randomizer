import random
import requests
import re
from osrsbox import items_api, monsters_api
from random import sample
from bs4 import BeautifulSoup
from flask import jsonify
import json

class OSRSBoxDatabase:
    def __init__(self):
        self.all_items = self.init_all_items_w_prices()
        # https://api.runelite.net/runelite-1.6.10-SNAPSHOT/item/prices.js try this
        self.all_foods = self.init_foods()  
        self.all_potions = self.init_potions()
        self.banned_monsters = self.init_banned_monsters()
        _all_monsters = monsters_api.load()
        self.all_monsters = self.init_monsters(_all_monsters)
        self.all_bosses = self.init_bosses(_all_monsters)
        self.all_slayer_monsters = self.init_slayer_monsters(_all_monsters)

    def init_all_items_w_prices(self):
        all_items = []
        '''URL = "https://rsbuddy.com/exchange/summary.json"
        r = requests.get(url = URL) 
        item_prices = r.json()
        for item in items_api.load():
            price_found = False
            try:
                for key in item_prices:
                    ge_item = item_prices[key]
                    if (ge_item["name"] == item.wiki_name):
                        item.price = ge_item['buy_average']
                        price_found = True
                        break
                if not price_found:
                    item.price = 0   
            except:
                item.price = 0
            all_items.append(item)'''
        URL = "https://api.runelite.net/runelite-1.6.10-SNAPSHOT/item/prices.js"
        r = requests.get(url = URL) 
        item_prices = r.json()
        for item in items_api.load():
            price_found = False
            try:
                for item_price in item_prices:
                    if (item_price["name"] == item.wiki_name):
                        item.price = item_price['price']
                        price_found = True
                        break
                if not price_found:
                    item.price = 0   
            except:
                item.price = 0
            all_items.append(item)    
        return all_items    

    def can_pick(self, item, att_lvl, def_lvl, str_lvl, ranged_lvl, magic_lvl, prayer_lvl, allow_untradeables, max_price):
        requirements = item.equipment.requirements
        if requirements == None:
            return True
        is_suitbale_array = []    
        for key in requirements:
            if 'attack' == key:
                is_suitbale_array.append(att_lvl >= requirements['attack'])
            if 'defence' == key:  
                is_suitbale_array.append(def_lvl >= requirements['defence'])
            if 'strength' == key:  
                is_suitbale_array.append(str_lvl >= requirements['strength'])
            if 'ranged' == key:  
                is_suitbale_array.append(ranged_lvl >= requirements['ranged'])
            if 'magic' == key:  
                is_suitbale_array.append(magic_lvl >= requirements['magic'])
            if 'prayer' == key:  
                is_suitbale_array.append(magic_lvl >= requirements['prayer'])
                    
        if False in is_suitbale_array:
            return False
        return True  

    def get_all_in_slot(self, item_slot, att_lvl , def_lvl , str_lvl, ranged_lvl, magic_lvl, prayer_lvl, allow_untradeables, max_price):
        items = []
        for item in self.all_items:
            if item.equipment:
                if (self.can_pick(item, att_lvl, def_lvl, str_lvl, ranged_lvl, magic_lvl, prayer_lvl, allow_untradeables, max_price)):
                    if item.equipment.slot == item_slot:
                        item_object = {
                            'Name': item.wiki_name,
                            'URL': item.wiki_url,
                            'base64_icon': item.icon,
                            'slot': item.equipment.slot,
                            'tradeable': item.tradeable_on_ge,
                            'id': item.id,
                            'price': item.price
                        }
                        items.append(item_object)
                    elif item_slot == None:
                        item_object = {
                            'Name': item.wiki_name,
                            'URL': item.wiki_url,
                            'base64_icon': item.icon,
                            'slot': item.equipment.slot,
                            'tradeable': item.tradeable_on_ge,
                            'id': item.id,
                            'price': item.price
                        }
                        items.append(item_object)
        return items 

    def get_full_gear(self, att_lvl = 99, def_lvl = 99, str_lvl = 99, ranged_lvl = 99, magic_lvl = 99, prayer_lvl = 99, allow_untradeables=True, max_price = 10000):
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
            item = sample(self.get_all_in_slot(slot, att_lvl, def_lvl, str_lvl, ranged_lvl, magic_lvl, prayer_lvl, allow_untradeables, max_price), 1)[0]
            # Reroll if needed

            while (not item['tradeable'] and not allow_untradeables):
                if (not item['tradeable'] and not allow_untradeables):
                    item = sample(self.get_all_in_slot(slot, att_lvl, def_lvl, str_lvl, ranged_lvl, magic_lvl, prayer_lvl, allow_untradeables, max_price), 1)[0]
                #if (price > max_price):
                #    item = sample(self.get_all_in_slot(slot, att_lvl, def_lvl, str_lvl, ranged_lvl, magic_lvl, prayer_lvl, allow_untradeables, max_price), 1)[0]
            items.append(item)
            # print(item['tradeable'], item['Name'])
        return items  

    def get_one_in_slot(self, slot = None, att_lvl = 99, def_lvl = 99, str_lvl = 99, ranged_lvl = 99, magic_lvl = 99, prayer_lvl = 99, allow_untradeables = True, max_price = 100000):
        #item = random.sample(self.get_all_in_slot(slot, att_lvl, def_lvl, str_lvl, ranged_lvl, magic_lvl, prayer_lvl, allow_untradeables), 1)
        item = sample(self.get_all_in_slot(slot, att_lvl, def_lvl, str_lvl, ranged_lvl, magic_lvl, prayer_lvl, allow_untradeables, max_price), 1)[0]

        while (not item['tradeable'] and not allow_untradeables):
            if (not item['tradeable'] and not allow_untradeables):
                item = sample(self.get_all_in_slot(slot, att_lvl, def_lvl, str_lvl, ranged_lvl, magic_lvl, prayer_lvl, allow_untradeables, max_price), 1)[0]
            #if (price > max_price):
            #    item = sample(self.get_all_in_slot(slot, att_lvl, def_lvl, str_lvl, ranged_lvl, magic_lvl, prayer_lvl, allow_untradeables, max_price), 1)[0]
        return item

    def get_random_monsters(self, monsters_pool, max_lvl):
        monsters = []
        regex = re.compile(r'[Dd]ragon')
        for monster in monsters_pool:
            if (monster.combat_level <= max_lvl):
                isDragonfire = False
                if (regex.search(monster.name)):
                    isDragonfire = True
                _monster = {
                    'Name': monster.name,
                    'wiki_url': monster.wiki_url,
                    'isSlayer': monster.slayer_monster,
                    'isPoisonous': monster.poisonous,
                    'isDragonfire': isDragonfire
                }
                monsters.append(_monster)   
        return monsters   

    def get_one_monster(self, bosses_only, slayer_only, max_lvl):
        monster = None
        try:
            if (bosses_only):
                monster = sample(self.get_random_monsters(self.all_bosses, max_lvl), 1)[0]
            elif (slayer_only):
                monster = sample(self.get_random_monsters(self.all_slayer_monsters, max_lvl), 1)[0]
            else:
                monster = sample(self.get_random_monsters(self.all_monsters, max_lvl), 1)[0]
        except:
            return {}
        monster_wiki_url = monster['wiki_url']
        page = requests.get(monster_wiki_url)
        soup = BeautifulSoup(page.content, "lxml")
        results = soup.find_all('td', class_='infobox-image infobox-full-width-content')
        string_result = str(results)
        r = re.compile("src=.*")
        result_list = list(filter(r.match, string_result.split(' ')))
        result = result_list[0][6:]
        monster['wiki_image_url'] = f"https://oldschool.runescape.wiki/{result}"
        return monster   

    def get_full_inventory(self, nr_of_pots=6, nr_of_food=22):
        inventory = []
        for i in range(0, nr_of_food):
            inventory.append(random.sample(self.all_foods, 1)[0])
        for i in range(0, nr_of_pots):
            inventory.append(random.sample(self.all_potions, 1)[0])    
        return inventory 

    def init_foods(self):
        return [
            {'name': 'Shrimps','base64_icon':'UklGRsIBAABXRUJQVlA4TLUBAAAvHoAFEFfCtpEkKTcz4L4WFiId8k8BH2HD9qXBuJEkJ6ubOSACUiFXIvTm6baRgkaSmnmKAPDvs0PmP1rQIm59sw+DG1yZglRiUomJqyeIsZGJsZAZ20IiRkIiRiJCKiQiJCQs0jB02REA/MDTAQCAAgAoLgAgAYBKALgqIfke7uuohA8mrrH7b+rjDFSwSEHCwoV3+4AOgNhIkiKp8pgZnhmWZveZmf/892jgzoSI/k+AVohTwYTA3f/h8dEx4GMdH2bYHydJFMVJiosMuWEy6ndH87M8y0xssIimHuYTbDOZztfT09xicY68IIn8fpjPNnaPM8eJWcfjhhg29w525oi/0zjbgiAJ8cx+adyFxVGUxVzi9EiC+dMTIolik5weLd7f3t7WAFxi8FRGgsIU55fX48mkW943eY7nvIlsuLu7uxuNhg8VAHmukReg1+08VVEoCseWDVh+HIGUtqeEkEAQr6XSKEhkCZJw8HKwMeiFiTwDcpxHa73u4xKiMOn7x+fX98/v4Vm784iW5fysOD46jIqbdqv5iJbn6vLywhQ3rWajXl+FgLvb62ajXgOtGLfCAQA='},
            {'name': 'Cooked chicken','base64_icon':'UklGRh4BAABXRUJQVlA4TBIBAAAvHMAFEI+gIAAINKWbHRQ1kqQs84Gs8/87NwratpFD3n8gb/4DAAD/hbrUQaNYYoklGuX+F/WoFJXj+RAF06G2ADGS3DYSRlgswDNv8g9XNoSI/k9A3IbYE4/y/hIRfHnm+/sm+Pw+wuvnhwg+fw9AqkXA+/8eKVsEyvcnuQYqWwQq28RlNtkWEch3YJNtA6jc19jStiszE1W3iXO2tF1SpjKzegwcscl2qfZKedpbbpzYlnxYKa+2peQgOyXb7m6neueSOFDZfTgtz5q2bSICye6e49bMWr0nAqncPee9m5kdUrl7ZtZau+luu4AIstw9M+t0ZrrbxJ7s3bo03cSFmXV19ifBrTVAXJhrQFzmZlwG'},
            {'name': 'Cooked meat','base64_icon':'UklGRqABAABXRUJQVlA4TJMBAAAvHIAHELfBoG0kR+dc+cYf3vNi0EiSots6hif/gt6WgrZtpPh+/qyO1fzHSBlpXIPve85arrOdvc06yGSQCSATAMoABAJQBgAgAAEQQCAAAAICAEQQAETg/z9AkG07baNX5poZvjDMifa/N0uWlxDR/wlgS8LNlkXf1kWWRFgERDR0TRUvAs6JrLV1uozg3Fpr2+wPYZBC2GlXRItIcgxVHAaluHXX6S+CtLDurvgHC4SR5Brr5C8AgOLW3eXR0xwARith3WOV/IN5gZVWUnDytHn85QJglBScrH+o0giMMQastBSc7Ow2T34mMEpwsoFDlcXPDk02vCnTP7CJ4R6aTvq6SN5daxHWVlkE5tjIoL4p00/PTs+y1tquLpIXz96Qy9u3Vf4N5jpujSCa0bdVkb35zsf9RgsicvRtXea/YJ7r+bjfrTXnRDQOfdsU/+8z7tfL6bDbrBTnnMahK6OPVx/D43Y5HXbbtZFCUF8lXwCbCeC4323WK63kUGc/YKEAjJaCj20OsCUBjH1Xgi0OACwQAA=='},
            {'name': 'Sardine','base64_icon':'UklGRtgAAABXRUJQVlA4TMwAAAAvEsADEGehoG0bOXX1PlinJoCCCA78RnvZv4orgrZtG13Sbf8xff7jqTzxv+/OMXPMGD2bRAF/9S2IBDMaK0jQbQKWRDUASKMbAVA1WAlYQShQQCyoqqCSAq4PMFlgGEmyqdtv27bzTxD3fwgR/Z8A4oK+Q8MPyh/yN0gaHhmAqKp2kGY5ngDJsKJlGgDQHRAUx/P3FaBnCLIZxGkF0CsE1U2zvAa9Q9LrLkmSlgEzqrq5ajoQIyzbaev6mlU043aMAHH69bwmEB934gM='},
            {'name': 'Bread','base64_icon':'UklGRn4BAABXRUJQVlA4THIBAAAvGgAGEFehoG0baUq63UPg+GM9EooaSYqjhO7meGEAhW3btlhM5/wTTNJU2zE1UsP3sy/3MZtedJ/RYaQokYgtgiaiYAKKLhJAI0gQQIYE+A+RhRkIAIexbTWRf7NKFCN8YHPqv0L4hhIi+s/AbdtGctV9+15RrAZIik0BOxjFSthkmIauEfUZtugSRvPqBLBm9Im+bSS7HPew0g/B2zGhRH3eLQGA1qfg1BstebkAQHS6GaxFRDu0WrA5EGMcO6PlaNE5N/XmMgNwmizOzmHRoxPHI9D+pE3XT5aeVXIM5WFmdGPXSNNNzubtjHUnKgS0zpOHNqNHp1ldU5+oZZP35wsqNkZRV2fIfh9h6pTS7YjonGEpWcot+tSR0gwumpmU5518slZJIUyXvEBB+b0eV0+vmjqcOOf9uAX6mgWrq+yc/ycPM5qVlzK7UBJX7xKyOpUrfw7cnjeyUbPz+r8I8RbyB+JkdrXQv4Z8lK3//LoF'},
            {'name': 'Herring','base64_icon':'UklGRlwBAABXRUJQVlA4TFABAAAvHIAFEP/BoG0bQZdku8Px9B+xg7aRJGna6f2QHOZj66iNJEmacM7JYvk/FuP8xzmHc/r9fubhfZ+Jmrmg0zQtNO0ke19sQkHYJBhLoaEEwwFYhLA42CBCaU+IUBChgHYcgA4CYZgddzogzkyzPbaLw///MziMJNu03nn8tm3b/vmndX0z2BfRfwVu2yjJMcMvHGPJsZGasIl1q1izgap2VKoWULlikVDJCJIsmkBwPT+IEql0oaiFEISJZArpTDaXL3IJilIyJa5XQrmCaq01H/fbBCGyseIFG2i2mvHwetguZ6Nei1gslirVeqPV7nR7ALAgSR5b3UG70+sPRkPBhXoj6o/+89V2NhVcLHW7Tv7L7X4uuliuNPlivTucLitgycRal29Z6XrbxjPuhhwNx/P1dn/uwdnFWj7v1wPv05FJgP7zgR++VyhaDBpMWwA='},
            {'name': 'Mackerel','base64_icon':'UklGRjIBAABXRUJQVlA4TCUBAAAvHEAFEH/BoG0bQfdx7/k86ceMoG3bXHV7TId6uAjatm3KzRD88x/ncM5+73l3ds8dt8dYz5oVPVvCRJmQCtEAgYQAyQQJZCQhYQol8BhJkEkK2/z/MziMJFuJeJy74+5O/unp/9QlsC+i/wrctlGSY4ZfKLKSskZ60Jp4XwPd/gZdb48nScfL9S4BzTxfb2II6ma72x+O54sYwjj2hGkLnvwiLJSOp+k5+cVvfDTL0L6faYEu49j354sfa8xGHPquYxn6j4b4fL2/P82AOdGNaeYY31/NMG3HBeAAcbK8EWlG73jBRJ9FEWT1XhDFU5M0E+TOWEqBJPIdSxRBQynJ8oKzIeQgRcBYKqtRZmYhw4iqbpkbVASIPx+ouGvrhRaJBtkWAAA='},
            {'name': 'Choc-ice','base64_icon':'UklGRswBAABXRUJQVlA4TMABAAAvHMAEEK/CqG0kSZPULoObP4Blt6/uGRpuI9t2mn/P+ZiciAaQ6b8R1aFIkX2fYdxIkpPpngMSsF8yJH+n+Y/RYjSex+q9n+xwC9X+XqjShVAhtIIQKIVChYASKEAKBEAlAgAy1bbU8TyI0ksEEBEp7GUgAsQBQiQiMjBlILJVHBIQGYkMTBmEIQzf4zbPmOMzK+b5mxVzRP1+PWLVryvm+HTFqvhfj94vKAVqXwcDBNm2TUfvts3vtmLbTn/GyfwH81F/COdG9H8CRGQS8RNwhLgIF3zOJ4QYCLhm5itc4piCwwh3wbd8w7tcqd4ejM8oiB7DH/geyWyx1uoNN0H0ZUihz3hCIlOo1FvdQ8jL+6ehqH5mWfpL5wrlWrNDCFA1/fVD1wzWGVB/0/miv3RDECBF1XQ23nQD+902ETG5PiNBkqxqOhvl7/YCwNK/4iUDHkgQZEXTuZnuWh6ABQDPvwBIAARF69dTfct0mdkDFsFLH0BoV5NDC/+m7XiL4CWvgkCNcmJk4n82MZ2gJa8iVIo/bALzachyxSARsjklwPznWcCSVwSIcIIAyPqfw1lgyQQRI1n/cBYEiHjJLyIC'},
            {'name': 'Trout','base64_icon':'UklGRmQBAABXRUJQVlA4TFcBAAAvHAAGEI+BoG3bLC6u80dwbgzathF0dYbuOT83BG3bZnFRnT+Lo5n/uHfu9X2PZjeLmS4zzC6ZhQgrzFBhBAGFMSogEkOBhgKQGJUGcCAkhtL4/wcIsm2nbf4zSDIzy0xh2P/y0srJDiL6PwH0fdAvEeMHCJIfwItAx/EXHD/+AgQ+INwwOQbBP8BsL0oBHOEMRIDObb/K0xhK4MwEoBnM9rO2AUiNmYauGcxyvGyZQOpgpmZyy3b9MJNnkDpgmFzYjh/FRTuB1GGYTFhOECdZ1c0gdZiMCzeI07yohwWkDHBhOX6cFWUlpxWkDC5s14/SoqplN68gZQjbC6KkqBrZDfMGUobjBXGaV03bDeOyg5SRjNO8rJuUUrbdCXSgHN+X075XxTjNC+hIN15Op9OproeuH46gnS/nz7ZdBikPLZfL5XK9jQM+6cjlers/nq8F9FX8S18FAA=='},
            {'name': 'Cod','base64_icon':'UklGRsYBAABXRUJQVlA4TLkBAAAvHAAGEMfCKJIkKds1WOFH4N8YL9gaLhFsIkkS8jvrhQj8KyOCm2MUSZKUnWouBdjgj38lyNijmH+xSYJ7dMc4zTh1ux/VTYJqAABzLmQTUI0EgMomBYBEQDUIqruAXymABCAUEgEQBAEEgIClu4D/xshHpVKp2p8rXVSfVq50uf5JdX7TnEkXXVSqOVKpepc5i+p4S6vz73q1Prf9eiVBSgAAoIAYybZp6z7btm3btr7yz+Rxn5vBX/dG9J+B20aKOuuFY/gFx14SDnwswMd6LuFhuwT7C0r2mwUYqPB6pd1qDgbKZySKw3Y5kwBUBMUjEpy0Rut4OltIKHIJcD5qjFbPYER1kjuZ9HLS6E0WT7Mt4Ujno1ZvNFnt3kiFhJNaqzOYrA6nP5YhnY4and5kc7o8wQRNrdHqHjOP1xdOZanr4/UIrz8QjKZzFK3OYLY6PIFgOBJP5yk6o9nmcPtD4Wg8mSlQjBa70+0LRWLxZCpbpMw77VazUY8CiMVL5I0mnWu5WhND/uddJByV/v/do0Jit9+DhDJolSvPignN7hBkhDKA21cKEgD0uiyI3z+/f+9/g2yvxQYA'},
            {'name': 'Pike','base64_icon':'UklGRrQBAABXRUJQVlA4TKcBAAAvHAAGEKeiEJIkZ272g95DP8LrBA1GkSRJmT4GV/i3gA+eC92M2jYSlGQG0/LHchjuvTv/wYDxuo82QmhaSq1BcAZCIozWIJiBkQojHRCpMJJgmGAkwUiEUQlGEH4EkWLx8vQJhhhGGKE4kMEwYRFGiA9CLGQ4EApVDMbvdfvMLhZi8EFIqBgu/Fwvz9glJSIkIyFViFDTOM9nvz84jCTbtO4+fdu2bdtm/rn43JdBRP8ZuG3byCk7b36D8RcYU8MEVWxQwWAD/w9CZ3GAQwLfTDYXaKGvQGOwODwAqLgiYADMTn80EXBZ8J/FEwf0Zrv7JZWPUx00Np+itzq94Vj2kSf3RJ2kNb9n6Vxh1CNBkPVWdzCWLdRGa9LnCn80nS0UG9sTSTHaveHPFY3xhgJo7f5oKpur1DvTNel9RTRVrNTq7dH2eKF8fj9XaXTGw9mO5vTHspX2aDrbrPfHK8XmCcQz+epmdzhdbnfyRb7IM19tvWf5d4FRiSTz1W7veLrwBJl8udntD87XW56jofTo9QeTxe0OAHSaL5P5cvX9NtDbP8V4igEA'},
            {'name': 'Roast beast meat','base64_icon':'UklGRgYBAABXRUJQVlA4TPoAAAAvHEAEENdgIG3b2Fh2B1fQtg3Tbj0Yxp/nZDBp29iatGz+IzhB/r38XHWti2bM4tmCMYFAIHSDyoCiC0I3LJYyWAAHkSQp0vQP7h4z+He6R+8gov8TQO9B/8QEfIex7xfgIwxt0zTTBuAD9HVV5aru1+PEK3Q5RaSUq3beX6HLpmYekXI9nHiGPhuzqJp7pAwqcdtlY2YWNfPI3QXGcZqXdWuTyoWoR+7mAk1b5/BUNSpX6hFRgQo3YbHIVfCleplqAAQTZlZPya/YyqjabQOEmVks3OOHS1VVS3U3gFCwRiSALgER8aoFFaqikUEPcUlEiAg3BehbXNK3'},
            {'name': 'Pineapple punch','base64_icon':'UklGRqICAABXRUJQVlA4TJYCAAAvFUAHELfkqLYdRvnJ0Htb4wAjOMArimbbIfk/NhzUtts231LSvVsWpVL+FEogW/pfsCPZVq30c8Pt19IgcRIhEodt8x8AwGIbjwxbwB6wA+x0wHHtgJB8RyEiIUIhIiEVEQoREokIyBaBCIkICUVshYTk5/jMNCeSWPmt/DcyE0k4Gvkt9GPqZiz49qwfa/6hOa3BaTrgwPEOOPA13wHHj/hh5SPmoUwDz++K+ZIbx9eKG+a4Yc6i50X+K+2/PLY3ZKkaVU2i1FSjakQE2IeIP2SJCMkgtsgA3gMWqkrVAqqpmgQZJIAFoFUNspQABhpSkwaZSkPVqobUqlrVyEylkUz/7Q8zqUZmykxkKrXf9i8zZYZ5+fH+vTpfXwBLbqOxDbdmtrTsN6wtAAunx/C2YG1pdz6zP7PvHwCCbdtmpLyybdtq27Ztu8to20Yy4MJPhhDRfwZuGynyMu/BKzDSAIVAYay6vramCtCppqG5qbG+rqYakPdtBegCRAMAspl0qqKnb2Cwt7OjpJbLZfNqUv2DOE4QRAEU9WQzLanUIEHgBI4XyWTSqUDEVx9OD+JFWTvkHaWSSfbwSKW/bCCfcKK7uDuRMHKG7BVyXV+hibcV29tVafTmconDG0y+IF4obIukCrXWYHG4PKiXCRt8gUAsU6rNzjXkKwYajy+UyHU2H8l7f6PT+CKpyblK8pGAyaAJxNYg6Zf7ZjF4RvcxGQy4LLotBBipOS5z54yChcXlFcDILf3MP1GAwd8vUGjDyfz/xRWQpcNoNDr6eH+D7oT1zZmJsXjq4e72GhDpa3ZmYmL8IJbMXV+izM5MTU5ObO1Hk9lzQDWmp6em3p83d6KJzCkywsz058fr+s4hAIVfHVA1DA=='},
            {'name': 'Salmon','base64_icon':'UklGRtwBAABXRUJQVlA4TM8BAAAvHAAGECfjIIDbuJF0CYRBG+uhGBDlI8G4bRtJjj2z2/9ra9wOrihgFEmSlKruPRCBAvwL4YmYI+a/DRIkf5+TUlMLOgxtQ9vQgpah6f/cNFhgDQQ6WPMRWIMCgTVYQIPye2CBAg0Wn35Y4AHxKlgNgYI2BArUr4I21Gjjc19IcBYRx4TlBFGOIsoecDiylUSsRLacYsU8B3bYEcuWrSRsxbL1ACti2ZKDCqpSFVWqqIhqekrF73rAYSTZpnXPt23btm3b/j//HHzezyCi/wzctm1kg7297xWEeoGQf9TgH5UG/KFUBeoPCIVyHSjIwceZssVKEyjIvgPpfKnWBgAs2cwrALGgx97ttOqASQNAIvKiH/awAZ5SyUQ05HM79Ks5EFQ8EvR5XHarTrpDQTQc9HvddotJI6GjouFQwOe2mY16lZCBes35XTazQaeR85nY+SEY8LntZr1WrZTSWJhgwOuyWwwalUImprMxAa/TZjFqlHKpWMjgYDxOm9mgVcokIgGfycU0Z/PFcrWWvioR89ALdWeP/XazUWreVwGCZTQ7bF9VKKaj8QQww+Vh965EspwO+mie9vvD8cTnAwDgy4fT+XK93ZkU/2P4LDUEAA=='},
            {'name': 'Tuna','base64_icon':'UklGRmABAABXRUJQVlA4TFQBAAAvG4AFEGfBkJEkQdc1z/EI7+/xPsfBsG3bMAlV9Mtduts2II4kGaavJCf/h2iY/ziznOk73/ccww5hDVJjBRiVQYMEMkABkIBiCYrluRtJgIRgAywH/3vd/7nfY4AY2bYS6d9x3J1xl/wTBD67Gdwb0f8JMDNh/hEOpjALLqfg829AQ2gWPIkGW5GeNAMa0NkJnksYa9CXRJcOXc7BdnSjNemQtMJueqvNerWTDRxrbTerpQVckp6fpYk76jAMMAZPfhAyT5NAkq8wqoo8xQB+EEZxoiIJnDhimGTFoW+bCoYoO6VZzrYq8jhI4qwoMWpINN/P5XwqC0l5RlWEmUTf/S7nU920fcWyIAljc7iceakXQw6tDpczL9dm0S3U1KRgpnE5ni/X271ZNAu1jQRjdb5cb/dH01d137WCsbve7o/nq2/H7Qjy8Xy99yRB0szGpJkN'},
            {'name': 'Jug of wine','base64_icon':'UklGRtYBAABXRUJQVlA4TMkBAAAvGMAGEAfCJpJkK29n3i8E/wrQR0hd9BDBppEkR7fd5zL3z5/bo9gP2TaSJOWmhs9D5G+SIxYrzf8bHFpZWsnrvd3rseelt80YO63VT1paVBQoRAqRAqwFIcQCACkAgQCAAAAcgOAXCMsBQhAgRIQACJ7xcuAsB+/3qX9UjsrflwMOZNtKm/y6KxCcurt7u/9lASFdQkT/GbhtpCjTamCP4RORCwhElBLAuNS9wWi6qEKKY8qEMqPZYinbAEFwTLk0k+V6vR7ENQjNEImZ6M+269XUplDudDGhcnh/PJeDuBJuVBuRz/t1uz9UN23DGWv9vq5gZYCUjS992kSMxiRfKFUbEPDqcpn3mVa41OpiiqoQyJfr9boeYipUbzAW7RL4PjqOw77RUpn+cEAbBXDeeHkz7PeMVo0cjHqkloMI5mePhUPJuAIw1ghs3nm+TIYDh+iU5H4ibV5ePPbTkUVLwcxYAHj7eFpb+g7OM5A4haeFjxKCZjMQ4uTR00ryOG8VYLecjX0Y6eaD7cYytGhBcaeYeOBBjOQxapdDHLeruXuAXm7WIUrqkEDZHPwQIImROO2ThuNuvZiOVOx96Smy2VCvStUf/0UEAA=='},
            {'name': 'Rainbow fish','base64_icon':'UklGRugBAABXRUJQVlA4TNwBAAAvHkAFEJ/CNpIkJ3M7jzRJA48kCVpdGo7bNpIkjus5E+8GuXnsaxO4y2xr25bx3WOuQKQE/VegFpHom9/95j+QoPo/V+yn98O+2Bf76n2xDxg1GmhBAw3UaKCBBmrUuh/+GXuiH2r8D+zueW2u2+w4fw4cONivUSLnfaHaSE0YkMFQEwwEA0FIZKgFEhEMJAGDgMQDIQZLOgHhfiSt+BX9t2bNYL+i2T6TAkigoEaKFBggRrJt2rr72zaebds280/mnHvvQwRrRfRfYdu2jZJ07/oKY7cJjENMkC3ggBYkUvsjCIajOxD7UjjqojOogXmCJMWmFI27AbjIgL9AUgxBnLBEIukxmW4IBYIKRGPuqBn5Hw0x6GM0nnDqBoIIhSNwuS3xh9+v+azb6w9UA3WDcpcF+fn99n4u6bA0YKQamGCcZr4/vfzgyrFczK3TM1lm0qaZ8v7x/gZU6VgtuTB7vlAqFnKZoBjy8PoCPLNWday5MnmhVK7WKqVCLqF4IvmI5xod1c0aqqBa6gKgXs5rv7kn757rNZLbzbpSqzc65t1QzosBubyBAqiRXqLRFuzQlJxdXd/c3t03ffSy1ZZ9NHJyenZ+4SPpFeyrMPhMhkME6iWJwxS8iyPoHw=='},
            {'name': 'Stew','base64_icon':'UklGRsABAABXRUJQVlA4TLMBAAAvHoAFEPfBsG3bSIWc3t0ot/92nzwHw7ZtIxUn5955bv9xboVXAYO2jST5/jtAxx/ZZuY/1mCN7X2OWZiZPX8mTJEixS4IUySnQEJCwnVATgNAAgAkAOEEAAEAAICpw7p+TLz3Yo862vm/RalDU4emPTR1KP6p0aHR+Efz3Omf3/jHAMG23bRRVGYIc9oOl5ln9r+uVEpmCV8R/VfkNlJD2EIoJ15hCKgEowzCVxjFSZqppqr6VyZo6/GYTlQ1jQE8iwQ5rs9jBuQRcu7Ew3bcgMfbeDQc9Ht+oKHqiliYtuOHyQB97WmX0ws1Cv0z5bEzbTcQdzsC7fWHgbcig/Zj0+lI2oK86fuusyccx2bBey0BgFw68yHhMDbl2aaEiY49HxDW18KzDQYXbcx7BPfE3hPUAQjRGs+7BHf9aGhdUgMgxGq5IIM8f7m//tYEVVUutj+ea5MBilT1e3P5q76oaJWJ9zDwHes1EsHnfHO8/d6Om48YiMLAs00yAMpepMUkMaLAFV+FoikmhWSvGRX9NILOCpginwmo7JeGmbRJHPFbpY14IzJ5958mBiLi3T+bcgMA'},
            {'name': 'Cake','base64_icon':'UklGRg4DAABXRUJQVlA4TAEDAAAvHcAFEGfluG0kRypM9e73XPaXqO1WnQvCYSRJjUM9C1L+iSg2L9zOQookyZHkp97Hn96RkFOR8/8GBxVUXrb/hSEJQxKGEkgykGRIwpAkAyH5f4SQwPwNkkDIQJKBQFIGTjIQmPYjGRJIEggMCWQ4cGCSQCBk2g+cZEIgEBJIAAKB/AIw8fwB7YMDgQwnBALB0/sxHAgkZHxgcMYHcp8/4gy5/37cxrdej96Pub64s3W2RvUPFtWoRgk3SrhRerMq1bAosYSFK9arqixh4YrFEvvtzbpYwpVrQYaDQOfI8IUBMzIaMGCgc+aP/mjDH61/s9GH15NDYb/z/H16nX+XxwdNBDg6yBgk2rZlSFJFtW3btm3btm2UzTZmpsdt/2RHpD7hRUT/Fblt2yhyd3vrJ0SMQtwl4i2UkVNQUlHT2NrVNzw+w3sVJSSnpmVk5xeXVze0dvePTMwuLK8hdqJi4hLJICsnr7iitrmjd2h8ZmEZMRMSFhEVG48H6ZmMpxtaOnqHx2cXEOD4BQSFhEdGxyUkpaZl5hWXVdU3t3f3DY9NzS0g8PDy8Q8MZixicwpKK2sb27p6B0cnZ1cQuLp7+vgFBIeGE1My84rKybRnYGR8+RmBo4ubh7evfxA2Jj4pLRt3dWQ6NP+MREjs6Ozq4YUNITK7xtbO3rFVBtTBydXdy4cYGZOYlp1fWlnf0tG39ACEYxt7JxdiIDY+JSOvqKymsW366fEeYz360tYOTE5uXn5BYXGp2YXlDR0D4w9wR3ixWM0mUi4+ITEpGbmFpRLa0LH1eHv3SCYvFjNTR89ApQyvSSjd2/p/+7iOMYlfCEYwgF6nkksolR7u7Wz9W1zfwOjN4te3949PvY5qqUoOILn59fvP32kSQBqD2c7R5YuT07Pzi8ur6+8/bn529I1skAAgnZFxzDeAybfS6ibMJmWi0VPGMQA1gFIuPdzf29neYgYAaVl7KkqVcpnkYG8Xg0TAkrVHqQJkksN9Djh/ggJADiA9PNgX9iGE/RQAAA=='},
            {'name': 'Meat pie','base64_icon':'UklGRp4BAABXRUJQVlA4TJIBAAAvHgAFEM/BuG0bSRNlZvZ4bgnbf3P7Xlh1MIwkKQrsgF8ORqD5p/YPxTSSJCE3c18oHI78oyIXduc/Rhmj8D1e967ru+Wvc7s0WNNRTUSNQKsvEKgBUSEQAQFZgAZEAFhVASACzLYKEM2u7/poOEpLQyujdPiHllZGxNLQ0pE//Esj1v/+nvMBiI0kKZK6npnxGP4HGmbm+M5/0xZNiOj/BFBb1FO/AHJOKZcVAHQAADMzPRe1lMtqDbQBi1a5XtTyaosmMLOIMPNJ5MRVTWWPVlU5iZxEhJlZLK+ACkKN1FZEmJk1b44ggqtIZ2axsgORd4GlX03lAPLO92V5vQFF/x/6USub7Q4Sg/vnHtRsvd2BoBy9++uklsp2ByKCcPDOOedrQ4zMaqlsdqAqFjF4H0IIMUZmUVXLZXMJqlvORjEys4iomqWUcrm5OmsgLKbDwWBgZinlnEsp5e76AtSM+WRUHQ5+v78+3l4e72+uLtsQZpPJZFzz+f769HALgFoDk/FoOPj9+fp4e34EqDtaU1s='},
            {'name': 'Lobster','base64_icon':'UklGRpQBAABXRUJQVlA4TIgBAAAvHQAHEJfBqI0kR1vVu3s5fY8/0yHBqG0kydlRuebafS+oVdRIUlR78sUB/r0hYv7Vpm3AjE79ow3aiN93LfMYa/z/N99mSaFYAtpAQBHCItBAAIpUCNUzACUCMNQBKQaQCUGc84HDSJJV5eZ93O3z5dk33Mk/O31kENH/CZCgvEpwJovpeEgwYW6yJCbcQDV1VUAora6X8+l4IFC5bfEqQVHb8x0JTazOdyQ0a1NGyM+8Q5lqf/0JFIgIqbL1AfkeekM1mwGLzKnmB+gOxrNlmmvdSTPXNMev6PRH08U6K+pGjbLcNqfTN/SGk3mcaledrsvFm8cXKKXi1PgoimDpcm3bJ+DTPE6Nr5pThJDXe23VKx/WmS3qanNDBL+/PBhOl+v0k3ZFvasOiAj55cFotkzS/FNR1lBvESEH+vNVmmnzqawRCkTIEWEaZ7m27oOAiCCCRoQ4zrVxvvj0JSKC1sa6oqwCvOKtK5RSKpQufNls90hgvK+a4+0PRXO6P/+wOQMSHJBvAQ=='},
            {'name': 'Bass','base64_icon':'UklGRjACAABXRUJQVlA4TCMCAAAvHcAFEKfjIJIkRWq4Bwus4/07eDU83Q8mHDeSpEgFCyacief9vTFLjiNJcpSqbqQTuMAf5/FJw56a/zZAgHzW5vK+6NABoEMAhg5lgSGgAENBBgxlBRDQASCgAENYFAAEFAAEBIBZQQD+CMgHBfnM8sHudeWG753lrOUsNlSpYkoRG6oU+SyfpYgJVooYqWKklCJGjFQxUsSICUZMMFL0B3Ys3rNLLqnsoMsOuaSQSwq57FiyI9W2Z3LQdX3cjSaj2Vuzmx5Gs9HkpWE0jIaXhtHfW18vDavnjQGWJNmmrdXX9rNt27Zt25z/z8G+Q+gV0f8JEEOIS4g55uCEYRphygX6IWbjMw7oHTDDyMQshLB09+dhaGyGgiUIunrM0Dc8PkMuEezs7ocYgt2Do9NYItHR1WOEpsYGkk3NLa1t7Z3dBmB9XW2NvdY3Nhmgtqa6qrKi3KVWu0FVZUV5WWnJyvJSqW1hdn4StEN5WWlJcVHhiqrSmkvFd9eXZkEhMT1TVFiQy2YsBaqajkduL0/2t9cWIcT8wuJyOpVc0dUV1QwTkTAchcTSv65tbEZj8USSKY1HQhCX2Fj739zeCYUZicbiynAQ4mpza2d3b9/vsUYYCnwa7O7tHxwe/3m8HvUHgvyCuMXx/uHR8enZt+dX9c/r+4a4Oz8+OT2/uPz45Jd+6w/E4PqK5PXN65u+69v7hwlBPtzz7uX58QkkJY9wlDwCAA=='},
            {'name': 'Plain pizza','base64_icon':'UklGRooBAABXRUJQVlA4TH4BAAAvHYAFEKfBqG0jwdEdZ567VA7XMWrbSNCu0++hOf4oDtAxbNs2Uqn0vi1u7Fv2gPmPc5Zz/N7XfR617dKorbHbgiWjaGGIbYCFVEQ3SgXEGEEQUoEBCWIEMgZAQMwNKO7y/s///eAwkmSl4nB357sLzuUf3HvHgxAi+s/AbdtGUoLum3mFRAWR0g7h2FRFlkToOdaODlxOBxaIGPiubW514HY9Hw91xcCQhy7swOt+403NiUMfEQ0NQMDjjtyFiVzbMjQVaP7eiFuwRdYl2f3ojEj0HNvUecDY/3fge45l6pypb3EjkOhYhg6Mof1/P691V3wBxjx27e/7FiSutUwDYBr77v/70AsKcW2LLAx9+xdeKs84vuvInHkcOhRaZGkShb6nkA/NpwhPQl3mWRJHgQHSiqEnFyTRVKSxBf+XQS74eiCeDqRxhcUBbdvyCz7v1zOpP3+rsuBNfFxPhypPwh1lCffb7XY+1kUa+Q5I0o7O6dSUWbyq+F2dzTUJ'},
            {'name': 'Swordfish','base64_icon':'UklGRmIBAABXRUJQVlA4TFYBAAAvHsAGEH/BKJIkRdu0sc+Tcf5l3YsZdDCKJEnRxjStpfXv5uDLxCiSJEXD4Gn9e9k37+H8R2mgNNiPosa5p9hEBhQCIQSKxWb9QRdlKdJYimCiEBVATDX+SFSJARipRIFikpAMwQhhGxSRTbPxWv3f770uz7m81+3/Xsc7DFPzf597G77rYoBY27bSiJvxwSHu7tJ/e/Yff6WB8yP6z8htG0d2ONtO9RORVUV+1RA/g55n+md56Z1v8nK5JXpus3SvP9+Pfn601MT5P34U/qBR0iKHDEJZx1+yZUVZ1XTCiVAXvzLlZajanSP7wH2yWFbKipojjpGt3TkxOm52+0CnXRgb1XTCPQjY7jh06lTgMg1h1jkpAp4uHTq9y00vmcBjHDei9WrhXKaPOt+hlnM5r8yMPdBsogjn1ny+I8PEfjsL1+1PsIFz2wguY94IjXjjH4UvfAE='},
            {'name': 'Potato with butter','base64_icon':'UklGRgoBAABXRUJQVlA4TP4AAAAvFQAEEEehNJKkOEzN7PJIHA7FbdvG0SCSe67QdxW2bdtisbvzH6Myyv9Zi0zmSCfNp3RgkqBENHHRKDHKvZNOdhRBI7x3Sc5dIDMAMNhJaAAg9EADB5EkKdL1PQ8/M6N/iUtvIaL/Cty2UZJjhl90LQF0fwUwGAz/NQDb/WG/26xXe6ARp9MZHU+z7KhHFWdE58v1wkxEs+kQRWTm+0P1fhMRTmGCHEVeln0+VYV5NkaO+vbSl2kujJGifSM8Itw/ZrmQUPvFvDAX3EwlIRHzRWFRMC3xmC8LF4vwhAg6cGJRMg+3GsuVBqrFU8O81eyG+p09Uks1rfVVaFnFDg=='},
            {'name': 'Apple pie','base64_icon':'UklGRp4BAABXRUJQVlA4TJIBAAAvHgAFEM/BuG0bSRNlZvZ4bgnbf3P7Xlh1MIwkKQrsgF8ORqD5p/YPxTSSJCE3c18oHI78oyIXduc/Rhmj8D1e967ru+Wvc7s0WNNRTUSNQKsvEKgBUSEQAQFZgAZEAFhVASACzLYKEM2u7/poOEpLQyujdPiHllZGxNLQ0pE//Esj1v/+nvMBiI0kKZK6npnxGP4HGmbm+M5/0xZNiOj/BFBb1FO/AHJOKZcVAHQAADMzPRe1lMtqDbQBi1a5XtTyaosmMLOIMPNJ5MRVTWWPVlU5iZxEhJlZLK+ACkKN1FZEmJk1b44ggqtIZ2axsgORd4GlX03lAPLO92V5vQFF/x/6USub7Q4Sg/vnHtRsvd2BoBy9++uklsp2ByKCcPDOOedrQ4zMaqlsdqAqFjF4H0IIMUZmUVXLZXMJqlvORjEys4iomqWUcrm5OmsgLKbDwWBgZinlnEsp5e76AtSM+WRUHQ5+v78+3l4e72+uLtsQZpPJZFzz+f769HALgFoDk/FoOPj9+fp4e34EqDtaU1s='},
            {'name': 'Chocolate cake','base64_icon':'UklGRnIBAABXRUJQVlA4TGYBAAAvHcAFEE+hKJLUCBZyvqIi/u1x6lDctm0koM7x7yrdfzG7gIK2bRh3hz/iafMfBETe+wSwKPQwoZsN0hig2BC9VEjBhQgpIKSAmhy4EPGgQ5r+VE6aDmkqlElT4b8GIUIOBodtJCnSLdwfPDMz5x/h787MfQjdEf1X5LZt4yh10nnqJwoRzo6iM9z1dufjOWTboCo7j7oLr5ATGLZoKpaBGnfmRRbG8aqEwp14FoXgoWACKY84kQZdu3CAjWFQssnWoT0zUFcoa5HlCve2Ma0KWR/aGNaUnknfzc4gC9Kq4POw3mxf2HG5F4/lgc9hU3kGMb3eLEXsjyc5PcJzGH0ZfBbWS8XhNBknHwF1LOX08g2SCwBzzCbjEYBB3YuV1GL1fu24P6QKScAgn0YV4Qq42Q8hiGPydEJkYi57QwktYZiL1SnJtDDo1+xRJuD0GifMKeUKKPQMKVzJAADyDIT/9yH++ykA'},
            {'name': "Tangled toad's legs",'base64_icon':'UklGRn4BAABXRUJQVlA4THEBAAAvHMAFED+hqG0k59oWJAfv+D8uwcGwbdtI6t/ueIPdrpEBhW3bNky6v+3/WPMfAwbx8jUUFEtCPg4EBFVAwIGAM9lU46/MYVAIBsVA0MOAKIjyhYAHBUJB8b7N4EC27TTJbyEe3KWCZf9blAbYwfsR/VfYtm0TK+nevUJ8E4l/RHP6x5Vsf4QAwCiCoKlqPg59x1aPb3JZRss5TT3nIhzgQyFnlaSJ99xFZLN+sYrjkwCrqPRn6fCwHAH0AwmapvfsVrbJ4qyJXT88Kp1GXZ6ulRFGy1nH/fik0rULq3sEoOQ8whkl793wfFN248OZLwkDFQEEZ273/vH6kCDrFufTEQnrst+vC3+7d7lI0vrT8cB7ZmuYmQ/H03KBOZA7E3JuB1jsgJJF0MxcdKT9bgs4C7PdAQXB2Y4ECjYAjHUJYLc/JM4XEpiwLrQBgEQ2JlGjooITQaBG1VL4+tOolh7yiJ8oWm4k8ANl71P/z+8Fag4A'},
            {'name': 'Chocolate bomb','base64_icon':'UklGRuwBAABXRUJQVlA4TOABAAAvGoAFEC/CNgDaNgKUNmXK7zkyU2aD3mDctpGjwdq3wHWQ+7767p3fnuAgkiRFymN0c0bP4qmAh575jzLKms9eaqRycU+77h2SZoudZgfo9ADYElsEYksEaAktEKEFtgTQWiJXuwgQkBAIkBAQve98JLATx06c5Tiw/1jYsbD4r9vxH97jtPzH+Wf/SpapSMZUcf5MlqlIhuMvWcYiEVPF8ZMsyTBAsG1bTfNf0bgHd0sC1PE6dP5z6v98OoT7IvrPwG3bRpXV3Zu/EDpIgCTiFgSgQqhJAOg1DQu1kmnZKtpQ4Dm2ubYd1/M5ck3SOS09v+5OsheE0erRKNO1s8nLxjDtkuTru1jeaVzMqnXDKtlvn5fzT4k/spyuLOoGTMvhU+ndqP1eznnBS1K0bHbYhcclPtqWUasWyLAiAVI+RsDsHva7ve/alrHMsxz3JEj5GHHE7m67QRT4rmNlCy7WDwTZS5i7ADrtKEHg2dl8ka9IUBSnzH1mHkgShL69mCOT02kDGDAPVRKOAmc+w0KWVnMwZB5d0UuT0JkyqxfCCGOJUvq9NHQ6bVa/9RONdQwH3O91Jprfqs1o2O915Zwm2qrfnZHAPzLCn3MSuJ0RMBx0FiRwM7LHg3b2DwFS0Qk='},
            {'name': 'Potato with cheese','base64_icon':'UklGRk4BAABXRUJQVlA4TEIBAAAvFQAEEK/BoJEkRXvs9ESfimeYmV0dbBtJUjR3z8l+zO+/fzQgtpEkOemXaPDwyD8r0tBQ8x8GDOEamwgimJC/54jqQT2oO2XrZSwMje3bhYlwAowPCRciXJ8wYbgg+dvLDSbv//pAFS4+YBOAsjHAPx4AEiIuRES+BnmY72o8jDspG+0gbxggRpKtWrnn23PBnacXrl80/+CexLAnov8TIDZpW+ymAf17j4/pk/bQ28vzF3D/+PT8RFsUX79/20t7xw/WbVHwP3XC58vVrbEuEhYU/V/KnFen842xzgcmAfLuP83QcVkcEm0sXCBBDo9plneLY6I0GwSCBZok65blMZ0Va/YEo6+TbrNI5cxqRSXjFmejnJUmQUbJPcwbXssRGwDWQKzkGgCJWREEAOJxBZDATBDrJMeOAUjMTGIn7RXr'},
            {'name': 'Meat pizza','base64_icon':'UklGRsQBAABXRUJQVlA4TLgBAAAvHUAFEN/BpJEkQbfVCw8+ev8CHr5Upo0kObqrGfrY5x+bg5+AI7dtJKmo9N5znIfPhweY/zhjOcNn/Xivr7vcymabStlUtpugySjUMITNAA0pEZqRlIAwRhAIKYEBCcIIZAyAgDAzIDEXGNmGDPp//u/vuxdIjG1bdZt3HPhMYmbpfzEnfuf0X9kHuYSI/k+AqUZT84MgR4MeqTgKAHyCJTkZkVJGhr4LNMJ6teB0TElkmkSB5wCoQb5ZL+ezyViSbbckku7fP6jAId9uVLbWWpXDwHP/VoBU2UqqoFUc+p7zF8bgfqlpqiQKfc8pPa4nfiApjaPAdx2UzqpmlbUSycB3YfC8nU+HfS5ZknVl33OB5/1yPh6KXJXWShIlhYEPg+/79XI6qtJaa9XvsRSFXzAGj9v1LIkkVRr0SCqJf8MYg+f9dqlQ9bDf67Sz1IMp4/W4lpTvJJIc9LqdVgBT9f/9vF9Ox0ORb6X5dDzs9zrRrxqD73+vx+183Be7zWoxm4wGvcSFqQfez/v1fNwX2/VyPhn1Mh+mMYDL6VDkm9ViNuymIczHwD7frZfTQScJnB8wBk1NLQ=='},
            {'name': 'Monkfish','base64_icon':'UklGRvYBAABXRUJQVlA4TOoBAAAvHwAFEIfCtpEkRUOPJmX+kb6/u2kwbiTJyez04u2XoEmUGHYRI0mSlLSsATfnxfzYdf4DAoiPs3jvHabZMhoqygwZDB1oCJSPIFSRFPDofiw0TOAkY0ozIpuTbJPNSaNVCQhFMLYIOiWCQSwYSwQNRTA2CwQZkk2QsH+JnAGh+2nRREghNAlhkEy0eAxk2r5IIescKWSfKudQu47e9y5KgP/VAvSvBNWfqlfVp/5X1ccAsbZt01XuZ+zkIbZtO09R/+U8jtfBPhH9Z+C2bSPFArpvvsLjqhg8Ln0RXPqOuYHhTXDl8xN1ajGHesJGZq43vegZCQAfmG7BRkl71iqlQvYuq/SKeANB4INogFnkeC7dapgbpJkSpaCuFZHnuh1zg7IPUwK6NghiuW9Eb1BJerz1eInZv69mvd/rdkwDeH6Af2KAXbPYbg4H/R4V87lveuAJRILe3x8GC/PV9dKsV8tF5CWNHsDzgdcn6rU02Hyx2l4vZz35nKKZGqQQ3lHvLzNYrtab7WhyLOpIitFIptIcpMf7zwpoMxrv8zlISCXjDGmOBxD3fTGd1Xo1ny42u/WMS6eSibBxL7wgCkj4zRO3xQzz9XZpGLe8DDEj8qkQM29ezBe0Oh24VJLZ/S06Meb8Tzn+aB4A'},
            {'name': 'Anchovy pizza','base64_icon':'UklGRsYBAABXRUJQVlA4TLoBAAAvHUAFEN/Bpo0kSdvuCS/8D+FxP0Js2kiStOPu9C79+RM6DMeDcRtJiraqlw6eHOlFf9L8x1rFWtyP3fsetm3RVFO1aKoW06qgqmjQihBMAqhQI0FHokZAEFEQINQIBFBBEAIVAYCAICMgMgUITYUC//+698/3/SAxtm3Vbd5x4DOJmaX/xZz4vNN/ZR/kEiL6PwGmGk3ND4IcDXqk4igA8AmW5GREShkZ+i7QCOvVgtMxJZFpEgWeA6AG+Wa9nM8mY0m23ZJIun//oAKHfLtR2VprVQ4Dz/1bAVJlK6mCVnHoe85fGIP7paapkij0Paf0uJ74gaQ0jgLfdVA6q5pV1kokA9+FwfN2Ph32uWRJ1pV9zwWe98v5eChyVVorSZQUBj4Mvu/Xy+moSmutVb/HUhR+wRg8btezJJJUadAjqST+DWMMnvfbpULVw36v085SD6aM1+NaUr6TSHLQ63ZaAUzV//fzfjkdD0W+lebT8bDf60S/agy+/70et/NxX+w2q8VsMhr0EhemHng/79fzcV9s18v5ZNTLfJjGAC6nQ5FvVovZsJuGMB8D+3y3Xk4HnSRwfsAYNDW1'},
            {'name': 'Cooked karambwan','base64_icon':'UklGRmABAABXRUJQVlA4TFQBAAAvHgAHEN/BOpKkKmzzRmPwy/yjJAhGbSQ5Dm57c8Bwr2PQSJLi2HU9gwWa/yxlKMX//73vpvJ9jwoAdQJQATeBKwIAIIGgtYkQEBBIAJIASAKQBFLrBGqdgGStXQQOI8k2rZ1v27Zt5B/Zv/oZRPR/AuSP/kucIFjooJDksbQCLWyNQNcJploYce9hqNgAF3Fu8lMyQT6XxUVsy0gUDBSKBZDbZ5GDShQJyuUS8uU9HvXbiShUqrUK8ue+nI5rqVit3gBZcX4cZr1SpNlCdt7v1+u1W4za1f3udV2NWtkOcsXxcv4+9pNCIZPELlfY3V+rbn1ynE+G3VatlE8ncGA6Xz5O61E1gavsLFbzCYvN8dZG/rBezkA0YFvCi816BRI7xGfqxXYLksQCiWcXN44gIxMkcaniJGSl9yOWHnZOBYMYEmaLzDQIsrAJBZk4hGXwJyF/'},
            {'name': 'Curry','base64_icon':'UklGRv4BAABXRUJQVlA4TPIBAAAvHoAFEIfiuG0kRxpIs+a7MW3+yXhzVx2Hw7aNHGkx8l4D1+GVn3P6HwOO2kiSJEf+9sCw/EnO1vxHK7TStftSTIV/jUJFgSLMhZ+CgCggCggASBAQAAIAEAJg/kMg9CYn6ZV//yhTJj5lyidJ+cSUiU8l8alkmx9Jvve04yf5lzz//FvaFxUZCRqJjARGAiOBGAOByPQ6RiAwvY4RA8TatpU4vHF3n7jhEnd3T//lwANSwr0R/Vfgto1yGR7TK4wUkoORh+DbsS1zbxfYA3CeVyFPvtaNdZJ7FsnTrAoJA0/rJhCro7kQrVEYuFq3drbXVhYzz4UDvIrSgyj0HHNluZjPphPN3IEN70ZifTyIAjceO1aMEsjZYtX1X8WQh+ZBOFIMAQwUQ4wmcy8IHwR3zYPUZvpkT9EnMBzPwo9DwX3zQM/XRSdFl2R/MIo+jgQvV101tk22NG0CXcTBx7EguFXzNQDUNY2kgp1u86MkCF5O6kCNZFVTI9BAi69v72KI7709XJ1VSJY1VBVPn34QiQGxSX49X58XC4oik4pfx/XC/aSYKX4+nu8uzy7vnv8s0nZcPzoQA5DdhL1sTIu2G0jqK9gbXM9kNxE766cJuJnBBmMxIXm/1NlN15qWrUflBqk57AMd/SewSFt09M8gvwY='},
            {'name': 'Ugthanki kebab','base64_icon':'UklGRoYBAABXRUJQVlA4THkBAAAvGoAFEC+hoG0baVra43fMD8WR2INDQRtJ0dwL+MK/CWSwlzBqI8mRNy+P40/uXrk1/xEQlPdspjMYBAYl0AkE715UqFBBooLscg5ERVREQVRklcHp5r/TTPSwP1rRE6NoRSnm/1oYJNa23bSSLrYlEYXJf0yG6b9IxxLujej/BJhPQdL8GNbJ8zdwPpYTfgBaH5MXJ/Ab2Gvk5URJJz4B6XWJnLy9ORU8wFdg3WX+dpG8EnspSHu94Al1W9C7K/MQe92ueRG7W5hAGnQF6W8MpBJnlcWpu+Xh3sxgHwrawJK03skqiZ0N93aEwRBYlEFyPk7pnU3iUN67Gob4G1gqME6eY2fvUjW0MCR6stPwLyFjkt6VUt82L7q2a9VQXT/QSy6wrUHzpEZk/RDZPNfUCPMSNZuaGklKEjnNMG8eqqlxmkWOEyXQvMf4EKd5kWYtWmE+xshpXtZNEneYLzHNy7rtJEHzNZZ1249TML/Eth/nf5jf4tl8DQA='},
            {'name': 'Dragonfruit pie','base64_icon':'UklGRvQCAABXRUJQVlA4TOcCAAAvIMAGEAfkKpJsV5mdfY/wD/7N4AMXGV404bi2bRninKsbW+YCkJG8q0uiZnqW20iSJKW69pPuwAX8V3EFM9DfYee/DhSgyPN0NfTLUItuGiIqUKkRkZVQBFVERFUkFCgiDRSGAmUChKFCYAxdB0JIYKAkMBQgiOt1SKXv/2V6tvks/+Xnf5TpLPO9cW/TWaZ7m48y3X/TXqaz/PYy7eUyPp2HCREhikgkQARFKIIiUIKAEBERIEVQQEQIwH1uDvXUNEVRtSnNWA2ippEQSaMSiUqjkhCJgkQikcoyRDvQNN/f3eco/wfv8+d/b7f94fG6MUi0re14o7yjqPiCH7Vt24jz/fV4OkZtvKNrT74/uIPni+g/A7eNFGV4eQ8+4VGFPOUKMZVPLaGc4eQhmCEmAZTeyzQybgQrw6woFae2QQwMT1jhqgoFYip6TzJ6+jsaolaFV40hWExRKhzaOhl1dtAnlPnhUP34TH0OAlwdnd1hQ+sKP2IbTHW1emxoZp4ABkgxiN4a2zIfA95kItbFTY0dTdNztvGb4XJCazZMRB2ZzaTbBVeF2QwHn0fcJoVlMKIMU2oHEaHtiKGD3oBBUMxRJCSFNuU/qa0moc1ote8pQSloZyuPNKJjU7P/5B+GGdGa8fzZomr7eRh/O4aGJxee+KpZam0xEHgulHp3L4dkNFqDemRq3hvOuiSd2FxWgZPNQHQ293YOjdZ6s25S8fWVJfJge/dgOwOgo7uvq71FvBAuMqnYquKyWzt7B5LRwYi0GtU+t6VTGyvqqhmZS15ya2NDfZ0hVGQ2nYytLbleD+T27j5QU9fUaIeVzMmkErF1NQKgu6vt3bwwhN7ddvLDEpu5OQW4vz4/2cYW4CC/tk7o+Oba2//kcfNwe3V2CiClkzoew6bW+vD9a/IABcLN5bkiZ6cnR79+fPvy6cObV0U+dVxfAhc5w/HRz+9fPx++K/5fEa4UTo7z8WNpvx0VkiIZAAA='},
            {'name': 'Mushroom potato','base64_icon':'UklGRoIBAABXRUJQVlA4THYBAAAvFUAEEDfCuG0bSWPN+drtH1veNnHbbTCOJKkNDJ4UiFqZ6odfGLdtI0nK/u4tYfsvcF+ZeP6jGBRT93bZ6m8Vtage1KIAOIBwAAFwEALgABIAgBqvWTY9FgBICFC9sBICCAGql6yqVw+F/3TPxQor3jWssMKK7wwrvj2u0a7eTrMTEvpmi8KK3BHFvxffyB1W+I7j+1jICwt5YcEAMZJt09bZz8d637bxbCP/mC5T2Dui/4rctm2k7GP7C5YXEJGVC3fnp5XyA9w/v748Pd7dABbm7BHx4fb6Yr5YQkFOJ+dXdHlxtliuAPNZH4/Gk+nst7Na83oVstlo9gf90WT6/t9TgjdrkCZxO6Qkxp/fHSLizQYw4NIcD84TbXcfX/jXlTxJUnrvfEjdvH38GK1kgrFbTyFiQKTt3qLRlEABEWPG4Mnmikqv7dSI5KyWggNDcD6eZMTgndGSt1KsC9mSQUlAhgjG+ZDNlOxD51ouqeinoMhcIg=='},
            {'name': 'Shark','base64_icon':'UklGRmoCAABXRUJQVlA4TF0CAAAvHEAHEJ/CKGDbOLHcXb/yJzRUdmkwiGQrCNwBagDt38Va//1xEMBt3PQk9y9/SgXVTZr/mLGYwf09pm2/p+/Zrb3SibWEHmJ4Y9YnFc89plZmsOBlVqyAeUHCGEuuPRDGEAgwBBoAAIJAAQGgCADAAAimSIAAACACEkwBoGgCwRQBgBAv+/9XEu04qaaaSKqJdiV/TTXRiqSSaFU6Uj8nZZAg27aqRvfE3T14w3fnCxp3l/mPJu//ZgjnRfR/AkQJUmaPr58tkDP7/P7dWFnG31l8fP1snZDH5DaUVfD6/vld+3uuPFidQ5WXt26nrWxpdhrH2wuVni2TNHpdGqZls3O+t1TJ91zHpuv5QRiFjtE+Wq+A2HMd27K1FyZZ0Q/s3vnuIsoi17Et/UYySHKd+Fb3cK2KY1umguQgiz2ztlOCfmJbJt+UUTooGLnGwSpKUss0VF7YL4Z5Ejq17ZI0Mw2alu24nh8k+ahI48DeVyDXmdH7ox0ScTZk3o/82joUg7RH0iBpQpDq8SBLQm9PMRilvQ7Jf1p3IUQxHhVp5NYhxHA0SY1Oq6lbWkNIYjQZppHT3oVgNJnOG+1Wo16rQ5SYDtPIbp9CMLm4is12s1E7Pyu7Hqah3TrZAaeXw8hsNeu1M0jJzW0aWs2TZfDiMg2sVqN+Dim7vUtDs7m1Al6OE99sNmqQUtzd64fQ/PzdBKdF7BrNOqTCg34kXz9+NsBRHjndBqTKI5+Il/fvrdk8PWsI3r5+IcgjB5SKeH7RFOL140cBqYyXVwpJvH9DCMp/vEGU+ILMEFIKAQA='},
            {'name': 'Sea turtle','base64_icon':'UklGRqgBAABXRUJQVlA4TJsBAAAvHoAFEGeBqI2kXGYWKfiXxRMBd6CDcdu2gdrQ7Y1y+090e1zyYNM2kqBkZo7H8a+O338x/1ELtbzfaz0R4z0iVDmhUZlQmaKkUqCsQCBUlKiSEFTd/RAkABIQYASC8/3+4M1nBq8xjTd4jf6hgFjbttKIF8Fd44om039/w/+fUMKTiP4zcNu2kQW1t6dfYS0CCms9sFEQrXa7t5kdZqB17va26wcasMa97YgXRBrhj41gEdgO+kGU6AgjLPkFcly1lGbMIiJx6MOSBLYXSEJpjhkiYkHzJtMPfm1PLWV5YcAUg+HfNOzdQLPUqIgkTcyMXb/3ta2VRj0nxwz0Xwf9ufVCZVkrGpGKiYrL9XbvR6DrBSNtuZZGITLbnlXUIMysLTeIByJCrIC69kxEZj2ikv896MxqD/OjQbNHDVlTBPgg4uGkOU4ICxgXHjps5XE6Hsah73riSYSZkEALdufL7foC+k7tGaWVTi54PbfGIHh/PF9gEYx9e7vzlR/Pt9zA3IyIbHy+9np/EdGbEZa7v/CINyOrq/7jigQA'},
            {'name': 'Pineapple pizza','base64_icon':'UklGRsQBAABXRUJQVlA4TLgBAAAvHUAFEN/BpJEkQbfVCw8+eq+v+A25aSRJkmYi213750/ooBwBR27bSFJR6b3nOA+fDw8w/3HWcpbP+fF+X/e41WYnDbVp2NkEk4yiCUNsA0xIRbSjVECMEQQhFRiQIEYgYwAExOyAYi8wshMy6P/zr+X7/UFibNuq27zjwGcSM0v/iznxO6f/yj7IJUT0fwJMNZqaHwQ5GvRIxVEA4BMsycmIlDIy9F2gEdarBadjSiLTJAo8B0AN8s16OZ9NxpJsuyWRdP/+QQUO+XajsrXWqhwGnvu3AqTKVlIFreLQ95y/MAb3S01TJVHoe07pcT3xA0lpHAW+66B0VjWrrJVIBr4Lg+ftfDrsc8mSrCv7ngs875fz8VDkqrRWkigpDHwYfN+vl9NRldZaq36PpSj8gjF43K5nSSSp0qBHUkn8G8YYPO+3S4Wqh/1ep52lHkwZr8e1pHwnkeSg1+20Apiq/+/n/XI6Hop8K82n42G/14l+1Rh8/3s9bufjvthtVovZZDToJS5MPfB+3q/n477YrpfzyaiX+TCNAVxOhyLfrBazYTcNYT4G9vluvZwOOkng/IAxaGpqAQ=='},
            {'name': 'Summer pie','base64_icon':'UklGRsgBAABXRUJQVlA4TLsBAAAvHMAEEP/BuG0bSQN5jv1vEfvd/hu7ozoYNJIk5dheXgHIIPgXhYANvccokiRF3bXH+D0D51/gQs9/tCFt+PG89nu1XVj7jFV6FkkkpQNSOgD0FEASIMGCAAJAAsZmY8P1fcqww+7K0KEMHTTKsAfnScMO7d5qvuq+qsqov3mqet/qnD8NjXXMwKAgDIwFgGAECAMQSBYGiI0kKZJ2jm9g8ZiZmeHBf7dm98CEqoj+K3IbNcowQLdTeYXzKvFOzkcJKEoUgQJJ8dGapCKpScqCwHsbTdJ0O+0mG55RxfybRsC19Eh22i00Sddu5kTSvmvYI7dgtwO0ADSNKqRE7MAzqt/rbmOANoBW07NhEZXQN3I46McA6BBo0ne1LApHVKPA06Mht31rwBrNBi15S60c+q4aDtCHpUsA7ZZnySaWthg1APpAr5uUoSpkUnGJbDFqyAGQDKOpmEsnHtZr1bI98oxW1MYltaLM2zVeoxSFCOjTQ8Jvv+a/Vq2Ukxu+a5TEeiOcV37+gN/n/Xo57Q6T2XyxXL/9cfH44RO36/n4wurDOOBxx83W/Tjm85wJXC9xHU9nAs4X+mI6AQA='},
            {'name': 'Wild pie','base64_icon':'UklGRg4CAABXRUJQVlA4TAICAAAvGgAFEN/CIADaNgnQPQf1L2Wq+ogNx5EkOVFt1QIvDFD+G4JZnAiHbdsGEuXeTXC//1Y/zv/NfwQE7ffj22/9+MgZzmEXFc4LCxpCdACiCKq5IJoDF1RjaHA6YATxf9FUIQygB4qAUIVQHgdQCAL/XrleCGU2+P/SMgKPEcT3x9utgYvAjsBG4KZBOhtgBHAW0DTIsgGOwEZwnAvSwMCBQckxKHAw8j9ffP8MEmxrT9vIf5mZ2zAzaDSjesIpM5P2v5FY9pzZwfdF9F+B2zZK02OGV3hhJArvHwhiJzjYJQkg2gKLBGPMVqp52tiBICKQpNXGp9J+J5s42d2QUMgDMPShawWwoUziYGtN4IZKh+z5RqtGGaiRPNlamRFPqvmshun0QN+oWpkNQNnY7ozgrJK3wdF6wwF83ZgEpZG1sRPB3Vk1G4TB8GzQMcoJhjaWEbxc1/NBINkJ+jhMorjg4/m60nHwtWKDJACL3LHg6/Xp+qxqSK3cVsACyOyJJ59vz3fnA+f+Qearziq5423xIF/vL3dXZ8Pf9QrYYSi4V/048dPD9dX52ZAD3wmz0+LB8ffH2+vL090VznomCPOzU2Hx/vZy9PdP82rYMQ2sLi3MiQfXgcbd03armDra34wW5B43F/3TX81iOnm4s768OC9elG8vgmLpJ3UY+nv/9yMB'},
            {'name': 'Manta ray','base64_icon':'UklGRroBAABXRUJQVlA4TK0BAAAvGwAHEEehKrZtytmbJBIIrtzrlxqK27aNAssZqr+O2+HuYwC2kSQ5+Zl77f4jAiB9ksPDm/8okZTgqI+a0qFaWloxJBMJtECCIA0ISAIQgigAgAICqKUCkADvdff/eEtzEWntTy/T77fZXgYIsm01YXg2UOmI6b3uf4uxZQfvR/R/AtSloLoen++4Cvz6eG1xCpt+Bkl1FH+tOPG0UJugIv7G4OnIwMi5ARWJ7zew1KXkFANJkURvu7aBIn7eobDeSF1SFEmSJfp56NlBEb9UxN393W0mWZiTeDsZLQNIKpLgIwu5sGSm6K3RQ9+1zQbx9FBFZCnMKYodjR76bod4XkXqwpJT8G40Wvp2j3i5vVmrLCXQ23kyeujaPeL2ZpW65EBnp/ECriUF0s0yGt2f4M2Sw9Y0Gt13LXaIu3VJgd5ZkXlj2MNDLSnQ04q4P2Y68nSXgyfpRMTOo7gwHritG06EYl2I2ZkdvNxmO09iPQMZc6nJHritk9FiRmyW9S7PR0QPPUi1Cd4WP26huqED1VFUZzaQrQbVSWRu2ZbqPKhIYtZUl2Om+keoqwEA'},
            {'name': 'Tuna potato','base64_icon':'UklGRoYBAABXRUJQVlA4THoBAAAvFQAFEPfBKpJkJ29nlxw+kYJt3KAlgw1GkSRJ2alq7heakIosTCAAJhhEkuRkdp6crGAAqQjExHPzH2WgjFyv0u6rakImZIKDTEjgaWThIIGD6z0d4yHDNCAZ1TQSAcKYz4sdJI0UFaBCQAhBgISokLKiJEOl2CzbqzuiWQRCYCQAIRJt92d/bm+X//+93X1f+bp7u/u+YoAY27bq5N3I87i7B4e4Q/995REo4ZyI/k+AelzUv8oNfxDgP+SHEIDfj8n1clhdb+SPpFOnY6VaP51R7qVFAVKp1uqNZrtS7k+T3URvNFsuWkBt8Exy3GklXp+W82kLTQ6XeY2cQAGCTP4dreZkORsZUjMrCsK8PpQ+pm8vy/lh5SwNcwJNms8vH0nutxsHS4oSY7n2iMndxjvAiBLtNj7wrhDDBrBGFIQukJEskJGBsFoUICYwFu6LjME7k09Y/wvvrBGVcD4kIu9EJcX5EAtkZCAh6lcBWWBkoIeoR+VBlQY='},
            {'name': 'Dark crab','base64_icon':'UklGRhICAABXRUJQVlA4TAUCAAAvHQAFEGfiOLLdtsEPyqpAR/V/VWvJBlAH4zaSpMxULzc/fuQfD/ks0LOM20iSMl3NDQmQf07kwXN3mWH+IyJE6HGv6Es4LBF6tS6bl8BYkUIW5jO0ScRC7ROxMRNJgmYAFiizYBkFp1BmIAkxg/ShqrRLjtJO7V+OVE5dJZ3KKcfv9732N8QfDN7/86+SVarK3Zu8ut+b9nMxTHbWjYgTApI4IUSC0ogoIYkSgyCwzou5TYhMbXY9D4ME27bVtnk3WDYK/pfZYinMzJz5T0hQD+G+iP5PgPw3SFkxqpc39yBXAP76o6p8TdZuH0C2A//87ZS15yenf69uH9AGnUF1SDp6fjLshC9JGwxJOqrq6qk373mDiOyiAQPHVVWP5JnPRdd/zDnq1IEcOB59U132zKJrogwepIrr+6fc8XxjAx2xyLvGgnfrkCp6afi8vUFjA/VHasYWFAy3Goo4vLh96vuBNb+D8eQVQtD90ZAubh7f8p+/7SDrmekjBNzSdW347KdhcvOc5WmiBUh2ho7rmV+o+cjC6OEtBcMoTv/tlI4fWDXqlBAIxtEy1wSCcBlq9G7VqKJ+D4LPNA4hRLwg5x+BVXN4vHl8tL/37UGIQZhDSESz+P1rHNg98mD326j6EBIflCpIjsajoGqrpmZUV8UosKbWqmqFkLZQoz5JVGWFqJdaAA=='},
            {'name': 'Anglerfish','base64_icon':'UklGRpICAABXRUJQVlA4TIUCAAAvH0AHEDfjNgDbtoEA0mXylP/zWv2gF8BvOGwkyVH2b2bPPJ4AiJu4CMR7bvbkIJIkRarpvWdGE6/8Hb0FZoae+Q8YYPFwSGsDRks3YHqaKypDGYg+/yE0JOowiqpoB/DVFDmAD+vPHb8O4klEZ0wN5dijyx3Duqy/XQ2WWRbVudvSakQRRQyixN4EkUsRRBCEkIKQQgRRlJB/x69/RclhjuSwyBwpYf+0A7yUg5QCuhZFbGVhPMaYivZCEE7CJAOhWVlbg55z9/dNRrrdVhx/Dnu+nu7Ph79srPZOp4+UF5aT43Ep4yfnoefrAfs16ytm98edZQYJtq0de/Pe37aN4Pdfu7GTunFSt/Ofw8fO4N6I/k+AscL8X7AN0j+wFOZ9ogwneMDPz7AmnDCFh09fYEgkKrDBdAbSDUFjqdJhNhdv4MYRFdGQ4Hwhv8oi+R0LGxrQC8ulnb2DfXak+eymjw3CFRYPO9u7T588fqTt9nx2s8FNgnSzfPRsW3qwjMRqy0dvNjY54XI+g4uXr153VCKjknqbJCfj+bTg5vjsblKR9CMeU2+Dm5PxSIW84PT17nJ0spZM1Gu9oro26wPC2MIQayuZVVU7W+r2iqSkvKQYLPhH/l0n11ZH5a56lsQ9U8oNYEji9x/w11gjrXOt0iuywHuQ6ezQ4fA5+G0saSRVWWA+BEOCdthttqRd68bLt1Um8gEYW9BYGrZtki/eTKpMEMY9anWRZFnS5miSSAY8RWuMxxxHyXvBuMf740g8FrVPVMMMeCHIYDRim5RChPERgaAUCd9LBI2PuLi+Deg4cBQmjK84vwIDZzoJwfiK03MY4gP5zq8zGBIfYWB8hrHC+AsA'},
            {'name': 'Basket of strawberries','base64_icon':'UklGRkACAABXRUJQVlA4TDQCAAAvGAAHEL/iuJEkRarO2v0y+a91EY7r3GAbSZKT+51Fe6RF/iY+Geg7HEeS5ChddRqND/hvAUbx08zMfyhCwXW72o9Ntx60HtiyZcNW4s3IsQEZYBkZGGHAwBLAEgAEMLAGCCCEAvUeJFuqpf6SLdWS5Zfl95dkS5ZUyVd+1b7Pz+P8SP0xP7T9qEFYAFtWgACgeblBAtEAQEIA0FTg0J0IiEIiAHRRnUQgiTj3J32Ritx/qvL/QhkGida2p22jv+MtnMhhkEFOaVy2LSgzt/d/LYbcwqeI/k8Aq0rFbGXCyBu5Ae/SCgQx5gQcjLwVSNoRJwb6Nx12qAptiTEnBtCP/QmvFs/7rRxoZz5sUxltq3GXWMHf/SmvU1k06zeLQP+PvConoy6xssMKFC+8ZoWdQ14hmfW+VTngjTI17VLF3TJCrMbt2uvz+8jrtmpfdvd54xMxUK3hq2Ht+ezy6W3Xnb2s7e73vtUaxOhnx1eDT+fXFw83l49312d77nuz3eWEP7Gvuh+ubi/vcf10d/O11uIyBjHQtq/Gg1678e3zx28tHjoXQS5zv32lkSFNBHwAgXNRnAP5ymiHLEXinAD8MIrXS6xxWiFDCkD4oVyWHcMap50CslQEkVxu5EDq9OQYFsY5nSV+EMXrJdnxiXMAYFSa+KGMN4kVJLbIapWKIJSbxIqEOXHHgIXOEhHITWKlpI5PAAujssSXm8QqZCZnnEqF3PxVBQQcW+d0JiQBbEUqZeU='},
            {'name': 'Saradomin brew','base64_icon':'UklGRsIBAABXRUJQVlA4TLYBAAAvFEAHELfiJpIkR+rT6r3nD+a9Z6S7ioajRpIcqdY7/oDue5C6ZzIdRJIkRTUPClCFDpQiBwv3dM1/JEjq839JxrCsISsZyRiysoxkJCNLe10fvxESgNt4gQRFIAEKwBQEAAQBABSIIDohQpjohAjQKRCgM/4jfi2e0/mt7V7j2satbNcYtzKuZVzLfbstx+HxeygSqVQKlUql+vUPhEoVgaGIKtHxB2GkiAJ1/nXGpz4MECPZNm3d/Wzbto1v///M/GM52OeHcHZE/xW5bdvQKXZ76isMKcBiKAPT8XAAal6ixQT+wTcfqwDjn41A4+3r0+sLTEfHPaA+3lm+N7sL7vXl6fHhZ3u84dhoTb/7612xsVxp/XcBbeDe1kTbMxgKz9xJycNsDjfFjtVNRJlyC9AWcTHRdLHZAYyN95FkoY51EHa6NJPI1bAOrC6ecCxbRjoIOQShaLqEdGBxalGqWGm0QeztTiHBSDIvd2B2yuI5qYOwTWIKxzK8q4IBJocUMzsodWBFJXnX6rKSWYKRBOvqPb5hI7LzWPlGsdEXn9JWbSNBptgGjf1fVjZzpqz8B2IMIRo='}
        ]   

    def init_potions (self):
        return [
            {'name': 'Attack potion','base64_icon':'UklGRjQCAABXRUJQVlA4TCcCAAAvFEAHEIfjOJIkR+muXnEIP/DfJfjz0mIWNxzHti0be99zv540RCNvaZib9d3DQRtJjtRdPXt3H4gc8ufxRJ5Dzj/zH0KEn/ar43ovCSr6bGINQZk1aySMtS6tB8pIoFEmrSXmYjZmQwJrrQsFyvo0WBFG2VofrfFXo9Vor8dHjVbjr77tdnm7nh/GcXXIzq62mhFCWkQsMUJANIElIkSvASNEBAQiBEa39BoQEBEACESAjWgQCAQghkE0CANEAMLCLZpELZ5EMbW4RRG1OaIWRRw7H07+/0bwuD/V7mD92vfzt0b7fX4upzMDdNu2jTd313HqNqjb2K5t27bf/+93c79X2Cei/xOg6oKkso2xSCwOe1/f8j8OW9/yMzxhBxT5HYmARujq/v75G406PTDqsXb6vS1mfewX6fA5Gs1CZDDQ7m5uMCI+P97e/a2gMusND4mvDcpGYFDE57D1Gh4Qv6sJRrh6Ibk8XTDC/vMLubc6W8rC5PqZ5P7GfCVvgIPHp2fyYGuxVsqi3tWT9XBnaaqSr4Oj+0fL0e7KTK2Yhu7iUXu8tzY3Wc5rcHT7IJaT/Y2F6VoxDcvZg/70YHtxbrKcgyIOru9JWg53lhemq8UMFE7u654d7a4uzk6Wc1C4vNPe8/x4b31pYbpaSEFBR16c7G+uLM5WklDEtdyI3Ipcnh7sLM+WElAkwcura7m55enh8kweVHqQV9c312dLU6Ayhl7pAQA='},
            {'name': 'Antipoison','base64_icon':'UklGRiACAABXRUJQVlA4TBMCAAAvFEAHEIcDOZIkRVJmxDJpsP/VewVkhkMlHLeN5Egt1fpNYn+Xf0IXgbe/PjiIJNlVeu+OHHzgCL2IQUJO81+HFKncnE7m+54ZWIbTUgksWFqUYkqIwbAwGAYUU0pgKZg2XlZG04IpJQbDKJSCZTiOFiEKJb73i8//56v/Pv1z/319+ufTf5/+Ob1fdpeb0flqMbFahtDCMACDhWmCwcIgGCi0CQRBAAREm1BQBMRCKQX5LwBASwsFAACFAltciCthKVmKC3EpjDi2Pq2Po8HYMAZjM8HzbDIv1UiFAZZtW4akuO1ytV1tlG2zbdvm/H8rMnIKNyL6PwHCECSFaSx7/QGY+/7Sbysw9aU/F1bNgF/6Y9ELKmFo+OvzfclndUBppH3Q7exRG+O41gMuS6faNDk10W/v7lAifv7/ft29oFAb9czT1QdhYnJWz7kspl49M9pt64ISrl/I17ViQgmHzy/kwUY5FYXKzTP5crhVzcQVcPT4TPJop55LRmF0/cRn8nivWUjHDXB8/9R+sr9eyiajkF0+asnBZqWQjktwfPcoPT3crpWyyTDaLh5kZ0e7jUo+HYMgjm4e5OfHe61aMZuIQODs3uDieH+9Uc6nYhC4uje8PDnYbFWLmUQYAgqnh9vr9XI6BEHcaq3vSF6dHe2tlVNBCJLg9Y2+1XfX58etUgwUcpA3+vbmolUghTLkQg4A'},
            {'name': 'Strength potion','base64_icon':'UklGRjQCAABXRUJQVlA4TCgCAAAvFEAHEJfjIJJkV9mdvSMaQRZqcYACJOR0HxsOIkl2ld3Z+wEQgiy04iQryOl+uY0k2VVm5+7/j0qEnImGUPCwlPnl/IcEKQ/bu/3mJmmgHkd2gEAWbCWSo2pQ1bAS2QGykZT1PFmNg0R2VDUbtkA9NAty2LDjv3maZbf0YXr3em6md9OH6d31NtPrbb8RKIGNBEmpgIoAgooCKPSgpAQQhAggINGDugBKAIAgCAIQxOGAIJZBIgAAgyDACABhNWkkFWkgNbtITW5SkZpUpGK18/Vj+vD7bZbl8PttLoe/0/5lpa/j7mEzjUxIYYBl23baRrccTplThjCnzMzMYU65nf+fFXkKVxH9nwDRFCSFacx7/V8wV6vzcwGm6mzMLJoB63yf9YJK6OuvNz7mfFYHlAaMvW5nh9oQh7XucVla1cbJsZFue3uLEvHz//fr7gSF2qBnmq4uCBOjk3rKZTFV9Uxot60NSnirkNxfjyvhulwhrw43kxGopMskr0+2l2IKuCmWyuTN2e5KMoJmbyXj7cXe2lKsCe7yRcPd5cHGSiIE2UtRen91tLWaiklwly1ow8P1yc76SiIEw1NB/nhzvru1mopCEDfpPEnD7cX+zvpyIgyBh3zTp7vLw93N1VQUAq85aZ7P91fHezvry/EgBGTky8P16cHu5lIAgkjrjNZZrV8fby72N5PfECTB17e0zmT5eLu/EQOFHORbOpN+2lsDhTLkQg4='},
            {'name': 'Guthix rest','base64_icon':'UklGRv4BAABXRUJQVlA4TPIBAAAvHsAGEBfCKJIkKWsG/x6wgBRey5HFYYJtI0lh6L9CWnDo9IFZBpEkOQH/6pCSMz3z/waHsQZjjbc9uf3O+0kq530VCtx+BSmISERFP1KQ4kZFeFSCEgRkACCGAAjSi4DwAx4Af4B4nPe1/6vlO6x3Nud2v59BggCwaRtVg2MMkykpMzP//1W13PQJUkT/Fbhto6TqMcMnGq7AVeMlAbWaVWlKLQUQvZKiC5JRssjSuuVDq3mp0W6zWswm4LhZXerQIosD7wqYstZB+OuvF/5dOhiqdeSFyZff8Q0QiqWgp+aEcqCf4RYjBRV5lnISR2FAHDHq+NUr7vCwKHDKdUwZUFd+/Ml2lhy3IAtyWij6/+3tR2gseBwmHMcJZcJ8f//8GQPZGjQ2YzhKKM1V+eXb79QZy6YCjhiXJWkmdPXrX+5eVsiBHzAjrHNpWqGAhkPge35AjOOHC121e9Bw8f6TbyO2ZQ9L0zyensTjEYKcskKocrM7gOMBksUpk3q2WG12gOn2h47siHkh5HA8nS/XDlWr0xuMmIdEA6Qhj6ez+WIJCG2qVnc4oTHjpjyZzphocXSiQpVNW2gLeISb0vxwdkCngIeZdJE6NNvDk6HsMQllqha7mj7/Q0CZTZBkxZrLdn8M9f+L8sImTOvlD/rq1yU='},
            {'name': 'Restore potion','base64_icon':'UklGRjgCAABXRUJQVlA4TCwCAAAvFEAHEJfjKLJtqbnn3QdYQAB7tvFvJQLmOXnv23AbSZIiNewee3H6e/L+yx8vM9PMuookSbG6Bu4EnAf6fP41MePM/IcgAtftJBfjyWHIAhAFsiBQgICBBQODCiwIGAgIsiBQERVIJGAgIJGARQICEgxRkGBASCIDCYQMJBBGmBDMlAhGSjgzJFwgJJwZDGeEw37Pwufz19n+v3LcnXW0itLRKtr79VXRKkpFu13fTocnvhs1qfwbrY3WRpbOMlr7/j46S8Xf43GzrTOXEDS2QQgaKLZbhtHcJdsAZHEiggiZrAGKAAgo+2ZnGQYQQRik29p2PM57x7Zt205GxdRTN6k9dc//3/fm/U7heSL6PwHiKIhI6MbNy7v3oG+7obNb0LWh3fltPaANnVxcgpTw7v1md3rjzqP7UPqgfXt49VTtE30merO/eqH2nejbl9cPnr1UIvz5/+/v4QlIqH28/k37xxA6vv7kX/srXevrH3x4+BxKGKyYORl0KKG6XDFX0mGXFSrDJTNXc1GPXQG1+WLJXCvEfS4rjg0W2nopEfDYj6AxnWsa5VTI5zRD1ptLm5VMxO+2S9AYz1jTquZiQZ/TDE1nJm/XivGI320jQagNp8ysqZeSsaDXaYFAa3q00yin42G/2waB/kQ65W6zkk3Egl6HCQIy5l6rmk/Fwx4jBGHII6IxUb9dKyXDLgMEEYH6gyGPxoN2PRmyg4QcRIPhiDuJAEgoQy7k'},
            {'name': 'Energy potion','base64_icon':'UklGRiYCAABXRUJQVlA4TBkCAAAvFEAHEE/juG0kRypV7563f5N/KheQv5uuNFxFku0q58w+MvwhIGrAPAqQk/M56yCSJEWaquMnEa/qHb8hpp75D0VR8HY8WyxmNRlZAjgB8gAzkGABDSwZgCzAwAIUaWBgYIQgYIQEABiASCABDEACFggAEIyUAKHiBCkAglJQ1qeI26j4fr8+77dRf3HpjriNinb8/z///5fcRkUcidId3RG33/ejO0b9PB43l8PTeb2zX81KKqGk1XxQkoVCJVw3J9NoYDCNBiX4crGazAAK3M9XcYuL3BLl9/vpjjjiYoBg29ay5H90d3d3g600dmAr2O38Z/D9H983hfci+q/IbdtG2aunvkJZEUBERSpwPT8/AzlPS7y/AilLXNxdygDG4+0cUGzbW8vFw83FdARCNlXZ6Q8PxazTGuLuYHYi5ofo939vfHQqGTy/vb70DwAVMRvf7zTYlz7094kfg5mU3vcX9ifHkkm1S9QLu80gtEyHkY54rUYQUesQdTMxn10UINtiUDYRcIgCVNvEyKVCLttqgHyzrUouHfE4LHrgqbRQJZ+Oel02E/Cx3kI1KWTifvdKgFKzxUkxmwx6nVyAbK2JiIxSLhX2u+0WAyhQbDQ5aZXy6QgLVhOj0iA+KeczsRALZh3TBvFJpZBJRAIem1Yd1LBO1CCqFrOpsMeq4Z/CqtpoVEu5kMcEKPq/LMFSyCX9B7wonCAA'},
            {'name': 'Defence potion','base64_icon':'UklGRjgCAABXRUJQVlA4TCsCAAAvFEAHEJfjKpJsV9ndOY8c/0ES8tCIghzusQE5kiRFUmTmMoMA+1r9tdo3812VG0mSHKW6ew4NFm/j/za2VjPzHwJCL7uzdWzlIAYwAGABoAgoLAEAZLIhBAPEAAPEMtkKRAIIFgMsQgDABliADTCAkYDYAAYxAiLToGi48CA0WGhYlNCgeBBKaFCUUIoGdsVISKhBsSQS26ZhMZDEgiW309Xr8/H//+seXWNU+1frar+/n9/fT/cY1bpb9xg9RrXu8f1+jGr//5/74+Z8fDru97arFSKJVWwxC2yJECNyOpzUMLDUMBLx+WIxWbHEEoN027aOvXn2Z9u2bcWo2zg1Urfx/f97n+95b+GciP5PgFgLIhK68fPq6xfou72hvz+g64au/3zXA7qh/7+vQEp4+eLm+t+vbxenUHqufXV08l5ti7aZXx9fflLbZ97beXP24bMS4e7x4f7oHUiobR484+O3EDp2n9DT40tdGweHfHT+EUoYrJg5GXQoobpcMVfSYZcVKsMlM1dzUY9dAbX5YslcK8R9LivWDRbaeikR8NjXoDGdaxrlVMjnNEPWm0ublUzE77ZL0BjPWNOq5mJBn9MMTWcmb9eK8YjfbSNBqA2nzKypl5KxoNdpgUBrurbTKKfjYb/bBoH+RDrlbrOSTcSCXocJAjLmXquaT8XDHiMEYcgjojFRv10rJcMuAwQRgfqDIY/Gg3Y9GbKDhBxEg+GIO4kASChDLuQA'},
            {'name': 'Agility potion','base64_icon':'UklGRuYBAABXRUJQVlA4TNoBAAAvFEAHEL/ioLZtKXn3nvshB2gG+/cwxDzr59dw3EiSIk1V9oIf+yb/feLdY2gHkSQpUtWikyNB5/yc8D3M/EcVVPGhbxJogRbCkNVAQoCGQAGEYoACAAAsQAxbACwAlg0MIwwsA4xjLowgMXpeH+/HR/+F/vvrv3A7Hqf5ovesEv3/MzKMDOP/t/3/Robv57X9//rv53Hb7bsBUVgJJLKsRAJkc9tNdQWJihJZSZbsJFUhoYokSVimTarEVqoES9tqbhtJlgwQZNtO2/iHycwMKaaccpMyM7f734okS1v4iui/IrdtGybpbk99hVILQERFGLA8Wd8Ase8vXFoBoS/8XFwVAeJjYQLIr4vLr8/38drOJnBd0Tifn+zz3chbKc9m0yO+Rykf7k63Do4FGz//f7/zPUCF7/rpTc52QRG4f8HX2VSoenqW8+1DwU5SIlaW2gNu+SXh21q/DTwpw9EHXQ4ICipwjWGP00FaSMozR5wOgrygEXqWyukgKVi+rY36bAdhxop8R1cHbAdxXkMO1joI0pyNKPBM2nVAgSiviUPPMrQh7SDh8W1THw16LZJ1SeQ7lqH2m3QjRcxoJHRD7TfYpzBBuoBRYKpdQN7/JYmxORL+AzYUJhA='},
            {'name': 'Combat potion','base64_icon':'UklGRgACAABXRUJQVlA4TPQBAAAvFEAHEEfjIJIkReqqPtL0/iW8iBfAMKfDVSTZrrIz5+WHBnygGUf8oyCne8txJElO1FVod/hjK7ZgkXzBiZn/SCLh5bQ41gmJZWi1WgCQAhBQ1WosY4sEQIUggVIdy2AdW4oEAIhWAwBYxw5EDptpZfrf2crj9nG/P3oZ7FNH0JLAAIpKJaqQUFUIFCIFoECgUkgUBSgqRBCCChBAUIAhUAiIKEVBAxUalFDQQAWldD/O9nlECuI5ryx8P1/Ty/9XbtfbtL/p5Wx/1/POAEG2LUNS/XG7x7bVtm3b1v6XkJmduYX8Ef1n5LaNI6UoU3ZP8wplK4CEIgxYv75/gJjJWC6eQchYTpcvIoAwW72C5NfZ+Xg6X7+ptcDlAhHx1KA74HN1fXOLJ3rVLp/7B5R3x9r9HcFBfzQYGg9BKnwuH59QfyT80d0TQSWkh4hGzZ7gpNpF7AWdv8CtTIeQCrtN38Cj1kHspqMeC0+QbREwE/fZeIJqWxKyyYCDI8g12zQwFXJxBOWWpOTTETcV63qLBCXmdW4JSs0WE4VMwu+2M4JstUmCUMRk0Ou0mv5AgUKjyUSrlEuFicxEUGkgO5Tz6SjV/xfJBrJDpZCJE1k+6UFN1hEbiFVyEHKbN+yvZJVuUIKuH5C890sGWQo6hO+ADYUJCQ=='},
            {'name': 'Prayer potion','base64_icon':'iVBORw0KGgoAAAANSUhEUgAAABUAAAAeCAYAAADD0FVVAAAAAXNSR0IB2cksfwAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAC1ElEQVRIx6WW/UtTURzG15/QDwUiIqWUqIjOfMW35suMzWzmttSFoqWLqWxrKHuhlWAWSoIZZYKVlo1pWG4KQkFESEREzP0/T3zPPGf3urvN6Q8Pg3Hu5z7n+zzn3qsCoEolleoMpEq3nl2TDvjQVQv7cDn6TcXQt148FjgtdC9gwu66kWnW34SJ0aq04LRQDtxe7cITXyPuWytODuUz5NCtNwZMu+vZKNLNNynQfOs2evv6hcuN5euYmqzD2JAazc3t0Go7koKTQgeHhhNkMltgMJih0xtQ36DJHGobHWcalcho7EVnpxEajRbl5VWZQ12uCSGn0wW73Ymb3T1o0+pRXV2HywVFmUE5OBj8hHB4B6FQGF+2Q2zrDY3NJwuKQ61WG9xuD3w+HxNtvelq6+kq5XA44fF4mbxer5jnqaAj0U3m1O2Jibbf0nINlZW1J+tpQ+QthqIbMhV+8CJv7h6yHd2ZQWlx6fd5DESDMmDpt2coDPqRvzCGnMkeZFkzKD8t1ETeMahUdKPiz9PIf+lArs+C7PGu40FpUdmPBfREA7BEAzIo/V+8M4OClUnkTg2mdKs4S8shVKqyn89RsjeLgjUP8matKd3KXe4voutgXTiVQfcXUfJ1DoWBB8ibt8XcuszIuqNLAMugFZEVBlSS+tcLFlbR5iPkL9pxYeYucjx9im5lLnWRNZiiH5kSoL9fibAuLTlZtZK5FdArf18LoJLUf5ZYWCW7T1lYUrdZthtyKE+cakTzlCoBehgWHQLh1j8QczsSbwKD0taOAo+KdiLCCvpjbhfGFN0yaE1kBR0H7xUloP+W42FtTbFqSd3S0T0/2B57LPKZJoNyUTNEWKHHrFrcLXX2nLkp7lR6NEltkVUhagMX7UaEdThX/hw4q69JTF/6SqaL6VRJb0JQ+o+HxZ5W8zbR0aTlV/p24nAC0y+FxY9pqldKRh9nx/1Q+w8w+h0pn5/PmgAAAABJRU5ErkJggg=='},
            {'name': 'Super attack','base64_icon':'iVBORw0KGgoAAAANSUhEUgAAABUAAAAeCAYAAADD0FVVAAAAAXNSR0IB2cksfwAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAACx0lEQVRIx6WW7WtSYRjG7U/owwYiMkwxURF1Ot3Y3HIvVnMNV+reYrGFM7SxmWz4AotBFCwYjCAiKCiKYcVqboNBQUSMiIhw/j9X3I8+x3Pm8W37cHHg8Jzfue77up9zHgUART0pFBcgVqP17JlGwIfJHixHOjEXMsM/fKkpcEPo0U4Ih++DTJvrA1iNuxqCG0I5cO/NBJ5k+/Eg6jw7lPeQQ3dfB/Ao1cda0ai/NYHhyduYnpkTXH54eQMba724v2DH4OBV+HxjNcE1ofMLkSqFwrMIBMIY9QfQ5/G2Do3Fl5jiIgWD0xgfD8Lr9aGz09U6NJlcFZRIJLG8nMDNW1MY8fnhdvfissHUGpSDc7lP2N8/QD6/jy97eVa6p3/wbEFxaDQaQyqVRjabZaLSB64Mn2+kVlYSSKczTJlMRujnuaCL94rMaSpdEpU/NHQNXV09Z5tTj7eAhUhRIqP5HbT6p1CpV1qD0mKr4zvuzEuBVvs3GC056PTbUHesQamKNp8+LfQOFxhULHqR2foZOsNzdGiyUKmXmoPSIpvjB6Zmipidk0Lpvtl2AIPpFTq0G3XdyvaSgKdlc/6ExX4Eg+kttLrNum6lLp3HmAieCE6l0GNY7F9hNO9Aq98qu01CqbpbBZZAnd0FBpST3fWLhWWyfITO8Awa3WOoNWlZtxKXo2MFhCaLTNXQ30JYeuMLNlq13ApQh/uvAJST3fWHhWWxHbKwxG6VqpgUyhOnMaJ+ilUFLYdFm0Bwq1kvu10UwAxKpZ0GnhZVIoRlyZXc6rdl3TJod18BY4ETWVWg/yphWXfZaInd0tZtV86XPou8p7WgXDQZlbDybLS4W5rZtvZwxal4a5JGrldE08BF1QhhlfvKvwMX2/zV6Yt/yfQw7SrxSwhK93hYpa/VljCjNYdf7uzE4QSmK4XFt2m9X0pLh7NmD2r/ATrr2e6kqAUzAAAAAElFTkSuQmCC'},
            {'name': 'Superantipoison','base64_icon':'iVBORw0KGgoAAAANSUhEUgAAABUAAAAeCAYAAADD0FVVAAAAAXNSR0IB2cksfwAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAC1klEQVRIx6WW70sTcRzH1yOfDO7BcRwcPaonFiFB2tRc19TZJi7W3NZ0LRQz3Zpr6tS2mTlSopAggiCiQIQKS0K3ioqIICIogoKI2B/zjs93fLe73O2XD94cHN973fvzeX8/3zsTAFMlmUz7oFW19eyZasDMfBdmJtswGmiBq+9gTeCq0HebAbx56mdaW+7G1an2quCqUA7Mbnhxe+kU5iKWxqG8hxy6vT6Im2mVtaJafw2BgUAIweBI0eWLR26sJK2IjR9Db68TDofLEGwIHRu7tEvnAiGc9QQwMODBSbWnfmg0GitoqiSfPwi324+eHgdaWy31QxNz80XNzCYQj8/A6xvGaccAOjqsaD50pD4oB28+30Iu9wrZbA47O1lWuqr2NhYUh4bDUSSTKSwuLjJR6TZb39621PT0LFKpNFM6nS72c0/QvHOVOU2lCqLy7fZ+HLecaGyf/lFmkbevlORcxTNpGHcEFxJma31QWvxJnkRezeigH+UJbEnncU88g5RgQ8TcXnv6tPCvkihAuewr7EXb0gU8ED1YFuyIm7tqg9Kiz3IY+bYlPVTNsPuvpVE8Fr1YFfqwYFYN3ZbvZef1gjTQL3IE7+WL2BD9WBP6cU3oNnSrA9KD+cPJElSjr/JlfJDHsSkFcVd04UYFtzroLyVeKJ1UBkphvZRCuC+6K7rVuzywUIL+p29KlIWVk0bwUBzUuZ0w6w+XIvSncgX5o2lD6HclxsJ6K49hXfQxt7cEJ3MbM3fqoTxxto0IaqAfSqwY1hNpiLmlQSC3NAza3jIouWABVYBSJQTlYZFbGgRyS8Ogdcugv5XpArSCKERtWOSWBoHc0jCQW97b0uFRA1QbFrmlQSC31NehppaS0yJ0/5xetBM0omp4WNRXOlz4OeBqat6dvvaTTBNFobHgNC+g+zwsKp22FO+j4eYv9++khdOVwiIgbfxKn5S6fs5q/VH7B3qX6i5RebqHAAAAAElFTkSuQmCC'},
            {'name': 'Super energy','base64_icon':'UklGRhwCAABXRUJQVlA4TBACAAAvFEAHEH/jIJJkV7nen/9Xggv8e0BDzvDQATmSZFfRqyo0V5zAf5+4aa12A0Ik2a6qM03OCMABrpGCqfDj/EeNUaO77d22PupaiIzTNSRCEKRzoRjDZKWbLAW6YAIYXQvTYmOcrXRhpJ8sFAmJ9NMljBpBMNriKaWLlMft2+v5rf39a39/2t+/6+XjuH85jJvv423dXGmBFCPBhYQgWojRgiBCBIQAigAihpQQhgiCEAEYRgBSDgKIghCSkZ5kjA46kpH9bmtarCEh99lD+//3+/75///7ff8YYNm2ZUiK2y5X29VW2bbbtu3u+X9XZOQUbkT0fwKEIUgK01jz+gMw9/2jV9dh6kf/rmyYAX/037IXVMLI6M/v/5LP6oDSWOew29mnNsFJrYdclm61WXJmatDe26VEvH99frj7QaE27lmkawDCxPS8XnBZTL155rTb1gMl3LySb61iQglHL6/k4WY5FYXK7Qv5erRdzSQUcPz0QvJ4t55LRWF088wX8mS/WcgkDHD68Nx5etAu5VIRyK6ftORwq1LIxCU4vX+Snh3t1Eq5ZAQdl4+y8+O9RiWfjkMQx7eP8ouT/VatmE3GIHD+YHB5crBZL+fTcQhcPxhenR5uN6vFbDIMAYWzo912vZwJQhB3Wut7ktfnx/utcioEQRK8udV3+v7m4qRVjoNCDvJW391etgqgUIZcyAE='},
            {'name': 'Super strength','base64_icon':'iVBORw0KGgoAAAANSUhEUgAAABUAAAAeCAYAAADD0FVVAAAAAXNSR0IB2cksfwAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAADJElEQVRIx6WWaU8TURSG8a/4RRP9JBEIkUUW0YCSogUEES0BChRoSwG7iCwWSABFiCgQZDOlVFlbkBp2hLAFEBBk8be85ly845S2tIUPT9JM7jxz7nnvmY4fAL+z8PO7BDGe1rN7PAnLNcFQZvkjPfE64qIveyX2KLWbEzFukjLqXoWjRBHoUexRyoWjPQmoNYShSH7z/FLeQy4d6pTAqA1hrfDUX7fCpOQ0pKSmC1V+aX+AytJbyM+4gcjIu4iJue9W7FYqy8hyIjHpCSSSJMTGSRASGuG7NE9RwFCIkEpTEB8vRUREDPz9A32XajQlAmq1BkqlGg8fPcadmDgEBd3ClavXfJNyscUyAJttDFarDSOjVrb10LDI8wXFpXJ5HrRaHQwGA4O2Hn47+mJHSqVSQ6fTM/R6vdDPC0n/HB+zSrW6E2j7UVH3EBAQfL5zura8jOOjIwd6WltRX1kJZU6Ob1JaPGG14uDgAEeHhwwSjo+MoK/zE95VV6NUWYgcmcz79Gnh+uqqg5Sw22yw9Pagpb4ehqIiFGZneyelRd/Hx7C/t8ekYuj6kNmMtsZGVOm0KCnIh/z5M5di516urDgJiamJb7AOfEVXy3vUlJWdWa2DkG7c3d7G7/19hlg6bbdjfHgYvW1tePO6ChUvSqFR5CEr/amT2EG6vLjItk5wMWd2cpKFZe7uQlNtDatWr1IhPzPTtZQuUiU/NzcFqRiSzk1NsbAGTCa0NjSwo1Ve6rpaQbo4P4+93V0nuHhhZoaFNWzpR0dzM6u2+qUBWpUSeRkZjlKe+MbaGn7t7Aiclv+Ym2U9tw0OoPvjB3a0eLXq3FxkpaUJYiadn55mARFisfgBSwsLQlimjg60NzWxQTDq9U7VCiO5/U96Gi6mEHlY/d3dQrV1FRUoKy5moytLTT15LfKeklTMafnq0pIQ1mBfHz63t7NBeGs0slOQnCD5XymXbq6vM7Y2NtgpILa3toSH0FDwsGgI6OVCQpqs2Oho5/TFf8l0M80+BUcP4XK6xsOirdMA8D66Pfyuvp24mKqn3xQWH9Oz/lJ8+jjz9kPtL8SLoQm4PIcRAAAAAElFTkSuQmCC'},
            {'name': 'Super restore','base64_icon':'iVBORw0KGgoAAAANSUhEUgAAABUAAAAeCAYAAADD0FVVAAAAAXNSR0IB2cksfwAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAACo0lEQVRIx6WW/WtSURzG7Y/ol4jBMKRtJQ11KprX183VLHGbu+aspViazjmnli8MVvRCMYKIIGLQKGKsFTUtBqP+tSe+Z5zb9arXl/3wIFzP/ZznfJ/vuedoAGjUpNGcgVy9xrN3egEfl+0opEyIi3rcmNH2Be4JPd4XcbS3xLS95cajnLUnuCeUAxufF/By04VSxjw8lNeQQ3/uzuN5TWCl6FXfrkAxEkN0eUVyebATxNOKA2tJI7zeWfj9ga7grtBE4n6blsQYQiERc4EQHIJncGg2mzvR6pqkcDiKYDAMj8cPo8kyOLRYKksqbBSRzxewsHgLM/4ArNarGBu7NBiUg/e/fkOz+QuNRhOHhw22dMHpHS4oDk2ns6hUqqjX60y0dJd7+nQttb6+gWq1xlSr1aR6ngr6d/ohc1qtnoiW7/Ndg9lsG65PvztX8cdXbtGLyUUUx/1YHrUMBqXBO9Y4jn2lFuAHy128MoRRmZhDXOvA4oix//Rp4A9nrg1KE702RlC/HEDygqDqtg340ZrAkbfIoHLR87dTMWzpg8jo3KpuO9ZSCeTQd+bbeHIlhPXxaVW3LcBdWxJNd545Vbql/95bVqSwyO0dra2j29YdJDyQgHIR9JP9Hgtr2yCysNTctrg8dOU7QkkE5WFt6m+qupWge440frsLkpTQL/YUg/KwyG3uoo+5jYy2ngZSX1JAcqgSTpPysJ5NzrPWkrsVR0wSmEHJBQVE6gQmUb15WLQJ1Nwy6IGQkaDd4ASVhyV3m9K5mNvQecPJZ5HXVAlVgmliHtabqShrLXJbnphlTq+f0/93Kt+aJOoALvkEVHMeFq8rAWlnCWd17enLj2R6WTkBh/KwOJDXsWvzd7o7yeH0S1ACUuOrHSkDXc76vaj9A0tn3GqAY5GyAAAAAElFTkSuQmCC'},
            {'name': 'Sanfew serum','base64_icon':'UklGRjACAABXRUJQVlA4TCMCAAAvFEAHEIfjuJEkRaqG3T0GA+h3v/PfkfMFp9INt5FkO9ETaOERAB5hkH8ycPqsnee4kSRF6mo4vvMC/+e/XTiV8x+yINPH8bSdTypLRprbrfCQkTKSXMKlooRLN62bFpEqUkaKkHCpLKtha+5GZQqTblt4CJeMNLUjLMglPMiE88e2uGyU2RbX4rJhBgYAUAEAMFABDGAFygAAgVFAAFBABgAYQIAFYIAMAsACZcgMABaQASwbBLFYhmDBggyA9/vt9/+7r3bejvbrqEyZ0plWU6lMmVKRKuWyX3RbMqTbUimv5up5vSz9RngITwZYtm2bju4uxyk7tm0nZdu2q/+/ue++LpwT0f8JEJogIqEbj3c319D39UmvD9D1SR8v93pAn/T+fAdSwtT058fb063RAqWZ/km7dURtjuaZJ2yGQbVloqWFcfPwgBLh5//v1z4KEmqzDg/ZxiB0LLrYbTPo+nY42W4aghJiXubv9taxEgo+L3OxuXF4BpWoj9lbqK/tnyggH/Axc766snt0Bq2Yn3zMuXJ3++BEA7mQvz9bam3uHZ1BlgiQpNhY3z44kSAXDkgzhdrq5t7RBfqSQVk6X+mt7xycQhDy0aA8lSt3Vrf2js8hkA5pJHOlVm9j5/AUAvGQZiJbbHTWtvaPLyCgkCnUWisbB5cQhAgRhZk5ns6X2xuHVxBEBIpFKULhWCrX2TwFCTmIohSJJjvbIKEMuZADAA=='},
            {'name': 'Super defence','base64_icon':'iVBORw0KGgoAAAANSUhEUgAAABUAAAAeCAYAAADD0FVVAAAAAXNSR0IB2cksfwAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAC1UlEQVRIx6WW/UtTURjH198QQYQIoki6HBOnSyxdbuKMFnOpu2qSuMzmO1PH3JZgJL2ZFIJkbyRZiZrmNl0WRVBEUASl/j3feM7dubt375s/fBnsnvu53+d8n+feowKgSiWV6gjkSree3ZMOeNN9Bq7rlegRNLjYWJgROC3006qADyt2pgfT9fAMV6cFp4VyYHC5BfemzmFiQJ87lO8hh24tXcJtXx3binT7mxQotHeh83K35HL9uRUzk7UY6dXBZGqC2WxJCk4KdTj64mQXumCzCbhgsaG2zpg9dHBwWNTQiKS2tk5YrW0wGs3QVZ7OHjo+4ZbkGhvH6KgLLa0daDRbUF19FiUlp7KDcvDa2gZCoW0EgyEEAkFWep3BlFtQHNrfP4TJSS/8fj8TlV5vbDxcS7lcY/B6fUw+nw/NzXY0NJw/HPRg18mcer2iqHyC6vU1ufXpv/cGHOz2KvTmvhpz7iKMdedlB6XFX5fKcRDuUQC/vCjH2pwa875ieK7mwymcyDx9WrgXMIlQmehBgXkNFqeKMeUswGhXXmZQWvRtqQL7O53YD19RQOn/nccavJwpxa3hgpRuE+4lAWP1/VUFPj7VYvlOKWYnilK6VQB/vK7A3naL5FQuuvb5mRYrs2o88hQxt+6efFxrjXerdLmpF4EJ9POtjoX17mEZFm4U466rEP6+/IRulS6DFuzvCBEpob9WdFJYT6ZPstZK5laC/lmvkgHj9XtVx8IKL2pZWHK3Qx0xUJ44tRHtp1yxUB4WDQF3Oz0gunXao2AGpdJigbGiSnhYNATklgYhkdtIG9VgL2RNrAj070aVFNbmfBlrLblbGl2H7bj4WpSmKBk0IuoMHlZoQcNai7ulnm1vOhZ1Kh9NUeaoghZJVA0Pi+8rfw9YDEfj05d/kulmmirFQxjUIIVFQBoA3qNJmz/R2SkKN7NfCouPaapPSlaHs0wPav8BE7stEPUy0csAAAAASUVORK5CYII='},
            {'name': 'Antidote+','base64_icon':'UklGRgICAABXRUJQVlA4TPYBAAAvFEAHEO/iKADbNrIkd90+APc//uiyRcON20iO1K2a9XuZDS+8/z/N+y7HbSM5Uqtqd8/7AC6uy/93Gazrmv+IKBH8n7/ss2tabf2IAAFpkA1E1IwpkrBBaUTUwDRKUgVpFIQhQUEYEVCEUGAKEQAhQAiYIAAiBKA8PyJgRzgcpX9Xq5oddhnfjSPmv7XPqrxm87+zwxWr2qzmauO3Gb+NHbN2doRjVVvV7NK+s1Vt/nff4993e/HcjCShkJJzNkkoCJHwO91lZwTZmQRdfo5hgixIMUCQbTtt4x9m5pjDWOZwym3KDPvfhyRLW/g/ov+K3LZtmKS7PfUVmicAETVlwNPm7hbUvr/o7RGVvujz9UEFmI+XDaC8jo++Pt+f71dzkDrkcTKZXcrt4x7R6XR9I7eFuL17trjyKzZ+/v9+JxeAmtzBeIDTc+VDO0PsT9dKvfGIJstrxY7bJaJiOgrSqneYeikTC4NMg9PL2XhEAvR2BxH1Sj4p68DtcEatkJJ0YLTayNWL6UTU04HT5tEx2UFvB0ZTgKZeybEuCJzdQuQsvZrPiIdBdxlEhh3Msi4EGlhNaglhG/WSpwOnSeLAMevlQpYdZtvAkUCvFHOZWIBvNIioSUSupdcK6ZhPfApdbBAxRiEdAZT9XzZAu5BS/gMxNCEQ'},
            {'name': 'Antifire potion','base64_icon':'iVBORw0KGgoAAAANSUhEUgAAABUAAAAeCAYAAADD0FVVAAAAAXNSR0IB2cksfwAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAACbklEQVRIx6WW32/SUBzF61NfmvShf4JPM8bEhMnYdIwBUt1YGBus2yTqiE42BAtjG5QQf0SNZsZEExNjNCHzwUx9cGBi4h93zLfzdpfSH8AeTiDl3k/PPefSXgGA4CVBOAdefuPNOX7Ap7tXUSmMY0O7hIXE+YHAvtC/Rxr+fFsx9ebJLPZLIV+wL5QBO1+X8boVQW07ODqUZcigv9pLeGmEzSj88nUFaqs5rN+6Y7n88XkRz+vTKN8LIBa7AVVdcAW7QvP5zT6taDmk0xrmk2lMh6PDQ4vF0okeli1ls+tIpbKIRlUExieGh+7Udi1VqjvQ9QqWM2tIqEmEQtcwNnZxOCgDH33/iW73NzqdLo6PO+bSwzOx0Ypi0EKhiHq9gWazaYqWHpm9frYtpetVNBqGKcMwrDzPBG0ph6bTRuNEtPx4/CaCwanR9mlVeY+W0uZ0iDWphqSUR1hcHA5Kg+/Lz2zAtnktJ+0hJW0iImYwIaqDt08Da8qHPugD+QVuywaWpC3ExVVMicnBoDSIJhvKF0fohtxCRiohIebMCNzcOrokqB28Jb9CXn4MTdIxJ931dNsDpIn7yicLyot+o1xZWV5u+xp3ApKK8kFPWeSWCnNye/oAkQ+wp3z0hPJlkVuKwMmtBX2kvHNdOqksv+0py8utlSUVRFA3EZQvy+52UpyzwCaUJngBSbQSvizmlgqzu7UKGgTKl8Xcsu1FbgPi/8ciy9QPSjfmy2JuKQJyelmcOXXKb3om2gV2EZSVxXJlwAvClf72+VcyTSbZb0DfWVkMyHJ03fxOZyceTJ+UK/uber1ShjqcDXpQ+wdUlKrcT+cD7AAAAABJRU5ErkJggg=='},
            {'name': 'Divine super attack potion','base64_icon':'UklGRuwBAABXRUJQVlA4TOABAAAvGgAHEK/iNpIkRaqGgzcA5fdffduOzw22kSQ5WfUPNjlA4uSHq7lnG0mSkxUoS4NLSuRIEKSmj5v/AAD4uWzkWliLK1NfIRMEFQwCZjYsASI1LAEmCBTDkAARBJJgwBAZBkUQIGZFErHQwNChhgammRqYJkoghhoSiCiBmGKwAe7uka7/d1Z4zA1IsYnwOOy1LJb1INN6fY437G/Yn/TbRm3SRo3999YNOL9w/GF/P4y0v59r/K5KjHRVuiqcFZbz9J0HkBjZtmlbczzbtnHe0TP2s/X9Z/7BHIYQ0f8JkIRqAqqNqSKEQB24hiqDamIHmzKh+mBQ2xi1jyoBmlTzePf6QjvwcPP63A5/ft3fvjydUqDJ35/fn2fHJwVMg3+/v94uzs/LTC3B74/LK9TO/x/vV1WoQf/k2tFRiWhA9/BCfnhYYaqQ6JtYzvI8RxIYCkCAruG5laQMO9hI2A5278T8apxlWYYEBkkCTOfQ1MJqlKZpiiSMKqF3dHphZz9J0zRFEqrRMTQ2vbi9FydJkhQqkegZHp9Z2tyN4iRJEqowYmBkfHZpY2c/LlZBMAyOTMwur2/vHRRjSrCvgz0wMjG3vLa1exBFUYTKwQaGRqfmV9a39vcBVWMkUa36qG0='},
            {'name': 'Divine super defence potion','base64_icon':'UklGRvYBAABXRUJQVlA4TOkBAAAvGgAHEK/iNpIkReqpPZDv2R7034vXGQbWDVeRbDvRueeSvhGAAsTgX0Nm897kNpIkRaqBA5Xem/Pfktdf4+/t+Q8BQjwum7Evcx+mrhymGZogWpNM0BTTEGCCmIYEU1OIaAwoYDICAgkoTIEkFDAYATF2wZjGJghNmIEiNGRlaMhCaEIBxdBMkqFJCihCeax34RJmYcP9/uhhf5MwcRP/W56XXsgQlWUOvaxiyJTX86kD6RIhbn8qc/urGipNZZVWKZmy1Or2fbjOl914Awm2bZt2tFds28bLU2w75V03/W/MYxMi+j8BklBNQLUxVYQQqAPfUGVQTexgUyZUHwxqG6P2USVAk2puLo9PaAeuL45P2+HPr6vzk7NnCjT5+/Pr4+XxqYBp8O/35+v9w0OZqSX4/X53i9r5/+Pttgo16J9cOzoqEQ3oHl7IDw8rTBUSfRPLWZ7nSAJDAQjQNTy3kpRhBxsJ28HunZhfjbMsy5DAIEmA6RyaWliN0jRNkYRRJfSOTi/s7CdpmqZIQjU6hsamF7f34iRJkkIlEj3D4zNLm7tRnCRJQhVGDIyMzy5t7OzHxSoIhsGRidnl9e29g2JMCfZ3sAdGJuaW17Z2D6IoilA52MDQ6NT8yvrW/j6gaowkqlUftQ0A'},
            {'name': 'Divine super strength potion','base64_icon':'UklGRvgBAABXRUJQVlA4TOwBAAAvGgAHECfjKJJsKXqfnRM3DKAfR7jYYeZV2XAdSbaqnOfv28gAAicvMnCXU3fGVSRJirVw/En+XZyZ8/Fwpmr+I6KIqLfDQ6USIVRJUgFUAIRKZChLUgEUhP7/QECBCgVSAQypFCqACqVSIQQoAAKgUimS9MugImCRKgn/DCDVP4MCgPBVqShI0jguoqrqpitVMZ67ebo821tpqvcb/pl+mX5/Lbtd0zVNVzVtt+678h81TVe3XYlif76E+mVAgEKBICWJ9ut7YNps2n7SHitIsG3t2Jt7vie2bduq/aZuUiP1nf8kPg4hov8TIAlVBFQZU0ZKiSpwCWUGVcRONkVC1cGgpjFqHpUC1CnnzcvrK5qB18+v3zXDzx+vXly9fUiOOr++f/3w6P6DHKbG75svn588flxkKgluPj59hpr5++3TszJU4/bWaJYViBq8P5lviSgxZUjc2Z5sjciQBIYckOD/yeJEW0QgYScbCdvJvru9MN4eERkSGCQJMP9ON+bHOiIikIRRKdzdX5/r72yJiAxJqMKf07212YGu1oiIXCkS9453V2cGu9tyGWUYcXG0szI91NOeizJIhvPD7eWp4d6OgowC7Mtk3zraXpoc6euMlpbWVlQMNnB2sLk4MdzX1g6oHCOJclVHTQM='},
            {'name': 'Ranging potion','base64_icon':'UklGRiwCAABXRUJQVlA4TCACAAAvFEAHEJfjsG0jRxrJd/epku+/sJz/57YNh5Ekq8rO7b7/P04axELeZOPuOIgk2al2Z8lghMI5MlCCi/TDzX+UpOTH1eYwWcRhYWkdMAsUwMBSUcicVtIQxKBMABLHZugtXSsGsilRmJiFqTVASgYG0sNBWwxtz8vH+/7R39Lfv/6W2+lx2l7em9WuFltPQqgoJDSiEISGQCIKCYmZFgpBCIAgCkFoTbQUBBIABYEKgEBBApmChBiChIIYBIIYESI0I1JNsBDDQgQLMSwVGevT+i/jXz6P11ju+lf+77/1V/7vPwMs27YMSXHb5Wq72irbRtu27e75/2VU5BRuRPR/AkRTkBSmseD1B2Du+0fPL8LUj/6dWzID/ui/WS+ohL7+n9//GZ/VAaUBY6/b2aE2xGGte1yWVrVxcmyk297eokR8vX98ujtBoTbomaarC8LE6KSecllMvXkmtNvWBiVcv5JcKSWVcPDySu6vVdIxqNy8aK0PNmvZhAIOn55ftD7cbuTTMTS7fjYe7S4Xs4kmOH54MhzvrZbzqQhkl0/Sk/31aiGTkOD47pGG04PNeimfisBw/ig/O9xpVAuZOARxePNA0nC0u1Iv5VJRCJw+ND0/3ltrVAqZOASu7qUPvDjZ31iul3LJMARkWl+eHmytNirZEARxw1vyTuurs8PdlUo6CEESvLq+4e3d9dnRSjkBCjnI65vbm/PlIiiUIRdy'},
            {'name': 'Divine ranging potion','base64_icon':'UklGRvQBAABXRUJQVlA4TOgBAAAvGgAHEK/iKJJsKXr1tiNnEIEH/Lsg0LDPvPdtOG4byZHUbnZe60JYbP7R+TPdrGrbtrEf915+FVBAGJVpI8HbuWf+QwCBt3WVNkgZhDVzm6maIaqFQoqljEwFJHWkKmCGqAiYqiiiCEKKKaZKYCqiiCIhDSomBQ40wAAHOuGgA+GAAQY4iBIOGGGAwdE3O4dRUP8glSq7Uan/XWU4j9MA6hf+//D7/qTS7/vr6jqTVOpMnaEyPPdl6ZN1X3zbLhpFmIdlGEbTOPAQD3I3SLBt27SjvWLbNl6eYtv7livpf2MemxDR/wmQhGoCqo2pIoRAHTiGKoNqYgebMqH6YFDbGLWPKgGaVPPj9/cX7cDPP9//2+Ht5dffr39XFGjy/vx4f31xWcA0+Hh9uDk7Py8ztQSvd6cnqJ3Pp9uTKtSgf3Lt6KhENKB7eCE/PKwwVUj0TSxneZ4jCQwFIEDX8NxKUoYdbCRsB7t3Yn41zrIsQwKDJAGmc2hqYTVK0zRFEkaV0Ds6vbCzn6RpmiIJ1egYGpte3N6LkyRJCpVI9AyPzyxt7kZxkiQJVRgxMDI+u7Sxsx8XqyAYBkcmZpfXt/cOijEl2MfBHhiZmFte29o9iKIoQuVgA0OjU/Mr61v7+4CqMZKoVn3UNg=='},
            {'name': 'Magic potion','base64_icon':'UklGRkYCAABXRUJQVlA4TDoCAAAvFEAHEAfkNpJkV7mZRWMRBvn7RIOvNdz7aTiOJMlRurpvDi3MwH9HcIEffy2HcxxJkqNMVe/tCxzBdOzAIa3Zmf8olRL3h4PtaicZtObjBNDSQgWUqMAsm1kNAiMRBiCJ1Xxa1CaJosyGASDQmtWASgEoADYn/V9Gt+7l/fjrXrpb93K7fpxqDwOjhAQEGgZYcZSLAcAIQyMVAA0MIikYDqGRQQBLGiABKWUIMDQwQIAoIEQqRCIIJYQQICVQCIAISUIBCUJBC0kEUJIAIYiUQOM8TVObpvZ+fUz7o9Ht//vrbv/fcjydHY4Xr8vTTm8GiLZtm27eqePUTo3USWrbtm3b+vaHe39h74j+K3LbtlH26qmvMBwiAAytSGW49l/0vH/wp0q0kJ9l1TrE5Ks8LFBbRubH53dFjdsnSrJIMj3oT1KTg1wyLeCKV1MIFOSlehPjNIO355fXYLLAUJMdKkUgRftQfjFLAi4tT6EiBj0JmsnJI/A00RcTpa3dPzxibWqwtUlUnD2QXJ8d6lAF2bi9Jx82Fka6WhrFyekd78nN5bGe9qgD2bq6I0msTPYrghzdArjj9ur0oDPI1sUNbgHsrs8N93U214vFwfUNANzubSyODna3RUxk4/Sa5A2wv7k8boUGMWT3irwmyQNzcWTAFuT48oq2xuH26szYUG9HrM7US8DWONpZmzdD+68YkLNzXMBsnOxtLI0PtP7Zn8LJqTU63d8c748IVP/XTHgw1qP9B3YxbAI='},
            {'name': 'Stamina potion','base64_icon':'UklGRgYCAABXRUJQVlA4TPoBAAAvFEAHEA/jIJIkRZquPngGAWfg/Yt4QUzTNhxHkuQou1V7h/5hAj7g/w93tGbaYdtGjmTp7j5V8J19yd9QTuP5j2pRjZfj2bRcIIYhiOryEIgJJjwkZIECoCwwJEBWAAACJANBB0oECIAQAQJgVBcAAJAhtEwaJoGGIQudL1aLHQF1XE9XSSVRqbT4fn+6RjKS+P1+KvH//30+X6/32/8/UpVU1/jXSI3f7+f3+0nqX3+VSqprdFVSn+9b1+j/3+1+sxyezvuT/W5nUAir1XphhTKwMkCwte1slK+2jSS1NZ6OXXeMjve/iuj/t/D+Ef1X5LZtwyTd7amvkCxBACRu0Pfm/Y34RkP8fxHXEIO/Tx7S9X83BHZdXw0HvZ+P1ZyYLgHgZjJ7ZDsXZ8DtdP3CdiTE8end4umVs7G1u7M9eSBIbBfjPTG95z50ciD2p2uu7vgQk+UzZ6fWAZAKe4lZcltXTEd9bmKpG+RsLMDqSGm1Aci5RJDVUa1tUArJsN9jQWqzJXRqMR0J+pxkVm0ZoctEQ5aO1LqJKMnZeCToNXVUbgphlk9YOpJrTWEalJVCKh4OeF0kUamBpikq+kG987l11QYAi2wypncOPRuWrJbkXDoR8duNjRrqQAOoGRsRn838FKo11GFIRjwE1v/VB5pkiPsPzCGZAg=='},
            {'name': 'Zamorak brew','base64_icon':'iVBORw0KGgoAAAANSUhEUgAAABUAAAAeCAYAAADD0FVVAAAAAXNSR0IB2cksfwAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAACsklEQVRIx6WW7UtTURzH1yvfDPbicuFy3/ZKiF4pa1Q+TXNZizGflg+ULVnmmtt02nanZKKSOIwEwyRjGSGWRNuKQiKQiKAICiL6a77xu+Mcz57uHnzxZbB77ud8f7/vOfccEwBTKZlMJ5Avo/H8vXLQ+9PnEL7ViBue07jSebIicFnowZ4HH3b7dSXm23A3YCsLLgtlwPSLHqzMtSIybq0dynrIoG+T3VjWmvVWlOtvSaDn6jAGh65zl6+furAYbcLEaAPa2y/C4XCWBJeEer2+AvV7huF2e3DZ6UZTs716qN8fyOrOBFdf3yBcrj7Y7Q40NJ6pHjoVmeYKT04hGAyjp3cAnQ4nbLbzqK8/VR2Ugfde7SOTeYd0OoNUKq2X3tzSXltQDDo25kc0GkM8HtdFpbe2XTjekgqFJhGLabo0TeP9PBb0346qO43FsqLyOzq6YLWerW2dft1Q8Pe5ykUTbE5JWPBa4HOaq4PS4NSSjD9JNQf6ZlHG9oyEpVELAt1mjDjMladPA789VnQoE0Fpoh1NwuqYBRGP2dBtATCzLOPXtpoDJdH/L2dlPApI0IaM3Rbt5e9nqi4R+n5Fxt68jI2QhNlrxm5zgPTizy2VQ0XRs/0FGVuRbFgzA+aSbnOgh+uKXjopH/pxVeFhPfBZDN3muPy+qXJoPvwgofCw1sYthm459PNDRS89H8r0aU3Rw9qdk7EePHIb6i10yxOngAgqqhiUhSW6ve0y42bXETh7uCUU/HiiFkBFOFUihkVLS3TrvZQH/bKehTIVA1OILKxkVNLd0kYQ3bLe8p6K0GJwmpiFRZtAdEuroLel7sipuDWZaBWQxAmo52Jf6eNC3wEq3WGtK0xfPJLJEQHECfKhDMhSL7n4i92fGJzA9EthEfDeiMXwSDFVe0Gr5KL2H8L47PNOsh/yAAAAAElFTkSuQmCC'},
            {'name': 'Divine magic potion','base64_icon':'UklGRgoCAABXRUJQVlA4TP4BAAAvGgAHEBfjOADbOLEkt9w8GYEN2Jb9GIAnWOJYwnEAto0iuVw/2lB8GYd9GYB3lxwHYBsnltQL3rAFM7ApM/K8Jc1/HQqjgLfbzWZa9LxYx5UeFwphCAOKwACSll4UYelFp6gEGIftTCFMAkFBRVAKOHZPuVyu+joCC+qtn5EZ9tKXbUYFYZkRdsQ2iNjGFlccUVkVVVzRsCqqOPwLq/7B/Cz/YYe/Mf/wP6K6zi/LAEtLt6wtSDgfdt3UDV3yzDuASFAsABIJJIBIIAgkkgpAEkEgkQDK/f7weD1Bgm3bph3tFTvl2LZtlCvmY7Kr/734T02I6P8ESEIFARXG5DEwMEARGIQ8gwpiD9hkCRUHg6rGqHqUC1Amn++/rq+oBn78vv5XDS1tP/9c/f1CDWWa2zu7P3/7WoMp0dTa9am3pyfLFBK0fujrR9X87/jYn4dKnG+Mv79niBI0Hs6nb285Jg+Ji83pOE1TJIGhBhiAhqPFqTBNEyTsARsJ2wP2xebCZJAkSYIEBkkCTP3R2vzESxzHMZIwyoXLndW5u6cojqMISahA3dH2yuzNYxBFWblIXB5sLc8M37+GteRhxOn+5tL0yN1zGIZBkAcDhpO9jcWp0dvHIJMM7MEB++xgc3FybOgheH15eUbZYAPHu+sLk2NDT0+A8jGSyFdxVDU='},
            {'name': 'Antidote++','base64_icon':'UklGRuABAABXRUJQVlA4TNQBAAAvFEAHEL/CILIVKPz/Qe1iPLOa5L6AGg4jyW0b4B6QVIvKVI9qJDoCdBxJkhN11SL+mMAfg3AdO06LmfkPszDjvG4iFDEogoSQQi4xlBljS0JIjBBwiUgCBUmOqBCgIIGIQJIIKoQIKBEcGVktu1S1rHI/f3+VqpZVtvOrrwMRABzSMC2rYZpJgsFzAg84iCJnsDAHPMyw7pfu8v9//v9Pj5b916PZaNWluvSI9/dWXbL+jvtm2XaeA4HnIEHHaZwX8IDLADGSbdPW2c+8tvFt27aRfyqHKewb0X9Fbts2TNLdnvoKIgQgIlEGLCyvjkHt+wtnFkHpCz9nl1SA+phbBpTX5tbX5/v8yt01SG2z2Li4epLbxb2mWb+8f5U7QjzcX7t5flNs/Pz//V48AhK5neNzvHwAonBwimeX90r18Ulzcfui2EkrxNrWBiCtoKICRx92QSbjuMaoLwFhyTSeORlIOshKZHxrKukgLEoWkW9rkg7Skhc4+nTIdxDlvDhwDW3Ed5AUAnpQ6CDMCj7i0LdY1wMCcSFIIt829QnrIJUJHMuYjgYdmqI0Dlzb1IZttpE1Tc4iZRvasMU/hSmyhSwOLa0PKPu/NLPEmir/AR+ECwQ='},
            {'name': 'Bastion potion','base64_icon':'UklGRvABAABXRUJQVlA4TOQBAAAvFEAHEMfCKJIkKVM93BhAAT/8G0DUXtA2XNW2bSWHtS7gM4ElbGNPM1jHb95sh5EkOc2cwUMQREXCROTkdTv/EYUo+3xa0yUtN0jQIJEiDIgENEgA1CCACSGAAKQIAZABAJBAAAQQwgRAqAMCMX9X57MhTOpSs16DcKlJ3PVaTL2RZmpBGP8369ijBMz72zno21eU/Kd8x58DR6LEkb79lOntO4sjjjjyn8WBI9/+N46f/yiOOHDKfxaXfPvfOH4cKfPT/T4Agm3bZqR3Y6ds27baKFe75z+VJD9TiOj/BJAnAJBvdJr1f/ibjMf9NnyNx6Neyw8wHg+7TYAJL8/j0aDTuJ7B9OR8PZy+2B7u73a7t+Ptl22zXm+27+fvPybCdDGb7z8BYntcLZfHD5CP7XK5PN581ZbL5f7yAybkq9VqNWRITEhWqtVqImzKAlgK1Wq1moxYisSAVLlSqVaT0YAmC/DKV5ypeFBXRA+kSm6JkKHKAtxy5bIjnQibuiK6IFUsu6aTUdtQZQGObNk9k4wFTF0RQYRkwSsVD9qGKkkgZEqe2VQiHDA1RQQh75VLJyJBy1AlAQSWZDQUMBUeRCh65jPJeMiUORARAYVCwZFNhUwRIHcAhUKxkA3pADHDndwB'},
            {'name': 'Battlemage potion','base64_icon':'UklGRiACAABXRUJQVlA4TBMCAAAvFEAHEDfjKpJsVzkzZATg/wM7OMBEzuesDccB2KaRLJXv9t/q3sw3ApMtV5Fku0q/HB2gHj84QAPfLwBn5z8KFJrH7QMYgIkYFUZgAEagB3qgl+tuMv6/2M8HsnFefnSVzpgqn9dfZ3SWqXjcvu73y4Vvm4lV15EsGhAGFSwaIAv1FBKFRIGQLNuORKGQQBSyIUEYKBQECtgxQEgkEgTkcHwCARuv1+m0eIn5/b4KMRWdfzFxFCKO3+/n/bp0lTjiiGOqxMTR/79//kyWOGLiMlWC6P/fP3/ieL8PBoiRbJu2znq2bevbtm2b+edw7js3hbUj+j8BaihIKttIZfMF2ItFGU/DVpShRMYOGGU4mQWNcHsTDUVSufdXGF3rd08v32aXF+dnvH/++DM7OZaT04fXn38j4mB/d+/xC1RmV0eHfP6EsnF6SD5/2Aoeko9vvzCCI0AGpwYNI6z4A+TyzGirChOnnwyszI11GgZY9fpJri6Md1tVDHP4xE+uLU72240hWPP4dC5Nj3SbFVhte0VbX54d7bdrFlhzeUXEJxsrc2ODbrMCbcujiWyuLkyM9to1KGLV4RERi8WpsUGnWYfChlsT8W6tLU1PjPZaNSjsuElNtteXZyfHBp1GGQpu3SOys7EyPz0+0i5BEU5xkW7Ssbm6ODXSKkKRBB1OcVGbGqmByhqkU1yyNdUHlTGslTUA'},
            {'name': 'Saradomin brew','base64_icon':'UklGRsIBAABXRUJQVlA4TLYBAAAvFEAHELfiJpIkR+rT6r3nD+a9Z6S7ioajRpIcqdY7/oDue5C6ZzIdRJIkRTUPClCFDpQiBwv3dM1/JEjq839JxrCsISsZyRiysoxkJCNLe10fvxESgNt4gQRFIAEKwBQEAAQBABSIIDohQpjohAjQKRCgM/4jfi2e0/mt7V7j2satbNcYtzKuZVzLfbstx+HxeygSqVQKlUql+vUPhEoVgaGIKtHxB2GkiAJ1/nXGpz4MECPZNm3d/Wzbto1v///M/GM52OeHcHZE/xW5bdvQKXZ76isMKcBiKAPT8XAAal6ixQT+wTcfqwDjn41A4+3r0+sLTEfHPaA+3lm+N7sL7vXl6fHhZ3u84dhoTb/7612xsVxp/XcBbeDe1kTbMxgKz9xJycNsDjfFjtVNRJlyC9AWcTHRdLHZAYyN95FkoY51EHa6NJPI1bAOrC6ecCxbRjoIOQShaLqEdGBxalGqWGm0QeztTiHBSDIvd2B2yuI5qYOwTWIKxzK8q4IBJocUMzsodWBFJXnX6rKSWYKRBOvqPb5hI7LzWPlGsdEXn9JWbSNBptgGjf1fVjZzpqz8B2IMIRo='},
            {'name': 'Extended antifire','base64_icon':'UklGRioCAABXRUJQVlA4TB4CAAAvFEAHEH/juJEkRcqG3T1y4f7n3FnOzF3tBuxIklxF072Lxgi+CCzDeq3F3XY5iCTZVW6XHIVgCJt4wFKG27n5D6pQutldrFZH3hbcNk42TOIWt5kESXjBJNmXsi+ZLWxuM4lZotlstjFOV6ItoJJ9yVRM5rZhsmRVkJiKSVjfVYYGauD9ihpDA/+B2/3ndHj5bm+ilXQZXMKye45KESAQAFDoAABoQKJrQACUAQEQgGhAACEAAIgg6AQEBQWkwVCCCg1AAyhBAtA0EkWQIE0IBDT9Xur3sN1/rTdnOTG3ZbdoYter2WzNLCYxwLJty5AUt12utquNsm23bduY/3dFRk7hRkT/J0AYgqQwjVWvPwBz3198W4OpL34urZsBv/ix7AWVMDL69fm+4rM6oDTWOex29qlNcFLrIZelW22WnJkatPd2KRE//3+/7n5QqI17FukagDAxPa8XXBZTUc+cdtt6oIR0hIzunN4poRqOkLWt45sHqKTCZKS6cXh1p4BKMEyy0tq/uHmAUTqkw2S5sXt2dWeAUjzUyfr2ycXNE2SZoJbUNo/Oru4lKCWC0mK1fXBycfuEjlxMVqg0947Or+8hiEoqJs+XGzsHp5e3jxAoxA1y5frW/vH59T0EMnHDbKm2sXt4enn7DAGFYrW1vX989QJBJEkmSGYKlcbO8c0rBEkwndJJJtL58s7xPSjkIFM6qXM7Z6BQhlzIAQ=='},
            {'name': 'Anti-venom','base64_icon':'UklGRrwBAABXRUJQVlA4TK8BAAAvFEAHEFfCuI0kRdvdSwe/e11kl38EzDCbBiO3bRzFzvTj7gP3/0DvdWYcRJIkRdPVDRgAGejBL57+e2b+w0lxon0z8zaCDUIkIWtBg8SJ0jI8IGOiiZAaaQKoJkIAFQtbqa3UZuXPSiu1Pd/Lyp/lr65dAOJNeBMgRJAABBQpsp9EN5CaQ/EmACEERLABKQ4CFEAs7agi4r4//tzO6+v/m+W/L/+t28fYH4Zu5S1IeAupYN5kPwIFEAPEAGDTNlHYdjhpO6ZkzB0z4/8X2Yr8ghXRf0Vu2zbKUPepr/BGATo8a8DD8+sb2Pn+4rtHsPLFn7dPNkDzcfMMjq69/a/P9/uXhU0gOTCxO2yt0By5Y+adfnGd5pz57GR7Y1VaNn7+/36HZXAezeH8mvsl60Onl+6qX7QynV/wMFuz7LQTZs5FDGRVpqpcJCFYXRUqoQRVh8nSOATKiDJLCUGNzHWZC0LQdA5R5cIIu+1QcFUokWhhE2RaBqhagjIzisCcHtFUZa6woCGoyzxTaRIHOimqQivR5aAdhabMROzjp8aDuspECI76v0icWv8BDg+FAwA='},
            {'name': 'Super combat potion','base64_icon':'UklGRooBAABXRUJQVlA4TH4BAAAvFEAHEB/CKJJsJy/sJwtACf4P2OEe3x8bDCJJcrIXyKAAT6hGDgI+scu4bRtJSjLHa9rYkrbi7elee/7DAEM8TmtAi0mAEg2QQ4AABYQuAgISkCEBOa5ns53TenXhISNlpHFL4SkjpKf9XjSF8KAs4aG+3bhMbuYWzveA8PVXp9QvJgOGgOzrr7s8OgUKALROQQbwj0+NX1FMhgxZpwCr8fv/D7K7nAAxkm3T1lnPtm3j6/l955/UZgoR/Vfktm1Dp9jtqa8IKqAEN2g3alX4xqNRrwXXaDTsNj0gg04DduH1ZTTst+uPG0xHztv5+m3b77abzfvl+WdbUdYft59/Z2Myn85OX0CwHZaLxeUTwbFekKerQk73X2enWKakkzGYLc8tl0nGzUJRShGzF7KpBJXTl/PZtAX5kpRLJ7l0r2QE1WvZlCizLxdoQxC9IZfmLo6AQtmSUR2KWpGlVBkKuSx3Ud4oqRR5mopH5FMwZFIxwPq/Qibp/gOZIBIA'},
            {'name': 'Super antifire potion','base64_icon':'UklGRigCAABXRUJQVlA4TBsCAAAvFEAHEE/jNpIkRZqePnoGmdS3/615V7DLDbcBHDnKScKbCAogpP+OKIHQ7chx20aSVPbc93Ny2IQ2+c1jX1bNf9QqtfTx/HgfHueEM2jbtJ1J0jbZJJHEHpRk3IyGzUg229omiSTe2LJfjLvJkEGpDJuRVCRr27gdaZWSSEWS17xCowGgDZAGAMAgDWhFBKQIgCgQAiKAQYgAiBBM0MhEtQDen7/77ed03+2uM8cccWw5DRxri2OOXB63cTPoyLAZdKTfX8t+Joskz1cBsMCAtgIUFKEBKCgAFABoKQAGCLZtHW++WzdO7ai2bbuNbc9/CN+f75/CfRH9nwDVEySVbXy+vTzDXjzG3w/YijH6824HjPH/+w00wuRULPr39er0wGhan/B7h81mZU5k3OcYMFsSWZwfcw/1GRGJdCrpHwGV2UwgIr5RKBsLIYbFYSsTCIrfNQgjVLMimd3TOyMs57IiK9snN48wqeRIWd48urozQLeQI9ndOLi4eUSvap45srO2d3511wOdYl7vrO6cXt48wqpeEK29sn18fnVngU65ICJ5tpY3D08vbx6hNYqaSLO7vn98fn0HRXSrRRGxWNs7PL28fYBCq6SJFBqd1Z2D4/PreyjUSiKa1NsrW3tHp5e3j1Ao6UWRWmt5Y+fg+OoJiqiQZZZEqs3u2u7JdT8USbBWrbCs7Z7cgcoaZLVSrjR2z0BlDGtlDQA='},
            {'name': 'Anti-venom+','base64_icon':'UklGRr4BAABXRUJQVlA4TLEBAAAvFEAHEHfiKpJtJ7pzDskBn1jCv4mc2b3PhsM2khRpu2v3KIe72C5/MdMD20iSnNzsokLAxSIk8iUmre7mPyKECOzrUZ0aTTHAEJDNGNEqTJgQYzLAbBEGYosswkRAIpsQD8BiiywIGEa6vNdkLWOhUMUGggQsdWoQQggoIGS1ErDluV7/b7nOz/9T8pt+37Str6nbxTUr/1L+JX8pf6X8y/s+8pfy+9n3zdBMEKrYGNtUJZGlSmLAtOjyDgaCAYIAsIWkZq2xZ3bP2rNt+//vKZIvJBH9V+O2baQcGpJ06iuUE6BDkQHHZxeXQPP9JYcnQPIlnwenFKD52D8Dxmtx6evz/ej8+hVQlk0sNG/3OKuyJjKrb55wtkQ216cvD8/E4Of/77e5A1Y4K/M9qW9BEWzs8G59Q1LNt7m5eiQmWanDG3YArciU+KNeB1DbjPsYEBcWwXigRZjjcDLQQuzgDRFBWrBF5I9cQZwXViR6YMk2wsQRxJlLHE6MuqAgKRzSOPQcQYYR+ZZMIuiBVr9tBrkTWRKF3qjfsp/iTMQi9kYdYOz/ZpJnqTck/4EdygoGAA=='},
            {'name': 'Divine super combat potion','base64_icon':'UklGRoYBAABXRUJQVlA4THkBAAAvGgAHEK/BuI0kKT1TPbsL/OGNyJ5giOcMhG0jSYqG9u7J+hQo1A/3bXIYRZKkqLp7Dp9k5oSfuoX5DwGC7n3qwNY3AA4KsFEAgAmjYAAYwDAAcW2fMR5QpCIloqQkaVVFlKpiB4kAluWEIm1BQSYKjiCmO9b1dR+/sDxP8//d93ffNx3nxWUuceK8GkCMZFtVdAZ3/mPdFXmsy8k/uP+fhBDR/wmQhDIBZWNSxBjJgSOkDMrEjjZdQvlgUG2M6qMkQEma74//P+rA19v/bx3OLz/f/36eaVFydnVz9/T60sIUnF7cPu622y6TJbi43x9QnZPrh0MKFQwmy82mQxTQH81CCAmTQmIwmYcQApLA0AIi9EezRQI72kjYjvZgMls0IYSABAZJAkxvNM0RRkkYjKfzVUdAEsrojSbT+WqdkURi0NW0AimMGI4ms/myCKJhOG6tugId2MdoD0aT2WK5WoemaRrUDTYwHE9mi+WqaQClMZJIKx/VBgA='},
            {'name': 'Extended super antifire','base64_icon':'UklGRkoCAABXRUJQVlA4TD0CAAAvFEAHEOfjKpJsV9mZfY/MNxbwbwkBOUcbjiNJcqKpQosvPuC/Xfy0uOEcRJLsKjuzn4wDHGAAy/hADAJyfvMfiUhwO+8th60WpZpUcwAVCgCoFTCWk6GcoKpUAEBLzZqFsZ4ZigoxlBMIkGqsJkQEQAAynrTA6/n5fcM3/x7Hzzf/vjl88++8vu2Xu91z8D4u1tNOFCAUlgplUSgsUCwVShSLQiKsKJCKYqKymERBoQAoEAoVpArA0gkCVKOgQKJCUGOIkBDUENQwoCghIagwQiFRQiFhQEKxec/+/+H/DY/77TMeWeB1f/1yeP9+DBBt2zbd3F3HqZ1aqWPXtm3b7t+/l/t+YZ+I/k+AygqSyjI6/D29sPbzzdZOWPrmb0uXFfCbf21+UAtl5d+//+3ddhe0KoylXneBXhWrRUo8tly9erKuptiZn6NFfL1/fHoLQaVX6WumpwjKQm2jNHlslt58DeJ15EELF6/k2/xoRAvbzy+v3F4cjwehc/UiIjsrk8mIBnYfn0VedtemM7Egsl0+ybPI3sbscDKcBft3T8b9rYWxdCwAs/NHkk9ysL00MZwIm2D/5oGPJA93VqdG09EADKf3D8bHo931mYmhRAiK2L26F5EH8mRvc25qNBUdhMLRnci98XR/a3F6fCgegsL57Z3xXs4OtpfnJkdSkQEo3JK8E5Hzw521henxRB8UcXXNG97y7uJ4d2N+PNYPRRK8uLy65s3l8d7cWAhU5iAvr67lZG4YVNowV+YA'}
        ] 
    def init_banned_monsters(self):
        return [
            "Trapped Soul",
            "Count Draynor",
            "Corsair Traitor",
            "Sand Snake",
            "Corrupt Lizardman",
            "King Roald",
            "Witch's experiment",
            "The Kendal",
            "Me",
            "Elvarg",
            "Moss Guardian",
            "Slagilith",
            "Nazastarool",
            "Treus Dayth",
            "Skeleton Hellhound",
            "Dagannoth mother",
            "Agrith-Naar",
            "Tree spirit",
            "Dad",
            "Tanglefoot",
            "Khazard warlord",
            "Arrg",
            "Black Knight Titan",
            "Ice Troll King",
            "Bouncer",
            "Glod",
            "Evil Chicken",
            "Agrith-Na-Na",
            "Flambeed",
            "Karamel",
            "Dessourt",
            "Gelatinnoth Mother",
            "Culinaromancer",
            "Chronozon",
            "Giant Roc",
            "Dessous",
            "Damis",
            "Fareed",
            "Kamil",
            "Nezikchened",
            "Barrelchest",
            "Giant scarab",
            "Jungle demon",
            "Elven traitor",
            "Essyllt",
            "The Untouchable",
            "The Everlasting",
            "The Inadequacy",
            "Vanguard",
            "Olm",
            "Holthion",
            "Tekton",
            "Ice Demon",
            "Muttadile",
            "Vasa Nistirio",
            "Vespula",
            "Scavenger"
            "Suganditi",
            "Bloat",
            "Nylocas",
            "Xarpus",
            "Verzik"
        ]
    def init_monsters(self, all_monsters):
        monster_regex = re.compile(".*([Hh]ard).*")
        indexes_to_remove = []
        for i, monster in enumerate(all_monsters):
            if (monster_regex.search(monster.wiki_name)):
                indexes_to_remove.append(i)
            else:
                for elem in self.banned_monsters:
                    new_regex = re.compile(f".*{elem}.*|.*{elem.lower}.*")     
                    if (new_regex.search(monster.wiki_name)):
                        indexes_to_remove.append(i)
                        break
        new_monsters = []
        for i, monster in enumerate(all_monsters):
            if i not in indexes_to_remove:
                new_monsters.append(monster)
        return new_monsters   

    def init_bosses(self, all_monsters):
        all_bosses = []
        added_names = []
        for monster in all_monsters:
            cat = monster.category
            if ("boss" in cat and monster.name not in added_names):
                all_bosses.append(monster)  
                added_names.append(monster.name) 
        return all_bosses;     

    def init_slayer_monsters(self, all_monsters):
        all_slayer = []
        added_names = []
        for monster in all_monsters:
            if (monster.slayer_monster and monster.name not in added_names):
                all_slayer.append(monster)  
                added_names.append(monster.name)                  
        return all_slayer;  

    def init_ge_prices(self):
        URL = "https://rsbuddy.com/exchange/summary.json"
        r = requests.get(url = URL) 
        return r.json() 