# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 09:43:45 2021

@author: Clemens
"""

import sqlite3
import time
from datetime import date
from datetime import timedelta
from selenium.webdriver.common.keys import Keys



# Loop to go through the universe and fill the database (universe Table)
def uni_loop(driver):
    con = sqlite3.connect('uni_list_21_12_2021.db')
    uni = con.cursor()
    for galaxy in range(73,101):
        for system in range(1,501):
            go_to_universe(driver, galaxy, system)
            browser = driver.find_elements_by_class_name('liste_list')
            for i in range(15):
                planet_list = planet(driver, browser,i*4)
                if type(planet_list) == list:
                    planet_list.insert(0,system)
                    planet_list.insert(0,galaxy)
                    is_in = [galaxy, system, planet_list[2], planet_list[3]]
                    planet_exists_in_sql = uni.execute('''SELECT galaxy, system, planet, user_name FROM universe
                                                       WHERE galaxy=? AND system=? AND planet=? AND user_name=?''', is_in)
                    planet_exists_in_sql = planet_exists_in_sql.fetchall()
                    if planet_exists_in_sql == []:
                        current_planet = farm_planet_sql(int(planet_list[0]))
                        planet_list.append(int(current_planet[0]))
                        uni.execute('''INSERT INTO universe (galaxy, system, planet, user_name, farm_planet, farm_intervall) values(?,?,?,?,?,?)''',
                                    (planet_list[0], planet_list[1], planet_list[2], planet_list[3], planet_list[5],5))
                    user = [planet_list[3]]
                    user_exists_in_sql = uni.execute(''' SELECT user_name FROM user WHERE user_name=?''', user)
                    user_exists_in_sql = user_exists_in_sql.fetchall()
                    if user_exists_in_sql == []:
                        user_liste = user_name(driver, browser, i*4)
                        uni.execute('''INSERT INTO user (user_name, score, allianz) values(?,?,?)''',
                                    (user_liste[0], user_liste[1], user_liste[2]))
                        go_to_universe(driver,galaxy,system)
                        browser = driver.find_elements_by_class_name('liste_list')
                    if len(planet_list[4]) > 2:
                        allianz_liste = [planet_list[4]]
                        allianz_exists_in_sql = uni.execute(''' SELECT allianz_name FROM allianz WHERE allianz_name=?''', allianz_liste)
                        allianz_exists_in_sql = allianz_exists_in_sql.fetchall()
                        if allianz_exists_in_sql == []:
                            allianz_liste = allianz(driver, browser, i*4)
                            uni.execute('''INSERT INTO allianz (allianz_name, members, allianz_score) values(?,?,?)''',
                                        (allianz_liste[0], allianz_liste[1], allianz_liste[2]))
                            go_to_universe(driver,galaxy,system)
                            browser = driver.find_elements_by_class_name('liste_list')
        con.commit()
    con.commit()
    con.close()


def go_to_universe(driver,galaxy,system):
    g = driver.find_element_by_id('pos1')
    g.send_keys(3*Keys.BACKSPACE)
    g.send_keys(galaxy)
    s = driver.find_element_by_id('pos2')
    s.send_keys(3*Keys.BACKSPACE)
    s.send_keys(system)
    s.send_keys(Keys.ENTER)
    time.sleep(0.2)


# Select data for Database  (universe Table)
def planet(driver, browser, i):
    if browser[i + 2].text != ' ':
        planet = []
        planet.append(int(browser[i].text))
        planet.append(browser[i + 2].text)
        planet.append(browser[i + 3].text)
        return planet
    return False


# Select data for Database  (user_name Table)
def user_name(driver, browser, i):
    browser[i + 2].click()
    user_liste = []
    user = driver.find_elements_by_class_name('fieldset_ablinks')
    user_liste.append(user[0].text)
    user_liste.append(int(user[1].text.replace('.','')))
    user_liste.append(user[4].text)
    driver.find_elements_by_class_name('sidebar_menu')[11].click()
    return user_liste


# Select data for Database  (allianz Table)
def allianz(driver, browser, i):
    browser[i + 3].click()
    alli_liste = []
    alli = driver.find_elements_by_class_name('fieldset_ablinks')
    alli_liste.append(alli[2].text)
    alli_liste.append(alli[6].text)
    alli_liste.append(int(alli[8].text.replace('.','')))
    driver.find_elements_by_class_name('sidebar_menu')[11].click()
    return alli_liste


# Planete of because I farm this planet
def farm_planet_sql(galaxy):
    if 1 <= galaxy <= 10 and galaxy != 5:
        # Alpha Basis Planet ID and coordinates
        return ['149987', '5:250:6']
    elif (11 <= galaxy <= 20 and galaxy != 15) or galaxy == 5:
        # Erde Planet ID and coordinates
        return ['149985', '15:250:7']
    elif (21 <= galaxy <= 30 and galaxy != 24) or galaxy == 15:
        # Atlantis Planet ID and coordinates
        return ['149984', '24:90:4']
    elif (31 <= galaxy <= 40 and galaxy != 35) or galaxy == 24:
        # Chulak Planet ID and coordinates
        return ['149986', '35:250:7']
    elif (41 <= galaxy <= 50 and galaxy != 45) or galaxy == 35:
        # Fingier Planet ID and coordinates
        return ['149988', '45:250:6']
    elif (51 <= galaxy <= 60 and galaxy != 55) or galaxy == 45:
        # Urban Planet ID and coordinates
        return ['149989', '55:250:7']
    elif (61 <= galaxy <= 70 and galaxy != 65) or galaxy == 55:
        # Olnaiphus Planet ID and coordinates
        return ['149990', '65:250:7']
    elif (71 <= galaxy <= 80 and galaxy != 75) or galaxy == 65:
        # Lagawa Planet ID and coordinates
        return ['149991', '75:250:6']
    elif (81 <= galaxy <= 90 and galaxy != 85) or galaxy == 75 or galaxy == 95:
        # Boria Planet ID and coordinates
        return ['149992', '85:250:7']
    else:
        # Cawei Planet ID and coordinates
        return ['149993', '95:250:7']


def update_status_in_sql(name, status):
    con = sqlite3.connect('uni_list_21_12_2021.db')
    uni = con.cursor()
    uni.execute(''' UPDATE user SET status = ? WHERE user_name=?''', (status,name,))
    con.commit()
    con.close()


def creat_farm_list(score, planet):
    if type(score) == str:
        score = int(score.replace("k","000"))
    con = sqlite3.connect('uni_list_21_12_2021.db')
    uni = con.cursor()
    today = date.today()
    farm_liste = uni.execute(''' SELECT u.galaxy, u.system, u.planet, u.user_name, u.farm_planet, u.farm_intervall
                             FROM universe AS u INNER JOIN user AS us
                             ON u.user_name = us.user_name
                             WHERE us.score <= ?
                             AND (u.next_farm <= ? OR u.next_farm IS NULL)
                             AND u.farm_planet = ?
                             AND NOT u.user_name = "Panoptos_1"
                             AND (us.allianz = "Ist bei keiner Allianz Mitglied" or us.allianz IN (
                                 SELECT al.allianz_name
                                 FROM allianz AS al
                                 WHERE al.allianz_score <= ?))
                             AND us.status IS NULL ''', (score,today,planet,score,))
    farm_liste = farm_liste.fetchall()
    con.close()
    return farm_liste


def last_and_next_farm(galaxy,system,planet,intervall):
    con = sqlite3.connect('uni_list_21_12_2021.db')
    uni = con.cursor()
    today = date.today()
    next_farm = today + timedelta(days=intervall)
    uni.execute('''UPDATE universe AS u SET last_farm =?, next_farm = ?
                WHERE u.galaxy = ? AND u.system = ? AND u.planet = ?''', (today, next_farm, galaxy, system, planet,))
    con.commit()
    con.close()


def update_intervall(galaxy,system,planet,intervall):
    con = sqlite3.connect('uni_list_21_12_2021.db')
    uni = con.cursor()
    intervall = intervall + 1
    next_farm = date.today() + timedelta(days=intervall)
    uni.execute('''UPDATE universe AS u SET farm_intervall = ?, next_farm = ?
                WHERE u.galaxy = ? AND u.system = ? AND u.planet = ?''', (intervall, next_farm, galaxy, system, planet,))
    con.commit()
    con.close()

def not_ships(galaxy,system,planet,spio):
    con = sqlite3.connect('uni_list_21_12_2021.db')
    uni = con.cursor()
    planet_exists_in_sql = uni.execute('''SELECT galaxy, system, planet FROM not_ships
                                       WHERE galaxy=? AND system=? AND planet=?''', (galaxy, system, planet,))
    planet_exists_in_sql = planet_exists_in_sql.fetchall()
    spio_message_list = spio.split('\n')
    spio_message_list_adjusted = [feld for feld in spio_message_list if feld != '']
    for i in range(5):
        del spio_message_list_adjusted[0]
    spio_adjusted = ""
    for string in spio_message_list_adjusted:
        spio_adjusted += string + "\n"
    if planet_exists_in_sql == []:
        uni.execute('''INSERT INTO not_ships (galaxy, system, planet, spio) values(?,?,?,?)''', (galaxy, system, planet, spio_adjusted))
    else:
        uni.execute('''UPDATE not_ships SET spio = ?
                    WHERE galaxy=? AND system=? AND planet=?''', (spio_adjusted, galaxy, system, planet,))
    con.commit()
    con.close()


def farm_to_day():
    con = sqlite3.connect('uni_list_21_12_2021.db')
    uni = con.cursor()
    today = date.today()
    current_farm_planet = uni.execute(''' SELECT farm.planet_id
                                          FROM farm
                                          WHERE farm.last_farm <= ?
                                          ORDER BY farm.last_farm''', (today,))
    current_farm_planet = current_farm_planet.fetchall()
    con.commit()
    con.close()
    return current_farm_planet[0][0]


def update_farm(planet_id):
    con = sqlite3.connect('uni_list_21_12_2021.db')
    uni = con.cursor()
    today = date.today()
    uni.execute('''UPDATE farm SET last_farm = ?
                WHERE farm.planet_id = ?''',(today, planet_id))
    con.commit()
    con.close()


# Creation of the "Uni_list" database
def create_uni_list_db():
    con = sqlite3.connect('uni_list_21_12_2021.db')
    uni = con.cursor()


    uni.execute('''CREATE TABLE universe
                (nr INTEGER PRIMARY KEY AUTOINCREMENT,
                 galaxy TINYINT UNSIGNED,
                 system TINYINT UNSIGNED,
                 planet TINYINT UNSIGNED,
                 user_name VARCHAR(50),
                 farm_planet VARCHAR(6),
                 last_farm DATE,
                 farm_intervall SMALLINT UNSIGNED,
                 next_farm DATE)''')

    uni.execute('''CREATE TABLE user
                (user_name VARCHAR(50),
                 score BIGINT UNSIGNED,
                 allianz VARCHAR(30),
                 status VARCHAR(4),
                 CONSTRAINT pk_unser_id PRIMARY KEY (user_name),
                 CONSTRAINT fk_unser_n FOREIGN KEY (user_name)
                 REFERENCES universe (user_name))''')

    uni.execute('''CREATE TABLE allianz
                (allianz_name VARCHAR(30),
                 members TINYINT UNSIGNED,
                 allianz_score BIGINT UNSIGNED,
                 CONSTRAINT pk_allianz_name PRIMARY KEY (allianz_name),
                 CONSTRAINT fk_allianz_name FOREIGN KEY (allianz_name)
                 REFERENCES unser_name)''')

    uni.execute('''CREATE TABLE not_ships
                (nr	INTEGER PRIMARY KEY AUTOINCREMENT,
                 galaxy	TINYINT UNSIGNED,
                 system	TINYINT UNSIGNED,
                 planet	TINYINT UNSIGNED,
                 spio	TEXT)''')

    uni.execute('''CREATE TABLE farm
                (nr INTEGER PRIMARY KEY AUTOINCREMENT,
                 galaxy TINYINT UNSIGNED,
                 system TINYINT UNSIGNED,
                 planet TINYINT UNSIGNED,
                 planet_id VARCHAR(6),
                 last_farm DATE)''')
    con.close()