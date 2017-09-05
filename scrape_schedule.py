from lxml import html
from datetime import datetime
import requests


def scrape_games(tree):

    # get all away teams and home teams
    home_teams = tree.xpath('//span[contains(@class, "team-name home")]/text()')
    away_teams = tree.xpath('//span[contains(@class, "team-name away")]/text()')
    date_ids = tree.xpath('//div[contains(@class, "schedules-list-content")]/@data-gameid')

    # get the proper datetime from the date ids
    dates = get_dates(date_ids)
 
    return (home_teams, away_teams, dates)

def get_dates(date_ids):
   
    # list to return
    dates = list()
   
    for date in date_ids:
        dates.append(str(datetime.strptime(date[0:-2], '%Y%m%d').strftime('%A %m-%d-%Y')))
    return dates


def write_to_text_file(game_info, week_num):

    # name text file and open
    text_file = open('week' + week_num + '.txt', 'w')
    text_file.write('NFL Week ' + week_num + ' Schedule:\n')
    text_file.write('\n')
    for home_team, away_team, date in game_info:
        text_file.write('%s: %s @ %s\n' % (date, away_team, home_team))
    text_file.close()


def main():
    # get the week number as user input
    week_num = input('Please enter the week number to scrape: ')

    # build the url based on the week number entered
    url = requests.get('http://www.nfl.com/schedules/2017/REG' + week_num)
    tree = html.fromstring(url.content)

    # scrape all games and return in a list
    home_teams, away_teams, dates = scrape_games(tree)

    # write and save to text file
    write_to_text_file(zip(home_teams, away_teams, dates), week_num)


if __name__ == '__main__':
    main()
