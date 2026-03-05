import tkinter
import webbrowser
import requests
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import warnings
from dotenv import load_dotenv
import os
import sys

# Get the base path for the application to handle both development and compiled exe
if getattr(sys, 'frozen', False):
    # Running as compiled exe
    base_path = sys._MEIPASS
    # Add the base path to sys.path so Python can find the local modules
    sys.path.insert(0, base_path)
else:
    # Running as script - go up one level from src/ to project root
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Add src/ directory to sys.path for local imports
    sys.path.insert(0, os.path.join(base_path, 'src'))

# Now import local modules after path is configured
import methods
from dicts import langOpts, serversList


# Getting the current version of the game to get the updated list of all the champs (needed as the game updates every 2 weeks and champ releases & reworks can alter the list if stored locally)
versReq = requests.get('https://ddragon.leagueoflegends.com/api/versions.json')
versions = versReq.json()
currVer = versions[0]
champ = ""
lang = ""
windowed = True
champDict = {}
champNamesBlue = []
champNamesRed = []
playerBlueSide= {}
playerRedSide = {}
# Hardcoded apikey for testing, will be stored in a different file and renewed after testing.
# API_KEY access from env variable, create a .env file in the same directory as this script and add the line API_KEY=your_api_key_here to store your API key securely
env_path = os.path.join(base_path, '.env')
load_dotenv(env_path)
API_KEY = os.getenv("API_KEY")

# Initialize the main window and all the widgets.
root = Tk()
root.geometry("1024x576")
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)
root.attributes('-transparentcolor', 'red') # Set the background color to a color that will be transparent so you are able to see the game while the app is open
root.title("League Casting Helper")
icon_path = os.path.join(base_path, 'static', 'imgs', 'appicon.ico')
githubPath = os.path.join(base_path,'static','imgs', 'github.png')
root.iconbitmap(icon_path) # Set the app icon

# Initialize the champion comboboxes with empty values, will be updated after language selection
cbChamp = ttk.Combobox(root, values="") 
cbChamp2 = ttk.Combobox(root, values="") 
cbChamp3 = ttk.Combobox(root, values="") 
cbChamp4 = ttk.Combobox(root, values="")
cbChamp5 = ttk.Combobox(root, values="") 
# Differenciate the cboxes by side selected, left or right, to show the spells of the selected champion in the correct side of the screen
cbChamp6 = ttk.Combobox(root, values="") 
cbChamp7 = ttk.Combobox(root, values="") 
cbChamp8 = ttk.Combobox(root, values="") 
cbChamp9 = ttk.Combobox(root, values="") 
cbChamp10 = ttk.Combobox(root, values="") 

# TextBox for the user to write the riot id
lblId = Label(root, text="Enter Riot ID:")
lblId.grid(row=0, column=0, pady=10, padx=10, sticky='w')
txtRiotID = Text(root, height=1, width=15)
txtRiotID.grid(row=0, column=0, columnspan=1, pady=10, padx=10)
# Server selection combobox
cbServers = ttk.Combobox(root, values=list(serversList.keys()))
cbServers.set("Select a server")
cbServers.grid(row=0, column=2, pady=10, padx=10, sticky='e')
# Language selection combobox
cbLang = ttk.Combobox(root, values=list(langOpts.keys()))
cbLang.set("Select a language")
cbLang.grid(row=0, column=1, columnspan=1, pady=10, padx=10)
# CheckBox to choose ultimate only mode, will show only the ultimate spell of each champ.
isChecked = IntVar()
chkUltimateOnly = Checkbutton(root, text="Ultimate Only Mode", onvalue=1, offvalue=0,variable=isChecked)
chkUltimateOnly.grid(row=1, column=1, pady=10, padx=10)

# Widgets for manual inputs search
lblBlue = Label(root, text="Write blue team champs separated by a ',' :")
txtBlue = Text(root, height=1, width=15)
lblRed = Label(root, text="Write red team champs separated by a ',' :")
txtRed = Text(root, height=1, width=15)

# List to store all the champion comboboxes for easy access and manipulation
boxesLeft = [cbChamp,cbChamp2,cbChamp3,cbChamp4,cbChamp5] 
boxesRight = [cbChamp6,cbChamp7,cbChamp8,cbChamp9,cbChamp10]

