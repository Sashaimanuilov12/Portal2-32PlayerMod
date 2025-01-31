from cmath import rect
from locale import getlocale
import sys
import os
import random
import asyncio
import threading
import time
import webbrowser
tk = ""
try:
    from tkinter import Tk
    tk = Tk()
    tk.withdraw()
except:
    print("ERROR TKINTER NOT FOUND (TO GET COPY PASTE FUNCTIONALLITY DOWNLOAD THE TKINTER (\"tk\" probably) MODULE FROM YOUR PACKAGE MANAGER)")
    pass


import pygame
from pygame.locals import *
import Scripts.GlobalVariables as GVars
from Scripts.BasicLogger import Log, StartLog
import Scripts.RunGame as RG
import Scripts.Configs as cfg

# populate the global variables

pygame.init()
pygame.mixer.init()
# change dir into the "GUI" folder
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/GUI")
cwd = os.getcwd()

blipsnd = pygame.mixer.Sound("assets/sounds/blip.wav")
blipsnd.set_volume(0.25)

pwrsnd = pygame.mixer.Sound("assets/sounds/power.wav")
pwrsnd.set_volume(0.25)

angrycube = pygame.image.load("assets/images/angrycube.png")

goldencube = pygame.image.load("assets/images/goldencube.png")

ERRORLIST = []

PopupBoxList = []

###############################################################################

fps = 60
fpsclock = pygame.time.Clock()

screen = pygame.display.set_mode((1280, 720), RESIZABLE)

running = True

# Define the name and image of the window
pygame.display.set_caption('Portal 2: Multiplayer Mod Launcher')

p2mmlogo = pygame.image.load("assets/images/p2mm.svg")

pygame.display.set_icon(p2mmlogo)

###############################################################################

Floaters = []

# surf = pygame.surface.Surface([int(W / 25) + int(H / 50), int(W / 25) + int(H / 50)])
#     surf.set_colorkey((0, 0, 0))
#     surf.fill((255, 255, 255))
#     surf = pygame.transform.rotate(surf, 19)

def Floater(width, height, rot, x, y, negrot):
    surf = pygame.image.load("assets/images/button.png")
    surf = pygame.transform.scale(surf, (width, height))
    # surf.set_colorkey((0, 0, 0))
    # surf.fill((130, 130, 140))
    surf = pygame.transform.rotate(surf, 0)
    nrot = rot
    nsurf = surf
    class Floater:
        rot = nrot
        surf = nsurf
    Floater.x = x
    Floater.y = y
    Floater.negrot = negrot
    return Floater


def AddFloater(width, height, rot, x, y):
    # random bool
    negrot = random.randint(0, 1) == 1
    Floaters.append(Floater(width, height, rot, x, y, negrot))

AddFloater(50, 50, 20, 75, 75)
AddFloater(50, 50, 20, 75, 75)
AddFloater(50, 50, 20, 75, 75)
AddFloater(50, 50, 20, 75, 75)
AddFloater(50, 50, 20, 75, 75)
AddFloater(50, 50, 20, 75, 75)
AddFloater(50, 50, 20, 75, 75)
AddFloater(50, 50, 20, 75, 75)
AddFloater(50, 50, 20, 75, 75)



def gradientRect( window, left_colour, right_colour, target_rect ):
    colour_rect = pygame.Surface( ( 2, 2 ) )                                   # tiny! 2x2 bitmap
    pygame.draw.line( colour_rect, left_colour,  ( 0,0 ), ( 0,1 ) )            # left colour line
    pygame.draw.line( colour_rect, right_colour, ( 1,0 ), ( 1,1 ) )            # right colour line
    colour_rect = pygame.transform.smoothscale( colour_rect, ( target_rect.width, target_rect.height ) )  # stretch!
    window.blit( colour_rect, target_rect )

def GetGamePath():
    def AfterInputGP(inp):
        if CheckPath(inp):
            cfg.EditConfig("portal2path", inp.strip())
            Log("Saved '" + inp.strip() + "' as the game path!")
            Error("Game path is correct!", 5, (75, 255, 75))
            Error("Saved path!", 5, (75, 200, 75))
        else:
            Error("You entered an invalid game path!")
    GetUserInputPYG( AfterInputGP , "Enter Your Portal 2 Game Path")
    
