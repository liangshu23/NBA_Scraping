import time
import bs4 as bs
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

tsd = pd.DataFrame()
Path = 'D:/Python/chromedriver.exe'
driver = webdriver.Chrome(executable_path = Path)
#link for opponent shooting by zone
# link = 'https://stats.nba.com/teams/opponent-shooting/?Season=2019-20&SeasonType=Regular%20Season&DistanceRange=By%20Zone'
#link for team shooting by zone
#link = 'https://www.nba.com/stats/players/advanced/?sort=PLAYER_NAME&dir=-1&Season=2020-21&SeasonType=Regular%20Season'
# link = 'https://www.nba.com/stats/players/bio/?Season=2020-21&SeasonType=Regular%20Season'

# pergame shooitng by zone
# link = 'https://www.nba.com/stats/players/shooting/'

# season total shooting by zone
link = 'https://www.nba.com/stats/players/shooting/?Season=2020-21&SeasonType=Regular%20Season&PerMode=Totals'

# link = 'https://www.nba.com/stats/players/shooting/?Season=2020-21&SeasonType=Regular%20Season'

driver.get(link)
try:
    WebDriverWait(driver,15).until(
        EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler'))
    )
except:
    pass

element = driver.find_element_by_id('onetrust-accept-btn-handler')
element.click()
time.sleep(1.5)
# source = bs.BeautifulSoup(driver.page_source, 'html.parser').find('table')
# whole = [b for b in source.find_all('tr')]
# whole_text = [b.text() for b in source.find_all('tr')]

# criteria = '<tr ng-repeat'
criteria = '<tr aria-hidden="false"'

temp = []
# print(whole)
# print(len(whole))

# print(whole_text)

def scrapepage():
    source = bs.BeautifulSoup(driver.page_source, 'html.parser').find('table')
    whole = [b for b in source.find_all('tr')]
    for i in range(0,len(whole)):
        blockstr = str(whole[i])
        # print(blockstr)
        if blockstr.startswith(criteria):
            row_text = whole[i].text
            row_text = row_text.replace('  ', '')
            #print(row_text)
            row_text = row_text.replace('\n', ',')
            #print(row_text)
            row_text = row_text.replace(',,', ',')
            #print(row_text)
            row_text = row_text.replace(',,', ',')
            #print(row_text)
            row_text = row_text.replace('\xa0', '')
            #print(row_text)
            team_data = row_text.split(',')
            #print(team_data)
            temp.append(team_data)


def nextpage():
    driver.implicitly_wait(3)
    next = driver.find_element_by_class_name('stats-table-pagination__next')
    next.click()
    driver.implicitly_wait(2)
    print('moving to next page')
    # new_url = driver.current_url

for i in range (0,11):
    scrapepage()
    nextpage()

print(temp)

# Advanced_stats_columns = ['blank','PLAYER', 'TEAM', 'AGE', 'GP', 'W', 'L', 'MIN', 'OFFRTG', 'DEFRTG', 	
# 'NETRTG', 'AST%', 'AST/TO', 'AST Ratio', 'OREB%', 'DREB%', 'REB%', 'TO Ratio', 'eFG%', 'TS%', 'USG%', 'PACE', 'PIE','bl']

# hustle_columns = ['blank', 'Player', 'TEAM', 'AGE', 'GP', 'MIN', 'Screen Assists', 'Screen Assists PTS', 'Deflections', 'OFF Loose BallsRecovered',
# 'DEF Loose Balls Recovered', 'Loose Balls Recovered', 'Percent Loose BallsRecovered OFF', 'Percent Loose BallsRecovered DEF',
# 'Charges Drawn', 'Contested 2PT Shots', 'Contested 3PT Shots', 	'Contested Shots', 'blank2']

# Basic_Stats_columns = ['Blank','Player','Team','GP','W','L','Minutes','Drives','FGM','FGA','FG%','FTM','FTA','FT%',
#             'PTS','PTS%','PASS','PASS%','Assist','AST%','TO','TOV%','PF','PF%','Blank2']

# player_bio_columns = ['blank','PLAYER', 'TEAM', 'AGE', 'Height', 'Weight', 'College', 'Country', 'DraftYear', 'DraftRound', 	
# 'DraftSpot', 'GP', 'PTS', 'REB', 'AST', 'NETRTG', 'OREBper', 'DREBper', 'USG', 'TS', 'ASTper','bl']

shooting_by_5ft_columns = ['Blank','Player','Team','Age','LT5 FGM','LT5 FGA','LT5 prct', 'Five-Nine FGM','Five-Nine FGA','Five-Nine prct',
           'Ten-Fourteen FGM','Ten-Fourteen FGA','Ten-Fourteen prct','Fifteen-Nineteen FGM','Fifteen-Nineteen FGA','Fifteen-Nineteen prct',
           'Twenty-TwentyFour FGM','Twenty-TwentyFour FGA','Twenty-TwentyFour prct','TwentyFive-TwentyNine FGM',
           'TwentyFive-TwentyNine FGA','TwentyFive-TwentyNine prct','Blank2']

df = pd.DataFrame(temp, columns = shooting_by_5ft_columns)
df = df.drop(columns=['Blank','Blank2'])

def get_rep_title_axis(dfname):
    wrong_rows = []
    for i in range(0, dfname.shape[0]):
        if dfname.iloc[i,0] == 'Player':
            print(i)
            wrong_rows.append(i-1)
            wrong_rows.append(i)
        else:
            pass

    return wrong_rows
    
   
df = df.drop(index = get_rep_title_axis(df)).reset_index()
df = df.drop(columns = ['index'])


print(df.head(10))

#df = df.drop(columns = [['blank','bl']], inplace=True)
#print(df.head(20))
#df = df.drop(columns = [['blank','bl']], inplace=True)
# df.to_csv('D:/Python/NBA/data/20-21_player_bio.csv')
df.to_csv('D:/Python/nba2020/nba20-21_shooting_by_5ft.2021.5.2.csv')
