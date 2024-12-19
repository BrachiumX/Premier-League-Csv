import csv
import requests
from bs4 import BeautifulSoup, Tag
import time

destination = '/home/user/Desktop/PremMatches/premTable'
startYear = 1889
endYear = 2025

if __name__ == '__main__':
    url1 = 'https://fbref.com/en/comps/9/'
    url2 = '/schedule/'
    url3 = 'Premier-League-Scores-and-Fixtures'
    argList = range(startYear, endYear)
    for arg in argList:

        with open(destination + str(arg) + '.csv', 'w', newline = '') as csvfile:

            if arg in range(1906, 1909) or arg in range(1940, 1946):
                continue

            writer = csv.writer(csvfile)

            year = str(arg - 1) + '-' + str(arg)
            request = requests.get(url1 + year + url2 + year + url3)
                
            html = BeautifulSoup(request.content, 'html.parser')
                
            table = html.find('table')

            assert table != None

            table = table.find('tbody') 

            assert isinstance(table, Tag)

            rows = table.find_all('tr')

            for curr in rows:
                row = {}

                assert isinstance(curr, Tag)

                list = curr.find_all('td')


                for element in list:
                    row[element.get('data-stat')] = element.text

                if not 'score' in row.keys() or not row['score'].split('–')[0].isnumeric():
                    continue

                writer.writerow([row['home_team'], row['away_team'], row['score'].split('–')[0], row['score'].split('–')[1]])


            print('Completed '+ str(arg))
            time.sleep(20)

