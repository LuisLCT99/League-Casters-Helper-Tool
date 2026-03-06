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
isCheckedR = IntVar()
isCheckedNames = IntVar()
chkUltimateOnly = Checkbutton(root, text="Ultimate Only Mode", onvalue=1, offvalue=0,variable=isCheckedR)
chkUltimateOnly.grid(row=1, column=1, pady=10, padx=10, sticky='w')
chkPrintNames = Checkbutton(root, text='Print Champ Names', onvalue=1, offvalue=0, variable=isCheckedNames)
chkPrintNames.grid(row=1, column=1, pady=10, padx=10, sticky='e')

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

def changeOrder(widget1, widget2, initial): #This function swaps the grid positions of two widgets using their grid information.
    target = widget1.grid_info()
    widget1.grid(row=initial['row'], column=initial['column'])
    widget2.grid(row=target['row'], column=target['column'])

def on_click(event): # This function initiates the drag action when you click on a widget.
    widget = event.widget
    if isinstance(widget, Label):
        start = (event.x,event.y)
        grid_info = widget.grid_info()
        widget.bind("<B1-Motion>", lambda event:drag_motion(event, widget, start))
        widget.bind("<ButtonRelease-1>", lambda event: drag_release(event, widget, grid_info))

def drag_motion(event, widget, start): # This function moves the widget according to the mouse's movement. The lift() method ensures the widget stays on top during the drag.
    x = widget.winfo_x() + event.x - start[0]
    y = widget.winfo_y() + event.y - start[1]
    widget.lift()
    widget.place(x=x, y=y)

def drag_release(event, widget, grid_info): # This function drops the widget and checks where it is released. It swaps the widgets if released over another.
    widget.lower()
    x,y = root.winfo_pointerxy()
    target_widget = root.winfo_containing(x,y)
    if isinstance(target_widget, Label):
        changeOrder(target_widget, widget, grid_info)
    else:
        widget.grid(row=grid_info['row'], column = grid_info['column'])

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
        msgError = tkinter.messagebox.showerror("Error", "The user does not exist.\nTry again with a different Riot ID.")
        print(f"An error occurred: {err}")
        puuid = "ERROR"
        return puuid
    except Exception as err:
        print(f"An error occurred: {err}")
        puuid = "ERROR"
        return

# Get live game info using PUUID
def getLiveGameInfo(puuid, server):
    
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
        msgError = tkinter.messagebox.showerror("Error", "The user is not currently in a game or has streamer mode active \nPlease try again with a different Riot ID.")
        print(f"An error occurred: {err}")
        return
    except Exception as err:
        msgError = tkinter.messagebox.showerror("Error", "The user is not currently in a game or has streamer mode active \nPlease try again with a different Riot ID.")
        print(f"An error occurred: {err}")
        return

# Get the list of champions in the live game
def getChamps(data):
    champIds = []
    playerBlueSide= []
    playerRedSide = []

    for participant in data['participants']:
        champIds.append(participant['championId'])
        if participant['teamId'] == 100:
            playerBlueSide.append(participant['championId'])
        elif participant['teamId'] == 200:
            playerRedSide.append(participant['championId'])
        
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

