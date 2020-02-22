import base64

items = [
    {"name": "Attack potion"},
    {"name": "Antipoison"},
    {"name": "Strength potion"},
    {"name": "Guthix rest"},
    {"name": "Restore potion"},
    {"name": "Energy potion"},
    {"name": "Defence potion"},
    {"name": "Agility potion"},
    {"name": "Combat potion"},
    {"name": "Prayer potion"},
    {"name": "Super attack"},
    {"name": "Superantipoison"},
    {"name": "Super energy"},
    {"name": "Super strength"},
    {"name": "Super restore"},
    {"name": "Sanfew serum"},
    {"name": "Super defence"},
    {"name": "Antidote+"},
    {"name": "Antifire potion"},
    {"name": "Divine super attack potion"},
    {"name": "Divine super defence potion"},
    {"name": "Divine super strength potion"},
    {"name": "Ranging potion"},
    {"name": "Divine ranging potion"},
    {"name": "Magic potion"},
    {"name": "Stamina potion"},
    {"name": "Zamorak brew"},
    {"name": "Divine magic potion"},
    {"name": "Antidote++"},
    {"name": "Bastion potion"},
    {"name": "Battlemage potion"},
    {"name": "Saradomin brew"},
    {"name": "Extended antifire"},
    {"name": "Anti-venom"},
    {"name": "Super combat potion"},
    {"name": "Super antifire potion"},
    {"name": "Anti-venom+"},
    {"name": "Divine super combat potion"},
    {"name": "Extended super antifire"}
]

newItems = []

txt_file = open('tempfile.txt', "w");

for elem in items:
    filename = f"{elem['name']}.png"
    with open(filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        item_string = "{'name': '" + elem["name"] + "',\n'base64_icon':'" + str(encoded_string)[2:].strip("'") + "'},\n"
        print(item_string)
        '''newItems.append({
            "name": elem["name"],
            "base64_icon": encoded_string
        })'''
        txt_file.write(item_string)

txt_file.close()      