import requests

# versReq = requests.get('https://ddragon.leagueoflegends.com/api/versions.json')
# versions = versReq.json()
# currVer = versions[0]
# Getting the current version of the game to get all the champs 



def champDropdown(currVer,lang): # Getting all the champs names for the drowpdown menu
    r = requests.get(f'https://ddragon.leagueoflegends.com/cdn/{currVer}/data/{lang}/champion.json')
    champs = r.json()
    champList = [] # Initialize empty list to stone champ names
    for champ in champs['data']:
        print(champ)
        champList.append(champ)
    return(champList)

def champSel(currVer,lang,champ): # Retrieve the spells of the selected champion
    r = requests.get(f'https://ddragon.leagueoflegends.com/cdn/{currVer}/data/{lang}/champion/{champ}.json')
    champData = r.json()
    spells= champData['data'][champ]['spells']
    champSpells = [] # Initialize empty list to store spell names
    spellFormated = [] # Initialize empty list to store formatted spell names
    for spell in spells:
        champSpells.append(spell['name'])
        
    for i in range(len(spells)):
        case = i
        if case == 0:
            print(f"Q: {champSpells[i]}")
            spellFormated.append(f"Q: {champSpells[i]}")
        elif case == 1:
            print(f"W: {champSpells[i]}")
            spellFormated.append(f"W: {champSpells[i]}")
        elif case == 2:
            print(f"E: {champSpells[i]}")
            spellFormated.append(f"E: {champSpells[i]}")
        elif case == 3:
            print(f"R: {champSpells[i]}")
            spellFormated.append(f"R: {champSpells[i]}")

    return spellFormated
    