def CheckPath(gamepath):
    if ((os.path.exists(gamepath)) != True) or (os.path.exists(gamepath + GVars.nf + "portal2_dlc2") != True):
        return False
    else:
        return True

def VerifyGamePath():
    Log("Verifying game path...")
    gamepath = GVars.configData["portal2path"]
    if CheckPath(gamepath) == False:
        Log("Game path is invalid!")
        Error("Game path is invalid!")
        GetGamePath()

def RunGameScript():
    VerifyGamePath()
    gamepath = GVars.configData["portal2path"]
    if (CheckPath(gamepath)):
        RG.MountMod(gamepath)
        RG.LaunchGame(gamepath)

def UnmountScript():
    VerifyGamePath()
    gamepath = GVars.configData["portal2path"]
    RG.DeleteUnusedDlcs(gamepath)
    RG.UnpatchBinaries(gamepath)

def SelectAnimation(btn, anim):
    if anim == "pop":
        btn.curanim = "pop1"

def RunAnimation(button, anim):
    if anim == "pop1":
        if button.sizemult < 1.3:
            button.sizemult += 0.1
        else:
            button.curanim = "pop2"
    if anim == "pop2":
        if button.sizemult > 1:
            button.sizemult -= 0.1
        else:
            button.sizemult = 1
            button.curanim = ""

directorymenu = []

CurrentMenu = None
SelectedButton = None
CurrentButtonsIndex = 0

def ChangeMenu(menu):
    global CurrentMenu
    global SelectedButton
    global directorymenu
    global CurrentButtonsIndex
    directorymenu.append(CurrentMenu)
    CurrentMenu = menu
    CurrentButtonsIndex = 0
    SelectedButton = CurrentMenu[0]

def BackMenu():
    if len(directorymenu) > 0:
        ChangeMenu(directorymenu[-1])
        directorymenu.pop()
        CurrentButtonsIndex = 0

def RefreshSettingsMenu():
        SettingsButtons.clear()
        for key in GVars.configData:
            if key != "cfgvariant":
                print(key + ": " + GVars.configData[key])
                class curkeyButton:
                    text = key + ": " + GVars.configData[key]
                    cfgkey = key
                    cfgvalue = GVars.configData[key]
                    activecolor = (255, 255, 0)
                    inactivecolor = (155, 155, 155)
                    sizemult = 1
                    selectanim = "pop"
                    selectsnd = pwrsnd
                    hoversnd = blipsnd
                    curanim = ""
                    def function(cfgkey = cfgkey, cfgvalue = cfgvalue, text = text):
                        if cfgkey != "portal2path":
                            if cfgvalue == "false":
                                cfg.EditConfig(cfgkey, "true")
                            # default to false to avoid errors
                            else:
                                cfg.EditConfig(cfgkey, "false")
                            RefreshSettingsMenu()

                    isasync = False
                SettingsButtons.append(curkeyButton)
        SettingsButtons.append(BackButton)

def GetUserInputPYG(afterfunc = None, prompt = ""):
    global LookingForInput
    global CurInput
    global AfterInputFunction
    global InputPrompt
    print("Getting User INPUT")
    LookingForInput = True
    CurInput = ""
    InputPrompt = prompt
    AfterInputFunction = afterfunc
    print("AfterInputFunction: " + str(AfterInputFunction))

def Error(text, time = 3, clr = (255, 75, 75)):
    Log(text)
    # if the text has newlines, split it up
    if "\n" in text:
        text = text.split("\n")
    else:
        ERRORLIST.append([text, time, clr])
        return
    for i in range(0, len(text)):
        ERRORLIST.append([text[i], time, clr])
    return

def PopupBox(tile, text, buttons):
    print("")


############ BUTTON CLASSES

class LaunchGameButton:
    text = "Start Game"
    activecolor = (50, 255, 120)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""
    function = RunGameScript
    isasync = True

class SettingsButton:
    text = "Settings"
    activecolor = (255, 255, 0)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""
    def function():
        RefreshSettingsMenu()
        ChangeMenu(SettingsButtons)
    isasync = False