# Print champion spells 
def printChampSpells3(currVer,lang,champ,lblsLeft, lblsRight, champNamesBlue, champNamesRed):
    for i,lbl in enumerate(lblsLeft, start=0):
        lbl.config(text="") # Clear the label text before displaying new spells
        lbl.grid(row=i, column=0, padx=10, pady=5, sticky='w')
        champPre = champNamesBlue[i]
        champ = champNamesBlue[i]
        champSpells = methods.champSel(currVer,lang,champ)
        if isCheckedNames.get() == 1:
            lbl.config(lbl.config(text=lbl.cget("text") + champPre))
        for spell in champSpells:
            lbl.config(text=lbl.cget("text") + "\n" + spell) # Update the label text to include the spells
            
    for i,lbl in enumerate(lblsRight, start=0):
        lbl.config(text="") # Clear the label text before displaying new spells
        lbl.grid(row=i, column=2, padx=10, pady=5, sticky='e')
        champPre = champNamesRed[i]
        champ = champNamesRed[i]
        champSpells = methods.champSel(currVer,lang,champ)
        if isCheckedNames.get() == 1:
            lbl.config(lbl.config(text=lbl.cget("text") + champPre))
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
        if isCheckedNames.get() == 1:
            lbl.config(lbl.config(text=lbl.cget("text") + "\t" + champ))
        lbl.config(lbl.config(text=lbl.cget("text") +"\t" + champSpells[3])) # Update the label text to include only the ultimate spell
            
    for i,lbl in enumerate(lblsRight, start=0):
        lbl.config(text="") # Clear the label text before displaying new spells
        lbl.grid(row=i, column=2, padx=10, pady=5, sticky='e')
        champ = champNamesRed[i]
        champSpells = methods.champSel(currVer,lang,champ)
        if isCheckedNames.get() == 1:
            lbl.config(lbl.config(text=lbl.cget("text") + champ))
        lbl.config(lbl.config(text=lbl.cget("text") +"\t" + champSpells[3])) # Update the label text to include only the ultimate spell
    destroyWidgets(3)

# Function to be called by the button showing warnings if needed and going to champ spells print (Live game search)
def login(txtRiotID, cbServers, cbLang):
    if cbLang.get() == "Select a language" or cbServers.get() == "Select a server" or txtRiotID.get("1.0", "end-1c") == "": # Check if the user has selected a language, a server and entered a riot ID before proceeding
        msgError = tkinter.messagebox.showerror("Error", "Please select a language,a server and enter a riot IDbefore proceeding.")
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
            if isCheckedR.get() == 1: # Check if the ultimate only mode is selected
                printOnlyUlt(currVer,lang,champ,lblsLeft, lblsRight, champNamesBlue, champNamesRed)
            else:
                printChampSpells3(currVer,lang,champ,lblsLeft, lblsRight, champNamesBlue, champNamesRed)

# Region selector function, chooses a region based on the chosen server
def regionSelector(server):
    print(f"Selected server: {server}") # Debug print to check if the server is being selected correctly
    if (server == 'EUW1' or server == 'EUN1' or server == 'RU' or server == 'TR1' or server == 'ME1'):
        region = 'EUROPE'
    elif (server == 'NA1' or server == 'BR1' or server == 'LA1' or server == 'LA2'):
        region = 'AMERICAS'
    elif (server == 'JP1' or server == 'KR' or server == 'SG2' or server == 'TW2' or server == 'VN2' or server == 'OC1'):
        region = 'ASIA'
    return region

# Function to be called by the button showing warnings if needed and going to champ spells print (Local games)
def loginLocal():
    if cbLang.get() == "Select a language": # Check if the user has selected a language before proceeding
        msgError = tkinter.messagebox.showerror("Error", "Please select a language before proceeding.")
        return
    else:
        lang = langOpts.get(cbLang.get(), "en_US") # Get the selected language code
        data = methods.getLocalGameInfo()
        playerBlueSide,playerRedSide = methods.getChampsLocal(data)
        if isCheckedR.get() == 1: # Check if the ultimate only mode is selected
            printOnlyUltLocal(lang,currVer,champ,lblsLeft, lblsRight, playerBlueSide, playerRedSide)
        else:
            printChampSpellsLocal(currVer,lang,champ,lblsLeft, lblsRight, playerBlueSide, playerRedSide)

# Function to be called by the button with the warnings if you dont select a language
def manualData():
    if cbLang.get() == "Select a language": # Check if the user has selected a language before proceeding
        msgError = tkinter.messagebox.showerror("Error", "Please select a language before proceeding.")
        return
    else:
        lang = langOpts.get(cbLang.get(), "en_US") 
        print(lang)
        getChampsManual()
        return lang

