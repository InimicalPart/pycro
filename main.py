# ***********************************************
# *  Copyright (c) 2022 InimicalPart 
# *  All rights reserved.
# *
# *  This program is under the MIT license.
# ***********************************************
import re, time, pyautogui, keyboard, string, os, PIL, json
from threading import Thread
from pathlib import Path
defaultDelay = None
pyautogui.FAILSAFE = False
stopExecution = True
safetyKey = "f12"
accepted = [*string.ascii_letters] + [*string.digits] + ["ENTER","DELETE","HOME","INSERT","PAGEUP","PAGEDOWN","UP","UPARROW","DOWN","DOWNARROW","LEFT","LEFTARROW","RIGHT","RIGHTARROW","TAB","END","ESC","ESCAPE","SPACE","PAUSE","BREAK","CAPSLOCK","NUMLOCK","PRINTSCREEN","SCROLLLOCK"]
for i in range(24): accepted += ["f"+str(i+1), "F"+str(i+1)]
def getIndex(a,b):
    for i in range(len(a)):
        if a[i] == b:
            return i
    return -1

def numbersBetween(a,b):
    return list(range(a,b+1))
scriptVariables = {}
def setVar(name, val):
    if name.startswith("$"):
        name = name[1:]
    if name.__contains__("."):
        print("VariableName can't have a dot in it")
        return
    scriptVariables[name] = val

def getVar(name):
    if name.startswith("$"): name = name[1:]
    if name.split(".")[0] in scriptVariables:
        thing = ""
        for i in name.split(".")[1:]: thing += "[\"" + i + "\"]"
        try: return eval("scriptVariables[theName]" + thing)
        except: return None
    else: return None

allScripts = []
for path in Path(os.path.join(os.path.dirname(__file__), "scripts")).rglob("*.pycro"):
    allScripts.append(path)

def getIndex(a,b):
    for i in range(len(a)):
        if a[i] == b:
            return i
    return -1