# Initialize label to display spells, set to empty string initially
lblSpells = Label(root, text=" ") 
lblSpells2 = Label(root, text=" ") 
lblSpells3 = Label(root, text=" ")
lblSpells4 = Label(root, text=" ")  
lblSpells5 = Label(root, text=" ")
# Differenciate the labels by side selected
lblSpells6 = Label(root, text=" ")
lblSpells7 = Label(root, text=" ")
lblSpells8 = Label(root, text=" ")
lblSpells9 = Label(root, text=" ")
lblSpells10 = Label(root, text=" ")
# List to store all the spell labels for easy access and manipulation
lblsLeft = [lblSpells,lblSpells2,lblSpells3,lblSpells4,lblSpells5] 
lblsRight = [lblSpells6,lblSpells7,lblSpells8,lblSpells9,lblSpells10]

# Empty lists to store the comboboxes that'll be filled with the champ names
initBoxesLeft = []
initBoxesRight = []

link = "http://github.com/LuisLCT99"
githubLogo = Image.open(githubPath).resize((40,40))
gitLogo = ImageTk.PhotoImage(githubLogo)



# Update the language and initialize the champ comboboxes with the champs names, also disable the language selection after selection and show the button to show the spells of the selected champions
def updateLang(boxesLeft,boxesRight):
    lang = langOpts.get(cbLang.get(), "en_US") # Default to English if no selection is made
    # lbl = Label(root, text=lang) # Debug tag to check if the language is being selected correctly
    # lbl.pack()
    
    btnLang.config(state=DISABLED) # Disable the button after selection
    cbLang.config(state=DISABLED) # Disable the combobox after selection
    initializeChampBoxes(boxesLeft,boxesRight)
    # cbChamp.set("Select a champion")
    # cbChamp.config(values=list(methods.champDropdown(currVer,lang)))
    # cbChamp.pack()
    btnLang.destroy() # Destroy the button after selection
    cbLang.destroy() # Destroy the combobox after selection
    fullScreenBtn.grid(row=6, column=0, columnspan=1, pady=10)
    closeBtn.grid(row=6, column=2, columnspan=1, pady=10) # Show the full screen and close buttons after the language is selected and the champ selection is shown
    btnChampSel=Button(root, text="Show Spells", command=lambda: printChampSpells2(currVer,lang,champ,lblsRight,lblsLeft,initBoxesLeft,initBoxesRight,btnChampSel))
    btnChampSel.grid(row=6, column=1, columnspan=1, pady=10)
    print(lang) # Debug print to check if the language is being selected correctly
    return lang,cbChamp,btnChampSel

# Deprecated function replaced by printChampSpells2 to show all the spells at the same time instead of one by one, but keeping it for reference
# def printChampSpells(currVer,lang,champ,cbChamp,lblSpells):
#     lblSpells.config(text="") # Clear the label text before displaying new spells
#     champ = cbChamp.get()
#     champSpells = methods.champSel(currVer,lang,champ)
#     for spell in champSpells:
#         lblSpells.config(text=lblSpells.cget("text") + "\n" + spell) # Update the label text to include the spells
#         lblSpells.pack()
#     # btnChampSel.destroy() # Destroy the button after selection

# Second version of the previous function to show all the spells at the same time, iterating through all the selected champs and showing their spells in order
def printChampSpells2(currVer,lang,champ,lblsLeft, lblsRight, initBoxesLeft, initBoxesRight,btnChampSel):
    for i,lbl in enumerate(lblsLeft, start=0):
        lbl.config(text="") # Clear the label text before displaying new spells
        lbl.grid(row=i, column=0, padx=10, pady=5, sticky='w')
        champ = initBoxesLeft[i].get()
        champSpells = methods.champSel(currVer,lang,champ)
        initBoxesLeft[i].destroy() # Destroy the combobox after selection
        for spell in champSpells:
            lbl.config(text=lbl.cget("text") + "\n" + spell) # Update the label text to include the spells
            
    for i,lbl in enumerate(lblsRight, start=0):
        lbl.config(text="") # Clear the label text before displaying new spells
        lbl.grid(row=i, column=2, padx=10, pady=5, sticky='e')
        champ = initBoxesRight[i].get()
        champSpells = methods.champSel(currVer,lang,champ)
        initBoxesRight[i].destroy() # Destroy the combobox after selection
        for spell in champSpells:
            lbl.config(text=lbl.cget("text") + "\n" + spell) # Update the label text to include the spells
    root.config(bg='red') # Set the background color to white to make the transparent color work
    btnChampSel.destroy() # Destroy the button after selection

