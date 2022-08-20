# Pycro
Pycro is a script that can make and execute macros with ease.
- - - -
### Usage

First of all, make sure you have all dependencies installed:
```shell
python3 -m pip install -r requirements.txt
```
After that, you are good to go! 

To create a macro, run `mkscript.py` and the script will guide you through the process.
> To view all shortcuts, press `h`

After creating your script, you need to assign a hotkey, otherwise you can't run it. So go ahead and press `z` and the script will ask you to set a hotkey.
When you are done. Press `s` to save the macro (The macro will save automatically when you exit the script too). Now you have a macro!

Time to try it! So exit `mkscript.py` and run `main.py`. It will announce which scripts have been loaded and what their hotkey is. And when you press your specified hotkey (the terminal doesn't have to be focused), the macro will start running.

Just in case, We've implemented a safety key, if the macro started doing some weird stuff, you can always press `F12` to immediately stop the execution of the macro.
> The safety key can be changed in `main.py`
