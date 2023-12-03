# thx to https://www.svgrepo.com/ for button icons
import pygame, sys, math, random, time, os, shutil, subprocess, tomlkit, toml, textwrap, ast
from sys import exit
from pygame import mixer
from pathlib import Path
from tomlkit import dumps, parse # tomlkit is a fucking pain. toml files in general in python are ass. i tried working with a txt instead and everything instantly worked.
from tkinter import Tk

screen_width = 1000
screen_height = 563
# 1000 x 563
ui_objects = []
intro_objects = []
run = False
Yv = -6
fade = 300
games = []
banners = []
mainscroll = 0
SubmenuScroll = 50
GameButtons = []
ConfigButtons = []
buildpaths = []
ConfigSettingsButtons = []
SettingsButtons = []
tooltips = []
SettingsTips = []
FNULL = open(os.devnull, 'w')
tomlpath = str()
TOMLToEdit = dict()
TOMLobj = 0
txtversion = []
SubmenuBGSurfaceYvar = -1000
TooltipTextSurfaceXvar = -5007
configEditorOpen = False
ConfigOpen = str()
TooltipOpen = False
SettingsTipsOpen = False
TooltipText = ['you shouldnt see this']
SettingsTipsText = ['you shoudlnt see this either']
ImportantConfigs = []
typing = -1
mousestate = 0
SettingsOpen = False
files = []
FilesButtons = []
VersionName = 'v7.7'
BuildPathsYvar = 1300
BuildPathsConfigOpen = -1
BuildPathsText = str()
timer = 0


def setup_pygame(): # we draw everything to screen then draw screen onto window, which is the final scaled display surface
    global keycodes, keynames, screen, clock, window, MonitorInfo, WindowInfo, Root, UIRoot, screen_width, screen_height
    pygame.init()
    pygame.display.set_caption('XenUI by Paths' + VersionName)
    MonitorInfo = pygame.display.Info()
    MonitorInfo = (MonitorInfo.current_w, MonitorInfo.current_h)
    if MonitorInfo[0] < 1920:
        WindowInfo = (1920 / 2, 1080 / 2)
        MonitorInfo = (1920, 1080)
    else:
        WindowInfo = MonitorInfo[0] / 2, MonitorInfo[1] / 2
    screen = pygame.Surface((1920, 1080))
    screen_width = 1920
    screen_height = 1080
    window = pygame.display.set_mode((WindowInfo[0], WindowInfo[1]))
    clock = pygame.time.Clock()
    keycodes = open(UIRoot + 'txt\\pygame keycodes.txt', 'r')
    keycodes = keycodes.readlines()
    keynames = open(UIRoot + 'txt\\pygame keynames.txt', 'r')
    keynames = keynames.readlines()
    for i, v in enumerate(keycodes):
        keycodes[i] = keycodes[i].strip()
        keynames[i] = keynames[i].strip()
    return(screen, clock)

def tick(framerate):
    clock.tick(framerate)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(), exit()

def getkeys():
    global keysPressed
    keysPressed = list()
    keys = pygame.key.get_pressed()
    for i in keycodes:
        if keys[eval(i)]:
            keysPressed.append(i)

def get_mouse():
    global mousestate, mx, my
    # 1 means i just clicked, 2 means ive held click, 0 means im not clicking
    if mousestate == 1:
        if pygame.mouse.get_pressed(num_buttons=3)[0] == True:
            mousestate = 2
        else:
            mousestate = 0
    if mousestate == 0:
        if pygame.mouse.get_pressed(num_buttons=3)[0] == True:
            mousestate = 1
    if pygame.mouse.get_pressed(num_buttons=3)[0] == False:
        mousestate = 0
    OldRange = WindowInfo[0]
    NewRange = 960
    mx = (((pygame.mouse.get_pos()[0]) * 1920) / WindowInfo[0])
    my = (((pygame.mouse.get_pos()[1]) * 1080) / WindowInfo[1])
    # mouse x and y offset for resolution

def getNonRepeatingKeys():
    global usedNonRepeatingKeys, NonRepeatingKeys, KeysPressed
    NonRepeatingKeys = []
    if len(keysPressed) == 0:
        usedNonRepeatingKeys = []
    for i in keysPressed:
        if i not in usedNonRepeatingKeys:
            NonRepeatingKeys.append(i)
            usedNonRepeatingKeys.append(i)

def get_key(val):
    for i, v1 in enumerate(list(TOMLToEdit)):
        for k, v2 in TOMLToEdit[v1].items():
            if val == v2:
                return k
    return "key not found"

def get_category(val):
    for i, v in enumerate(list(TOMLToEdit)):
        if val in list(TOMLToEdit[v].NonRepeatingKeys()):
            return v

def has_numbers(string):
    return any(i.isdigit() for i in string)