# Function to initialize the champ comboboxes with the names of all the champs
def initializeChampBoxes(boxesLeft,boxesRight):

    for i, box in enumerate(boxesLeft, start=0):
        box.set("Select a champion")
        box.config(values=list(methods.champDropdown(currVer,langOpts.get(cbLang.get(), "en_US"))))
        box.grid(row=i, column=0, padx=10, pady=5, sticky='ew')
        initBoxesLeft.append(box)

    for i, box in enumerate(boxesRight, start=0):
        box.set("Select a champion")
        box.config(values=list(methods.champDropdown(currVer,langOpts.get(cbLang.get(), "en_US"))))
        box.grid(row=i, column=2, padx=10, pady=5, sticky='ew')
        initBoxesRight.append(box)
    
    return (initBoxesLeft,initBoxesRight)

# All methods related to the api calls to get the info of a live game giving riot ID
def retrieveAllChamps(lang):
    r = requests.get(f'https://ddragon.leagueoflegends.com/cdn/{currVer}/data/{lang}/champion.json')
    champs = r.json()
    for champ in champs['data']:
        champDict.update({champ: champs['data'][champ]['key']})

# Split the riot ID into name and tag
def userNameSplit(userId):
    userName = userId.split("#")
    name = userName[0]
    tag = userName[1]
    return name, tag

# Get PUUID of the summoner
def getPUUID(name, tag, region):
   
    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}?api_key={API_KEY}"
    warnings.filterwarnings("ignore")
    try:        
        response = requests.get(url, verify=False)
        response.raise_for_status()
        data = response.json()
        puuid = data['puuid']
        print(f"PUUID: {puuid}") # debug print
        return puuid
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        msgError= tkinter.messagebox.showerror("Error", "The user does not exist.\nTry again with a different Riot ID.")
        print(f"An error occurred: {err}")
        puuid = "ERROR"
        return puuid
    except Exception as err:
        print(f"An error occurred: {err}")
        puuid = "ERROR"
        return

def getLiveGameInfo(puuid, server):
    # Get live game info using PUUID
    url = f"https://{server}.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{puuid}?api_key={API_KEY}"
    warnings.filterwarnings("ignore")
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        data = response.json()
        return data
        # print(f"Live Game Data: {data}") # debug print
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        msgError= tkinter.messagebox.showerror("Error", "The user is not currently in a game or has streamer mode active \nPlease try again with a different Riot ID.")
        print(f"An error occurred: {err}")
        return
    except Exception as err:
        msgError= tkinter.messagebox.showerror("Error", "The user is not currently in a game or has streamer mode active \nPlease try again with a different Riot ID.")
        print(f"An error occurred: {err}")
        return
    

def getChamps(data):
    # Get the list of champions in the live game
    champIds = []
    # participantRoles = [] 
    playerBlueSide= []
    playerRedSide = []

    for participant in data['participants']:
        champIds.append(participant['championId'])
        if participant['teamId'] == 100:
            playerBlueSide.append(participant['championId'])
        elif participant['teamId'] == 200:
            playerRedSide.append(participant['championId'])
    
    # for champId in champIds:
    #     for champName, champKey in champDict.items():
    #         if champKey == str(champId):
    #             print(f"Champion ID: {champId}, Champion Name: {champName}") # debug print to check if the champion IDs are being correctly matched to their names

        
    for champId in playerBlueSide:
        for champName, champKey in champDict.items():
            if champKey == str(champId):
                champNamesBlue.append(champName)
    print(f"Champions in the blue team: {champNamesBlue}") # debug print

    
    for champId in playerRedSide:
        for champName, champKey in champDict.items():
            if champKey == str(champId):
                champNamesRed.append(champName)
    print(f"Champions in the red team: {champNamesRed}") # debug print

def printChampSpells3(currVer,lang,champ,lblsLeft, lblsRight, champNamesBlue, champNamesRed):
    for i,lbl in enumerate(lblsLeft, start=0):
        lbl.config(text="") # Clear the label text before displaying new spells
        lbl.grid(row=i, column=0, padx=10, pady=5, sticky='w')
        champ = champNamesBlue[i]
        champSpells = methods.champSel(currVer,lang,champ)
        for spell in champSpells:
            lbl.config(text=lbl.cget("text") + "\n" + spell) # Update the label text to include the spells
            
    for i,lbl in enumerate(lblsRight, start=0):
        lbl.config(text="") # Clear the label text before displaying new spells
        lbl.grid(row=i, column=2, padx=10, pady=5, sticky='e')
        champ = champNamesRed[i]
        champSpells = methods.champSel(currVer,lang,champ)
        for spell in champSpells:
            lbl.config(text=lbl.cget("text") + "\n" + spell) # Update the label text to include the spells
    destroyWidgets(3) # Destroy the initial widgets after showing the spells to prevent changes while the app is running

