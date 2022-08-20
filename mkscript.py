# ***********************************************
# *  Copyright (c) 2022 InimicalPart 
# *  All rights reserved.
# *
# *  This program is under the MIT license.
# ***********************************************
import random, time, os, string, keyboard, os, win32gui
from pathlib import Path
from colorama import Fore, init
from threading import Thread
init()
arr = []
mainFile = ""
def getRandomId():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))
os.system("title MKSCRIPT_" + getRandomId()) # This sets the title of the cmd prompt to "MKSCRIPT_" and then 16 random letters/digits. This allows the program to know when this window is focused. 
time.sleep(0.1) # wait a bit so the title can be set
title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
def blockIsFocus(): # Block up and down arrows when window is focused (prevents user from accessing python history by accident)
    isBlocked = False
    while True:
        time.sleep(0.1)
        othertitle = win32gui.GetWindowText(win32gui.GetForegroundWindow()) # Save new title to a variable so it doesnt get get it twice which results in slowing down the pc
        if title == othertitle and isBlocked == False:
            keyboard.block_key("up")
            keyboard.block_key("down")
            # This blocks the up and down key when the terminal is focused, this is to prevent accessing the python history and breaking everything.
            isBlocked = True
        if title != othertitle and isBlocked == True:
            keyboard.unblock_key("up")
            keyboard.unblock_key("down")
            # Of course we don't want the keys to be blocked when the user wants to do something else, so as soon as the window loses focus, the up and down keys get unblocked.
            isBlocked = False


def selectFile(): #Select a file to be edited, allows the user to create one too
    global mainFile
    paths = []
    for path in Path(os.path.join(os.path.dirname(__file__), "scripts")).rglob("*.pycro"):
        paths.append(str(path.name))
    for path in range(len(paths)):
        print(str(path) + ": " + paths[path])
    if len(paths) > 0:
        print("\nSelect one of the files to modify, to create a new one, type 'c'")
    option = input("option> ") if len(paths)>0 else "c"
    if option == "c":
        print("What do you want the file to be called? (extension gets added automatically)")
        fileName = input("filename> ")
        with open(os.path.join(os.path.dirname(__file__), "scripts", fileName + ".pycro"), "w") as f:
            f.write("")
            f.close()
        mainFile = str(Path(os.path.join(os.path.dirname(__file__), "scripts", fileName + ".pycro")))
    else:
        if int(option) in range(len(paths)):
            mainFile = str(Path(paths[int(option)]))
        else:
            print("Invalid Option!")
            exit()
        





selectFile()
with open(mainFile,"r") as f:
    arr = str(f.read()).splitlines()
# keyboard.wait()
Thread(target=blockIsFocus, name="keyBlocker", daemon=True).start()
def numbersBetween(a,b):
    return list(range(a,b+1))

accepted = [*string.ascii_letters] + [*string.digits] + ["ENTER","DELETE","HOME","INSERT","PAGEUP","PAGEDOWN","UP","UPARROW","DOWN","DOWNARROW","LEFT","LEFTARROW","RIGHT","RIGHTARROW","TAB","END","ESC","ESCAPE","SPACE","PAUSE","BREAK","CAPSLOCK","NUMLOCK","PRINTSCREEN","SCROLLLOCK"]
for i in range(24):
    accepted.append("f"+str(i+1))
    accepted.append("F"+str(i+1))

befnAft = 10
line = 0
interval = 0.1
def getGrabLine():
    tempLine = line
    b = True
    while b:
        tempGrabLine = numbersBetween(tempLine-befnAft,tempLine+befnAft)
        if tempGrabLine[-1] > len(arr)-1: tempLine-=1
        else: b = False; return tempGrabLine;
grabLine = getGrabLine()
os.system('cls')

def displayLines():
    linesToDisplay = []
    for num in grabLine:
        try:
            if num < 0: grabLine.append(grabLine[-1] + 1); continue
            if num == line:
                linesToDisplay.append(Fore.LIGHTGREEN_EX + str(num) + ": " + arr[num] + Fore.RESET)
            else:
                linesToDisplay.append(str(num) + ": " + arr[num])
        except:pass
    #print using sys.stdout.write instead of print
    if len(linesToDisplay) == 0:
        linesToDisplay.append(Fore.LIGHTRED_EX + "No lines, use 'a' to add a new line" + Fore.RESET)
    print("\r" + '\n'.join(linesToDisplay))

