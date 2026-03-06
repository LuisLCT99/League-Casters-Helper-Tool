Readme:

- To use this app you have 3 ways:
    - Spectate a live game with a RIOT Id, choosing language for the spells and the server of the RIOT Id → Click "Show Selection"
    - Spectating a game in your computer (live game by being spectator in lobby or a replay) choosing language → Click "Spectating locally"
    - Write the names manually, choosing language first → Click "Choose the champ manually"
- For all the options you can add the champion name along the spells & only printing the ultimate.

- Files in the repo: 
    - main.py # Main GUI 
    - methods.py # Methods to retrieve data
    - dicts.py # Dict to store all languages listed in https://ddragon.leagueoflegends.com/cdn/languages.json & all RIOT Games servers (Not auto-updated yet)
    - requirements.txt # List of required libraries
    - .env.example # Example of the .env file, to store your RIOT Games API KEY
    - dist/League Casting Helper.exe # Executable file for the app

Main screen:

<img width="1026" height="608" alt="Main Screen" src="https://github.com/user-attachments/assets/c73b5d66-e129-4370-aadb-a71ba84139a1" />

Preview of the tool during game spectate:

<img width="1918" height="1079" alt="Preview ingame" src="https://github.com/user-attachments/assets/bcfe3488-34b4-4ef7-b207-db684e25b030" />

Write the names manually:

<img width="1022" height="594" alt="Manual Input" src="https://github.com/user-attachments/assets/34584c2f-6168-4b89-8c3e-a3a799ffe07f" />



- TODO List: 
    - Switch language.
    - Clean the code & remove redundant methods.
    - Write in comboBox to search in the lists.
    - Update graphics to make it more appealing.
    - Save last Lang & Server used
    - Light & Dark mode with switch and auto adjust to system theme

- Past updates
    - ~~Draggable labels to temp fix the problem of not getting the champs in correct order when spectating a ranked game~~
    - ~~**Optional** Character names along the spell names.~~
    - ~~Exit button~~
    - ~~Full screen app~~ (Still needs to be able to comeback to original size)
    - ~~Live data from an actual game~~
    - ~~Live data from a local game/replay~~
    - ~~Only ults to appear (R button)~~
    - ~~Verify boxes are selected and text is not empty~~