# Print only the ult spell
def printOnlyUlt(currVer,lang,champ,lblsLeft, lblsRight, champNamesBlue, champNamesRed):
    for i,lbl in enumerate(lblsLeft, start=0):
        lbl.config(text="") # Clear the label text before displaying new spells
        lbl.grid(row=i, column=0, padx=10, pady=5, sticky='w')
        champ = champNamesBlue[i]
        champSpells = methods.champSel(currVer,lang,champ)
        lbl.config(text=champSpells[3]) # Update the label text to include only the ultimate spell
            
    for i,lbl in enumerate(lblsRight, start=0):
        lbl.config(text="") # Clear the label text before displaying new spells
        lbl.grid(row=i, column=2, padx=10, pady=5, sticky='e')
        champ = champNamesRed[i]
        champSpells = methods.champSel(currVer,lang,champ)
        lbl.config(text=champSpells[3]) # Update the label text to include only the ultimate spell
    destroyWidgets(3)

def login(txtRiotID, cbServers, cbLang):
    if cbLang.get() == "Select a language" or cbServers.get() == "Select a server" or txtRiotID.get("1.0", "end-1c") == "": # Check if the user has selected a language, a server and entered a riot ID before proceeding
        msgError= tkinter.messagebox.showerror("Error", "Please select a language,a server and enter a riot IDbefore proceeding.")
        return
    else:
        userId = txtRiotID.get("1.0", "end-1c") # Get the text from the Text widget
        lang = langOpts.get(cbLang.get(), "en_US") # Get the selected language code
        retrieveAllChamps(lang) # Retrieve all the champs and their keys to match them with the champion IDs from the live game data
        name, tag = userNameSplit(userId)
        region = regionSelector(serversList.get(cbServers.get()))
        puuid = getPUUID(name, tag, region)
        if puuid != "ERROR":
            data = getLiveGameInfo(puuid, serversList.get(cbServers.get()))
            getChamps(data)
            if isChecked.get() == 1: # Check if the ultimate only mode is selected
                printOnlyUlt(currVer,lang,champ,lblsLeft, lblsRight, champNamesBlue, champNamesRed)
            else:
                printChampSpells3(currVer,lang,champ,lblsLeft, lblsRight, champNamesBlue, champNamesRed)
        
def regionSelector(server):
    print(f"Selected server: {server}") # Debug print to check if the server is being selected correctly
    if (server == 'EUW1' or server == 'EUN1' or server == 'RU' or server == 'TR1' or server == 'ME1'):
        region = 'EUROPE'
    elif (server == 'NA1' or server == 'BR1' or server == 'LA1' or server == 'LA2'):
        region = 'AMERICAS'
    elif (server == 'JP1' or server == 'KR' or server == 'SG2' or server == 'TW2' or server == 'VN2' or server == 'OC1'):
        region = 'ASIA'
    return region

def loginLocal():
    if cbLang.get() == "Select a language": # Check if the user has selected a language before proceeding
        msgError= tkinter.messagebox.showerror("Error", "Please select a language before proceeding.")
        return
    else:
        lang = langOpts.get(cbLang.get(), "en_US") # Get the selected language code
        data = methods.getLocalGameInfo()
        playerBlueSide,playerRedSide = methods.getChampsLocal(data)
        if isChecked.get() == 1: # Check if the ultimate only mode is selected
            printOnlyUltLocal(lang,currVer,champ,lblsLeft, lblsRight, playerBlueSide, playerRedSide)
        else:
            printChampSpellsLocal(currVer,lang,champ,lblsLeft, lblsRight, playerBlueSide, playerRedSide)

def manualData():
    if cbLang.get() == "Select a language": # Check if the user has selected a language before proceeding
        msgError= tkinter.messagebox.showerror("Error", "Please select a language before proceeding.")
        return
    else:
        lang = langOpts.get(cbLang.get(), "en_US") 
        print(lang)
        getChampsManual()
        return lang
    