def lineExec(line, lines, linesNumbers, isRepeating=False):
    lines[line] = lines[line].strip()
    if lines[line] == "":
        if not isRepeating:
            return
        else:
            return lineExec(line-1, lines, True)
    if lines[line].startswith("REM ") or lines[line].startswith("@REM "):
        print("Line " + str(line+1) + " is a comment - " + lines[line])
    elif lines[line].startswith("DEFAULTDELAY ") or lines[line].startswith("DEFUALT_DELAY "):
        args = lines[line].replace("DEFAULTDELAY ","",1).replace("DEFUALT_DELAY ","",1)
        if args == "RESET": args = 100
        print("Line " + str(line+1) + " wants to set the delay between commands to "+args+"ms - " + lines[line])
        pyautogui.PAUSE = int(args) / 1000
    elif lines[line].startswith("DELAY "):
        args = lines[line].replace("DELAY ","",1)
        print("Line " + str(line+1) + " wants to wait for "+args+"ms - " + lines[line])
        time.sleep(int(args) / 1000)
    elif lines[line].startswith("STRING "):
        args = lines[line].replace("STRING ","",1)
        print("Line " + str(line+1) + " wants to write '"+args+"' - " + lines[line])
        pyautogui.typewrite(args)
    elif lines[line].startswith("GUI "):
        args = lines[line].replace("GUI ","",1)
        print("Line " + str(line+1) + " wants to execute WIN + "+args+" - " + lines[line])
        pyautogui.hotkey("win",args)
    elif lines[line] == "MENU":
        print("Line " + str(line+1) + " wants to execute MENU - " + lines[line])
        pyautogui.hotkey("ctrl","esc")
    elif lines[line].startswith("CTRL ") or lines[line].startswith("CONTROL "):
        args = lines[line].replace("CTRL ","",1).replace("CONTROL ","",1)
        print("Line " + str(line+1) + " wants to execute CTRL + "+args+" - " + lines[line])
        exec("pyautogui.hotkey"+str(tuple(["ctrl"] + args.split(" "))))
    elif lines[line].startswith("SHIFT "):
        args = lines[line].replace("SHIFT ","",1)
        print("Line " + str(line+1) + " wants to execute SHIFT + "+args+" - " + lines[line])
        exec("pyautogui.hotkey"+str(tuple(["shift"] + args.split(" "))))
    elif lines[line].startswith("ALT "):
        args = lines[line].replace("ALT ","",1)
        print("Line " + str(line+1) + " wants to execute ALT + "+args+" - " + lines[line])
        exec("pyautogui.hotkey"+str(tuple(["alt"] + args.split(" "))))

    elif lines[line].startswith("REPEAT ") or lines[line].startswith("REPLAY "):
        args = lines[line].replace("REPEAT ","",1).replace("REPLAY ","",1)
        print("Line " + str(line+1) + " wants to repeat line "+str(line-1)+": '"+lines[line-1]+"' "+args+" times - " + lines[line])
        repeatTimes = int(args)
        currentIteration = 0
        while currentIteration < repeatTimes:
            lineExec(line-1, lines, linesNumbers, True)
            currentIteration += 1
    elif lines[line] in accepted:
        if lines[line] == "UPARROW": lines[line] = "UP"
        elif lines[line] == "DOWNARROW": lines[line] = "DOWN"
        elif lines[line] == "LEFTARROW": lines[line] = "LEFT"
        elif lines[line] == "RIGHTARROW": lines[line] = "RIGHT"
        elif lines[line] == "BREAK": lines[line] = "PAUSE"

        print("Line " + str(line+1) + " wants to press "+lines[line])
        pyautogui.press(lines[line])
    #Custom
    elif lines[line] == "REPEATSTART":
        print("Line " + str(line+1) + " annotates a start of a repeat loop - " + lines[line])
    elif lines[line].startswith("REPEATEND "):
        args = lines[line].replace("REPEATEND ","",1)
        # go back in the list and find the start of the loop
        startAnnotationLine = 0
        for i in range(line-1,-1,-1):
            if lines[i] == "REPEATSTART":
                startAnnotationLine = i
                break
        repeatLines = numbersBetween(startAnnotationLine+1, line-1)
        print("Line " + str(line+1) + " annotates the end of a repeat loop, wants to repeat lines ("+str(startAnnotationLine+1)+"-"+str(line-1)+") " + lines[line])
        repeatTimes = int(args)
        currentIteration = 0
        while currentIteration < repeatTimes:
            for line in repeatLines:
                lineExec(line, lines, linesNumbers)
            currentIteration += 1
    elif lines[line].startswith("MOVEMOUSE "):
        args = lines[line].replace("MOVEMOUSE ","",1)
        print("Line " + str(line+1) + " wants to move the mouse to x:"+args.split(" ")[0] + ", y:" + args.split(" ")[1]+" - " + lines[line])
        duration = pyautogui.MINIMUM_DURATION
        splitArgs = args.split(" ")
        splitArgs[0] = None if splitArgs[0]=="None" else int(splitArgs[0])
        splitArgs[1] = None if splitArgs[1]=="None" and splitArgs[0]!="None" else int(splitArgs[1])
        if len(splitArgs) == 3:
            duration = float(splitArgs[2])
        pyautogui.moveTo(x=splitArgs[0], y=args.split(" ")[1], duration=duration)
    elif lines[line].startswith("MOVEMOUSEREL "):
        args = lines[line].replace("MOVEMOUSEREL ","",1)
        print("Line " + str(line+1) + " wants to move the mouse (relative) by x:"+args.split(" ")[0] + ", y:" + args.split(" ")[1]+" - " + lines[line])
        duration = pyautogui.MINIMUM_DURATION
        splitArgs = args.split(" ")
        splitArgs[0] = None if splitArgs[0]=="None" else int(splitArgs[0])
        splitArgs[1] = None if splitArgs[1]=="None" and splitArgs[0]!="None" else int(splitArgs[1])
        if len(splitArgs) == 3:
            duration = float(splitArgs[2])
        pyautogui.move(int(args.split(" ")[0]), int(args.split(" ")[1]), duration=duration)
    elif lines[line].startswith("DRAGMOUSE "):
        args = lines[line].replace("DRAGMOUSE ","",1)
        x = int(args.split(" ")[0])
        y = int(args.split(" ")[1])
        print("Line " + str(line+1) + " wants to drag the mouse to x:" + str(x) + ", y:" + str(y) + " - " + lines[line])
        duration = pyautogui.MINIMUM_DURATION
        button = "left"
        if len(args.split(" ")) >= 3:
            button = args.split(" ")[2].lower()
        if len(args.split(" ")) == 4:
            duration = float(args.split(" ")[3])
        pyautogui.dragTo(x=x, y=y, duration=duration, button=button)
    elif lines[line].startswith("DRAGMOUSEREL "):
        args = lines[line].replace("DRAGMOUSEREL ","",1)
        x = int(args.split(" ")[0])
        y = int(args.split(" ")[1])
        print("Line " + str(line+1) + " wants to drag the mouse (relative) by x:"+str(x)+", y:"+str(y)+" - " + lines[line])
        duration = pyautogui.MINIMUM_DURATION
        button = "left"
        if len(args.split(" ")) >= 3:
            button = args.split(" ")[2].lower()
        if len(args.split(" ")) == 4:
            duration = float(args.split(" ")[3])

        pyautogui.dragRel(x, y, duration=duration)
    elif lines[line] == "LMB" or lines[line].startswith("LMB "):
        args = lines[line].replace("LMB ","",1).replace("LMB","",1)
        x,y = None, None
        if args.split(" ")[0] != "":
            if args.split(" ")[0].startswith("$"):
                x = int(getVar(args.split(" ")[0]))
            else:
                x = int(args.split(" ")[0])
        if len(args.split(" ")) > 1 and args.split(" ")[1] != "":
            if args.split(" ")[1].startswith("$"):
                y = int(getVar(args.split(" ")[1]))
            else:
                y = int(args.split(" ")[1])
        print("Line " + str(line+1) + " wants to press LMB - " + lines[line])
        pyautogui.click(x=x, y=y,button='left')
    elif lines[line] == "RMB" or lines[line].startswith("RMB "):
        args = lines[line].replace("RMB ","",1).replace("RMB","",1)
        x,y = None, None
        if args.split(" ")[0] != "":
            if args.split(" ")[0].startswith("$"):
                x = int(getVar(args.split(" ")[0]))
            else:
                x = int(args.split(" ")[0])
        if len(args.split(" ")) > 1 and args.split(" ")[1] != "":
            if args.split(" ")[1].startswith("$"):
                y = int(getVar(args.split(" ")[1]))
            else:
                y = int(args.split(" ")[1])
        print("Line " + str(line+1) + " wants to press RMB - " + lines[line])
        pyautogui.click(x=x, y=y,button='right')
    elif lines[line] == "MMB" or lines[line].startswith("MMB "):
        args = lines[line].replace("MMB ","",1).replace("MMB","",1)
        x,y = None, None
        if args.split(" ")[0] != "":
            if args.split(" ")[0].startswith("$"):
                x = int(getVar(args.split(" ")[0]))
            else:
                x = int(args.split(" ")[0])
        if len(args.split(" ")) > 1 and args.split(" ")[1] != "":
            if args.split(" ")[1].startswith("$"):
                y = int(getVar(args.split(" ")[1]))
            else:
                y = int(args.split(" ")[1])
        print("Line " + str(line+1) + " wants to press MMB - " + lines[line])
        pyautogui.click(x=x, y=y, button='middle')
    elif lines[line].startswith("HOLD "):
        args = lines[line].replace("HOLD ","",1)
        print("Line " + str(line+1) + " wants to hold "+args+" - " + lines[line])
        if args == "LMB":
            pyautogui.mouseDown(button='left')
        elif args == "RMB":
            pyautogui.mouseDown(button='right')
        elif args == "MMB":
            pyautogui.mouseDown(button='middle')
        else:
            pyautogui.keyDown(args)
    elif lines[line].startswith("RELEASE "):
        args = lines[line].replace("RELEASE ","",1)
        print("Line " + str(line+1) + " wants to release "+args+" - " + lines[line])
        if args == "LMB":
            pyautogui.mouseUp(button='left')
        elif args == "RMB":
            pyautogui.mouseUp(button='right')
        elif args == "MMB":
            pyautogui.mouseUp(button='middle')
        else:
            pyautogui.keyUp(args)
    elif lines[line].startswith("SCROLL "):
        args = lines[line].replace("SCROLL ","",1)
        print("Line " + str(line+1) + " wants to scroll "+args+" - " + lines[line])
        amount = int(args.split(" ")[0])
        x = None
        y = None
        if len(args.split(" ")) >= 2:
            x = int(args.split(" ")[1])
            if len(args.split(" ")) == 3:
                y = int(args.split(" ")[2])
        pyautogui.scroll(amount, x=x, y=y)
    elif lines[line].startswith("HSCROLL "):
        args = lines[line].replace("HSCROLL ","",1)
        print("Line " + str(line+1) + " wants to scroll (horizontally) "+args+" - " + lines[line])
        amount = int(args.split(" ")[0])
        x = None
        y = None
        if len(args.split(" ")) >= 2:
            x = int(args.split(" ")[1])
            if len(args.split(" ")) == 3:
                y = int(args.split(" ")[2])
        pyautogui.hscroll(amount, x=x, y=y)
    elif lines[line].startswith("SCREENSHOT "):
        args = lines[line].replace("SCREENSHOT ","",1)
        print("Line " + str(line+1) + " wants to take a screenshot - " + lines[line])
        pyautogui.screenshot(args)
    elif lines[line] == "QUIT" or lines[line] == "EXIT":
        print("Line " + str(line+1) + " wants to quit - " + lines[line])
        return []
    elif lines[line] == "PAUSE":
        print("Line " + str(line+1) + " wants to pause - " + lines[line])
        input("Press enter to continue...")
    elif lines[line].startswith("FOS "):
        args = lines[line].replace("FOS ","",1)
        imgPath = " ".join(args.split(" ")[:getIndex(args.split(" "),"=")])
        variableName = " ".join(args.split(" ")[getIndex(args.split(" "),"=")+1:])
        result = pyautogui.locateOnScreen(imgPath)
        if result is not None:
            setVar(variableName, {
                "left": result.left,
                "top": result.top,
                "width": result.width,
                "height": result.height
            })
        else:
            setVar(variableName, None)
    elif lines[line].startswith("FCOS "):
        args = lines[line].replace("FCOS ","",1)
        imgPath = " ".join(args.split(" ")[:getIndex(args.split(" "),"=")])
        variableName = " ".join(args.split(" ")[getIndex(args.split(" "),"=")+1:])
        result = pyautogui.locateCenterOnScreen(imgPath)
        if result is not None:
            setVar(variableName, {
                "x": result.x,
                "y": result.y
            })
        else:
            setVar(variableName, None)
    elif lines[line].startswith("IF "):
        args = lines[line].replace("IF ","",1)
        uniqueIdentifier = re.search("\[.*\]", args).group(0)[1:-1]
        toBeEvaldSplit = re.search("\(.*\)", args).group(0)[1:-1].split(" ")
        for i in range(len(toBeEvaldSplit)):
            if toBeEvaldSplit[i].startswith("$"):
                toBeEvaldSplit[i] = "getVar('"+toBeEvaldSplit[i]+"')"
        toBeEvald = " ".join(toBeEvaldSplit)
        IFStatementLine = line
        elseStatementLine = -1
        endIFLine = -1
        for i in range(line+1,len(lines)):
            if lines[i] == "ELSE [" + uniqueIdentifier + "]":
                elseStatementLine = i
            elif lines[i] == "ENDIF [" + uniqueIdentifier + "]":
                endIFLine = i
                break
        if endIFLine == -1:
            print("[!] Line " + str(line+1) + " has an unclosed IF statement - " + lines[line])
            return []
        if elseStatementLine != -1:
            linesBetweenIFandELSE = numbersBetween(IFStatementLine+1,elseStatementLine-1)
            linesBetweenELSEandENDIF = numbersBetween(elseStatementLine+1,endIFLine-1)
        linesBetweenIFandENDIF = numbersBetween(IFStatementLine+1,endIFLine-1)
        

        if eval(toBeEvald):
            linesToRemove = [endIFLine]
            if elseStatementLine != -1:
                linesToRemove += linesBetweenELSEandENDIF
                linesToRemove.append(elseStatementLine)
            return list(set(linesNumbers) - set(linesToRemove))
        else:
            linesToRemove = [endIFLine]
            if elseStatementLine != -1:
                linesToRemove += linesBetweenIFandELSE
                linesToRemove.append(elseStatementLine)
            else:
                linesToRemove += linesBetweenIFandENDIF
            return list(set(linesNumbers) - set(linesToRemove))
    elif lines[line].startswith("ELSE") or lines[line].startswith("ENDIF"):
        print("[!] Line " + str(line+1) + " has an unclosed IF statement - " + lines[line])
        return []
    elif lines[line].startswith("ALERT "):
        args = lines[line].replace("ALERT ","",1)
        splitMSG = args.split(" ")
        for i in range(len(splitMSG)):
            if splitMSG[i].startswith("$") or splitMSG[i].startswith("'$") or splitMSG[i].startswith('"$'):
                prefix = ""
                suffix = ""
                if not splitMSG[i].startswith("$"):
                    prefix = splitMSG[i][0]
                    suffix = splitMSG[i][-1]
                    splitMSG[i] = splitMSG[i][1:-1]
                splitMSG[i] = prefix + getVar(splitMSG[i]) + suffix
        args = " ".join(splitMSG)
        print("Line " + str(line+1) + " wants to alert - " + lines[line])
        pyautogui.alert(args)
    elif lines[line].startswith("CONFIRM "):
        args = lines[line].replace("CONFIRM ","",1)
        splitMSG = args.split(" ")[:getIndex(args.split(" "),"=")]
        for i in range(len(splitMSG)):
            if splitMSG[i].startswith("$") or splitMSG[i].startswith("'$") or splitMSG[i].startswith('"$'):
                prefix = ""
                suffix = ""
                if not splitMSG[i].startswith("$"):
                    prefix = splitMSG[i][0]
                    suffix = splitMSG[i][-1]
                    splitMSG[i] = splitMSG[i][1:-1]
                splitMSG[i] = prefix + getVar(splitMSG[i]) + suffix
        message = " ".join(splitMSG)
        variableName = " ".join(args.split(" ")[getIndex(args.split(" "),"=")+1:])
        print("Line " + str(line+1) + " wants to confirm - " + lines[line])
        output = pyautogui.confirm(message)
        setVar(variableName, output)
    elif lines[line].startswith("PROMPT "):
        args = lines[line].replace("PROMPT ","",1)
        splitMSG = args.split(" ")[:getIndex(args.split(" "),"=")]
        for i in range(len(splitMSG)):
            if splitMSG[i].startswith("$") or splitMSG[i].startswith("'$") or splitMSG[i].startswith('"$'):
                prefix = ""
                suffix = ""
                if not splitMSG[i].startswith("$"):
                    prefix = splitMSG[i][0]
                    suffix = splitMSG[i][-1]
                    splitMSG[i] = splitMSG[i][1:-1]
                splitMSG[i] = prefix + getVar(splitMSG[i]) + suffix
                
        message = " ".join(splitMSG)
        variableName = " ".join(args.split(" ")[getIndex(args.split(" "),"=")+1:])
        print("Line " + str(line+1) + " wants to prompt - " + lines[line])
        output = pyautogui.prompt(message)
        setVar(variableName, output)
    else:
        print("Unknown Line: " + lines[line] )