a = True
infoDisplayed = False
pauseOriginalKeys = False
displayLines()
print("\nPress 'h' for help.")
flippedDict = {}
import json
try:
    with open("scripts.json","r") as f:
        text = str(f.read())
        if text == "": text = "{}"
        # print(text)
        loaded = json.loads(text)
        for item in loaded:
            flippedDict[loaded[item]] = item
        # print(loaded,flippedDict)
except Exception as e: print(e)
def getInfo(infoLine):
    lineString = arr[line]
    if lineString.startswith("REM ") or lineString.startswith("@REM "): return f"Line {infoLine}: This line is a comment. It won't be processed by the main script. ex. REM This is a comment." 
    elif lineString.startswith("DEFAULTDELAY ") or lineString.startswith("DEFUALT_DELAY "): return f"Line {infoLine}: This line sets the default delay between actions. This delay is set in milliseconds (ms). ex. DEFAULTDELAY 1000" 
    elif lineString.startswith("DELAY "): return f"Line {infoLine}: This line causes the program to wait for the milliseconds (ms) that the action provides. ex. DELAY 1000" 
    elif lineString.startswith("STRING "): return f"Line {infoLine}: This line types out the arguments as a keyboard. ex. STRING Hello World!" 
    elif lineString.startswith("GUI "): return f"Line {infoLine}: This line executes the Windows key and the button specified in the arguments. ex. GUI r" 
    elif lineString == "MENU": return f"Line {infoLine}: This line opens the Windows start menu." 
    elif lineString.startswith("CTRL ") or lineString.startswith("CONTROL "): return f"Line {infoLine}: This line allows the user to create a combination of keys where the first one starts with CTRL. ex. CTRL SHIFT ESC" 
    elif lineString.startswith("SHIFT "): return f"Line {infoLine}: This line allows the user to create a combination of keys where the first one starts with SHIFT. ex. SHIFT TAB" 
    elif lineString.startswith("ALT "): return f"Line {infoLine}: This line allows the user to create a combination of keys where the first one starts with ALT. ex. ALT SHIFT Z" 
    elif lineString.startswith("REPEAT ") or lineString.startswith("REPLAY "): return f"Line {infoLine}: This line repeats the previous line the amount of times specified by the arguments. ex. REPEAT 5" 
    elif lineString in accepted: return f"Line {infoLine}: This line presses on the key specified. ex. F11" 
    elif lineString == "REPEATSTART": return f"Line {infoLine}: This line annotates a start of a loop" 
    elif lineString.startswith("REPEATEND "): return f"Line {infoLine}: This line annotates the end of a loop. It runs the actions that are specified by REPEATSTART. The amount of times that it should loop are specified in the arguments of REPEATEND. ex.\nREPEATSTART\nSTRING Hello World!\nENTER\REPEATEND 3" 
    elif lineString.startswith("MOVEMOUSE "): return f"Line {infoLine}: This line moves the mouse to the specified X and Y coords. ex. MOVEMOUSE 150 150" 
    elif lineString.startswith("MOVEMOUSEREL "): return f"Line {infoLine}: This line moves the mouse relative to it's current position. The X and Y specified by the arguments are added to the current position. A duration of how long the mouse should move can be specified in seconds. ex. MOVEMOUSEREL 150 -30 3" 
    elif lineString.startswith("DRAGMOUSE "): return f"Line {infoLine}: This line drags the mouse from X1 Y1 to X2 Y2. A duration can be specified in seconds. ex. DRAGMOUSE 0 0 200 200 3" 
    elif lineString.startswith("DRAGMOUSEREL "): return f"Line {infoLine}: This line drags the mouse relative to it's current position. The X and Y specified by the arguments are added to the current position. A duration of how long the mouse should drag can be specified in seconds. ex. DRAGMOUSEREL 150 150 2" 
    elif lineString == "LMB" or lineString.startswith("LMB "): return f"Line {infoLine}: This line clicks the left button on the mouse. An X and Y argument can be specified. ex. LMB 10 20" 
    elif lineString == "RMB" or lineString.startswith("RMB "): return f"Line {infoLine}: This line clicks the right button on the mouse. An X and Y argument can be specified. ex. RMB 10 20"
    elif lineString == "MMB" or lineString.startswith("MMB "): return f"Line {infoLine}: This line clicks the middle (scroll wheel) button on the mouse. An X and Y argument can be specified. ex. MMB 10 20"
    elif lineString.startswith("HOLD "): return f"Line {infoLine}: This line holds down a key. ex. HOLD LMB" 
    elif lineString.startswith("RELEASE "): return f"Line {infoLine}: This line releases a key that is held down by HOLD. ex. RELEASE LMB" 
    elif lineString.startswith("SCROLL "): return f"Line {infoLine}: This line scrolls the amount that is specified by the arguments, a positive numbers scrolls up, a negative number scrolls down. ex. SCROLL 1000" 
    elif lineString.startswith("HSCROLL "): return f"Line {infoLine}: This line scrolls horizontally the amount that is specified by the arguments, a positive numbers scrolls right, a negative number scrolls left. ex. HSCROLL 1000" 
    elif lineString.startswith("SCREENSHOT "): return f"Line {infoLine}: This line takes a screenshot of the primary monitor and saves it to the path specified by the arguments. ex. SCREENSHOT C:\\funimg.png" 
    elif lineString == "QUIT" or lineString == "EXIT": return f"Line {infoLine}: This line stops the execution of the script." 
    elif lineString == "PAUSE": return f"Line {infoLine}: This line pauses the script until the user presses enter on the terminal screen." 
    elif lineString.startswith("FOS "): return f"Line {infoLine}: This line finds an image on the primary screen and saves the position from the top side, position from the left side, the width and the height to a variable specified in arguments. ex. FOS iwanttofindthis.png = $XYZ" 
    elif lineString.startswith("FCOS "): return f"Line {infoLine}: This line finds an image on the primary screen and saves the X and Y coordinates of the middle of the found image on screen and saves it to a variable specified in arguments. ex. FCOS iwanttofindthis.png = $XYZ" 
    elif lineString.startswith("IF "): return f"Line {infoLine}: This line creates an IF statement, The condition has to be specified in parentheses. The statement also requires a unique identifier specified in square brackets. ex. IF ($XYZ == None) [3f2gGde4]" 
    elif lineString.startswith("ELSE"): return f"Line {infoLine}: This line annotates that if the IF statement is false, the following actions should run. This requires to have the same unique identifier as the IF statement. ex. ELSE [3f2gGde4]"
    elif lineString.startswith("ENDIF"): return f"Line {infoLine}: This line annotates that the IF statement ends here. This requires to have the same unique identifier as the IF statement. ex. ENDIF [3f2gGde4]" 
    elif lineString.startswith("ALERT "): return f"Line {infoLine}: This line shows an alert to the user with a custom message specified in arguments." 
    elif lineString.startswith("CONFIRM "): return f"Line {infoLine}: This line shows a confirmation alert to the user with an OK button and a CANCEL button. The output is saved to the specified variable. ex. CONFIRM Are you sure you want to delete this file? = $XYZ" 
    elif lineString.startswith("PROMPT "): return f"Line {infoLine}: This line shows a prompt where the user can type. The output is saved to the specified variable. ex. PROMPT What do you want the folder to be called? = $XYZ" 
    else: return "Line " + str(infoLine) + ": Unknown."