def getChampsManual():
    destroyWidgets(0)
    lblBlue.grid(row=0, column=0, pady=10, padx=10, sticky='w')
    txtBlue.grid(row=0, column=1, columnspan=2, pady=10, padx=10, sticky= 'ew')
    lblRed.grid(row=1, column=0, pady=10, padx=10, sticky='w')
    txtRed.grid(row=1, column=1, columnspan=2, pady=10, padx=10, sticky='ew')
    btnLocal.grid(row=2, column=1, pady=10, padx=10)
    return 

def printChampsManual(currVer,lang,champ):
    lang = langOpts.get(cbLang.get(), "en_US")
    if txtBlue.get("1.0", "end-1c")=="" or txtRed.get("1.0", "end-1c") == "":
        msgError= tkinter.messagebox.showerror("Error", "Fields can't be empty")
        return
    else:
        champSplitBlue = txtBlue.get("1.0", "end-1c").split(',')
        champSplitRed = txtRed.get("1.0", "end-1c").split(',')

    if len(champSplitBlue) > 5 or  len(champSplitRed) > 5:
        msgError= tkinter.messagebox.showerror("Error", "Please write only 5 champs")
        return
    else:
        if isChecked.get() == 1: # Check if the ultimate only mode is selected
            for i,lbl in enumerate(lblsLeft, start = 0):
                lbl.config(text="") # Clear the label text before displaying new spells
                lbl.grid(row=i, column=0, padx=10, pady=5, sticky='w')
                champ = methods.validateNames(champSplitBlue[i])
                champSpells = methods.champSel(currVer,lang,champ)
                for spell in champSpells:
                    lbl.config(text=lbl.cget("text") + "\n" + spell) # Update the label text to include the spells
            
            for i,lbl in enumerate(lblsRight, start=0):
                lbl.config(text="") # Clear the label text before displaying new spells
                lbl.grid(row=i, column=2, padx=10, pady=5, sticky='e')
                champ = methods.validateNames(champSplitRed[i])
                champSpells = methods.champSel(currVer,lang,champ)
                for spell in champSpells:
                    lbl.config(text=lbl.cget("text") + "\n" + spell) # Update the label text to include the spells
        else:
            for i,lbl in enumerate(lblsLeft, start = 0):
                lbl.config(text="") # Clear the label text before displaying new spells
                lbl.grid(row=i, column=0, padx=10, pady=5, sticky='w')
                champ = methods.validateNames(champSplitBlue[i])
                champSpells = methods.champSel(currVer,lang,champ)
                lbl.config(text=champSpells[3])
            
            for i,lbl in enumerate(lblsRight, start=0):
                lbl.config(text="") # Clear the label text before displaying new spells
                lbl.grid(row=i, column=2, padx=10, pady=5, sticky='e')
                champ = methods.validateNames(champSplitRed[i])
                champSpells = methods.champSel(currVer,lang,champ)
                lbl.config(text=champSpells[3])
    destroyWidgets(3)

def printChampSpellsLocal(currVer,lang,champ,lblsLeft, lblsRight, playerBlueSide, playerRedSide):
    champNamesBlue = list(playerBlueSide.keys())
    champNamesRed = list(playerRedSide.keys())
    for i,lbl in enumerate(lblsLeft, start=0):
        lbl.config(text="") # Clear the label text before displaying new spells
        lbl.grid(row=i, column=0, padx=10, pady=5, sticky='w')
        champ = champNamesBlue[i]
        champSpells = methods.champSel(currVer,lang,champ)
        for spell in champSpells:
            lbl.config(text=lbl.cget("text") + "\n" + spell) # Update the label text to include the spells
            
    for i,lbl in enumerate(lblsRight, start=0):
        lbl.config(text="") # Clear the label text before displaying new spells
        lbl.grid(row=i, column=2, padx=10, pady=5, sticky='e')
        champ = champNamesRed[i]
        champSpells = methods.champSel(currVer,lang,champ)
        for spell in champSpells:
            lbl.config(text=lbl.cget("text") + "\n" + spell) # Update the label text to include the spells
    destroyWidgets(3) # Destroy the initial widgets after showing the spells to prevent changes while the app is running