def load_assets():
    global ui_assets, testsurface, banners, Root, imgW, imgH, ratio, BannerFont, banner_height, SubmenuBGSurface, configEditorBGtxt, ImportantConfigNames, ImportantConfigs, tooltips, TooltipSurfaceBack, ConfigFont, TooltipFont, ConfigTextSurface, SettingsTips, Root, UIRoot, buildpaths, BuildPathsSurface, BuildPathsYvar, SaveSurface, PasteSurface, BuildPathFont, CloseSurface, gamesroot, EraseSurface, FilesButtons
    ImportantConfigNames = open(UIRoot + 'txt\\important configs.txt').readlines() # load this here so we can append the tooltip button surfaces
    ImportantConfigs = []
    txtversion = open(Root + 'xenia-canary.config.toml').readlines()
    counter = 0
    for i, v in enumerate(txtversion):
        txtversion[i] = v.replace('\t', '')
        if txtversion[i] == '\n' or '':
            txtversion[i] = ' '
    while counter < len(txtversion):
        if txtversion[counter] == ' ':
            txtversion.pop(counter)
        else:
            counter += 1
    for i, v in enumerate(ImportantConfigNames):
        for i2, v2 in enumerate(txtversion):
            if v2[:v2.find(' =')] == v.strip():
                ImportantConfigs.append(i2 + 1)
                break
    ui_objects.append([pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\close.png').convert_alpha(), (80, 80)), 24, 980, 60, 60, 'close'])
    ui_objects.append([pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\credits.png').convert_alpha(), (80, 80)), 24, 880, 60, 60, 'credits'])
    ui_objects.append([pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\settings.png').convert_alpha(), (80, 80)), 24, 780, 60, 60, 'settings'])
    ui_objects.append([pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\patch.png').convert_alpha(), (80, 80)), 24, 680, 60, 60, 'patches'])
    for i, v in enumerate(games):
        try:
            img = pygame.image.load(gamesroot + '\\' + v[0] + '\\' + v[1])
        except:
            img = pygame.image.load(UIRoot + 'textures and sfx\\default banner.png')
        imgW = img.get_width()
        imgH = img.get_height()
        if imgW > imgH:
            ratio = imgW / imgH
        else:
            ratio = imgH / imgW
        img = pygame.transform.scale(img, (1700, 1400 / ratio))
        imgW = img.get_width()
        imgH = img.get_height()
        banners.append([img, (180, 20), (0, (imgH / 2) - 50, 1700, banner_height)])
    for i, v in enumerate(games):
        GameButtons.append([pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\play.png').convert_alpha(), (banner_height / 1.7, banner_height / 1.7)), 1750, 38 + ((banner_height * 1.3) * i), 60, 60, v[0]])
        ConfigButtons.append([pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\config.png').convert_alpha(), (banner_height / 1.7, banner_height / 1.7)), 1640, 38 + ((banner_height * 1.3) * i), 60, 60, v[0]])
        buildpaths.append([pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\build path.png').convert_alpha(), (banner_height / 1.7, banner_height / 1.7)), 1530, 38 + ((banner_height * 1.3) * i), 60, 60, v[0]])
        FilesButtons.append([pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\files.png').convert_alpha(), (banner_height / 1.7, banner_height / 1.7)), 1420, 38 + ((banner_height * 1.3) * i), 60, 60, v[0]])
    for i, v in enumerate(ImportantConfigs):
        ImportantConfigs[i] = int(v) - 1
        tooltips.append([pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\tooltip.png').convert_alpha(), (90, 90)), 0, 0, v])
    for i, v in enumerate(settings):
        SettingsTips.append([pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\tooltip.png').convert_alpha(), (90, 90)), 0, 0, v[v.find('#') + 2:]])
    pygame.font.init()
    BannerFont = pygame.font.SysFont(Font, int(banner_height / 3.3))
    BannerFont.set_bold(True)
    ConfigFont = pygame.font.SysFont(Font, 50)
    ConfigFont.set_bold(False)
    TooltipFont = pygame.font.SysFont(Font, 36)
    TooltipFont.set_bold(True)
    BuildPathFont = pygame.font.SysFont(Font, 35)
    BuildPathFont.set_bold(False)
    GeneralBoldFont = pygame.font.SysFont(Font, 40)
    GeneralBoldFont.set_bold(True)
    SubmenuBGSurface = pygame.Surface((screen_width - 70, screen_height - 120)); SubmenuBGSurface.fill('black')
    configEditorBGtxt = GeneralBoldFont.render('Press Enter to save' + str([' ' * 80])[2:-2] + 'Press Escape to discard changes', False, (250, 250, 250))
    TooltipSurfaceBack = [pygame.Surface((1680, 10)), 1020, -1000]
    TooltipSurfaceBack[0].fill('grey10')
    TooltipSurfaceBack[0].set_alpha(200)
    TooltipTextSurface =  ConfigFont.render('you shouldnt see this.... report this bug pls', False, (250, 250, 250))
    ConfigTextSurface = pygame.Surface((450, 80))
    ConfigTextSurface.fill('grey5')
    BuildPathsSurface = pygame.Surface((1680, 120))
    BuildPathsSurface.fill('#524e21')
    CloseSurface = [pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\close.png').convert_alpha(), (80, 80)), 220, 0,]
    SaveSurface = [pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\save build path.png').convert_alpha(), (80, 80)), 320, 0,]
    PasteSurface = [pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\paste.png').convert_alpha(), (80, 80)), 420, 0,]
    EraseSurface = [pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\erase.png').convert_alpha(), (80, 80)), 520, 0,]

def load_config():
    global ConfigSettingsButtons, Root, UIRoot, ImportantConfigs, txtversion
    ConfigSettingsButtons = []
    x = 1400
    for i, v in enumerate(ImportantConfigs):
        line = txtversion[v]
        if line[line.find('=') + 2:line.find('  ')] == 'true':
            ConfigSettingsButtons.append([pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\true.png').convert_alpha(), (80, 80)), x, i * 35 - 20, 'bool', True])
        elif line[line.find('=') + 2:line.find('  ')] == 'false':
            ConfigSettingsButtons.append([pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\false.png').convert_alpha(), (80, 80)), x, i * 35 - 20, 'bool', False])
        else:
            ConfigSettingsButtons.append([pygame.Surface((550, 80)), x, i * 35 - 20, 'text', line[line.find('= ') + 2:line.find('#')].strip().replace('"', '')])
        ConfigSettingsButtons[i][0].set_alpha(100)

def load_settings():
    global SettingsButtons, settings, Root, UIRoot
    SettingsButtons = []
    x = 1400
    for i, v in enumerate(settings[:-2]):
        line = v[v.find('= ') + 2:v.find('# ') - 1]
        if line == 'True':
            SettingsButtons.append([pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\true.png').convert_alpha(), (80, 80)), x, (i * 100) - 20, 'bool', True])
        elif line == 'False':
            SettingsButtons.append([pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\false.png').convert_alpha(), (80, 80)), x, (i * 100) - 20, 'bool', False])
        else:
            SettingsButtons.append([pygame.Surface((550, 100)), x, (i * 100) - 20, 'text', line.replace("'", '')])

def load_games():
    global Root, UIRoot, gamesroot
    for file in os.listdir(gamesroot):
        gamename = os.fsdecode(file)
        pngname = 'NULL'
        tomlname = 'NULL'
        for file in os.listdir(gamesroot + '\\' + gamename):
            if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jpeg'):
                pngname = os.fsdecode(file)
            if file.endswith('.toml'):
                tomlname = os.fsdecode(file)
        games.append([gamename, pngname, 'need to keep this here in order to not shift the list elements lmao', tomlname])

def render():
    global GameButtons, banner_height, SubmenuBGSurface, configEditorBGtxt, ImportantConfigs, txtversion, NonRepeatingKeysPressed, tooltips, TooltipSurfaceBack, TooltipText, TooltipTextSurfaceXvar, ConfigFont, TooltipFont, ConfigSettingsButtons, ConfigTextSurface, SettingsTipsOpen, SettingsTips, SettingsTipsText, SettingsButtons, MonitorInfo, buildpaths, BuildPathsSurface, BuildPathsYvar, SaveSurface, PasteSurface, BuildPathFont, CloseSurface, FilesButtons
    ticks = int(str(pygame.time.get_ticks()))
    shade = round((math.sin(ticks / 500) * 20) + 30)
    screen.blit(pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\bg.png').convert_alpha(), (screen_width, screen_height)), (0, 0))
    screen.blit(pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\sidebar.png').convert_alpha(), (140, 1080)), (0, 0))
    dark = pygame.Surface((1700, banner_height), 32)
    dark.set_alpha(200, pygame.RLEACCEL)
    for i, v in enumerate(ui_objects):
        screen.blit(ui_objects[i][0], (ui_objects[i][1], ui_objects[i][2]))
    # here is the code for the banners (and effects, and name, and play button)
    for i, v in enumerate(banners):
        screen.blit(v[0], (v[1][0], v[1][1] + (i * (banner_height * 1.3)) + (mainscroll * 10)), v[2])
        screen.blit(dark, (v[1][0], v[1][1] + (i * (banner_height * 1.3)) + (mainscroll * 10)))
        NameText = BannerFont.render(games[i][0], False, (250, 250, 250))
        BannerFont.set_bold(True)
        screen.blit(NameText, (v[1][0] + 40, v[1][1] + (banner_height) / 3 + (i * (banner_height * 1.3)) + (mainscroll * 10) - 3))
    for i, v in enumerate(GameButtons):
        screen.blit(v[0], (v[1], v[2]))
        GameButtons[i][2] = 17 + (banner_height / 4) + ((banner_height * 1.3) * i) + (mainscroll * 10)
    for i, v in enumerate(ConfigButtons):
        screen.blit(v[0], (v[1], v[2]))
        ConfigButtons[i][2] = 17 + (banner_height / 4) + ((banner_height * 1.3) * i) + (mainscroll * 10)
    for i, v in enumerate(buildpaths):
        screen.blit(v[0], (v[1], v[2]))
        buildpaths[i][2] = 17 + (banner_height / 4) + ((banner_height * 1.3) * i) + (mainscroll * 10)
    for i, v in enumerate(FilesButtons):
        screen.blit(v[0], (v[1], v[2]))
        FilesButtons[i][2] = 17 + (banner_height / 4) + ((banner_height * 1.3) * i) + (mainscroll * 10)
    screen.blit(SubmenuBGSurface, (36, SubmenuBGSurfaceYvar + 6)) # the very back black background
    # screen.blit(configEditorBGtxt, (40, SubmenuBGSurfaceYvar + 465))
    if configEditorOpen:
        for i, v in enumerate(ImportantConfigs):
            if SubmenuScroll + (i * 100) + 25 > 20 and SubmenuScroll + (i * 100) + 25 < 900:
                screen.blit(ConfigFont.render(txtversion[int(v)][:txtversion[int(v)].find('=')].replace('_', ' '), False, (250, 250, 250)), (180, SubmenuBGSurfaceYvar + SubmenuScroll + (i * 100) + 10))
        for i, v in enumerate(tooltips):
            if SubmenuScroll + (i * 100) + 25 > 20 and SubmenuScroll + (i * 100) + 25 < 940:
                screen.blit(v[0], (v[1], v[2]))
        for i, v in enumerate(ConfigSettingsButtons):
            if v[2] > 50 and v[2] < SubmenuBGSurfaceYvar + 920:
                if v[3] == 'bool':
                    screen.blit(v[0], (v[1], v[2] + 20))
                elif v[3] == 'text':
                    screen.blit(ConfigTextSurface, (v[1], v[2] + 20))
                    pygame.draw.rect(screen, 'grey10', pygame.Rect(v[1], v[2] + 20, 450, 80),  12, 12, 12, 12)
                    screen.blit(ConfigFont.render(v[4], False, (250, 250, 250)), (v[1] + 20, v[2] + 22))
                    if typing == i:
                        pygame.draw.circle(screen, 'grey' + str(shade), (v[1] - 20, v[2] + 58), 10)
        pygame.draw.rect(screen, 'grey10', pygame.Rect(980, TooltipSurfaceBack[2] - 20, 850, len(TooltipText * 45) + 50),  30, 30, 1, 30)
        screen.blit(TooltipSurfaceBack[0], (TooltipSurfaceBack[1] - 20, TooltipSurfaceBack[2]))
        for i, v in enumerate(TooltipText):
            screen.blit(TooltipFont.render(str(v), False, (250, 250, 250)), (1025, TooltipSurfaceBack[2] + (i * 45) + 8))
    if TooltipOpen:
        TooltipSurfaceBack[0] = pygame.Surface((800, len(TooltipText * 45) + 20)) # we need to set the size here
    if SettingsTipsOpen:
        TooltipSurfaceBack[0] = pygame.Surface((800, len(SettingsTipsText * 45) + 20)) # we need to set the size here
    TooltipSurfaceBack[0].fill('grey10')
    if TooltipOpen or SettingsTipsOpen:
        TooltipSurfaceBack[2] += (175 - TooltipSurfaceBack[2]) / 7
    else:
        TooltipSurfaceBack[2] += (-810 - TooltipSurfaceBack[2]) / 7
    if SettingsOpen:
        for i, v in enumerate(settings[:-2]):
            if SubmenuScroll + (i * 100) + 25 > 35 and SubmenuScroll + (i * 100) + 25 < 900:
                screen.blit(ConfigFont.render(v[:v.find('= ')].replace('_', ' '), False, (250, 250, 250)), (180, SubmenuBGSurfaceYvar + SubmenuScroll + (i * 100) + 10))
        for i, v in enumerate(SettingsButtons):
            if i < 5:
                if v[2] > 50 and v[2] < SubmenuBGSurfaceYvar + 950:
                    if v[3] == 'bool':
                        screen.blit(v[0], (v[1], v[2] + 20))
                    elif v[3] == 'text':
                        screen.blit(ConfigTextSurface, (v[1], v[2] + 20))
                        pygame.draw.rect(screen, 'grey10', pygame.Rect(v[1], v[2] + 20, 450, 80),  12, 12, 12, 12)
                        screen.blit(ConfigFont.render(v[4], False, (250, 250, 250)), (v[1] + 20, v[2] + 20))
                        if typing == i:
                            pygame.draw.circle(screen, 'grey' + str(shade), (v[1] - 20, v[2] + 58), 10)
        pygame.draw.rect(screen, 'grey10', pygame.Rect(980, TooltipSurfaceBack[2] - 20, 850, len(SettingsTipsText * 45) + 50),  30, 30, 1, 30)
        screen.blit(TooltipSurfaceBack[0], (TooltipSurfaceBack[1] - 20, TooltipSurfaceBack[2]))
        for i, v in enumerate(SettingsTips):
            if i < 4:
                if SubmenuScroll + (i * 100) + 25 > 45 and SubmenuScroll + (i * 100) + 25 < 900:
                    screen.blit(v[0], (v[1], v[2]))
        for i, v in enumerate(SettingsTipsText):
            screen.blit(TooltipFont.render(str(v), False, (250, 250, 250)), (1000, TooltipSurfaceBack[2] + (i * 45) - 5))
    pygame.draw.rect(screen, 'black', pygame.Rect(13, SubmenuBGSurfaceYvar, screen_width - 24, 1000),  50, 50, 50, 50)
    screen.blit(configEditorBGtxt, (40, SubmenuBGSurfaceYvar + 940))
    screen.blit(BuildPathsSurface, (190, BuildPathsYvar))
    pygame.draw.rect(screen, 'grey5', pygame.Rect(180, BuildPathsYvar - 10, 1700, 140),  20, 20, 20, 20)
    screen.blit(CloseSurface[0], (CloseSurface[1], CloseSurface[2]))
    screen.blit(SaveSurface[0], (SaveSurface[1], SaveSurface[2]))
    screen.blit(PasteSurface[0], (PasteSurface[1], PasteSurface[2]))
    screen.blit(EraseSurface[0], (EraseSurface[1], EraseSurface[2]))
    if BuildPathsText == '':
        screen.blit(BuildPathFont.render('no custom path given, game will launch with default xenia canary executable', False, (250, 250, 250)), (610, BuildPathsYvar + 35))
    else:
        screen.blit(BuildPathFont.render(BuildPathsText.replace('"', ''), False, (250, 250, 250)), (610, BuildPathsYvar + 35))
    BannerFont.set_bold(True)

def intro_update():
    global fade
    for i in intro_objects:
        i[0].set_alpha(fade)
        screen.blit(i[0], (i[1][0], i[1][1]))
    newscreen = pygame.transform.smoothscale(screen, WindowInfo)
    window.blit(newscreen, (0, 0))
    pygame.display.update()

def askforgamepath():
    global GamesPopup, gamesroot, screen, window, newscreen, WindowInfo
    get_mouse()
    PasteSurface = [pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\paste.png').convert_alpha(), (80, 80)), 140, 570,]
    textbox = pygame.Surface((1670, 120))
    textbox.fill('#878236')
    BannerFont = pygame.font.SysFont('segoeuivariable', 35)
    BannerFont.set_bold(True)
    text = ''
    popup = ''
    y = 2200
    state = 0 # -1 means idle, -1 means invalid path, 1 means successful path, 2 means we trigger the intro / loading
    Valid = False
    timer = 0
    while Valid == False:
        getkeys()
        get_mouse()
        if state == 0:
            y += (1200 - y) / 12
        else:
            y += (700 - y) / 12
        screen.fill('grey3')
        screen.blit(textbox, (115, 1080 / 2))
        pygame.draw.rect(screen, 'grey10', pygame.Rect(100, 1080 / 2, 1700, 140),  20, 20, 20, 20)
        screen.blit(BannerFont.render('No games file was found, please press the paste button below to paste a valid games folder location to use', False, (250, 250, 250)), (110, 460))
        screen.blit(BannerFont.render(text, False, (250, 250, 250)), (240, 580))
        screen.blit(BannerFont.render(popup, False, (250, 250, 250)), ((WindowInfo[0]) - len(popup) * 20, y))
        screen.blit(PasteSurface[0], (PasteSurface[1], PasteSurface[2]))
        if PasteSurface[0].get_rect().collidepoint((mx - PasteSurface[1], my - PasteSurface[2])):
            PasteSurface[0].set_alpha(200 - PasteSurface[0].get_alpha()/ 3)
            if mousestate == 1:
                try:
                    gamesroot = Tk().clipboard_get().replace('"', '')
                except:
                    state = -1
                    popup = 'Your clipboard is empty or invalid :('
                text = gamesroot
                if os.path.exists(gamesroot):
                    popup = 'Valid!'
                    state = 1
                else:
                    popup = 'Invalid'
                    state = -1
        else:
            PasteSurface[0].set_alpha(PasteSurface[0].get_alpha() - -20 / 3)
        newscreen = pygame.transform.smoothscale(screen, WindowInfo)
        window.blit(newscreen, (0, 0))
        clock.tick()
        pygame.display.update()
        if state == 1:
            timer += 1
        else:
            timer -= 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(), exit()
        if timer > 500:
            Valid = True
        if timer < -500:
            state = 0
            timer = 0
            text = ''
    GamesPopup = False

# applying setting variables now
Root = sys.argv[0]
UIRoot = Root[:Root.rindex('\\')] + '\\'
Root = UIRoot[:UIRoot.rfind('\\')]
Root = Root[:Root.rfind('\\')] + '\\'
setup_pygame()
settings = open(UIRoot + 'txt\\settings.txt', 'r')
settings = settings.readlines()
if len(settings) < 6:
    if os.path.exists(Root + 'Games'):
        settings.append(Root + 'Games')
    else:
        GamesPopup = True
        while GamesPopup:
            askforgamepath()
        settings.append(gamesroot)
else:
    if os.path.exists(Root + 'Games'):
        settings[5] = Root + 'Games'
gamesroot = settings[5] + '\\'
for i, v in enumerate(settings[:-2]):
    settings[i] = str(v.strip('\n'))
for i, v in enumerate(settings[:-2]):
    exec(v)
buildpathsdata = ast.literal_eval(settings[4])
for i, v in enumerate(settings):
    settings[i] = settings[i].strip()
with open(UIRoot + 'txt\\settings.txt', 'w+') as i:
    i.write('\n'.join(settings))
    i.close()

icon = pygame.image.load(UIRoot + 'textures and sfx\\canary.png')
load_settings()
load_config()
load_games()
load_assets()
pygame.display.set_icon(icon)
# now setting up the startup animation and mixer for sfx
if playintro == True:
    mixer.init()
    mixer.music.load(UIRoot + 'textures and sfx\\startup.wav')
    mixer.music.set_volume(0.1)
    screen.fill('grey3')
    intro_objects.append([pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\intro bg.png').convert_alpha(), (MonitorInfo[0], MonitorInfo[1])), (0, 0)])
    intro_objects.append([pygame.image.load(UIRoot + 'textures and sfx\\xenia back.png').convert_alpha(), (screen_width / 2 - 120, screen_height / 2 - 100)])
    intro_objects.append([pygame.image.load(UIRoot + 'textures and sfx\\X.png').convert_alpha(), ((screen_width / 2) - 60, (screen_height / 2) - 100)])
    # starting animation
    for i in range (37):
        time.sleep(1 / 60)
        intro_objects[2][1] = (intro_objects[2][1][0], intro_objects[2][1][1] + Yv)
        Yv += .4
        intro_update()
    intro_objects[2][1] = ((screen_width / 2) - 60, (screen_height / 2) - 40)
    intro_update()
    mixer.music.play() 
    intro_objects[2][1] = ((screen_width / 2) - 60, (screen_height / 2) + 15)
    intro_objects[1][1] = ((screen_width / 2) - 120, (screen_height / 2) - 40)
    intro_update()
    Yv = -3.4
    for i in range (38):
        time.sleep(1 / 60)
        intro_objects[2][1] = (screen_width / 2) - 60, ((intro_objects[2][1][1]) + Yv)
        intro_objects[1][1] = (screen_width / 2) - 120, ((intro_objects[1][1][1]) + Yv)
        Yv += .1
        intro_update()
    intro_objects[2][1] = ((screen_width / 2) - 60, (screen_height / 2) - 45)
    intro_objects[1][1] = ((screen_width / 2) - 120, (screen_height / 2) - 100)
    intro_update()
    time.sleep(0.3)
    # startup sequence has ended
    run = True
else:
    run = True

while run: # this is the main loop. father forgive me for i have sinned
    tick(60)
    getkeys()
    getNonRepeatingKeys()
    get_mouse()
    render()
    intro_update()
    settings[4] = buildpathsdata
    if fade > 0:
        fade -= 10
    if BuildPathsText == 'Invalid!':
        timer += 1
    if timer > 80:
        timer = 0
        BuildPathsText = ''
    elif pygame.time.get_ticks() > 5000:
        intro_objects = []
    if configEditorOpen or SettingsOpen:
        SubmenuBGSurfaceYvar += (40 - SubmenuBGSurfaceYvar) / 12
    else:
        SubmenuBGSurfaceYvar += (-1250 - SubmenuBGSurfaceYvar) / 12
    if BuildPathsConfigOpen != -1:
        BuildPathsYvar += (910 - BuildPathsYvar) / 12
    else:
        BuildPathsYvar += (1300 - BuildPathsYvar) / 12
    if mousestate == 1:
        typing = -1
    if 'pygame.K_RETURN' in NonRepeatingKeys:
        if configEditorOpen:
            if typing != -1:
                typing = -1
            else:
                configEditorOpen = False
                for i, v in enumerate(ImportantConfigs):
                    ConfigToSet = txtversion[int(v)][txtversion[int(v)].find('= ') + 2:txtversion[int(v)].find('#')] # value of the setting we are going to change, True, False, etc
                    ConfigName = txtversion[int(v)][:txtversion[int(v)].find('= ')] # the name of the config option itself, mute, xop_left_shifts, etc
                    ConfigValueToSet = ConfigSettingsButtons[i][4] # new version from the buttons updated data, True, "any", etc
                    if ConfigSettingsButtons[i][3] == 'text':
                        if has_numbers(ConfigSettingsButtons[i][4]):
                            txtversion[v] = txtversion[v].replace(ConfigToSet,str(ConfigValueToSet).strip().lower() + str([' ' * 20])[2:-2])
                        else:
                            txtversion[v] = txtversion[v].replace(ConfigToSet, '"' + str(ConfigValueToSet).strip().lower() + '"' + str([' ' * 20])[2:-2])
                    elif ConfigSettingsButtons[i][3] == 'bool':
                        txtversion[v] = txtversion[v].replace(ConfigToSet, str(ConfigValueToSet).strip().lower() + str([' ' * 20])[2:-2])
                    updatedTOMl = dumps(TOMLToEdit) # TOMLToEdit is the doc
                    with open(gamesroot + '\\' + ConfigOpen + '\\' + ConfigOpen + '.toml', 'w+') as i:
                        i.write(''.join(txtversion))
                        i.close()
                    if os.path.exists(gamesroot + '\\' + ConfigOpen + '\\' + ConfigOpen + '.txt'):
                        os.remove(gamesroot + '\\' + ConfigOpen + '\\' + ConfigOpen + '.txt')
                    TooltipOpen = False
        elif SettingsOpen:
            if typing != -1:
                typing = -1
            else:
                Settingstxt = open(UIRoot + 'txt\\settings.txt', 'r').readlines()
                while '' in Settingstxt: Settingstxt.remove('')
                print('settings txt is: ' + str(Settingstxt))
                for i, v in enumerate(Settingstxt[:-2]):
                    ConfigToSet = Settingstxt[i][Settingstxt[i].find('= ') + 2:Settingstxt[i].find('#')] # value of the setting we are going to change, True, False, etc
                    ConfigName = Settingstxt[i][:Settingstxt[i].find('= ')] # the name of the config option itself, mute, xop_left_shifts, etc
                    ConfigValueToSet = SettingsButtons[i][4] # new version from the buttons updated data, True, "any", etc
                    if SettingsButtons[i][3] == 'text':
                        if has_numbers(SettingsButtons[i][4]):
                            Settingstxt[i] = Settingstxt[i].replace(ConfigToSet,str(ConfigValueToSet).strip().lower() + ' ')
                        elif '"' not in ConfigValueToSet:
                            Settingstxt[i] = Settingstxt[i].replace(ConfigToSet, '"' + str(ConfigValueToSet).strip().lower() + '"' + str([' ' * 20])[2:-2])
                        else:
                            Settingstxt[i] = Settingstxt[i].replace(ConfigToSet, str(ConfigValueToSet).strip().lower() + str([' ' * 20])[2:-2])
                    elif SettingsButtons[i][3] == 'bool':
                        Settingstxt[i] = Settingstxt[i].replace(ConfigToSet, str(ConfigValueToSet).strip().lower().capitalize() + ' ')
                    else:
                        print(v)
                with open(UIRoot + 'txt\\settings.txt', 'w+') as i:
                    i.write(''.join(Settingstxt))
                    i.close()
                load_settings()
                SettingsOpen = False

    if 'pygame.K_ESCAPE' in NonRepeatingKeys:
        configEditorOpen = False
        TooltipOpen = False
        SettingsOpen = False
        if os.path.exists(gamesroot + ConfigOpen + '\\' + ConfigOpen + '.txt'):
            os.remove(gamesroot + '\\' + ConfigOpen + '\\' + ConfigOpen + '.txt')
    for i, v in enumerate(ui_objects):
        if ui_objects[i][0].get_rect().collidepoint((mx - ui_objects[i][1], my - ui_objects[i][2] )):
            ui_objects[i][0].set_alpha(200 - ui_objects[i][0].get_alpha()/ 3)
            if mousestate == 1 and configEditorOpen == False and SettingsOpen == False:
                if v[5] == 'close':
                    pygame.quit(), exit()
                if v[5] == 'settings':
                    SettingsOpen = True
                    SubmenuScroll = 50
                if v[5] == 'credits':
                    os.startfile(r'txt\\credits.txt')
                if v[5] == 'patches':
                    try:
                        os.startfile(Root + 'patches')
                    except:
                        pass
        else:
            ui_objects[i][0].set_alpha(ui_objects[i][0].get_alpha() - -20 / 3)
    for i, v in enumerate(GameButtons):
        if GameButtons[i][0].get_rect().collidepoint((mx - GameButtons[i][1], my - GameButtons[i][2] )):
            GameButtons[i][0].set_alpha(200 - GameButtons[i][0].get_alpha()/ 3)
            if mousestate == 1 and configEditorOpen == False and SettingsOpen == False:
                pygame.mouse.set_pos((screen_width / 2, screen_height / 2))
                try:
                    os.remove(Root + '\\' + 'xenia-canary-config.toml')
                except:
                    pass
                for i2, v2 in enumerate(games): # you need to copy the config file to the specified xenia build path if there is one, instead of the root folder
                    if v2[0] == GameButtons[i][5]:
                        exepath = ''
                        for i3, v3 in enumerate(buildpathsdata):
                            if v3[0] == games[i][0]:
                                exepath = v3[1]
                        if exepath == '':
                            exepath = Root + 'xenia_canary.exe'
                        gamepath = gamesroot + games[i2][0] + '\\'
                        shutil.copyfile(gamepath + games[i2][3], exepath[:exepath.rfind('\\')] + '\\' + games[i2][3])
                        try:
                            os.remove(exepath[:exepath.rfind('\\')] + '\\' + 'xenia-canary.config.toml')
                        except:
                            pass
                        os.rename(exepath[:exepath.rfind('\\')] + '\\' + games[i2][3],exepath[:exepath.rfind('\\')] + '\\' + 'xenia-canary.config.toml')
                        counter = 0
                        for file in os.listdir(gamepath + games[i2][0]):
                            counter += 1
                            files.append(os.fsdecode(file))
                        if len(files) == 1:
                            gamepath += '\\' + files[0]
                        else:
                            for i in files:
                                if '.xex' in i:
                                    gamepath += games[i2][0] + '\\' + i
                                    break
                        subprocess.run([exepath, gamepath])
                        if CloseLaunch == True:
                            pygame.quit(), exit()
        else:
            GameButtons[i][0].set_alpha(GameButtons[i][0].get_alpha() - -20 / 3)
        for i, v in enumerate(buildpaths):
            if buildpaths[i][0].get_rect().collidepoint((mx - buildpaths[i][1], my - buildpaths[i][2] )):
                buildpaths[i][0].set_alpha(200 - buildpaths[i][0].get_alpha()/ 3)
                if mousestate == 1 and configEditorOpen == False and SettingsOpen == False and BuildPathsConfigOpen == -1:
                    BuildPathsConfigOpen = i
                    for i2, v2 in enumerate(buildpathsdata):
                        if v2[0] == games[i][0]:
                            BuildPathsText = v2[1]
            else:
                buildpaths[i][0].set_alpha(buildpaths[i][0].get_alpha() - -20 / 3)
        for i, v in enumerate(ConfigButtons):
            if ConfigButtons[i][0].get_rect().collidepoint((mx - ConfigButtons[i][1], my - ConfigButtons[i][2] )):
                    ConfigButtons[i][0].set_alpha(200 - ConfigButtons[i][0].get_alpha()/ 3)
                    if mousestate == 1 and configEditorOpen == False and SettingsOpen == False:
                        pygame.mouse.set_pos((screen_width/2, screen_height / 2))
                        tomlpath = gamesroot + games[i][0]
                        ConfigOpen = games[i][0]
                        shutil.copyfile(tomlpath + '\\' + games[i][0] + '.toml', tomlpath + '\\' + Path(tomlpath).stem + '.txt') # we copy the toml file and paste it as a txt file
                        txtversion = open(gamesroot + games[i][0] + '\\' + games[i][0] + '.txt').readlines() # we read and edit the txt file as a list, then save it back as the toml file
                        counter = 0
                        for i, v in enumerate(txtversion):
                            txtversion[i] = v.replace('\t', '')
                            if txtversion[i] == '\n' or '':
                                txtversion[i] = ' '
                        while counter < len(txtversion):
                            if txtversion[counter] == ' ':
                                txtversion.pop(counter)
                            else:
                                counter += 1
                        load_config()
                        SubmenuScroll = 50
                        configEditorOpen = True
                        # config editor code here
            else:
                ConfigButtons[i][0].set_alpha(ConfigButtons[i][0].get_alpha() - -20 / 3)
        for i, v in enumerate(FilesButtons):
            if FilesButtons[i][0].get_rect().collidepoint((mx - FilesButtons[i][1], my - FilesButtons[i][2])):
                FilesButtons[i][0].set_alpha(200 - FilesButtons[i][0].get_alpha()/ 3)
                if mousestate == 1 and configEditorOpen == False and SettingsOpen == False:
                    os.startfile(gamesroot + '\\' + games[i][0])
            else:
                FilesButtons[i][0].set_alpha(FilesButtons[i][0].get_alpha() - -20 / 3)
    TooltipOpen = False
    if configEditorOpen == True:
        for i, v in enumerate(tooltips):
            tooltips[i][1] = 64
            tooltips[i][2] = (i * 100) + SubmenuScroll + SubmenuBGSurfaceYvar
            if tooltips[i][0].get_rect().collidepoint((mx - tooltips[i][1], my - tooltips[i][2] )):
                tooltips[i][0].set_alpha(200 - tooltips[i][0].get_alpha()/ 3)
                TooltipSurfaceBack[2] += (70 - TooltipSurfaceBack[2]) / 6
                TooltipOpen = True
                counter = ImportantConfigs[i]
                TooltipText = txtversion[counter][txtversion[counter].find('#') + 2:]
                counter += 1
                while txtversion[counter + 1][0] == ' ':
                    TooltipText = TooltipText + ' ' + txtversion[counter][txtversion[counter].find('#') + 2:].strip()
                    counter += 1
                TooltipText = textwrap.fill(TooltipText, 45)
                TooltipText = TooltipText.split('\n')
                # Tooltiptext is the list with all the text the tooltip has, just need to render the popup
            else:
                tooltips[i][0].set_alpha(tooltips[i][0].get_alpha() - -20 / 3)
        if TooltipOpen == False:
            TooltipSurfaceBack[2] += (-500 - TooltipSurfaceBack[2]) / 6
            TooltipText = []
            TooltipText.append('what do you call a magic dog?') # this is a funny joke please laugh
            [TooltipText.append('') for i in range (3)]
            TooltipText.append('a labra-cadabra dor')
        for i, v in enumerate(ConfigSettingsButtons):
            # config text surface
            ConfigSettingsButtons[i][2] = (i * 100) + SubmenuScroll + SubmenuBGSurfaceYvar - 5
            if ConfigSettingsButtons[i][0].get_rect().collidepoint((mx - ConfigSettingsButtons[i][1], my - ConfigSettingsButtons[i][2] )):
                try:
                    ConfigSettingsButtons[i][0].set_alpha(140 - ConfigSettingsButtons[i][0].get_alpha() / 3)
                except:
                    pass
                if mousestate == 1: 
                    if v[3] == 'bool':
                        if v[4] == True:
                            ConfigSettingsButtons[i][4] = False
                            v[0] = pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\false.png').convert_alpha(), (80, 80))
                            ConfigSettingsButtons[i][0].set_alpha(140)
                        elif v[4] == False:
                            ConfigSettingsButtons[i][4] = True
                            v[0] = pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\true.png').convert_alpha(), (80, 80))
                            ConfigSettingsButtons[i][0].set_alpha(140)
                    else:
                        if v[3] == 'text':
                            typing = i
            if typing == i and v[3] == 'text':
                if len(NonRepeatingKeys) > 0:
                    if NonRepeatingKeys[0] == 'pygame.K_BACKSPACE': 
                        ConfigSettingsButtons[typing][4] = ConfigSettingsButtons[typing][4][:-1]
                    elif len(NonRepeatingKeys[0]) == 10:
                        ConfigSettingsButtons[typing][4] += NonRepeatingKeys[0][-1]
                    elif NonRepeatingKeys[0] == 'pygame.K_PERIOD':
                        ConfigSettingsButtons[typing][4] += '.'
                    elif NonRepeatingKeys[0] == 'pygame.K_SPACE':
                        ConfigSettingsButtons[typing][4] += ' '
            else:
                pass
                try:
                    ConfigSettingsButtons[i][0].set_alpha(200 - ConfigSettingsButtons[i][0].get_alpha() / 3)
                except:
                    pass
    SettingsTipsOpen = False
    if SettingsOpen:
        for i, v in enumerate(SettingsTips):
            SettingsTips[i][1] = 64
            SettingsTips[i][2] = (i * 100) + SubmenuScroll + SubmenuBGSurfaceYvar
            if SettingsTips[i][0].get_rect().collidepoint((mx - SettingsTips[i][1], my - SettingsTips[i][2] )):
                SettingsTips[i][0].set_alpha(200 - SettingsTips[i][0].get_alpha() / 3)
                TooltipSurfaceBack[2] += (70 - TooltipSurfaceBack[2]) / 6
                SettingsTipsOpen = True
                SettingsTipsText = v[3]
                SettingsTipsText = textwrap.fill(SettingsTipsText, 45)
                SettingsTipsText = SettingsTipsText.split('\n')
            else:
                SettingsTips[i][0].set_alpha(SettingsTips[i][0].get_alpha() - -20 / 3)
        for i, v in enumerate(SettingsButtons):
            # config text surface
            SettingsButtons[i][2] = (i * 100) + SubmenuScroll + SubmenuBGSurfaceYvar - 5
            if SettingsButtons[i][0].get_rect().collidepoint((mx - SettingsButtons[i][1], my - SettingsButtons[i][2] )):
                try:
                    SettingsButtons[i][0].set_alpha(140 - SettingsButtons[i][0].get_alpha() / 3)
                except:
                    pass
                if mousestate == 1: 
                    if v[3] == 'bool':
                        if v[4] == True:
                            SettingsButtons[i][4] = False
                            v[0] = pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\false.png').convert_alpha(), (80, 80))
                            SettingsButtons[i][0].set_alpha(140)
                        elif v[4] == False:
                            SettingsButtons[i][4] = True
                            v[0] = pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\true.png').convert_alpha(), (80, 80))
                            SettingsButtons[i][0].set_alpha(140)
                    else:
                        if v[3] == 'text':
                            typing = i
            if typing == i and v[3] == 'text':
                if len(NonRepeatingKeys) > 0:
                    if NonRepeatingKeys[0] == 'pygame.K_BACKSPACE': 
                        SettingsButtons[typing][4] = SettingsButtons[typing][4][:-1]
                    elif len(NonRepeatingKeys[0]) == 10:
                        SettingsButtons[typing][4] += NonRepeatingKeys[0][-1]
                    elif NonRepeatingKeys[0] == 'pygame.K_PERIOD':
                        SettingsButtons[typing][4] += '.'
                    elif NonRepeatingKeys[0] == 'pygame.K_SPACE':
                        SettingsButtons[typing][4] += ' '
            else:
                pass
                try:
                    SettingsButtons[i][0].set_alpha(200 - SettingsButtons[i][0].get_alpha() / 3)
                except:
                    print('the maths aint mathing chief')
    SaveSurface[2] = BuildPathsYvar + 20
    PasteSurface[2] = BuildPathsYvar + 20
    CloseSurface[2] = BuildPathsYvar + 20
    EraseSurface[2] = BuildPathsYvar + 20
    if SaveSurface[0].get_rect().collidepoint((mx - SaveSurface[1], my - SaveSurface[2] )):
        SaveSurface[0].set_alpha(140 - SaveSurface[0].get_alpha() / 3)
        if mousestate == 1:
            print('saving')
            Settingstxt = open(UIRoot + 'txt\\settings.txt', 'r').readlines()
            if BuildPathsText != '':
                if len(buildpathsdata) > 1:
                    for i, v in enumerate(buildpathsdata):
                        if v[0] == games[BuildPathsConfigOpen][0]:
                            buildpathsdata[configEditorOpen][1] = BuildPathsText.replace('"', '')
                else:
                    print(games[BuildPathsConfigOpen][0])
                    print(BuildPathsConfigOpen)
                    buildpathsdata.append([games[BuildPathsConfigOpen][0], BuildPathsText.replace('"', '')])
                try:
                    Settingstxt[4] = str(buildpathsdata) + '\n'
                except:
                    print('this was useful')
                    settingstxt.append(str(buildpathsdata) + '\n')
            else:
                for i, v in enumerate(buildpathsdata):
                    if v[0] == games[BuildPathsConfigOpen][0]:
                        buildpathsdata.pop(i)
                        try:
                            Settingstxt[4] = str(buildpathsdata) + '\n'
                        except:
                            print('this was useful')
                            settingstxt.append(str(buildpathsdata) + '\n')
            with open(UIRoot + 'txt\\settings.txt', 'w+') as i:
                i.write(''.join(Settingstxt))
                i.close()
            BuildPathsConfigOpen = -1
            BuildPathsText = ''
            load_settings()
    else:
        SaveSurface[0].set_alpha(200 - PasteSurface[0].get_alpha() / 3)
    if PasteSurface[0].get_rect().collidepoint((mx - PasteSurface[1], my - PasteSurface[2] )):
        PasteSurface[0].set_alpha(140 - PasteSurface[0].get_alpha() / 3)
        if mousestate == 1:
            if os.path.exists(Tk().clipboard_get().replace('"', '')):
                BuildPathsText = Tk().clipboard_get()
            else:
                BuildPathsText = 'Invalid!'
    else:
        PasteSurface[0].set_alpha(200 - CloseSurface[0].get_alpha() / 3)
    if CloseSurface[0].get_rect().collidepoint((mx - CloseSurface[1], my - CloseSurface[2] )):
        CloseSurface[0].set_alpha(140 - CloseSurface[0].get_alpha() / 3)
        if mousestate == 1:
            BuildPathsConfigOpen = -1
            BuildPathsText = ''
    else:
        CloseSurface[0].set_alpha(200 - CloseSurface[0].get_alpha() / 3)
    if EraseSurface[0].get_rect().collidepoint((mx - EraseSurface[1], my - EraseSurface[2] )):
        EraseSurface[0].set_alpha(140 - EraseSurface[0].get_alpha() / 3)
        if mousestate == 1:
            BuildPathsText = ''
    else:
        EraseSurface[0].set_alpha(200 - EraseSurface[0].get_alpha() / 3)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and configEditorOpen == False and SettingsOpen == False:
            if event.button == 4:
                mainscroll += 4
            elif event.button == 5:
                mainscroll -= 4
        elif event.type == pygame.MOUSEBUTTONDOWN and (configEditorOpen or SettingsOpen):
            if event.button == 4:
                SubmenuScroll += 22
            elif event.button == 5:
                SubmenuScroll -= 22
    if mainscroll > 0: mainscroll = 0
    if SubmenuScroll > 50: SubmenuScroll = 50
    newscreen = pygame.transform.smoothscale(screen, WindowInfo) 
    window.blit(newscreen, (0, 0))
    pygame.display.update()