class UpdateButton:
    text = "Update Launcher"
    activecolor = (255, 0, 255)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""
    def function():
        # open the github releases page in the default browser
        webbrowser.open("https://github.com/kyleraykbs/Portal2-32PlayerMod/releases")
    isasync = True

class ManualButton:
    text = "Manual Mounting"
    activecolor = (255, 255, 0)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""
    def function():
        ChangeMenu(ManualButtons)
    isasync = False

class GuideButton:
    text = "Steam Guide"
    activecolor = (255, 255, 0)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""
    def function():
        # open the steam guide in the default browser
        webbrowser.open("https://steamcommunity.com/sharedfiles/filedetails/?id=2458260280")
    isasync = True

class DiscordButton:
    text = "Discord Server"
    activecolor = (75, 75, 150)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""
    def function():
        # open the discord invite in the default browser
        webbrowser.open("https://discord.com/invite/kW3nG6GKpF")
    isasync = True

class TestingButton:
    text = "Testing"
    activecolor = (175, 75, 0)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""
    def function():
        ChangeMenu(TestingMenu)
    isasync = False

class InputButton:
    text = "Input"
    activecolor = (255, 255, 0)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""
    def function():
        def AfterInput(input):
            Error("Input: " + input, 3, (255, 255, 0))
        GetUserInputPYG(AfterInput)
    isasync = False

class RunButton:
    text = "Mount"
    activecolor = (50, 255, 120)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""
    function = RunGameScript
    isasync = True

class StopButton:
    text = "Unmount"
    activecolor = (255, 50, 50)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""
    function = UnmountScript
    isasync = True

class BackButton:
    text = "Back"
    activecolor = (255, 255, 0)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""
    def function():
        BackMenu()
    isasync = False

##############################

### BUTTONS
SettingsButtons = []

ManualButtons = [RunButton, StopButton, BackButton]

MainButtons = [LaunchGameButton, SettingsButton, UpdateButton, ManualButton, GuideButton, DiscordButton, TestingButton]

TestingMenu = [InputButton, BackButton]
###########

CurrentMenu = MainButtons

SelectedButton = CurrentMenu[CurrentButtonsIndex]


LookingForInput = False
CurInput = ""
AfterInputFunction = None
InputPrompt = ""

###############################################################################

SecAgo = time.time()