def printOnlyUltLocal(lang,currVer,champ,lblsLeft, lblsRight, playerBlueSide, playerRedSide):
    champNamesBlue = list(playerBlueSide.keys())
    champNamesRed = list(playerRedSide.keys())
    for i,lbl in enumerate(lblsLeft, start=0):
        lbl.config(text="") # Clear the label text before displaying new spells
        lbl.grid(row=i, column=0, padx=10, pady=5, sticky='w')
        champ = champNamesBlue[i]
        champSpells = methods.champSel(currVer,lang,champ)
        lbl.config(text=champSpells[3]) # Update the label text to include only the ultimate spell
            
    for i,lbl in enumerate(lblsRight, start=0):
        lbl.config(text="") # Clear the label text before displaying new spells
        lbl.grid(row=i, column=2, padx=10, pady=5, sticky='e')
        champ = champNamesRed[i]
        champSpells = methods.champSel(currVer,lang,champ)
        lbl.config(text=champSpells[3]) # Update the label text to include only the ultimate spell
    destroyWidgets(3)

def destroyWidgets(int):
    # Destroy the buttons after showing the spells to prevent changes while the app is running
    match int:
        case 0:
            lblId.destroy()
            txtRiotID.destroy() 
            cbServers.destroy() 
            cbLang.grid_forget() 
            btnLang.destroy()
            localGameBtn.destroy() 
            manualEntryBtn.destroy() 
            chkUltimateOnly.destroy()
            fullScreenBtn.grid(row=6, column=0, columnspan=1, pady=10)
            closeBtn.grid(row=6, column=2, columnspan=1, pady=10) # Show the full screen and close buttons after the language is selected and the champ selection is shown
        case 1:
            lblBlue.destroy()
            lblRed.destroy()
            txtBlue.destroy()
            txtRed.destroy()
        case 2:
            root.config(bg='red') # Set the background color to white to make the transparent color work
        case 3:
            lblId.destroy()
            txtRiotID.destroy() 
            cbServers.destroy() 
            cbLang.destroy() 
            btnLang.destroy()
            lblBlue.destroy()
            lblRed.destroy()
            txtBlue.destroy()
            txtRed.destroy()
            localGameBtn.destroy() 
            manualEntryBtn.destroy() 
            chkUltimateOnly.destroy()
            btnLocal.destroy()
            fullScreenBtn.grid(row=6, column=0, columnspan=1, pady=10)
            closeBtn.grid(row=6, column=2, columnspan=1, pady=10) # Show the full screen and close buttons after the language is selected and the champ selection is shown
            root.config(bg='red') # Set the background color to white to make the transparent color work

    #gitBtn.destroy()


# Function to toggle full screen with fullScreenBtn NEEDS WORK 
def fullScreen(windowed):
    if windowed:
        root.attributes('-fullscreen', windowed)
        windowed = False
        print(windowed)
    else:
        root.attributes('-fullscreen', windowed)
        windowed = True
        print(windowed) # Debug print to check if the full screen toggle is working correctly
    return windowed

# Function to close the app toggled by closeBtn
def closeApp():
    root.destroy()

def openUrl(url):
    webbrowser.open_new(url)

# Button to call the function that updates the language and starts the champ sel
btnLang=Button(root, text="Show Selection", command=lambda: login(txtRiotID, cbServers, cbLang))
btnLang.grid(row=2, column=1, columnspan=1, pady=10)

fullScreenBtn = Button(root, text="Toggle Full Screen",repeatdelay=100, repeatinterval=100, command=lambda: fullScreen(windowed))
fullScreenBtn.grid_forget() # Hide the button until the language is selected and the champ selection is shown
closeBtn = Button(root, text="Close App", command=closeApp)
closeBtn.grid_forget() # Hide the button until the language is selected and the champ selection is shown

localGameBtn = Button(root, text="Spectating locally", command=lambda: loginLocal())
localGameBtn.grid(row=6, column=2, columnspan=1, padx=10,pady=10, sticky='e')

manualEntryBtn = Button(root, text="Choose the champ manually", command=lambda: manualData())
manualEntryBtn.grid(row=6, column=1, columnspan=1, padx=10,pady=10)

btnLocal = Button(root, text="Get the champs spells", command=lambda: printChampsManual(currVer,lang,champ))
btnLocal.grid_forget()

gitBtn = Button(root, image=gitLogo, command=lambda: openUrl(link), border=0)
gitBtn.image=gitLogo
gitBtn.grid(row=6, column=0, columnspan=1, padx=10,pady=10, sticky='w')

root.mainloop()