def editMode(addMode=False):
    global pauseOriginalKeys, grabLine
    if addMode == False:
        if len(arr) < 1: 
            print("No line selected, can't edit. Use 'a' to add a new line")
            pauseOriginalKeys = False
            return
        print("Currently editing line: {}, {}".format(line, arr[line]))
        print("'c' or 'cancel' to cancel.")
        print("What do you want to change the line to? (PREVIOUS VALUE WILL BE OVERWRITTEN!!)")
    else:
        if len(arr) >= 1:
            print("Adding new line below line: {}, {}".format(line, arr[line]))
        else:
            print("Adding a new line")
        print("'c' or 'cancel' to cancel.")
        print("What do you want to set the new line to?")
        if len(arr) >= 1:
            arr.insert(line, "@REM TEMPLATE, YOU SHOULDNT SEE THIS")
        else:
            arr.append("@REM TEMPLATE, YOU SHOULDNT SEE THIS")

    allThings = []
    allThings.append("1. Comment (REM)")
    allThings.append("2. Default Delay (DEFAULTDELAY)")
    allThings.append("3. Delay (DELAY)")
    allThings.append("4. Type (STRING)")
    allThings.append("5. Win + ? (GUI)")
    allThings.append("6. Start Menu (MENU)")
    allThings.append("7. Control (CTRL)")
    allThings.append("8. Shift (SHIFT)")
    allThings.append("9. Alt (ALT)")
    allThings.append("10. Repeat Last Action (REPEAT)")
    allThings.append("11. Press a key")
    allThings.append("12. Annotate Start Loop (REPEATSTART)")
    allThings.append("13. Annotate End and Run Loop (REPEATEND)")
    allThings.append("14. Move Mouse (MOVEMOUSE)")
    allThings.append("15. Move Mouse Relative (MOVEMOUSEREL)")
    allThings.append("16. Drag Mouse (DRAGMOUSE)")
    allThings.append("17. Drag Mouse Relative (DRAGMOUSEREL)")
    allThings.append("18. Left Click (LMB)")
    allThings.append("19. Right Click (RMB)")
    allThings.append("20. Middle Click (MMB)")
    allThings.append("21. Hold down a key (HOLD)")
    allThings.append("22. Release a key (RELEASE)")
    allThings.append("23. Scroll (SCROLL)")
    allThings.append("24. Horizontal Scroll (HSCROLL)")
    allThings.append("25. Take a screenshot (SCREENSHOT)")
    allThings.append("26. Stop Script Execution (QUIT)")
    allThings.append("27. Pause (PAUSE)")
    allThings.append("28. Find On Screen (FOS)")
    allThings.append("29. Find Center On Screen (FCOS)")
    allThings.append("30. If Statement (IF)")
    allThings.append("31. Else Statement (ELSE)")
    allThings.append("32. End an IF Statement (ENDIF)")
    allThings.append("33. Alert box (ALERT)")
    allThings.append("34. Confirmation box (CONFIRM)")
    allThings.append("35. Prompt box (PROMPT)")
    print("\n".join(allThings))
    output = input("Option> ")
    if output.lower() == "cancel" or output.lower() == "c":
        pauseOriginalKeys = False
        if addMode: del arr[line]
        print("Cancelled")
        return
    try:
        output = int(output)
    except: 
        print("Must be a number!")
        if addMode: del arr[line]
        pauseOriginalKeys = False
        return
    
    if output == 1:
        #! Comment (REM)
        print("What do you want to comment?")
        arr[line] = "@REM " + input("Comment> ")
    elif output == 2:
        #! Default Delay (DEFAULTDELAY)
        print("How long should the interval between actions be? (in milliseconds)")
        arr[line] = "DEFAULTDELAY " + input("ms> ")
    elif output == 3:
        #! Delay (DELAY)
        print("How long should the program wait before executing the next action? (in milliseconds)")
        arr[line] = "DELAY " + input("ms> ")
    elif output == 4:
        #! Type (STRING)
        print("What should the program type out?")
        arr[line] = "STRING " + input("text> ")
    elif output == 5:
        #! Win + ? (GUI)
        print("What key should be press along side the Windows key?")
        arr[line] = "GUI " + input("key> ")
    elif output == 6:
        #! Start Menu (MENU)
        arr[line] = "MENU"
    elif output == 7:
        #! Control (CTRL)
        print("What key(s) should be pressed along side the CTRL key? (separate by spaces)")
        arr[line] = "CTRL " + input("key(s)> ")
    elif output == 8:
        #! Shift (SHIFT)
        print("What key(s) should be pressed along side the SHIFT key? (separate by spaces)")
        arr[line] = "SHIFT " + input("key(s)> ")
    elif output == 9:
        #! Alt (ALT)
        print("What key(s) should be pressed along side the ALT key? (separate by spaces)")
        arr[line] = "ALT " + input("key(s)> ")
    elif output == 10:
        #! Repeat Last Action (REPEAT)
        print("How many times do you want to repeat the last line?")
        arr[line] = "REPEAT " + input("times> ")
    elif output == 11:
        #! Press a key
        print("What key do you want to press?")
        arr[line] = input("key> ")
    elif output == 12:
        #! Annotate Start Loop (REPEATSTART)
        arr[line] = "REPEATSTART"
    elif output == 13:
        #! Annotate End and Run Loop (REPEATEND)
        print("How many times do you want to repeat?")
        arr[line] = "REPEATEND " + input("times> ")
    elif output == 14:
        #! Move Mouse (MOVEMOUSE)
        print("To what coordinates do you want to move the mouse to? Leave blank or type 'None' to use the current mouse position.")
        x = input("x> ")
        x = x if x!="" else "None"
        y = input("y> ")
        y = y if y!="" else "None"
        if x=="None" and y=="None":
            print("Both values cant be None/blank")
            if addMode: del arr[line]
            return
        print("How long should the movement take? (in seconds). Leave blank for default.")
        duration = input("duration> ")
        arr[line] = str(f"MOVEMOUSE {x} {y} {duration}").strip()
    elif output == 15:
        #! Move Mouse Relative (MOVEMOUSEREL)
        print("By how many coordinates should the mouse move? Leave blank or type 'None' to use the current mouse position.")
        x = input("x> ")
        x = x if x!="" else "None"
        y = input("y> ")
        y = y if y!="" else "None"
        if x=="None" and y=="None":
            print("Both values cant be None/blank")
            if addMode: del arr[line]
            return
        print("How long should the movement take? (in seconds). Leave blank for default.")
        duration = input("duration> ")
        arr[line] = str(f"MOVEMOUSEREL {x} {y} {duration}").strip()
    elif output == 16:
        #! Drag Mouse (DRAGMOUSE)
        print("To what coordinates do you want to drag the mouse?")
        x = input("x> ")
        y = input("y> ")
        print("With what button? (left, right, middle). Leave blank to use default. NOTE: if you leave this blank, you can't specify the duration in the next step.")
        button = input("btn> ")
        duration = ""
        if button != "":
            print("How long should the movement take? (in seconds). Leave blank for default.")
            duration = input("duration> ")
        arr[line] = str(f"DRAGMOUSE {x} {y} {button} {duration}".strip())
    elif output == 17:
        #! Drag Mouse Relative (DRAGMOUSEREL)
        print("To what coordinates from the current mouse position do you want to drag the mouse to?")
        x = input("x> ")
        y = input("y> ")
        print("With what button? (left, right, middle). Leave blank to use default. NOTE: if you leave this blank, you can't specify the duration in the next step.")
        button = input("btn> ")
        duration = ""
        if button != "":
            print("How long should the movement take? (in seconds). Leave blank for default.")
            duration = input("duration> ")
        arr[line] = str(f"DRAGMOUSEREL {x} {y} {button} {duration}".strip())
    elif output == 18:
        #! Left Click (LMB)
        print("On what coordinates do you want to click? Leave blank to click at current mouse position")
        x = input("x> ")
        y = input("y> ") if x != "" else ""
        arr[line] = str(f"LMB {x} {y}").strip()
    elif output == 19:
        #! Right Click (RMB)
        print("On what coordinates do you want to click? Leave blank to click at current mouse position")
        x = input("x> ")
        y = input("y> ") if x != "" else ""
        arr[line] = str(f"RMB {x} {y}").strip()
    elif output == 20:
        #! Middle Click (MMB)
        print("On what coordinates do you want to click? Leave blank to click at current mouse position")
        x = input("x> ")
        y = input("y> ") if x != "" else ""
        arr[line] = str(f"MMB {x} {y}").strip()
    elif output == 21:
        #! Hold down a key (HOLD)
        print("What key/button do you want to hold down?")
        arr[line] = "HOLD " + str(input("key/button> "))
    elif output == 22:
        #! Release a key (RELEASE)
        print("What key/button do you want to release?")
        arr[line] = "RELEASE " + str(input("key/button> "))
    elif output == 23:
        #! Scroll (SCROLL)
        print("How many pixels do you want to scroll? (positive number scrolls up, negative number scrolls down")
        arr[line] = "SCROLL " + str(input("amount> "))
    elif output == 24:
        #! Horizontal Scroll (HSCROLL)
        print("How many pixels do you want to scroll? (positive number scrolls right, negative number scrolls left")
        arr[line] = "HSCROLL " + str(input("amount> "))
    elif output == 25:
        #! Take a screenshot (SCREENSHOT)
        print("Where should the image be saved? You can specify a full path (C:\\test\\screenshot.png) or just the name (screenshot.png)")
        arr[line] = "SCREENSHOT " + str(input("path> "))
    elif output == 26:
        arr[line] = "EXIT"
    elif output == 27:
        arr[line] = "PAUSE"
    elif output == 28:
        print("Where is the image that you want to find located?")
        path = str(input("path> "))
        print("In what variable do you want to store the result in? (stores: left, top, width, height)")
        variableName = "$" + str(input("varname> "))
        arr[line] = f"FOS {path} = {variableName}"
    elif output == 29:
        print("Where is the image that you want to find located?")
        path = str(input("path> "))
        print("In what variable do you want to store the result in? (stores: x, y)")
        variableName = "$" + str(input("varname> "))
        arr[line] = f"FCOS {path} = {variableName}"
    elif output == 30:
        print("What is the condition that you are checking? (works like python). You can specify a variable by doing '$' and then the variable name")
        condition = str(input("condition> "))
        print("What unique identifier should be used? Leave blank to generate a custom one. (The unique identifier is specified on the ELSE statement and the ENDIF statement)")
        uniqIdent = str(input("unique> "))
        uniqIdent = uniqIdent if uniqIdent == "" else getRandomId()
        arr[line] = f"IF ({condition}) [{uniqIdent}]"
    elif output == 31:
        print("What is the unique identifier? (specified in the IF statement that this ELSE statement is gonna be connected to)")
        uniqIdent = str(input("unique> "))
        arr[line] = f"ELSE [{uniqIdent}]"
    elif output == 32:
        print("What is the unique identifier? (specified in the IF statement that this ENDIF statement is gonna be connected to)")
        uniqIdent = str(input("unique> "))
        arr[line] = f"ENDIF [{uniqIdent}]"
    elif output == 33:
        print("What message would you want to alert? Variables can be specified by using '$' and then the variable name")
        msg = str(input("msg> "))
        arr[line] = f"ALERT " + msg
    elif output == 34:
        print("What message would you like to alert? (Will show an OK and CANCEL button)")
        msg = str(input("msg> "))
        print("In what variable do you want to store the result in? (stores: 'OK' or 'CANCEL')")
        variableName = str(input("varname> "))
        arr[line] = f"CONFIRM {msg} = {variableName}"
    elif output == 35:
        print("What message would you like to alert?")
        msg = str(input("msg> "))
        print("In what variable do you want to store the result in? (stores: the user input")
        variableName = str(input("varname> "))
        arr[line] = f"PROMPT {msg} = {variableName}"
    else:
        print("Invalid option!")
        if addMode: del arr[line]
        pauseOriginalKeys = False
        return

    if addMode and len(arr)>=2: arr[line], arr[line+1] = arr[line+1], arr[line]
    grabLine = getGrabLine()
    os.system("cls")
    displayLines()
    pauseOriginalKeys = False

    return

