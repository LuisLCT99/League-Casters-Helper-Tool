import requests
import threading
from tkinter import *
from tkinter import ttk
import methods
from language import langOpts

# Getting the current version of the game to get the updated list of all the champs (needed as the game updates every 2 weeks and champ releases & reworks can alter the list if stored locally)
versReq = requests.get('https://ddragon.leagueoflegends.com/api/versions.json')
versions = versReq.json()
currVer = versions[0]
champ = ""

# Initialize the main window and all the widgets.
root = Tk()
root.geometry("1000x700")
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
root.attributes('-transparentcolor', 'red')
root.title("League Casting Helper")


cbLang = ttk.Combobox(root, values=list(langOpts.keys()))
cbLang.set("Select a language")
cbLang.grid(row=0, column=0, columnspan=2, pady=10, padx=10)
# lang = "" 
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

# Button to call the function that updates the language and starts the champ sel
btnLang=Button(root, text="Show Selection", command=lambda: updateLang(boxesLeft,boxesRight))
btnLang.grid(row=1, column=0, columnspan=2, pady=10)


root.mainloop()

