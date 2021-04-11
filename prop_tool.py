"""
How to build - In the terminal from the project root, run:

pyinstaller --onefile --paths=./venv/Lib/site-packages prop_tool.py

Build artifact will be output to ./dist/prop_tool.exe
"""

from tkinter import *
from tkinter import filedialog
from tkinter.font import Font
import json
import chardet

root = Tk()
std_out_text = StringVar()
std_out_text.set("Any output will go here.")
std_out = Label(root, textvariable=std_out_text).grid(row=3, column=1, padx=5, pady=5)
ALPHA_INDEX = 3

def selectDifficultyFile():
    """
    Pops open dialog for selecting the difficulty file to change.
    :return: none
    """
    global difficulty_file_path
    difficulty_file_path = filedialog.askopenfile(initialdir="C:/Program Files (x86)/Steam/steamapps/common/"
                                                             "Beat Saber/Beat Saber_Data/CustomWIPLevels", parent=root,
                                                  mode='r', filetypes=[('Measurement Files', '*.dat')],
                                                  title="Choose Difficulty File...").name
    difficulty_file_name.set("/".join(difficulty_file_path.split('/')[-2:]))


def adjustBrightnessOfRingProp():
    """
    Logic for altering the brightness of the lights. Json in Python is not pretty, that's my excuse :)
    :return: none
    """
    multiplier = light_multiplier.get()
    if difficulty_file_path != "":
        try:
            std_out_text.set('Brightening stuff up...')
            with open(difficulty_file_path, "rb") as map_file:
                data = map_file.read()
                map_data = json.loads(data.decode(chardet.detect(data)['encoding']))
            for i in range(len(map_data["_events"])):
                if "_customData" in map_data["_events"][i].keys():
                    if "_lightID" in map_data["_events"][i]["_customData"].keys() and "_color" in map_data["_events"][i][
                        "_customData"].keys():
                        for j in range(len(map_data["_events"][i]["_customData"]["_color"])):
                            if j == ALPHA_INDEX:
                                pass
                            else:
                                map_data["_events"][i]["_customData"]["_color"][j] *= float(multiplier)
            std_out_text.set('Done! Made all the ring prop lights ' + multiplier + ' times as bright.')
            with open(difficulty_file_path, "w") as map_file:
                map_file.write(json.dumps(map_data))
        except Exception as e:
            std_out_text.set('Something went wrong. Is your path correct? Did you choose a file first?')


def changeRingPropEventsToOnsAndOffs():
    """
    Logic for converting any lightID lights to solids.
    :return: none
    """
    if difficulty_file_path != "":
        try:
            std_out_text.set('Brightening stuff up...')
            with open(difficulty_file_path, "rb") as map_file:
                data = map_file.read()
                map_data = json.loads(data.decode(chardet.detect(data)['encoding']))
            for i in range(len(map_data["_events"])):
                if "_customData" in map_data["_events"][i].keys():
                    if "_lightID" in map_data["_events"][i]["_customData"].keys() and int(
                            map_data["_events"][i]["_value"]) not in [0, 5]:
                        map_data["_events"][i]["_value"] = 5
            std_out_text.set('Done! Changed all Fades and Flashes on individual rings to Ons.')
            with open(difficulty_file_path, "w") as map_file:
                map_file.write(json.dumps(map_data))
        except Exception as e:
            std_out_text.set('Something went wrong. Is your path correct? Did you choose a file first?')


# Bullet sucks at coding lmao yoinking Tranqs code
def changePropEventsFromOffsToOns():
    """
    Logic for converting any lightID Off events into invisible Ons
    :return: none
    """
    if difficulty_file_path != "":
        try:
            std_out_text.set('Brightening stuff up...')
            with open(difficulty_file_path, "rb") as map_file:
                data = map_file.read()
                map_data = json.loads(data.decode(chardet.detect(data)['encoding']))
            for i in range(len(map_data["_events"])):
                if "_customData" in map_data["_events"][i].keys():
                    if "_lightID" in map_data["_events"][i]["_customData"].keys() and map_data["_events"][i]["_value"] == 0: # Off Event

                        j = i # Look at previous events of same type and event to On of previous color
                        while j > 0:
                            j -= 1
                            if map_data["_events"][i]["_type"] == map_data["_events"][j]["_type"]:
                                
                                # Blue
                                if int(map_data["_events"][j]["_value"]) in {1,2,3}:
                                    map_data["_events"][i]["_value"] = 1
                                    map_data["_events"][i]["_customData"]["_color"] = [0,0,0,0]

                                # Red
                                elif int(map_data["_events"][j]["_value"]) in {5,6,7}:
                                    map_data["_events"][i]["_value"] = 5
                                    map_data["_events"][i]["_customData"]["_color"] = [0,0,0,0]

                                # Off - Don't bother
                                break

            std_out_text.set('Done! Changed all prop Offs to matching Ons with invisible colour.')
            with open(difficulty_file_path, "w") as map_file:
                map_file.write(json.dumps(map_data))
        except Exception as e:
            std_out_text.set('Something went wrong. Is your path correct? Did you choose a file first?')


# UI code
difficulty_file_name = StringVar()
difficulty_file_name.set("Waiting for file selection...")

difficulty_file_path = ""

difficulty_file_label = Label(root, textvariable=difficulty_file_name).grid(row=0, column=0, padx=5, pady=5)

brighten_btn = Button(root, text="Brighten", command=adjustBrightnessOfRingProp)
brighten_btn.grid(row=2, column=0, padx=5, pady=5)
set_prop_lights_to_on_btn = Button(root, text="Set Ring Prop lights to On and Off only",
                                   command=changeRingPropEventsToOnsAndOffs)
set_prop_lights_to_on_btn.grid(row=1, column=1, padx=5, pady=5)
choose_difficulty_btn = Button(root, text="Choose Difficulty File", command=selectDifficultyFile)
choose_difficulty_btn.grid(row=0, column=1, padx=5, pady=5)
light_multiplier = Spinbox(values=(0.5, 0.75, 0.9, 1.1, 1.5, 2),
                           font=Font(family='Helvetica', size=16, weight='bold'))
light_multiplier.grid(row=3, column=0, padx=5, pady=5)

# propOff Button
prop_off_on_btn = Button(root, text="Change Prop Offs to invisible Ons",
                         command=changePropEventsFromOffsToOns)
prop_off_on_btn.grid(row=2, column=1, padx=5, pady=5)

if __name__ == "__main__":
    root.mainloop()
