# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 22:21:22 2021

@author: Clemens
"""

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.errorhandler import NoSuchElementException
import time
from base64 import b64decode


# Import functions for database communication
from sql_database_communication import *


# Navigat to Website and Login
def start_season(password, username):
    driver.get("https://spacegate-galaxys.com")
    # Search for the login field
    login = driver.find_element_by_name('loginname')
    # Enter login name
    login.send_keys(username)
    # Search for the password field
    pw = driver.find_element_by_name('password')
    # Enter password
    pw.send_keys(b64decode(password).decode("utf-8"))
    # Search for uni Dropdown Menu
    uni = Select(driver.find_element_by_id('uni'))
    # Select Universe
    uni.select_by_value('1')
    # Search the login Button
    login_button = driver.find_element_by_id('login_href')
    # Sleep 1 second
    time.sleep(1)
    # Enter Login
    login_button.click()


# Shwitch planet
def shwitch_planet(number):
    # Search planet ID on website
    planet = Select(driver.find_element_by_id('planetid'))
    # Send a Value to switch the planet
    planet.select_by_value(number)


# Planete of because I farm this planet
def farm_planet(number):
    if number == 0:
        # Alpha Basis Planet ID and coordinates
        return ['149987', '5:250:6']
    elif number == 1:
        # Erde Planet ID and coordinates
        return ['149985', '15:250:7']
    elif number == 2:
        # Atlantis Planet ID and coordinates
        return ['149984', '24:90:4']
    elif number == 3:
        # Chulak Planet ID and coordinates
        return ['149986', '35:250:7']
    elif number == 4:
        # Fingier Planet ID and coordinates
        return ['149988', '45:250:6']
    elif number == 5:
        # Urban Planet ID and coordinates
        return ['149989', '55:250:7']
    elif number == 6:
        # Olnaiphus Planet ID and coordinates
        return ['149990', '65:250:7']
    elif number == 7:
        # Lagawa Planet ID and coordinates
        return ['149991', '75:250:6']
    elif number == 8:
        # Boria Planet ID and coordinates
        return ['149992', '85:250:7']
    elif number == 9:
        # Cawei Planet ID and coordinates
        return ['149993', '95:250:7']
    elif number == 10:
        # Hangar 1 Planet ID and coordinates
        return ['150068', '20:250:7']
    elif number == 11:
        # Hangar 2 Planet ID and coordinates
        return ['150069', '30:250:6']
    else:
        # Hangar 3 Planet ID and coordinates
        return ['150070', '10:250:7']


# Transport resources to other planets
def shipment(of, to, iron, naquada, deuterium):
    # Switch to fleet commands on the sidebar
    sidebar_menu(8)
    # Switch to the planet from sending resources
    shwitch_planet(farm_planet(of)[0])
    # Select the Planet box
    own = Select(driver.find_element_by_name('own_planets'))
    # Select the planet from the drop-down menu where resources should be sent
    own.select_by_value(farm_planet(to)[1])
    # Search the field for the big vans
    big = driver.find_element_by_id('anzahl_25')
    # Calculate the number of big vans and write them down
    big.send_keys(big_trans(iron + naquada + deuterium))
    # Search the field for the assignment
    order = Select(driver.find_element_by_id('auftrag'))
    # Select the right order(Transport)
    order.select_by_value('transport')
    for res in ['eisen', 'naquada', 'deuterium']:
        # Find the field for the resources
        reso = driver.find_element_by_id(res)
        # Clear the field
        reso.send_keys(Keys.BACKSPACE)
        # Paste the separate resource quantities into the resource field
        if res == 'eisen':
            reso.send_keys(int(1000000000 * iron))
        elif res == 'naquada':
            reso.send_keys(int(1000000000 * naquada))
        else:
            reso.send_keys(int(1000000000 * deuterium))
    # Search the confirmed fild
    send = driver.find_element_by_id('send')
    # Confirmed the shipment
    send.click()


def where():
    legend = driver.find_elements_by_class_name('fieldset_main_legend')
    liste = []
    for i in range(len(legend)):
        liste.append(legend[i].text)
    return liste


def where_to(name, number):
    liste = where()
    if name not in liste:
        sidebar_menu(number)


# Build ships
def hangar(ship, number):
    where_to('Flottenliste', 4)
    name = driver.find_element_by_name(str(ship))
    name.send_keys(Keys.RIGHT ,Keys.BACKSPACE, number)


def defensive():
    where_to('Defensivliste', 5)
    try:
        construction_orders = driver.find_elements_by_class_name("see_normal")[-2].text
        construction_orders = construction_orders.split(' ')
        if construction_orders[2] not in "1999999999":
            for construction in range(2):
                construction_orders = driver.find_elements_by_class_name("see_normal")
                driver.find_elements_by_link_text("abbrechen")[len(construction_orders)-2].click()
        for i in [36, 34]:
            name = driver.find_element_by_name(str(i))
            number = driver.find_elements_by_class_name("technik_wrapper")[i - (32 + 2)].text
            number = int(number.split(" ")[-1].replace(".",""))
            if i == 34:
                number -= 200000
            if number < 1999999999:
                name.send_keys(Keys.RIGHT ,Keys.BACKSPACE, number, Keys.ENTER)
            else:
                name.send_keys(Keys.RIGHT ,Keys.BACKSPACE, 1999999999, Keys.ENTER)
    except IndexError:
        print("Termination not possible")



# Calculate the big trans number for shipment
def big_trans(resource):
    number = round(1000000000*resource/40000)
    number2 = 1000000000*resource/40000
    if number2 > number:
        return number + 1
    return number


def gebaeude_build(planetid,number):
    where_to('Gebäudeliste',1)
    shwitch_planet(farm_planet(planetid)[0])
    legend = where()
    if 'Bauaufträge' in legend:
        return driver.find_element_by_id('zaehler_gebaeude1001').text
    else:
        gebaeude = driver.find_elements_by_partial_link_text('Ausbauen')
        if len(gebaeude) > 0:
            gebaeude[number].click()
            return driver.find_element_by_id('zaehler_gebaeude1001').text
        return "Ausbau nicht moeglich"


def ship_handel(ships, ships_amount, surcharge, iron_build, naquada_build, deuterium_build):
    sidebar_menu(14)
    driver.find_elements_by_class_name('ebene_2')[2].click()
    iron = driver.find_element_by_name('biete_eisen')
    naquada = driver.find_element_by_name('biete_naquada')
    deuterium = driver.find_element_by_name('biete_deuterium')
    iron_resources = iron_build*ships_amount+iron_build*ships_amount*surcharge
    naquada_resources = naquada_build*ships_amount+naquada_build*ships_amount*surcharge
    deuterium_resources = deuterium_build*ships_amount+deuterium_build*ships_amount*surcharge
    iron.send_keys(Keys.BACKSPACE, int(iron_resources))
    naquada.send_keys(Keys.BACKSPACE, int(naquada_resources))
    deuterium.send_keys(Keys.BACKSPACE, int(deuterium_resources))
    #fleet = driver.find_element_by_id('suche_type_fleet')


def resource_hand(offer, resTyp, resTyp2, multi = 1):
    where_to("Handel", 14)
    driver.find_elements_by_class_name('ebene_2')[2].click()
    if resTyp == "e":
        offerRes = driver.find_element_by_name('biete_eisen')
    elif resTyp == "n":
        offerRes = driver.find_element_by_name('biete_naquada')
    else:
        offerRes = driver.find_element_by_name('biete_deuterium')
    offerRes.send_keys(Keys.BACKSPACE, int(offer * multi))
    if resTyp2 == "e":
        searchRes = driver.find_element_by_name('suche_eisen')
    elif resTyp2 == "n":
        searchRes = driver.find_element_by_name('suche_naquada')
    else:
        searchRes = driver.find_element_by_name('suche_deuterium')
    if resTyp == "e":
        if resTyp2 == "n":
            resMulti = 0.401
        elif resTyp2 == "d":
            resMulti = 0.681
    if resTyp == "d":
        if resTyp2 == "e":
            resMulti = 1.468
        elif resTyp2 == "n":
            resMulti = 0.589
    if resTyp == "n":
        if resTyp2 == "e":
            resMulti = 2.493
        elif resTyp2 == "d":
            resMulti = 1.698
    searchRes.send_keys(Keys.BACKSPACE, int(offer * multi * resMulti))
    send = driver.find_element_by_name('send')
    send.click()


# Navigate in the sidebar menu
def sidebar_menu(number):
    driver.find_elements_by_class_name('sidebar_menu')[number].click()


# Navigate to Ingame Messages
def messages():
    driver.find_elements_by_class_name('MenuBarItemSubmenu')[1].click()


# Navigate to Ingame Spionage Massages
def spionage():
    messages()
    spio = driver.find_elements_by_class_name('ebene_2')[4]
    spio.click()
    mes = driver.find_element_by_id('boxen_class_0')
    mes.click()
    message = driver.find_elements_by_class_name('fieldset_div')[1]
    spio_message = message.find_element_by_xpath('table/tbody/tr/td').text
    return spio_message


def spio_string(spio_message):
    spio_message_list = spio_message.split('\n')
    spio_message_list_adjusted = [feld for feld in spio_message_list if feld != '']
    yes_for_farm = ['Dieser Planet hat keine Verteidigungsanlagen.',
                    'Im Orbit des Planeten befinden sich keine Raumschiffe.']
    if yes_for_farm[0] in spio_message:
        if yes_for_farm[1] in spio_message:
            del spio_message_list_adjusted[0]
            if 'Keine Daten verfübar' not in spio_message:
                for message in spio_message_list_adjusted:
                    if 'Eisen' in message:
                        iron = float(int(message[7:].replace('.',''))/1000000000)
                    elif 'Naquada' in message:
                        naquada = float(int(message[9:].replace('.',''))/1000000000)
                    elif 'Deuterium' in message:
                        deuterium = float(int(message[11:].replace('.',''))/1000000000)
                summe = iron + naquada + deuterium
                round_summe = round(summe)
                if summe > 0.1:
                    if round_summe < summe:
                        round_summe += 1
                    return round_summe
                else:
                    return False
    return 'def'


# Delete War or Spio Messages
def delete_messages(typ):
    messages()
    try:
        delete = driver.find_elements_by_class_name('ebene_2')[typ]
        delete.click()
        check = ActionChains(driver)
        check.click(driver.find_element_by_id('schalter'))
        check.perform()
        delete = Select(driver.find_element_by_id('aktion'))
        delete.select_by_value('delete')
    except:
        pass


# Navigate to Universe Map
def universe():
    sidebar_menu(11)
    uni_loop(driver)


# Flight duration in seconds
def flight_duration():
    try:
        duration = driver.find_element_by_id('flotte_dauer').text
        hour = int(duration[:2])*60*60
        minutes = int(duration[3:-3])*60
        seconds = int(duration[6:])
        summe = hour + minutes + seconds
        return summe
    except ValueError:
        return 6


# Fleet commands
def fleetcommands(galaxy, system, planet, number, typ, befehl):
    where_to('Flottenbewegungen',8)
    max_fleet()
    galaxy_pos = driver.find_element_by_id('pos1')
    galaxy_pos.send_keys(galaxy)
    system_pos = driver.find_element_by_id('pos2')
    system_pos.send_keys(system)                                      # 47 = Spionagesonde
    planet_pos = driver.find_element_by_id('pos3')                    # 24 = Kleiner Transporter
    planet_pos.send_keys(planet)                                      # 25 = Großer Transporter
    feetType = driver.find_element_by_id('anzahl_' + str(typ))        # 26 = Kleiner Truppentransporter
    feetType.send_keys(number)                                        # 27 = Großer Truppentransporter
    order = Select(driver.find_element_by_id('auftrag'))              # 28 = Kolonieschiff
    order.select_by_visible_text('Auftrag wählen')                    # 29 = Todesgleiter
    if befehl == "s":                                                 # 30 = Hatak
        order.select_by_value('spionage')                             # 32 = Flaggschiff
    elif befehl == "a":                                               # 33 = Anubis-Mutterschiff
        order.select_by_value('angriff')                              # 48 = Flotten-Verband
    sleep = flight_duration()
    send = driver.find_element_by_id('send')
    send.click()
    is_bannd = failed()
    if is_bannd != False:
        return [0, is_bannd]
    else:
        return [sleep, is_bannd]


def failed():
    try:
        failed = driver.find_element_by_class_name('failed')
        if 'Fehler:\nDer Benutzer, den Sie anfliegen wollen ist gebannt!' == failed.text:
            return 'banned'
        elif 'Fehler:\nSie haben nicht genug Schiffe!' == failed.text:
            return 'schiffe'
        elif 'Fehler:\nDer Benutzer, den Sie anfliegen wollen ist im Urlaubsmodus!' == failed.text:
            return 'urlaub'
        elif 'Fehler:\nSie können nicht mehr Ressourcen transportieren als Sie haben!' == failed.text:
            return 'ressourcen'
        else:
            return 'admin'
    except:
        return False


def current_fleet():
    fleet = driver.find_element_by_class_name('liste_head').text
    fleet = fleet.split(" ")
    fleet = fleet[1].replace("(","")
    fleet = fleet.replace(")","")
    fleet = fleet.split("/")
    return [int(fleet[0]), int(fleet[1])]


def max_fleet():
    fleet = current_fleet()
    while fleet[0] >= fleet[1]:
        sidebar_menu(8)
        time.sleep(30)


def auto_farm(score):
    dic = myPlanets()
    current_farm = farm_to_day()
    liste = creat_farm_list(score, current_farm,"<INGAME NAME>")
    print(len(liste),time.strftime("%d.%m.%Y %H:%M:%S"))
    #auto_build(0,1)
    counter = 0
    try:
        for planet in liste:
            counter += 1
            current_planet = driver.find_element_by_class_name('koordinaten').text
            current_planet = current_planet.replace("]","")
            current_planet = current_planet.replace("[","")
            current_planet = current_planet.split(":")
            if dic[current_planet[0]] != planet[4]:
                shwitch_planet(planet[4])
            if counter == 1:
                defensive()
            spio_fleet = fleetcommands(planet[0],planet[1],planet[2],11,47,'s')
            time.sleep(spio_fleet[0])
            if spio_fleet[1] == False:
                spio_message = spionage()
                spio = spio_string(spio_message)
                if type(spio) == int:
                    fleet = fleetcommands(planet[0],planet[1],planet[2],big_trans(spio),25,'a')
                    if fleet[1] == False:
                        last_and_next_farm(planet[0],planet[1],planet[2],planet[5])
                    elif fleet[1] == 'schiffe':
                        print('Not enough ships: {}:{}:{}'.format(planet[0],planet[1],planet[2]))
                        not_ships(planet[0],planet[1],planet[2],spio_message)
                elif spio == 'def':
                    update_status_in_sql(planet[3],'def')
                else:
                    update_intervall(planet[0],planet[1],planet[2], planet[5])
            elif spio_fleet[1] == 'banned':
                update_status_in_sql(planet[3],'banned')
            elif spio_fleet[1] == 'admin':
                update_status_in_sql(planet[3], 'admin')
            if counter == 100:
                auto_build(0, 1)
                counter = 0
        update_farm(current_farm)
        try:
            delete_messages(4)
            delete_messages(3)
        except:
            print("Keine Nachricht zum löschen.")
        sidebar_menu(0)
    except KeyboardInterrupt:
        print("Farmen forzeitig beendet.")
    except (NoSuchElementException ,IndexError):
        print("Auto Logout.")
        start_season()
        auto_farm("200kkk")


def auto_build(number, manuell):
    for i in range(3,13):
        if manuell == 0:
            print(str(i) + ': ' + gebaeude_build(i,number))
        gebaeude_build(i,number)
    if manuell == 0:
        print(time.strftime("%d.%m.%Y %H:%M:%S"))


driver = webdriver.Edge(executable_path=r"edgedriver_win32\msedgedriver.exe")
start_season("<YOUR PASSWORD IN B64CODE>","<USERNAME>")