from threading import Thread
import threading
import urllib
import urllib.request
import json
from time import gmtime, strftime, sleep, time
from bs4 import BeautifulSoup
import pickle
from os import listdir, _exit
from os.path import isfile, join
from shutil import copyfile
import re
import requests
from proxylist import PROXYES, GetProxyNumber

PATH = './'
PHPSESSID = 'c43bd2plvusgsvl40slorrc367'
FLOAT = 0.01
SLEEP = 60
Inventoryes = dict()
TradeHrefs = list()
WRITE = open("results.txt", 'a+')
START = 277000000
END = 277000000
LASTERROR = None

class Weapon:
    def __init__(self, Name, AssetId, Float, InstanceId, ClassId, InformationD):
        self.Name = Name
        self.AssetId = AssetId
        self.Float = Float
        self.InstanceId = InstanceId
        self.ClassId = ClassId
        self.InformationD = InformationD
    def __str__(self):
        return('{} {} {} {} {} {}'.format(self.Name, self.AssetId, self.InstanceId, self.ClassId, self.InformationD, self.Float))

class InventoryInformation:
    def __init__(self, Inventory:str, LinkOnCsgolounge:str, LinkOnTrade:str):
        self.Inventory = Inventory
        self.LinkOnTrade = LinkOnTrade
        self.LinkOnCsgolounge = LinkOnCsgolounge

        self.WeaponsLoad = False
        self.Weapons = []
        self.TimeCheck = ''

        self.WeaponsChecked = False
        self.Blocked = False
    def __str__(self):
        return('{}'.format(self.Inventory))

def FindingWeaponsWithDownFloat():
    while True:
        for Information in filter(lambda x: not x.WeaponsChecked and x.WeaponsLoad and not x.Blocked, list(Inventoryes.values())):
            for weapon in Information.Weapons:
                if weapon.Float < FLOAT:
                    timecheck = str(Information.TimeCheck)
                    out = (str(Information.LinkOnTrade)+'\t'+
                    str(Information.LinkOnCsgolounge)+'\t'+
                    str(weapon.Name)+'\t'+
                    str(weapon.Float)+'\t'+
                    timecheck+'\r\n')
                    out = ''.join([i if ord(i) < 256 else ' ' for i in out])
                    WRITE.write(out)
                    WRITE.flush()
                    print("Weapon: {}".format(weapon))
            Information.WeaponsChecked = True
            print("SteamId checked: {}".format(Information))

        sleep(1)

def FindingWeapons():
    firstTime = time()
    while True:
        for Information in filter(lambda x: not x.WeaponsLoad and not x.Blocked, list(Inventoryes.values())):
            while time() - firstTime < 5:
                sleep(1)
                pass
            firstTime = time()
            try:
                urltoload = 'http://steamcommunity.com/profiles/{}/inventory/json/730/2?count=1000'.format(Information.Inventory)
                #req = urllib.request.Request('https://steamcommunity.com/profiles/{}/inventory/json/730/2?count=1000'.format(Information.Inventory),
                #                 headers={'User-Agent': 'Mozilla/5.0'})
                #with urllib.request.urlopen(req) as url:
                #    u=url.read()
                #    jsonResponse = json.loads(u.decode('utf-8'))
                #with open('test.txt', 'r') as url:
                    #jsonResponse = json.loads(url.read())
                #url = requests.get(urltoload, proxies={'http':PROXYES[GetProxyNumber()]})
                url = requests.get(urltoload, proxies=dict(http='socks5://127.0.0.1:9050'))
                jsonResponse = json.loads(url.text)
                if jsonResponse == None:
                    print('Steam returns null')
                    continue
                print("SteamId load: {}".format(Information))
                if jsonResponse['success'] != True:
                    if jsonResponse['Error'] == 'This profile is private.':
                        Information.Blocked = True
                    continue
                if type(jsonResponse['rgInventory']) is list:
                    Information.Blocked = True
                    continue
                for id, info in jsonResponse['rgInventory'].items():
                    AssetId = id
                    ClassId = info['classid']
                    InstanceId = info['instanceid']
                    anotherinfo = jsonResponse['rgDescriptions']['{}_{}'.format(ClassId, InstanceId)]
                    try:
                        wear = anotherinfo['tags'][5]['name']
                        if wear != 'Factory New':
                            continue
                        Name = anotherinfo['name']
                        link = anotherinfo['actions'][0]['link']
                        InformationD = link[link.find('%assetid%') + 10:]
                        #NEEDHELP
                        urlfind ='https://api.csgofloat.com:1738/?s={}&a={}&d={}'.format(Information.Inventory, AssetId, InformationD)
                        while True:
                            try:
                                with urllib.request.urlopen(urlfind) as url2:
                                    jsonWithFloat = json.loads(url2.read().decode('utf-8'))
                                    Float = jsonWithFloat['iteminfo']['floatvalue']
                                    break
                            except urllib.error.HTTPError as httperror:
                                print(httperror.read())
                                continue
                            except Exception as ssss:
                                print(ssss)
                                continue

                        
                        weapon = Weapon(Name, AssetId, Float, InstanceId, ClassId, InformationD)
                        Information.Weapons.append(weapon)

                    except Exception as sss:
                        continue
            except requests.packages.urllib3.exceptions.NewConnectionError as ex:
                continue
            except requests.exceptions.ConnectionError:
                continue
            except Exception as ex:
                print(ex)
                continue
            Information.WeaponsLoad = True
            Information.TimeCheck = strftime("%d %b %Y %H:%M", gmtime())