# Removes the comboboxes, labels & creates new ones for the manual input 
def getChampsManual():
    destroyWidgets(0)
    lblBlue.grid(row=0, column=0, pady=10, padx=10, sticky='w')
    txtBlue.grid(row=0, column=1, columnspan=2, pady=10, padx=10, sticky= 'ew')
    lblRed.grid(row=1, column=0, pady=10, padx=10, sticky='w')
    txtRed.grid(row=1, column=1, columnspan=2, pady=10, padx=10, sticky='ew')
    btnLocal.grid(row=2, column=1, pady=10, padx=10)
    return 

# Print spells when you input the names manually
def printChampsManual(currVer,lang,champ):
    lang = langOpts.get(cbLang.get(), "en_US")
    if txtBlue.get("1.0", "end-1c")=="" or txtRed.get("1.0", "end-1c") == "":
        msgError = tkinter.messagebox.showerror("Error", "Fields can't be empty")
        return
    else:
        champSplitBlue = txtBlue.get("1.0", "end-1c").split(',')
        champSplitRed = txtRed.get("1.0", "end-1c").split(',')

    if len(champSplitBlue) > 5 or  len(champSplitRed) > 5:
        msgError = tkinter.messagebox.showerror("Error", "Please write only 5 champs")
        return
    else:
        if isCheckedR.get() == 1: # Check if the ultimate only mode is selected
            for i,lbl in enumerate(lblsLeft, start = 0):
                lbl.config(text="") # Clear the label text before displaying new spells
                lbl.grid(row=i, column=0, padx=10, pady=5, sticky='w')
                champPre = champSplitBlue[i]
                champ = methods.validateNames(champSplitBlue[i])
                champSpells = methods.champSel(currVer,lang,champ)
                if isCheckedNames.get() == 1:
                    lbl.config(text = lbl.config(text=lbl.cget("text") + champPre))
                for spell in champSpells:
                    lbl.config(text=lbl.cget("text") + "\n" + spell) # Update the label text to include the spells
            
            for i,lbl in enumerate(lblsRight, start=0):
                lbl.config(text="") # Clear the label text before displaying new spells
                lbl.grid(row=i, column=2, padx=10, pady=5, sticky='e')
                champPre = champSplitRed[i]
                champ = methods.validateNames(champSplitRed[i])
                champSpells = methods.champSel(currVer,lang,champ)
                if isCheckedNames.get() == 1:
                    lbl.config(text = lbl.config(text=lbl.cget("text") + champPre))
                for spell in champSpells:
                    lbl.config(text=lbl.cget("text") + "\n" + spell) # Update the label text to include the spells
        else:
            for i,lbl in enumerate(lblsLeft, start = 0):
                lbl.config(text="") # Clear the label text before displaying new spells
                lbl.grid(row=i, column=0, padx=10, pady=5, sticky='w')
                champPre = champSplitBlue[i]
                champ = methods.validateNames(champSplitBlue[i])
                champSpells = methods.champSel(currVer,lang,champ)
                if isCheckedNames.get() == 1:
                    lbl.config(lbl.config(text=lbl.cget("text") + champPre))
                lbl.config(lbl.config(text=lbl.cget("text") +"\t" + champSpells[3]))
            
            for i,lbl in enumerate(lblsRight, start=0):
                lbl.config(text="") # Clear the label text before displaying new spells
                lbl.grid(row=i, column=2, padx=10, pady=5, sticky='e')
                champPre = champSplitRed[i]
                champ = methods.validateNames(champSplitRed[i])
                champSpells = methods.champSel(currVer,lang,champ)
                if isCheckedNames.get() == 1:
                    lbl.config(lbl.config(text=lbl.cget("text") + champPre))
                lbl.config(lbl.config(text=lbl.cget("text") +"\t" + champSpells[3]))
    destroyWidgets(3)