def executeScript(script):
    print("Running macro: " + Path(script).name)
    with open(script,"r") as f:
        script = str(f.read())
        f.close()
    lines = script.splitlines()
    linesNumbers = list(range(len(lines)))
    stopExecution = False
    while len(linesNumbers) > 0:
        if stopExecution == True:
            break
        # print("Lines left:",linesNumbers)
        output = lineExec(linesNumbers.pop(0), lines, linesNumbers)
        if output is not None:
            linesNumbers = output 

if not os.path.exists("scripts.json"):
    with open("scripts.json","w") as f:
        f.write("{}")
        f.close()
if open("scripts.json","r").read() == "":
    with open("scripts.json","w+") as f:
        f.truncate(0)
        f.flush()
        f.write("{}")
        f.close()
loadedScripts = json.load(open("scripts.json","r"))
for script in loadedScripts.keys():
    hotkey = script.split("#")[0] # The stuff after # is just to allow duplicate hetkeys (e.g ctrl+shift+alt#33fg4)
    print("Hotkey: " + " + ".join(hotkey.upper().split("+")) + ", Macro name: " + Path(loadedScripts[script]).name)
    keyboard.add_hotkey(hotkey, lambda: Thread(target=executeScript, args=(loadedScripts[script],), daemon=True).start())
if len(loadedScripts) < 1:
    print("No macros loaded. Make a macro using 'mkscript.py'. Exiting...")
    exit()
def stopExec():
    global stopExecution
    print("SAFETY KEY PRESSED! Execution stopped!")
    stopExecution = True

keyboard.add_hotkey(safetyKey, lambda: stopExec())
keyboard.wait()