def InitialiseDate():
    global Inventoryes
    global TradeHrefs
    pathes = [f.upper() for f in listdir(PATH) if isfile(join(PATH, f))]
    if 'DATA.DAT' not in pathes:
        with open("DATA.DAT", 'wb') as f:
            pickle.dump(Inventoryes, f)
    else:
        with open('DATA.DAT', 'rb') as f:
            Inventoryes = pickle.load(f) 
    
    if 'TRADEHREFS.DAT' not in pathes:
        with open('TRADEHREFS.DAT', 'wb') as f:
            pickle.dump(TradeHrefs, f)   
    else:
        with open('TRADEHREFS.DAT', 'rb') as f:
            TradeHrefs = pickle.load(f)   

def SaveDate():
    while True:
        sleep(300)
        with open("DATA.DAT", 'wb') as f:
            pickle.dump(Inventoryes, f)
        with open('TRADEHREFS.DAT', 'wb') as f:
            pickle.dump(TradeHrefs, f)
        copyfile('DATA.DAT', 'DATA.BAK')
        copyfile('TRADEHREFS.DAT', 'TRADEHREFS.BAK')
        print('DATA SAVED')


def FindingInventoryes():
    global TradeHrefs
    global Inventoryes
    global PHPSESSID
    req = urllib.request.Request("https://csgolounge.com/",
                                 headers={'User-Agent': 'Mozilla/5.0',
                                 'Cookie':'PHPSESSID='+PHPSESSID+
                                 ';id=76561198066508066;uid=6291bdc49a87c880041f24f671d2e61e',
                                                                            })
    while True:
        try:
            with urllib.request.urlopen(req) as url:
                u=url.read().decode('utf-8')
                soup = BeautifulSoup(u, 'html.parser')
                if not soup.find('div', {'id':'status-coins'}):
                    print('PHPSESSID IS CLOSED')
                    PHPSESSID = input()
                    continue
                tradepolls = soup.find_all('div', {'class' : 'tradepoll'})
                counthrefs = 0
                for tradehref in ["https://csgolounge.com/" + i.find('div', {'class':'tradeheader'}).find_all('a')[1]['href'] for i in tradepolls]:
                    if tradehref not in TradeHrefs:
                        tradereq = urllib.request.Request(tradehref,
                                 headers={'User-Agent': 'Mozilla/5.0',
                                 'Cookie':'PHPSESSID='+PHPSESSID+
                                 ';id=76561198066508066;uid=6291bdc49a87c880041f24f671d2e61e',
                                                                            })
                        try:
                            with urllib.request.urlopen(tradereq) as url2:
                                u=url2.read().decode('utf-8')
                                soup = BeautifulSoup(u, 'html.parser')
                                inventory = soup.find('a', {'class':'profilesmall'})['href'][-18:-1]
                                if inventory in Inventoryes:
                                    continue
                                try:
                                    tradelink = soup.find('div', {'id':'offer'}).find('a', {'class':'buttonright'})['href']
                                except:
                                    try:
                                        message = str(soup.find('p', {'class': 'standard msgtxt'}))
                                        tradelink = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)[0]
                                        tradelink = tradelink.replace('<br>', '').replace('<br/>','').replace('<p>','').replace('<p/>','').replace('</br>','').replace('</p>','')
                                    except:
                                        tradelink = ''
                                TradeHrefs.append(tradehref)
                                Inventoryes[inventory] = InventoryInformation(inventory, tradehref, tradelink)
                                counthrefs += 1
                        except urllib.error.URLError as ex:
                            continue   
                        except:
                            continue
                print('{} - Inventories added'.format(counthrefs))
        except urllib.error.URLError:
            continue
        except Exception as ex:
            print(ex)
            continue

