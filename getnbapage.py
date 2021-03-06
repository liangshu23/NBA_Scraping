## FOR WALK THROUGH PLEASE REFER TO getnbapage.ipynb ##

import time
import bs4 as bs
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# enter path to your selenium chrome driver
Path = 'D:/____________/chromedriver.exe'
driver = webdriver.Chrome(executable_path = Path)
# link for the page you want to scrape data from
    # season total shooting by zone
link = 'https://www.nba.com/stats/players/shooting/?Season=2020-21&SeasonType=Regular%20Season&PerMode=Totals'

# opening page & getting rid of cookiepolicy pop-up
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


# criteria = '<tr ng-repeat'
criteria = '<tr aria-hidden="false"'

temp = []
# identify all table rows and isloate text & numbers
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
            row_text = row_text.split(',')
            #print(team_data)
            temp.append(row_text)

# find and click to move onto the next page
def nextpage():
    driver.implicitly_wait(3)
    next = driver.find_element_by_class_name('stats-table-pagination__next')
    next.click()
    driver.implicitly_wait(2)
    print('moving to next page')
    
    
#looping through all pages
for i in range (0,11):
    scrapepage()
    nextpage()

print(temp)

    # Column names you can use!

# Advanced_stats_columns = ['Blank','PLAYER', 'TEAM', 'AGE', 'GP', 'W', 'L', 'MIN', 'OFFRTG', 'DEFRTG', 	
# 'NETRTG', 'AST%', 'AST/TO', 'AST Ratio', 'OREB%', 'DREB%', 'REB%', 'TO Ratio', 'eFG%', 'TS%', 'USG%', 'PACE', 'PIE','Blank2']

# hustle_columns = ['Blank', 'Player', 'TEAM', 'AGE', 'GP', 'MIN', 'Screen.Assists', 'Screen.Assists.PTS', 'Deflections', 'OFF.Loose.Balls.Recovered',
# 'DEF.Loose.Balls.Recovered', 'Loose.Balls.Recovered', 'Percent Loose.Balls.Recovered.OFF', 'Percent.Loose.Balls.Recovered.DEF',
# 'Charges.Drawn', 'Contested.2PT.Shots', 'Contested.3PT.Shots', 'Contested.Shots', 'Blank2']

# Basic_Stats_columns = ['Blank','Player','Team','GP','W','L','Minutes','Drives','FGM','FGA','FG%','FTM','FTA','FT%',
#             'PTS','PTS%','PASS','PASS%','Assist','AST%','TO','TOV%','PF','PF%','Blank2']

# player_bio_columns = ['Blank','PLAYER', 'TEAM', 'AGE', 'Height', 'Weight', 'College', 'Country', 'DraftYear', 'DraftRound', 	
# 'DraftSpot', 'GP', 'PTS', 'REB', 'AST', 'NETRTG', 'OREBper', 'DREBper', 'USG', 'TS', 'ASTper','Blank2']

shooting_by_5ft_columns = ['Blank','Player','Team','Age','LT5 FGM','LT5 FGA','LT5 prct', 'Five-Nine FGM','Five-Nine FGA','Five-Nine prct',
           'Ten-Fourteen FGM','Ten-Fourteen FGA','Ten-Fourteen prct','Fifteen-Nineteen FGM','Fifteen-Nineteen FGA','Fifteen-Nineteen prct',
           'Twenty-TwentyFour FGM','Twenty-TwentyFour FGA','Twenty-TwentyFour prct','TwentyFive-TwentyNine FGM',
           'TwentyFive-TwentyNine FGA','TwentyFive-TwentyNine prct','Blank2']
# convert temp into dataframe
df = pd.DataFrame(temp, columns = shooting_by_5ft_columns)
df = df.drop(columns=['Blank','Blank2'])

#get row numbers with header rows we want to remove
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
    
# removing header rows and index column
df = df.drop(index = get_rep_title_axis(df)).reset_index()
df = df.drop(columns = ['index'])

# export file
df.to_csv()