def Update():
    global CurrentMenu
    global SelectedButton
    global CurInput
    global LookingForInput
    global AfterInputFunction
    global SecAgo

    W = screen.get_width()
    H = screen.get_height()

    ########### BACKGROUND

    for floater in Floaters:
        surf = floater.surf
        if (SelectedButton.text == "Unmount"):
            surf = angrycube
        elif (SelectedButton.text == "Back"):
            surf = goldencube
        surf = pygame.transform.scale(surf, (W/15, W/15))
        surf = pygame.transform.rotate(surf, floater.rot)
        center = surf.get_rect().center
        screen.blit(surf, (floater.x - center[0], floater.y - center[1]))
        if floater.negrot:
            floater.rot -= (1 + random.randint(0, 2))
        else:
            floater.rot += (1 + random.randint(0, 2))
        if (SelectedButton.text == "Back"):
            floater.x -= W / 60
            if floater.x < (floater.surf.get_width() * -2):
                floater.y = random.randint(0, H)
                floater.x = (floater.surf.get_width() * 2) + (random.randint(W, W * 2)) * 1
                floater.negrot = random.randint(0, 1) == 1
        elif (SelectedButton.text == "Unmount"):
            floater.y -= H / 60
            if floater.y < (floater.surf.get_height() * -2):
                floater.y = (floater.surf.get_height() * 2) + (random.randint(H, H * 2))
                floater.x = random.randint(0, W)
                floater.negrot = random.randint(0, 1) == 1
        else:
            floater.y += H / 60
            if floater.y > (H + floater.surf.get_height() * 2):
                floater.y = (floater.surf.get_height() * -2) + (random.randint(0, H)) * -1
                floater.x = random.randint(0, W)
                floater.negrot = random.randint(0, 1) == 1


    # Put assets/images/keys.png on the top right corner of the screen
    keys = pygame.image.load("assets/images/keys.png")
    keys = pygame.transform.scale(keys, (W/10, W/10))
    screen.blit(keys, ((W / 1.05) - keys.get_width(), H/15))

    ########### MENU

    # loop through all buttons
    indx = 0
    for button in CurrentMenu:
        indx += 1
        clr = (0, 0, 0)
        if button == SelectedButton:
            clr = button.activecolor
        else:
            clr = button.inactivecolor
        RunAnimation(button, button.curanim)
        text1 = pygame.font.Font("assets/fonts/pixel.ttf", int(int((int(W / 25) + int(H / 50)) / 1.5) * button.sizemult)).render(button.text, True, clr)
        if not (LookingForInput):
            screen.blit(text1, (W / 16, (H / 2 - (text1.get_height() / 2)) * (indx / 5)  ))

    SelectedButton = CurrentMenu[CurrentButtonsIndex]

    ############# OVERLAY

    indx = 0
    for error in ERRORLIST:
        indx += 1
        errortext = pygame.font.Font("assets/fonts/pixel.ttf", int(int(W / 60) + int(H / 85))).render(error[0], True, error[2])
        screen.blit(errortext, (W / 30, ((errortext.get_height() * indx) * -1) + (H / 1.05)))

    # every 1 second go through each error and remove it if it's been there for more than 1 second
    if (time.time() - SecAgo) > 1:
        for error in ERRORLIST:
            if (error[1] < 0):
                ERRORLIST.remove(error)
            error[1] -= 1
        SecAgo = time.time()
    ####################### DRAW INPUT BOX
    if LookingForInput:
        fntdiv = 32
        fntsize = int(W / fntdiv)
        mindiv = int(fntdiv / 1.25)

        # divide the CurrentInput into lines
        lines = []
        # every  23 characters, add a new line
        lines.append(CurInput[0:mindiv])
        for i in range(mindiv, len(CurInput), mindiv):
            lines.append(CurInput[i:i+mindiv])


        InputText = ""
        for i in range(len(lines)):
            InputText = pygame.font.Font("assets/fonts/pixel.ttf", fntsize).render(lines[i], True, (255, 255, 175))
            screen.blit(InputText, (W / 2 - (InputText.get_width() / 2), (     (((H / 2) - (InputText.get_height() * 1.25)) + ((text1.get_height() * 1.25) * i))) - ((((text1.get_height() * 1.25) * (len(lines) / 2))))        ))

        surf1 = pygame.Surface((W / 1.5, W / 100))
        surf1.fill((255, 255, 255))
        surf2 = pygame.Surface((W / 1.5, W / 100))
        blitpos = ((W / 2) - (surf2.get_width() / 2), (H / 2) + ((InputText.get_height() * 1.725) * ((len(lines) / 2) - 1)))
        screen.blit(surf1, blitpos)
        
        surfInputPrompt = pygame.font.Font("assets/fonts/pixel.ttf", fntsize).render(InputPrompt, True, (255, 255, 255))
        # blit it right below the surf1
        screen.blit(surfInputPrompt, (blitpos[0] + (surf1.get_width() / 2) - (surfInputPrompt.get_width() / 2), blitpos[1] + surfInputPrompt.get_height()))


###############################################################################