'''
def FindingInventoryes():
    global TradeHrefs
    global Inventoryes
    global PHPSESSID
    global START
    global LASTERROR
    global END
    while True:

        tradehref = 'https://csgolounge.com/trade?t={}'.format(START)
        if tradehref not in TradeHrefs:
            tradereq = urllib.request.Request(tradehref,
                        headers={'User-Agent': 'Mozilla/5.0',
                        'Cookie':'PHPSESSID='+PHPSESSID+
                        ';id=76561198066508066;uid=6291bdc49a87c880041f24f671d2e61e',
                                                                })
            try:
                with urllib.request.urlopen(tradereq) as url2:
                    u=url2.read().decode('utf-8')
                    soup = BeautifulSoup(u, 'html.parser')
                    if not soup.find('div', {'id':'status-coins'}):
                        print('PHPSESSID IS CLOSED')
                        PHPSESSID = input()
                        continue
                    inventory = soup.find('a', {'class':'profilesmall'})['href'][-18:-1]
                    if inventory in Inventoryes:
                        START += 1
                        continue
                    try:
                        tradelink = soup.find('div', {'id':'offer'}).find('a', {'class':'buttonright'})['href']
                    except:
                        try:
                            message = str(soup.find('p', {'class': 'standard msgtxt'}))
                            tradelink = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)[0]
                            tradelink = tradelink.replace('<br>', '').replace('<br/>','').replace('<p>','').replace('<p/>','').replace('</br>','').replace('</p>','')
                        except:
                            tradelink = ''
                    TradeHrefs.append(tradehref)
                    LASTERROR = None
                    if tradelink != '':
                        Inventoryes[inventory] = InventoryInformation(inventory, tradehref, tradelink)
                        print('{} - To check added'.format(START))
            except urllib.error.URLError as ex:
                print(ex)
                LASTERROR = START
                if START < END:
                    TradeHrefs.append(tradehref)
                START += 1
                continue   
            except Exception as exx:
                print(str(exx) + '\n' + str(START))
                START += 1
                TradeHrefs.append(tradehref)
                continue
        START += 1
'''

def StartFinder(sl:int):
    global SLEEP
    SLEEP = sl
    InitialiseDate()
    Thread(target=SaveDate).start()
    Thread(target=FindingInventoryes).start()
    Thread(target=FindingWeapons).start()
    Thread(target=FindingWeaponsWithDownFloat).start()
    while True:
        NotLoadInventories = len(list(filter(lambda x: not x.WeaponsLoad and not x.Blocked, list(Inventoryes.values()))))
        NotCheckedInventories = len(list(filter(lambda x: not x.WeaponsChecked and x.WeaponsLoad and not x.Blocked, list(Inventoryes.values()))))
        allInventories = len(list(Inventoryes.values()))
        allCheckedInventories = len(list(filter(lambda x: x.WeaponsChecked and x.WeaponsLoad and not x.Blocked, list(Inventoryes.values()))))
        print('{}\t- Not Load Inventories\n{}\t- Not Checked Inventories\n{}\t- All Checked Inventories\n{}\t- All Inventories\n{}- Now href\n{}\t-Last Error'.format(
            NotLoadInventories, NotCheckedInventories, allCheckedInventories, allInventories, START, LASTERROR))
        sleep(100)
