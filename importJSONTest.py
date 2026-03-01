# This file is for testing the API calls to get the champion spells and display them in the console, it is not used in the main program but it was useful for testing and debugging the API calls before integrating them into the main program.
import requests

lang = input("Enter language code (e.g., 'en_US'): ")

# Getting the current version of the game to get all the champs 
versReq = requests.get('https://ddragon.leagueoflegends.com/api/versions.json')
versions = versReq.json()
currVer = versions[0]



# Getting all the champs names for the drowpdown menu
r = requests.get(f'https://ddragon.leagueoflegends.com/cdn/{currVer}/data/{lang}/champion.json')
champs = r.json()
for champ in champs['data']:
    print(champ)

champ = input("Enter champion name: ") # Retrieve the spells of the selected champion
if champ in champs['data']:
    r = requests.get(f'https://ddragon.leagueoflegends.com/cdn/{currVer}/data/{lang}/champion/{champ}.json')
    champData = r.json()
    spells= champData['data'][champ]['spells']
    champSpells = []
    for spell in spells:
        champSpells.append(spell['name'])
        
    for i in range(len(spells)):
        case = i
        if case == 0:
            print(f"Q: {champSpells[i]}")
        elif case == 1:
            print(f"W: {champSpells[i]}")
        elif case == 2:
            print(f"E: {champSpells[i]}")
        elif case == 3:
            print(f"R: {champSpells[i]}")
