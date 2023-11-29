# thx to https://www.svgrepo.com/ for button icons
# 315, 119
import pygame, sys, math, random, time, os, shutil, subprocess, tomlkit, toml, textwrap
from sys import exit
from pygame import mixer
from pathlib import Path
from tomlkit import dumps, parse # tomlkit is a fucking pain. toml files in general in python are ass. i tried working with a txt instead and everything instantly worked.

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
ConfigSettingsButtons = []
SettingsButtons = []
tooltips = []
SettingsTips = []
FNULL = open(os.devnull, 'w')
tomlpath = str()
TOMLToEdit = dict()
TOMLobj = 0
txtversion = []
SubmenuBGSurfaceXvar = -500
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
VersionName = 'XenUI v7'


def setup_pygame(): # we draw everything to screen then draw screen onto window, which is the final scaled display surface
    global keycodes, keynames, screen, clock, window, screen_info, Root, UIRoot
    pygame.init()
    pygame.display.set_caption('XenUI by Paths (v7.0)')
    screen_info = pygame.display.Info()
    screen = pygame.Surface((screen_info.current_w, screen_info.current_h))
    window = pygame.display.set_mode((screen_info.current_w / 1.99, screen_info.current_h / 1.99))
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
    global mousestate
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
    global ui_assets, testsurface, banners, Root, imgW, imgH, ratio, BannerFont, banner_height, SubmenuBGSurface, configEditorBGtxt, ImportantConfigs, tooltips, TooltipSurfaceBack, ConfigFont, TooltipFont, ConfigTextSurface, SettingsTips, Root, UIRoot
    gamesroot = Root + 'Games'
    ImportantConfigs = open(UIRoot + 'txt\\important configs.txt').readlines() # load this here so we can append the tooltip button surfaces
    ui_objects.append([pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\close.png').convert_alpha(), (40, 40)), 16, 480, 60, 60, 'close'])
    ui_objects.append([pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\credits.png').convert_alpha(), (40, 40)), 16, 420, 60, 60, 'credits'])
    ui_objects.append([pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\settings.png').convert_alpha(), (40, 40)), 16, 360, 60, 60, 'settings'])
    for i, v in enumerate(games):
        try:
            img = pygame.image.load(gamesroot + '\\' + v[0] + '\\' + v[1])
        except:
            img = pygame.image.load(r'textures and sfx\\default banner.png')
        imgW = img.get_width()
        imgH = img.get_height()
        if imgW > imgH:
            ratio = imgW / imgH
        else:
            ratio = imgH / imgW
        img = pygame.transform.scale(img, (840, 850 / ratio))
        imgW = img.get_width()
        imgH = img.get_height()
        banners.append([img, (100, 20), (0, (imgH / 2) - 50, 880, banner_height)])
    for i, v in enumerate(games):
        GameButtons.append([pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\play.png').convert_alpha(), (banner_height / 1.7, banner_height / 1.7)), 870, 38 + ((banner_height * 1.3) * i), 60, 60, v[0]])
    for i, v in enumerate(games):
        ConfigButtons.append([pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\config.png').convert_alpha(), (banner_height / 1.7, banner_height / 1.7)), 820, 38 + ((banner_height * 1.3) * i), 60, 60, v[0]])
    for i, v in enumerate(ImportantConfigs):
        ImportantConfigs[i] = int(v) - 1
        tooltips.append([pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\tooltip.png').convert_alpha(), (40, 40)), 0, 0, v])
    for i, v in enumerate(settings):
        SettingsTips.append([pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\tooltip.png').convert_alpha(), (40, 40)), 0, 0, v[v.find('#') + 2:]])
    pygame.font.init()
    BannerFont = pygame.font.SysFont(Font, int(banner_height / 3.3))
    BannerFont.set_bold(True)
    ConfigFont = pygame.font.SysFont(Font, 20)
    ConfigFont.set_bold(False)
    TooltipFont = pygame.font.SysFont(Font, 18)
    TooltipFont.set_bold(True)
    SubmenuBGSurface = pygame.Surface((screen_info.current_w / 2.09, 470)); SubmenuBGSurface.fill('black')
    configEditorBGtxt = BannerFont.render('Press Enter to save' + str([' ' * 70])[2:-2] + 'Press Escape to discard changes', False, (250, 250, 250))
    TooltipSurfaceBack = [pygame.Surface((430, 400)), 520, -1000]
    TooltipSurfaceBack[0].fill('grey10')
    TooltipSurfaceBack[0].set_alpha(200)
    TooltipTextSurface =  ConfigFont.render('you shouldnt see this.... report this bug pls', False, (250, 250, 250))
    ConfigTextSurface = pygame.Surface((150, 35))
    ConfigTextSurface.fill('grey5')

def load_config():
    global ConfigSettingsButtons, Root, UIRoot
    ConfigSettingsButtons = []
    x = screen_info.current_w - (screen_info.current_w / 1.67)
    print(x)
    for i, v in enumerate(ImportantConfigs):
        line = txtversion[v]
        if line[line.find('=') + 2:line.find('  ')] == 'true':
            ConfigSettingsButtons.append([pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\true.png').convert_alpha(), (40, 40)), x, i * 35 - 20, 'bool', True])
        elif line[line.find('=') + 2:line.find('  ')] == 'false':
            ConfigSettingsButtons.append([pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\false.png').convert_alpha(), (40, 40)), x, i * 35 - 20, 'bool', False])
        else:
            ConfigSettingsButtons.append([pygame.Surface((300, 50)), x, i * 35 - 20, 'text', line[line.find('= ') + 2:line.find('#')].strip().replace('"', '')])
        ConfigSettingsButtons[i][0].set_alpha(100)
    for i, v in enumerate(ConfigSettingsButtons):
        if v[3] == 'text':
            if v[4] == 'true':
                ConfigSettingsButtons[i] = [pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\true.png').convert_alpha(), (40, 40)), x, i * 35 - 20, 'bool', True]
            if v[4] == 'false':
                ConfigSettingsButtons[i] = [pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\false.png').convert_alpha(), (40, 40)), x, i * 35 - 20, 'bool', False]

def load_settings():
    global SettingsButtons, settings, Root, UIRoot
    SettingsButtons = []
    x = screen_info.current_w - (screen_info.current_w / 1.67)
    for i, v in enumerate(settings):
        line = v[v.find('= ') + 2:v.find('# ') - 1]
        if line == 'True':
            SettingsButtons.append([pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\true.png').convert_alpha(), (40, 40)), x, i * 35 - 20, 'bool', True])
        elif line == 'False':
            SettingsButtons.append([pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\false.png').convert_alpha(), (40, 40)), x, i * 35 - 20, 'bool', False])
        else:
            SettingsButtons.append([pygame.Surface((400, 50)), x, i * 35 - 20, 'text', line.replace("'", '')])

def load_games():
    global Root, UIRoot
    Root = sys.argv[0]
    Root = Root[:Root.find('XenUI') - 1] + '\\'
    for file in os.listdir(Root + '\\' + 'Games'):
        gamename = os.fsdecode(file)
        pngname = 'NULL'
        xexname = 'NULL'
        tomlname = 'NULL'
        for file in os.listdir(Root + '\\' + 'Games' + '\\' + gamename):
            if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jpeg'):
                pngname = os.fsdecode(file)
            if file == gamename:
                xexname = Root + gamename + gamename + 'default.xex'
            if file.endswith('.toml'):
                tomlname = os.fsdecode(file)
        games.append([gamename, pngname, xexname, tomlname])

def render():
    global GameButtons, banner_height, SubmenuBGSurface, configEditorBGtxt, ImportantConfigs, txtversion, NonRepeatingKeysPressed, tooltips, TooltipSurfaceBack, TooltipText, TooltipTextSurfaceXvar, ConfigFont, TooltipFont, ConfigSettingsButtons, ConfigTextSurface, SettingsTipsOpen, SettingsTips, SettingsTipsText, SettingsButtons
    screen.blit(pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\bg.png').convert_alpha(), (screen_width, screen_height)), (0, 0))
    screen.blit(pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\sidebar.png').convert_alpha(), (80, 563)), (0, 0))
    dark = pygame.Surface((840, banner_height), 32)
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
    screen.blit(SubmenuBGSurface, (19, SubmenuBGSurfaceXvar + 12)) # the very back black background
    # screen.blit(configEditorBGtxt, (40, SubmenuBGSurfaceXvar + 465))
    if configEditorOpen:
        for i, v in enumerate(ImportantConfigs):
            if SubmenuScroll + (i * 45) + 25 > 40 and SubmenuScroll + (i * 45) + 25 < 490:
                screen.blit(ConfigFont.render(txtversion[int(v)][:txtversion[int(v)].find('=')], False, (250, 250, 250)), (100, SubmenuBGSurfaceXvar + SubmenuScroll + (i * 45) - 10))
        for i, v in enumerate(tooltips):
            if SubmenuScroll + (i * 45) + 25 > 40 and SubmenuScroll + (i * 45) + 25 < 490:
                screen.blit(v[0], (v[1], v[2]))
        for i, v in enumerate(ConfigSettingsButtons):
            if v[2] > 50 and v[2] < SubmenuBGSurfaceXvar + 470:
                if v[3] == 'bool':
                    screen.blit(v[0], (v[1], v[2] - 10))
                elif v[3] == 'text':
                    screen.blit(ConfigTextSurface, (v[1], v[2] - 10))
                    pygame.draw.rect(screen, 'grey10', pygame.Rect(v[1], v[2] - 10, 150, 35),  5, 5, 5, 5)
                    screen.blit(ConfigFont.render(v[4], False, (250, 250, 250)), (v[1] + 10, v[2] - 8))
        pygame.draw.rect(screen, 'grey10', pygame.Rect(520, TooltipSurfaceBack[2], 450, len(TooltipText * 22) + 20),  20, 20, 20, 20)
        screen.blit(TooltipSurfaceBack[0], (TooltipSurfaceBack[1], TooltipSurfaceBack[2]))
        for i, v in enumerate(TooltipText):
            screen.blit(TooltipFont.render(str(v), False, (250, 250, 250)), (550, TooltipSurfaceBack[2] + (i * 22) + 8))
    if TooltipOpen:
        TooltipSurfaceBack[0] = pygame.Surface((430, len(TooltipText * 22))) # we need to set the size here
    if SettingsTipsOpen:
        TooltipSurfaceBack[0] = pygame.Surface((430, len(SettingsTipsText * 22))) # we need to set the size here
    TooltipSurfaceBack[0].fill('grey10')
    if TooltipOpen or SettingsTipsOpen:
        TooltipSurfaceBack[2] += (50 - TooltipSurfaceBack[2]) / 7
    else:
        TooltipSurfaceBack[2] += (-500 - TooltipSurfaceBack[2]) / 7
    if SettingsOpen:
        for i, v in enumerate(settings[0:len(settings)]):
            if SubmenuScroll + (i * 45) + 25 > 40 and SubmenuScroll + (i * 45) + 25 < 490:
                screen.blit(ConfigFont.render(v[:v.find('= ')], False, (250, 250, 250)), (100, SubmenuBGSurfaceXvar + SubmenuScroll + (i * 45) - 10))
        for i, v in enumerate(SettingsButtons):
            if v[2] > 50 and v[2] < SubmenuBGSurfaceXvar + 470:
                if v[3] == 'bool':
                    screen.blit(v[0], (v[1], v[2] - 10))
                elif v[3] == 'text':
                    screen.blit(ConfigTextSurface, (v[1], v[2] - 10))
                    pygame.draw.rect(screen, 'grey10', pygame.Rect(v[1], v[2] - 10, 150, 35),  5, 5, 5, 5)
                    screen.blit(ConfigFont.render(v[4], False, (250, 250, 250)), (v[1] + 10, v[2] - 8))
        pygame.draw.rect(screen, 'grey10', pygame.Rect(520, TooltipSurfaceBack[2], 450, len(SettingsTipsText * 22) + 20),  20, 20, 20, 20)
        screen.blit(TooltipSurfaceBack[0], (TooltipSurfaceBack[1], TooltipSurfaceBack[2]))
        for i, v in enumerate(SettingsTips):
            if SubmenuScroll + (i * 45) + 25 > 40 and SubmenuScroll + (i * 45) + 25 < 490:
                screen.blit(v[0], (v[1], v[2]))
        for i, v in enumerate(SettingsTipsText):
            screen.blit(TooltipFont.render(str(v), False, (250, 250, 250)), (550, TooltipSurfaceBack[2] + (i * 22) + 8))
    pygame.draw.rect(screen, 'black', pygame.Rect(13, SubmenuBGSurfaceXvar, screen_info.current_w / 2.04, 500),  30, 30, 30, 30)
    screen.blit(configEditorBGtxt, (40, SubmenuBGSurfaceXvar + 465))
    BannerFont.set_bold(True)

def intro_update():
    global fade
    for i in intro_objects:
        i[0].set_alpha(fade)
        screen.blit(i[0], (i[1][0], i[1][1]))
        newscreen = pygame.transform.smoothscale(screen, (screen_info.current_w, screen_info.current_h)) 
        window.blit(newscreen, (0, 0))
    pygame.display.update();

# applying setting variables now
Root = sys.argv[0]
Root = Root[:Root.find('XenUI') - 1] + '\\'
UIRoot = Root + VersionName + '\\'
settings = open(UIRoot + 'txt\\settings.txt', 'r')
settings = settings.readlines()
for i, v in enumerate(settings):
    settings[i] = str(v.strip('\n'))
for i, v in enumerate(settings):
    exec(v)
settings[1] = settings[1].replace('"', '')
print(settings)


icon = pygame.image.load(UIRoot + 'textures and sfx\\canary.png')
setup_pygame()
load_settings()
load_config()
load_games()
pygame.display.set_icon(icon)
load_assets()
# now setting up the startup animation and mixer for sfx
if playintro == True:
    mixer.init()
    mixer.music.load(UIRoot + 'textures and sfx\\startup.wav')
    mixer.music.set_volume(0.1)
    screen.fill('grey3')
    intro_objects.append([pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\intro bg.png').convert_alpha(), (screen_info.current_w, screen_info.current_h)), (0, 0)])
    intro_objects.append([pygame.image.load(UIRoot + 'textures and sfx\\xenia back.png').convert_alpha(), (screen_width / 2 - 120, screen_height / 2 - 100)])
    intro_objects.append([pygame.image.load(UIRoot + 'textures and sfx\\X.png').convert_alpha(), ((screen_width / 2) - 60, (screen_height / 2) - 100)])
    # starting animation
    for i in range (37):
        time.sleep(1 / 120)
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
        time.sleep(1 / 120)
        intro_objects[2][1] = (screen_width / 2) - 60, ((intro_objects[2][1][1]) + Yv)
        intro_objects[1][1] = (screen_width / 2) - 120, ((intro_objects[1][1][1]) + Yv)
        Yv += .1
        intro_update()
    intro_objects[2][1] = ((screen_width / 2) - 60, (screen_height / 2) - 45)
    intro_objects[1][1] = ((screen_width / 2) - 120, (screen_height / 2) - 100)
    intro_update()
    time.sleep(.3)
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
    if fade > 0:
        fade -= 10
    elif len(intro_objects) > 1:
        intro_objects = []
    if configEditorOpen or SettingsOpen:
        SubmenuBGSurfaceXvar += (32 - SubmenuBGSurfaceXvar) / 12
    else:
        SubmenuBGSurfaceXvar += (-520 - SubmenuBGSurfaceXvar) / 12
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
                    with open(Root + '\\' + 'Games' + '\\' + ConfigOpen + '\\' + ConfigOpen + '.toml', 'w+') as i:
                        i.write(''.join(txtversion))
                        i.close()
                    if os.path.exists(Root + '\\' + 'Games' + '\\' + ConfigOpen + '\\' + ConfigOpen + '.txt'):
                        os.remove(Root + '\\' + 'Games' + '\\' + ConfigOpen + '\\' + ConfigOpen + '.txt')
                    TooltipOpen = False
        elif SettingsOpen:
            if typing != -1:
                typing = -1
            else:
                Settingstxt = open(UIRoot + 'txt\\settings.txt', 'r').readlines()
                for i, v in enumerate(Settingstxt):
                    ConfigToSet = Settingstxt[i][Settingstxt[i].find('= ') + 2:Settingstxt[i].find('#')] # value of the setting we are going to change, True, False, etc
                    ConfigName = Settingstxt[i][:Settingstxt[i].find('= ')] # the name of the config option itself, mute, xop_left_shifts, etc
                    ConfigValueToSet = SettingsButtons[i][4] # new version from the buttons updated data, True, "any", etc
                    if SettingsButtons[i][3] == 'text':
                        if has_numbers(SettingsButtons[i][4]):
                            Settingstxt[i] = Settingstxt[i].replace(ConfigToSet,str(ConfigValueToSet).strip().lower() + ' ')
                        else:
                            Settingstxt[i] = Settingstxt[i].replace(ConfigToSet, '"' + str(ConfigValueToSet).strip().lower() + '"' + ' ')
                    elif SettingsButtons[i][3] == 'bool':
                        Settingstxt[i] = Settingstxt[i].replace(ConfigToSet, str(ConfigValueToSet).strip().lower().capitalize() + ' ')
                with open(UIRoot + 'txt\\settings.txt', 'w+') as i:
                    i.write(''.join(Settingstxt))
                    i.close()
                load_settings()
                SettingsOpen = False

    if 'pygame.K_ESCAPE' in NonRepeatingKeys:
        configEditorOpen = False
        TooltipOpen = False
        SettingsOpen = False
        if os.path.exists(Root + '\\' + 'Games' + '\\' + ConfigOpen + '\\' + ConfigOpen + '.txt'):
            os.remove(Root + '\\' + 'Games' + '\\' + ConfigOpen + '\\' + ConfigOpen + '.txt')
    for i, v in enumerate(ui_objects):
        if ui_objects[i][0].get_rect().collidepoint((pygame.mouse.get_pos()[0] - ui_objects[i][1], pygame.mouse.get_pos()[1] - ui_objects[i][2] )):
            ui_objects[i][0].set_alpha(200 - ui_objects[i][0].get_alpha()/ 3)
            if mousestate == 1 and configEditorOpen == False and SettingsOpen == False:
                if v[5] == 'close':
                    pygame.quit(), exit()
                if v[5] == 'settings':
                    SettingsOpen = True
                    SubmenuScroll = 50
                    #os.startfile(r'settings and info.txt')
                if v[5] == 'credits':
                    os.startfile(r'txt\\credits.txt')
        else:
            ui_objects[i][0].set_alpha(ui_objects[i][0].get_alpha() - -20 / 3)
    for i, v in enumerate(GameButtons):
        if GameButtons[i][0].get_rect().collidepoint((pygame.mouse.get_pos()[0] - GameButtons[i][1], pygame.mouse.get_pos()[1] - GameButtons[i][2] )):
            GameButtons[i][0].set_alpha(200 - GameButtons[i][0].get_alpha()/ 3)
            if mousestate == 1 and configEditorOpen == False and SettingsOpen == False:
                pygame.mouse.set_pos((screen_width/2, screen_height / 2))
                try:
                    os.remove(Root + '\\' + 'xenia-canary-config.toml')
                except:
                    pass
                for i2, v2 in enumerate(games):
                    if v2[0] == GameButtons[i][5]:
                        shutil.copyfile(Root + '\\' + 'Games' + '\\' + v2[0] + '\\' + games[i2][3], Root + '\\' + games[i2][3])
                        try:
                            os.remove(Root + '\\' + 'xenia-canary.config.toml')
                        except:
                            pass
                        os.rename(Root + '\\' + games[i2][3], Root + '\\' + 'xenia-canary.config.toml')
                        os.startfile(Root + '\\' + 'Games' + '\\' + v2[0] + '\\' + v2[0] + '\\' + 'default.xex')
                        if CloseLaunch == True:
                            pygame.quit(), exit()
        else:
            GameButtons[i][0].set_alpha(GameButtons[i][0].get_alpha() - -20 / 3)
        for i, v in enumerate(ConfigButtons):
            if ConfigButtons[i][0].get_rect().collidepoint((pygame.mouse.get_pos()[0] - ConfigButtons[i][1], pygame.mouse.get_pos()[1] - ConfigButtons[i][2] )):
                    ConfigButtons[i][0].set_alpha(200 - ConfigButtons[i][0].get_alpha()/ 3)
                    if mousestate == 1 and configEditorOpen == False and SettingsOpen == False:
                        pygame.mouse.set_pos((screen_width/2, screen_height / 2))
                        tomlpath = Root + '\\' + 'Games' + '\\' + games[i][0]
                        ConfigOpen = games[i][0]
                        shutil.copyfile(tomlpath + '\\' + games[i][0] + '.toml', tomlpath + '\\' + Path(tomlpath).stem + '.txt') # we copy the toml file and paste it as a txt file
                        txtversion = open(Root + '\\' + 'Games' + '\\' + games[i][0] + '\\' + games[i][0] + '.txt').readlines() # we read and edit the txt file as a list, then save it back as the toml file
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
    TooltipOpen = False
    if configEditorOpen == True:
        for i, v in enumerate(tooltips):
            tooltips[i][1] = 42
            tooltips[i][2] = (i * 45) + SubmenuScroll + SubmenuBGSurfaceXvar - 15
            if tooltips[i][0].get_rect().collidepoint((pygame.mouse.get_pos()[0] - tooltips[i][1], pygame.mouse.get_pos()[1] - tooltips[i][2] )):
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
            ConfigSettingsButtons[i][2] = (i * 45) + SubmenuScroll + SubmenuBGSurfaceXvar - 5
            if ConfigSettingsButtons[i][0].get_rect().collidepoint((pygame.mouse.get_pos()[0] - ConfigSettingsButtons[i][1], pygame.mouse.get_pos()[1] - ConfigSettingsButtons[i][2] )):
                try:
                    ConfigSettingsButtons[i][0].set_alpha(140 - ConfigSettingsButtons[i][0].get_alpha() / 3)
                except:
                    pass
                if mousestate == 1: 
                    if v[3] == 'bool':
                        if v[4] == True:
                            ConfigSettingsButtons[i][4] = False
                            v[0] = pygame.transform.scale(pygame.image.load(UIRoot + 'false.png').convert_alpha(), (40, 40))
                            ConfigSettingsButtons[i][0].set_alpha(140)
                        elif v[4] == False:
                            ConfigSettingsButtons[i][4] = True
                            v[0] = pygame.transform.scale(pygame.image.load(UIRoot + 'true.png').convert_alpha(), (40, 40))
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
            SettingsTips[i][1] = 42
            SettingsTips[i][2] = (i * 45) + SubmenuScroll + SubmenuBGSurfaceXvar - 15
            if SettingsTips[i][0].get_rect().collidepoint((pygame.mouse.get_pos()[0] - SettingsTips[i][1], pygame.mouse.get_pos()[1] - SettingsTips[i][2] )):
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
            SettingsButtons[i][2] = (i * 45) + SubmenuScroll + SubmenuBGSurfaceXvar - 5
            if SettingsButtons[i][0].get_rect().collidepoint((pygame.mouse.get_pos()[0] - SettingsButtons[i][1], pygame.mouse.get_pos()[1] - SettingsButtons[i][2] )):
                try:
                    SettingsButtons[i][0].set_alpha(140 - SettingsButtons[i][0].get_alpha() / 3)
                except:
                    pass
                if mousestate == 1: 
                    if v[3] == 'bool':
                        if v[4] == True:
                            SettingsButtons[i][4] = False
                            v[0] = pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\false.png').convert_alpha(), (40, 40))
                            SettingsButtons[i][0].set_alpha(140)
                        elif v[4] == False:
                            SettingsButtons[i][4] = True
                            v[0] = pygame.transform.scale(pygame.image.load(UIRoot + 'textures and sfx\\true.png').convert_alpha(), (40, 40))
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
                    pass
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
    newscreen = pygame.transform.smoothscale(screen, (screen_info.current_w, screen_info.current_h)) 
    window.blit(newscreen, (0, 0))
    pygame.display.update()