# Print spells when watching a live/replay game in your device 
def printChampSpellsLocal(currVer,lang,champ,lblsLeft, lblsRight, playerBlueSide, playerRedSide):
    champNamesBlue = list(playerBlueSide.keys())
    champNamesRed = list(playerRedSide.keys())
    for i,lbl in enumerate(lblsLeft, start=0):
        lbl.config(text="") # Clear the label text before displaying new spells
        lbl.grid(row=i, column=0, padx=10, pady=5, sticky='w')
        champPre = champNamesBlue[i]
        champ = methods.validateNames(champNamesBlue[i])
        champSpells = methods.champSel(currVer,lang,champ)
        if isCheckedNames.get() == 1:
            lbl.config(lbl.config(text=lbl.cget("text") + champPre))
        for spell in champSpells:
            lbl.config(text=lbl.cget("text") + "\n" + spell) # Update the label text to include the spells
            
    for i,lbl in enumerate(lblsRight, start=0):
        lbl.config(text="") # Clear the label text before displaying new spells
        lbl.grid(row=i, column=2, padx=10, pady=5, sticky='e')
        champPre = champNamesRed[i]
        champ = methods.validateNames(champNamesRed[i])
        champSpells = methods.champSel(currVer,lang,champ)
        if isCheckedNames.get() == 1:
            lbl.config(lbl.config(text=lbl.cget("text") + champPre))
        for spell in champSpells:
            lbl.config(text=lbl.cget("text") + "\n" + spell) # Update the label text to include the spells
    destroyWidgets(3) # Destroy the initial widgets after showing the spells to prevent changes while the app is running

# Print spells when watching a live/replay game in your device (ult only version)
def printOnlyUltLocal(lang,currVer,champ,lblsLeft, lblsRight, playerBlueSide, playerRedSide):
    champNamesBlue = list(playerBlueSide.keys())
    champNamesRed = list(playerRedSide.keys())
    for i,lbl in enumerate(lblsLeft, start=0):
        lbl.config(text="") # Clear the label text before displaying new spells
        lbl.grid(row=i, column=0, padx=10, pady=5, sticky='w')
        champPre = champNamesBlue[i]
        champ = methods.validateNames(champNamesBlue[i])
        champSpells = methods.champSel(currVer,lang,champ)
        if isCheckedNames.get() == 1:
            lbl.config(lbl.config(text=lbl.cget("text") + champPre))
        lbl.config(lbl.config(text=lbl.cget("text") + "\n" + champSpells[3])) # Update the label text to include only the ultimate spell
            
    for i,lbl in enumerate(lblsRight, start=0):
        lbl.config(text="") # Clear the label text before displaying new spells
        lbl.grid(row=i, column=2, padx=10, pady=5, sticky='e')
        champPre = champNamesRed[i]
        champ = methods.validateNames(champNamesRed[i])
        champSpells = methods.champSel(currVer,lang,champ)
        if isCheckedNames.get() == 1:
            lbl.config(lbl.config(text=lbl.cget("text") + champPre))
        lbl.config(lbl.config(text=lbl.cget("text") + "\n" + champSpells[3])) # Update the label text to include only the ultimate spell
    destroyWidgets(3)

# Destroy the buttons after showing the spells to prevent changes while the app is running
def destroyWidgets(int):
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
            chkPrintNames.destroy()
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
            chkPrintNames.destroy()
            btnLocal.destroy()
            fullScreenBtn.grid(row=6, column=0, columnspan=1, pady=10)
            closeBtn.grid(row=6, column=2, columnspan=1, pady=10) # Show the full screen and close buttons after the language is selected and the champ selection is shown
            root.config(bg='red') # Set the background color to white to make the transparent color work

# Function to toggle full screen with fullScreenBtn
def fullScreen():
    if root.state() == 'normal':
       root.state('zoomed')
    else:
        root.state('normal')
# Function to close the app toggled by closeBtn
def closeApp():
    root.destroy()

# Open url for github link and possible other social links in the future // link to champ wiki
def openUrl(url):
    webbrowser.open_new(url)

# Button to call the function that updates the language and starts the champ sel
btnLang=Button(root, text="Show Selection", command=lambda: login(txtRiotID, cbServers, cbLang))
btnLang.grid(row=2, column=1, columnspan=1, pady=10)

fullScreenBtn = Button(root, text="Toggle Full Screen",repeatdelay=100, repeatinterval=100, command=lambda: fullScreen())
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


root.bind("<Button-1>", on_click)
root.mainloop()

