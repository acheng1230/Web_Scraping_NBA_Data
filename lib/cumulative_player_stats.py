# Load packages
import re
import pandas as pd
import numpy as np

# Load selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome webdriver
driver = webdriver.Chrome('/Users/alexcheng/Downloads/chromedriver')

def get_per_game(url):
    """
    takes in a specific player url and scrapes the career averages from the per game table.
    must use in conjunction with `get_pergame_cols` in order to sync the columns.
    """
    driver.get(url)

    # share & more
    driver.find_element_by_xpath("""//*[@id="all_per_game"]/div[1]/div/ul/li[1]/span""").click()

    # get table as csv (for excel)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, """//*[@id="all_per_game"]/div[1]/div/ul/li[1]/div/ul/li[3]/button"""))).click()

    # table
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, """table_outer_container""")))

    # capture csv text
    per_game = driver.find_element_by_id("csv_per_game")

    # data cleaning
    per_game = per_game.text.encode('ascii', 'ignore').split()

    for stats in per_game:
        if stats.startswith('Career'):
            per_game = re.findall('(\d[\d.,-]+)$', stats)[0]

    player_id = re.findall('(\w+\d)', url)

    per_game_list = [player_id[0]]
    for i in per_game.split(','):
        if i == '':
            per_game_list.append(0.0)
        else:
            i = float(i)
            per_game_list.append(i)

    return per_game_list


def get_100(url):
    """
    takes in a specific player url and scrapes the career averages from the per-100 possessions table.
    must use in conjunction with `get_100_cols` in order to sync the columns.
    """
    driver.get(url)
    driver.find_element_by_xpath("""//*[@id="all_per_poss"]/div[1]/div/ul/li[1]/span""").click()

    WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
        (By.XPATH, """//*[@id="all_per_poss"]/div[1]/div/ul/li[1]/div/ul/li[3]/button"""))).click()

    WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
        (By.CLASS_NAME, """table_outer_container""")))

    # capture csv text
    all_per_poss = driver.find_element_by_id("csv_per_poss")

    # data cleaning
    all_per_poss = all_per_poss.text.encode('ascii').split()

    for stats in all_per_poss:
        if stats.startswith('Career'):
            all_per_poss = re.findall('(\d[\d.,-]+)$', stats)[0]

    player_id = re.findall('(\w+\d)', url)

    all_per_poss_list = [player_id[0]]
    for i in all_per_poss.split(','):
        if i == '':
            all_per_poss_list.append(0.0)
        else:
            i = float(i)
            all_per_poss_list.append(i)

    del all_per_poss_list[25]
    return all_per_poss_list

def get_shooting(url):
    """
    takes in a specific player url and scrapes the career averages from the shooting table.
    must use in conjunction with `get_shoot_cols` in order to sync the columns.
    """
    driver.get(url)

    # share & more
    driver.find_element_by_xpath("""//*[@id="all_shooting"]/div[1]/div/ul/li[2]/span""").click()

    # get table as csv (for excel)
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(
            (By.XPATH, """//*[@id="all_shooting"]/div[1]/div/ul/li[2]/div/ul/li[3]/button"""))).click()

    # table
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, """table_outer_container""")))

    # capture csv text
    shooting = driver.find_element_by_id("csv_shooting")

    # data cleaning
    shooting = shooting.text.encode('ascii', 'ignore').split()

    for stats in shooting:
        if stats.startswith('Career'):
            shooting = re.findall('(\d[\d.,-]+)$', stats)[0]

    player_id = re.findall('(\w+\d)', url)

    shooting_list = [player_id[0]]
    for i in shooting.split(','):
        if i == '':
            shooting_list.append(0.0)
        else:
            i = float(i)
            shooting_list.append(i)

    return shooting_list



def get_advanced(url):
    """
    takes in a specific player url and scrapes the career averages from the advanced table.
    must use in conjunction with `get_adv_cols` in order to sync the columns.
    """
    driver.get(url)
    # scraping advanced table
    driver.find_element_by_xpath("""//*[@id="all_advanced"]/div[1]/div/ul/li[1]/span""").click()

    WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
            (By.XPATH, """//*[@id="all_advanced"]/div[1]/div/ul/li[1]/div/ul/li[3]/button"""))).click()

    WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
            (By.CLASS_NAME, """table_outer_container""")))

    # capture csv text
    advanced = driver.find_element_by_id("csv_advanced")

    # data cleaning
    advanced = advanced.text.encode('ascii').split()

    for stats in advanced:
        if stats.startswith('Career'):
            advanced = re.findall('(\d[\d.,-]+)$', stats)[0]

    player_id = re.findall('(\w+\d)', url)

    advanced_list = [player_id[0]]
    for i in advanced.split(','):
        if i == '':
            advanced_list.append(0.0)
        else:
            i = float(i)
            advanced_list.append(i)

    del advanced_list[15]
    del advanced_list[19]
    return advanced_list


def get_shoot_cols():
    shooting_cols = ['Player_ID1', 'Games', 'Min_Played', 'FG%', 'AVG_DIST_FGA', '%FGA_2P', '%FGA_0-3ft',
                     '%FGA_3-10ft','%FGA_10-16ft', '%FGA_16ft<3', '%FGA_3P', '2P%',
                     '0-3_FG%', '3-10_FG%', '10-16_FG%', '16<3_FG%', '3P%', '%ASTd_2P',
                     '%FGA_DUNK', 'DUNKS', '%ASTd_3P', '%_CORNER3PA', '3P%_CORNER3',
                     'HEAVE_ATT', 'HEAVE_MD']
    return shooting_cols

def get_adv_cols():
    advanced_cols = ['Player_ID1','Games_', 'Minutes_Played', 'PER', 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%',
                     'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%', 'OWS', 'DWS', 'WS',
                     'WS/48', 'OBPM', 'DPM', 'BPM', 'VORP']
    return advanced_cols

def get_100_cols():
    points_poss_cols = ["Player_ID2", "GAMES","GS","MP_","FG_100","FGA_100","FG%_100","3P_100","3PA_100","3P%_100","2P_100","2PA_100",
                        "2P%_100","FT_100","FTA_100","FT%_100","ORB_100","DRB_100","TRB_100","AST_100","STL_100","BLK_100",
                        "TOV_100","PF_100","PTS_100","ORtg","DRtg"]
    return points_poss_cols

def get_pergame_cols():
    per_game_cols = ['Player_ID', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%',
                     '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB',
                     'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']

    return per_game_cols