def Main():
    global running
    global screen
    global fps
    global SelectedButton
    global CurrentButtonsIndex
    global LookingForInput
    global CurInput
    global AfterInputFunction
    LastBackspace = 0
    BackspaceHasBeenHeld = False

    while running:
        ############################ INPUT BOX INPUT
        if (LookingForInput):
            BACKSPACEHELD = pygame.key.get_pressed()[pygame.K_BACKSPACE]
            BACKSPACEHELD = BACKSPACEHELD > 0

            if (BACKSPACEHELD):
                if BackspaceHasBeenHeld == False:
                    LastBackspace = time.time() + 0.5
                    BackspaceHasBeenHeld = True
                # if its been a second since the last backspace, delete the last character
                elif (time.time() - LastBackspace > 0.05):
                    if (len(CurInput) > 0):
                        CurInput = CurInput[:-1]
                    LastBackspace = time.time()
            else:
                BackspaceHasBeenHeld = False
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif (LookingForInput):
                CTRLHELD = pygame.key.get_mods() & pygame.KMOD_CTRL
                CTRLHELD = CTRLHELD > 0
                SHIFTHELD = pygame.key.get_mods() & pygame.KMOD_SHIFT
                SHIFTHELD = SHIFTHELD > 0

                if event.type == pygame.KEYDOWN:
                    # get the key and add it to CurInput
                    name = pygame.key.name(event.key)
                    if name == "backspace" and len(CurInput) >0:
                        # if the last char is a newline, remove it
                        if CurInput[len(CurInput) - 1] == "\n":
                            CurInput = CurInput[:-2]
                        else:
                            CurInput = CurInput[:-1]
                    elif name == "space":
                        CurInput += " "
                    elif name == "return":
                        LookingForInput = False
                        AfterInputFunction( CurInput )
                    elif name == "escape":
                        LookingForInput = False
                    elif name == "tab":
                        CurInput += "   "
                    elif CTRLHELD and name == "v":
                        try:
                            str1 = str(tk.selection_get(selection="CLIPBOARD"))
                            print(str1)
                            str1 = str1.replace("\n", "")
                            print("=================================")
                            print(str1)
                            CurInput += str1
                        except:
                            print("ERROR TKINTER NOT FOUND (TO GET COPY PASTE FUNCTIONALLITY DOWNLOAD THE TKINTER (\"tk\" probably) MODULE FROM YOUR PACKAGE MANAGER)")
                            pass
                    elif len(name) == 1:
                        if SHIFTHELD:
                            # if the name doesnt contain a letter
                            if not name.isalpha():
                                name = name.replace("1", "!").replace("2", "@").replace("3", "#").replace("4", "$").replace("5", "%").replace("6", "^").replace("7", "&").replace("8", "*").replace("9", "(").replace("0", ")").replace("`", "~").replace("-", "_").replace("=", "+").replace("[", "{").replace("]", "}").replace("\\", "|").replace(";", ":").replace("'", "\"").replace(",", "<").replace(".", ">").replace("/", "?")
                            # convert lowercase to uppercase
                            else:
                                name = name.upper()
                            CurInput += name
                        else:
                            CurInput += name

            ######################## NORMAL INPUT
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    BackMenu()
                elif event.key == K_BACKSPACE:
                    BackMenu()
                elif event.key == K_DOWN or event.key == K_s:
                    if CurrentButtonsIndex < len(CurrentMenu) - 1:
                        CurrentButtonsIndex += 1
                        SelectedButton = CurrentMenu[CurrentButtonsIndex]
                        pygame.mixer.Sound.play(SelectedButton.hoversnd)
                    else:
                        CurrentButtonsIndex = 0
                        SelectedButton = CurrentMenu[CurrentButtonsIndex]
                        pygame.mixer.Sound.play(SelectedButton.hoversnd)
                elif event.key == K_UP or event.key == K_w:
                    if CurrentButtonsIndex > 0:
                        CurrentButtonsIndex -= 1
                        SelectedButton = CurrentMenu[CurrentButtonsIndex]
                        pygame.mixer.Sound.play(SelectedButton.hoversnd)
                    else:
                        CurrentButtonsIndex = len(CurrentMenu) - 1
                        SelectedButton = CurrentMenu[CurrentButtonsIndex]
                        pygame.mixer.Sound.play(SelectedButton.hoversnd)
                elif event.key == K_SPACE:
                    if SelectedButton.function:
                        if SelectedButton.isasync:
                            threading.Thread(target=SelectedButton.function).start()
                        else:
                            SelectedButton.function()

                    SelectAnimation(SelectedButton, SelectedButton.selectanim)

                    pygame.mixer.Sound.play(SelectedButton.selectsnd)


        # make the screen a gradient
        screen.fill((0, 0, 0))
        gradientRect( screen, (0, 2, 10), (2, 2, 10), pygame.Rect( 0, 0, screen.get_width(), screen.get_height() ) )
        Update()
        pygame.display.update()
        fpsclock.tick(fps)

    pygame.quit()
    sys.exit()

def OnStart():
    # Load the global variables
    GVars.init()
    # to do the fancy log thing
    StartLog()
    # load the config file into memmory
    GVars.LoadConfig()

if __name__ == '__main__':
    OnStart()
    Main()