import tkinter

import requests
import warnings
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
    print(f'https://ddragon.leagueoflegends.com/cdn/{currVer}/data/{lang}/champion/{champ}.json')
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
    
def getLocalGameInfo():
    # Get live game info using PUUID
    url = f"https://127.0.0.1:2999/liveclientdata/playerlist"
    warnings.filterwarnings("ignore")
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        data = response.json()
        return data
        # print(f"Live Game Data: {data}") # debug print
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        msgError= tkinter.messagebox.showerror("Error", "There's no game being spectated right now.")
        print(f"An error occurred: {err}")
        return
    

def getChampsLocal(data):
    # Get the list of champions in the live game and their roles
    playerBlueSide= {}
    playerRedSide = {}
    verifiedName = ""

    for participant in data:
        if participant['team'] == 'ORDER':
            verifiedName = participant['championName'] 
            verifiedName = validateNames(verifiedName)
            playerBlueSide.update({verifiedName: participant['position']})
        elif participant['team'] == 'CHAOS':
            verifiedName = participant['championName']
            verifiedName = validateNames(verifiedName)
            playerRedSide.update({verifiedName: participant['position']})
    
    # print(f"\nBlue Side Champions and Roles:") # debug print 
    # for i in playerBlueSide:
    #     print(f"Champion: {i}, Role: {playerBlueSide[i]}") # debug print 
    
    # print(f"\nRed Side Champions and Roles:") # debug print 
    # for i in playerRedSide:
    #     print(f"Champion: {i}, Role: {playerRedSide[i]}") # debug 
    return playerBlueSide, playerRedSide


def validateNames(verifiedName):
    if verifiedName == "Nunu & Willump":
         verifiedName = "Nunu"
    elif verifiedName == "Wukong":
         verifiedName = "MonkeyKing"

    if " " in verifiedName: # Remove space and apostrophes from champion names to match the API format
                listVer = verifiedName.split(" ")
                listVer[0] = listVer[0].capitalize()
                listVer[1] = listVer[1].capitalize()
                if verifiedName[0].islower:
                    verifiedName = "".join(listVer)
                return verifiedName
    elif "'" in verifiedName:
                listVer = verifiedName.split("'")
                listVer[0] = listVer[0].capitalize()
                listVer[1] = listVer[1].capitalize()
                if verifiedName[0].islower:
                    verifiedName = "".join(listVer)
                return verifiedName
    else:
                if verifiedName[0].islower:
                    verifiedName = verifiedName[0].capitalize() + verifiedName[1:]
                return verifiedName
    
    