while a:
    try:
        if win32gui.GetWindowText(win32gui.GetForegroundWindow()) == title:
            if keyboard.is_pressed('down') and not keyboard.is_pressed("ctrl") and pauseOriginalKeys == False:
                if line == len(arr)-1:
                    continue
                infoDisplayed = False
                line += 1
                grabLine = getGrabLine()
                os.system("cls")
                displayLines()
            elif keyboard.is_pressed('up') and not keyboard.is_pressed("ctrl") and pauseOriginalKeys == False:
                if line == 0:
                    continue
                infoDisplayed = False
                line -= 1
                grabLine = getGrabLine()
                os.system("cls")
                displayLines()
            
            if keyboard.is_pressed('down') and  keyboard.is_pressed("ctrl") and pauseOriginalKeys == False:
                if line == len(arr)-1:
                    continue
                if len(arr)<2: continue
                infoDisplayed = False
                arr[line], arr[line+1] = arr[line+1], arr[line]
                line+=1
                grabLine = getGrabLine()
                os.system("cls")
                displayLines()
            elif keyboard.is_pressed('up') and  keyboard.is_pressed("ctrl") and pauseOriginalKeys == False:
                if line == 0:
                    continue
                if len(arr)<2: continue
                infoDisplayed = False
                arr[line], arr[line-1] = arr[line-1], arr[line]
                line-=1
                grabLine = getGrabLine()
                os.system("cls")
                displayLines()
            if keyboard.is_pressed("shift") and pauseOriginalKeys == False:
                interval = 0.05
            else:
                interval = 0.1
            if keyboard.is_pressed("i") and pauseOriginalKeys == False and infoDisplayed == False:
                keyboard.send("backspace")
                infoDisplayed = True
                print("\n" + getInfo(line))
            if keyboard.is_pressed("e") and pauseOriginalKeys == False:
                infoDisplayed = False
                pauseOriginalKeys = True
                grabLine = getGrabLine()
                os.system("cls")
                displayLines()
                print("\n\n"+"="*os.get_terminal_size().columns)
                keyboard.send("backspace")
                editMode()
            if keyboard.is_pressed("a") and pauseOriginalKeys == False:
                infoDisplayed = False
                pauseOriginalKeys = True
                grabLine = getGrabLine()
                os.system("cls")
                displayLines()
                print("\n\n"+"="*os.get_terminal_size().columns)
                keyboard.send("backspace")
                editMode(True)
            if keyboard.is_pressed("g") and pauseOriginalKeys == False:
                keyboard.send("backspace")
                infoDisplayed = False
                pauseOriginalKeys = True
                grabLine = getGrabLine()
                os.system("cls")
                displayLines()
                print("\n\n"+"="*os.get_terminal_size().columns)
                print("There are a total of " + str(len(arr)-1) + " lines. Which line do you want to go to? 'cancel' to cancel")
                newLine = input("Line> ")
                if newLine.lower() == "cancel" or newLine.lower() == "c":
                    grabLine = getGrabLine()
                    os.system("cls")
                    displayLines()
                    pauseOriginalKeys = False
                    continue
                try:
                    newLine = int(newLine)
                except:
                    print("Line number must be a number!")
                    pauseOriginalKeys = False
                    continue
                if newLine < 0 or newLine > len(arr)-1:
                    print("Invalid Line Number!")
                    pauseOriginalKeys = False
                    continue
                line = newLine
                grabLine = getGrabLine()
                os.system("cls")
                displayLines()
                pauseOriginalKeys = False
            if keyboard.is_pressed("d") and pauseOriginalKeys == False:
                keyboard.send("backspace")
                infoDisplayed = False
                pauseOriginalKeys = True
                grabLine = getGrabLine()
                os.system("cls")
                displayLines()
                print("\n\n"+"="*os.get_terminal_size().columns)
                print("Are you sure you want to delete line " + str(line) + "? Line " + str(line) + " is:",arr[line])
                output = input("yes/no> ")
                keyboard.send("backspace")
                keyboard.send("backspace")
                keyboard.send("backspace")

                if output.lower() == "yes" or output.lower() == "y":
                    del arr[line]
                    if line != 0:
                        line-=1
                    grabLine = getGrabLine()
                    os.system("cls")
                    displayLines()
                    pauseOriginalKeys = False
                else:
                    print("Cancelled.")
                    pauseOriginalKeys = False
            if keyboard.is_pressed("q") and pauseOriginalKeys == False:
                keyboard.send("backspace")
                a = False
            if keyboard.is_pressed("c") and pauseOriginalKeys == False:
                grabLine = getGrabLine()
                os.system("cls")
                displayLines()
                keyboard.send("backspace")
            if keyboard.is_pressed("z") and pauseOriginalKeys ==False:
                keyboard.send("backspace")
                infoDisplayed = False
                pauseOriginalKeys = True
                grabLine = getGrabLine()
                os.system("cls")
                displayLines()
                print("\n\n"+"="*os.get_terminal_size().columns)
                if mainFile in flippedDict:
                    print("This script has the hotkey: " + " + ".join(flippedDict[mainFile].split("#")[0].upper().split("+")) + " assigned.")
                else:
                    print("This script has no hotkey assigned.")
                
                print("Please put in the hotkey that you want use. "+"Leave blank to delete the currently assigned hotkey." if mainFile in flippedDict else "" +" Here are some examples on how the hotkey should look like:\nCTRL+SHIFT+X\nalt+shift+q\nCTRL+enter")
                print("'msq' to cancel")
                newhotkey = input("hotkey> ")
                if newhotkey=="":del flippedDict[mainFile];pauseOriginalKeys=False;grabLine = getGrabLine();os.system("cls");displayLines();continue
                elif newhotkey == "msq": pauseOriginalKeys = False;print("Cancelled");continue
                newhotkey = newhotkey.lower()+"#"+getRandomId()
                flippedDict[mainFile] = newhotkey
                grabLine = getGrabLine()
                os.system("cls")
                displayLines()
                pauseOriginalKeys = False
            if keyboard.is_pressed("s") and pauseOriginalKeys == False:
                keyboard.send("backspace")
                pauseOriginalKeys = True
                grabLine = getGrabLine()
                os.system("cls")
                displayLines()
                print("Saving...")
                with open(mainFile, "w+") as f:
                    f.truncate(0)
                    f.flush()
                    f.write("\n".join(arr))
                    f.close()
                with open("scripts.json","w+") as f:
                    f.truncate(0)
                    f.flush()
                    #reflipping dict
                    tempFlipped = {}
                    for item in flippedDict:
                        tempFlipped[flippedDict[item]] = item
                    f.write(json.dumps(tempFlipped))
                    f.close()
                print("Saved.")
                pauseOriginalKeys = False
            if keyboard.is_pressed("h") and pauseOriginalKeys == False:
                keyboard.send("backspace")
                infoDisplayed = False
                pauseOriginalKeys = True
                grabLine = getGrabLine()
                os.system("cls")
                displayLines()
                print("\n\n"+"="*os.get_terminal_size().columns)
                print("\n")
                print("↑ = Move up one line")
                print("↓ = Move down one line")
                print("CTRL + ↑ = Move the selected line up")
                print("CTRL + ↓ = Move the selected line down")
                print("SHIFT (HOLD) = Speed up movement by 2x when holding ↑/↓")
                print("a = Add line below selected line")
                print("c = Refresh Screen")
                print("d = Delete selected line")
                print("e = Edit selected line")
                print("g = Go to line")
                print("z = Assign Hotkey")
                print("i = Get info about selected line")
                print("s = Save")
                print()
                print("q / CTRL + C = Quit")
                print("h = This help page")
                pauseOriginalKeys = False
            time.sleep(interval)
    except KeyboardInterrupt:
        a = False
        break
print("Saving and exiting...")
with open(mainFile, "w+") as f:
    f.truncate(0)
    f.flush()
    f.write("\n".join(arr))
    f.close()
with open("scripts.json","w+") as f:
    f.truncate(0)
    f.flush()
    #reflipping dict
    tempFlipped = {}
    for item in flippedDict:
        tempFlipped[flippedDict[item]] = item
    f.write(json.dumps(tempFlipped))
    f.close()
print("Saved.")
exit()

