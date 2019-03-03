from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import sleep
import re
from random import randrange
from selenium import webdriver



def get_pages():

    # Open csv file and create header for url_name
    filename = "bgg_page_urls.csv"
    f = open(filename, "w")
    header = ('url_name\n')
    f.write(header)

    # Loop through each page of BGG game rankings
    page_number = 1
    while page_number < 169:
        html = urlopen('https://boardgamegeek.com/browse/boardgame/page/{}'.format(page_number))
        bs = BeautifulSoup(html, 'html.parser')
        rows = bs.find_all('tr', id='row_')

        # Loop through each row on each page and collect URL extension info for each game
        for row in rows:
            page_url = row.find_all('a', href=re.compile('^(/boardgame/)'))[1].attrs['href']
            print(page_url)
            f.write(page_url + '\n')

        page_number += 1
        sleep(randrange(1,10))


def get_stats():

    # Read in list of URL extensions
    page_urls = pd.read_csv('bgg_page_urls.csv')

    # Open csv file and create headers
    filename = "bgg.csv"
    f = open(filename, "w")
    headers = ("game_name,avg_rating,ratings,std_deviation,weight,comments,"
        "fans,page_views,overall_rank,player_range,avg_play_time,age_rating,year, "
        "categories,mechanisms,families\n")
    f.write(headers)

    # Loops through each page
    count = 0
    for url in page_urls.url_name:
        try:
            # Souping each stats page
            stats_url = 'https://boardgamegeek.com{}/stats'.format(url)
            stats_driver = webdriver.Chrome()
            stats_driver.get(stats_url)
            stats_html = stats_driver.page_source
            stats_bs = BeautifulSoup(stats_html, 'html.parser')
            print(stats_bs.div)

            # Grabbing stats variables
            game_name = stats_bs.find_all('h1')[1].get_text().strip()
            avg_rating = stats_bs.find_all('div', class_="outline-item-description")[0].get_text().strip()
            ratings = stats_bs.find_all('div', class_="outline-item-description")[1].get_text().strip().replace(',', '')
            std_deviation= stats_bs.find_all('div', class_="outline-item-description")[2].get_text().strip()
            weight = stats_bs.find_all('div', class_="outline-item-description")[3].get_text().strip().split()[0]
            comments = stats_bs.find_all('div', class_="outline-item-description")[4].get_text().strip().replace(',', '')
            fans = stats_bs.find_all('div', class_="outline-item-description")[5].get_text().strip().replace(',', '')
            page_views = stats_bs.find_all('div', class_="outline-item-description")[6].get_text().strip().replace(',', '')
            overall_rank = stats_bs.find_all('div', class_="outline-item-description")[7].get_text().strip()
            players = re.findall(r'\d+', stats_bs.find_all('div', class_='gameplay-item-primary')[0].get_text())
            player_range = ' '.join(players)
            play_time = np.asarray(re.findall(r'\d+', stats_bs.find_all('div', class_='gameplay-item-primary')[1].get_text()))
            avg_play_time = str(play_time.astype(float).mean())
            age_rating = re.findall(r'\d+', stats_bs.find_all('div', class_='gameplay-item-primary')[2].get_text())[0]
            stats_driver.close()
            print("game_name " + str(game_name))
            print("avg_rating " + str(avg_rating))
            print("ratings " + str(ratings))
            print("std_deviation " + str(std_deviation))
            print("weight " + str(weight))
            print("comments " + str(comments))
            print("fans " + str(fans))
            print("page_views " + str(page_views))
            print("overall_rank " + str(overall_rank))
            print("player_range " + str(player_range))
            print("play_time " + str(play_time))
            print("avg_play_time " + str(avg_play_time))
            print("age_rating " + str(age_rating))
            print("stats_driver " + str(stats_driver))

            # Souping each credits page
            credits_url = 'https://boardgamegeek.com{}/credits'.format(url)
            credits_driver = webdriver.Chrome()
            credits_driver.get(credits_url)
            credits_html = credits_driver.page_source
            credits_bs = BeautifulSoup(credits_html, 'html.parser')
            print(credits_bs.div)

            # Grabbing credits variables
            year = credits_bs.find_all('div', class_='outline-item-description')[2].get_text().strip()
            categories = credits_bs.find_all('div', class_='outline-item-description')[6].get_text().strip().replace(',', '')
            mechanisms = credits_bs.find_all('div', class_='outline-item-description')[7].get_text().strip().replace(',', '')
            families = credits_bs.find_all('div', class_='outline-item-description')[8].get_text().strip().replace(',', '') 
            credits_driver.close()
            print("year " + str(year))
            print("categories " + str(categories))
            print("mechanisms " + str(mechanisms))
            print("families " + str(families))

            # Writing all variables to csv file
            f.write(game_name + ', ' + avg_rating + ', ' + ratings 
                + ', ' + std_deviation + ', ' + weight + ', ' + 
                comments + ', ' + fans + ', ' + page_views + ', '
                + overall_rank + ', ' + player_range
                + ', ' + avg_play_time + ', ' + age_rating + ', ' + 
                year + ', ' + categories + ', ' + mechanisms + ', ' + families + '\n')

            # Command line helpers
            print(game_name)
            count += 1
            print(count)

            sleep(randrange(1,3))

            if count == 600:
                break

        except (IndexError, UnicodeEncodeError, MemoryError):
            continue
        




get_pages()

get_stats()

f.close()

