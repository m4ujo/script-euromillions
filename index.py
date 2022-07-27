import requests, json
from bs4 import BeautifulSoup
from datetime import date

BEGIN_YEAR = 2004
END_YEAR = date.today().year + 1

def getSoup(year):
  response = requests.get(f'https://www.euromillones.com.es/historico/resultados-euromillones-{year}.html')
  tables = BeautifulSoup(response.text, 'html.parser').find_all('table')
  rows = tables[0].find_all('tr')
  rows.pop(0)
  rows.pop(0)
  return rows

def removeUnnecesaryData(ticket):
  if len(ticket) > 9:
    if year >= 2011 and year <= 2015:
      ticket.pop(0)
    if year >= 2016:
      del ticket[-1]
      if len(ticket) > 9:
        ticket.pop(0)

  return ticket

def fixDate(date):
  dateItem = ''.join([date, f'-{year}'])
  dateItem = dateItem.replace("ene", "1")
  dateItem = dateItem.replace("feb", "2")
  dateItem = dateItem.replace("mar", "3")
  dateItem = dateItem.replace("abr", "4")
  dateItem = dateItem.replace("may", "5")
  dateItem = dateItem.replace("jun", "6")
  dateItem = dateItem.replace("jul", "7")
  dateItem = dateItem.replace("ago", "8")
  dateItem = dateItem.replace("sep", "9")
  dateItem = dateItem.replace("oct", "10")
  dateItem = dateItem.replace("nov", "11")
  dateItem = dateItem.replace("dic", "12")
  dateItem = dateItem.replace("-", "/")
  return dateItem

def saveDataInList(list, ticket, year, dateItem, indexItem):
  list[f'{year}'].append({
    'date': dateItem,
    'index': indexItem,
    'num1': 0 if ('br' in str(ticket[2].contents[0])) else int(ticket[2].contents[0]),
    'num2': 0 if ('br' in str(ticket[3].contents[0])) else int(ticket[3].contents[0]),
    'num3': 0 if ('br' in str(ticket[4].contents[0])) else int(ticket[4].contents[0]),
    'num4': 0 if ('br' in str(ticket[5].contents[0])) else int(ticket[5].contents[0]),
    'num5': 0 if ('br' in str(ticket[6].contents[0])) else int(ticket[6].contents[0]),
    'str1': 0 if ('br' in str(ticket[7].contents[0])) else int(ticket[7].contents[0]),
    'str2': 0 if ('br' in str(ticket[8].contents[0])) else int(ticket[8].contents[0])
  })

if __name__ == "__main__":
  print('Getting data...')
  listTickets = {}
  L = []
  
  yearTest = 2022

  for year in range(BEGIN_YEAR, END_YEAR):
    listTickets[f'{year}'] = []
    rows = getSoup(year)
    for index, row in enumerate(rows):
      ticket = row.find_all('td')
      if len(ticket) > 2:
        removeUnnecesaryData(ticket)
        dateItem = fixDate(ticket[1].contents[0])
        indexItem = ticket[0].contents[0].replace(" ", "")
        saveDataInList(listTickets, ticket, year, dateItem, indexItem)

  datatxt = open('data.txt', 'w')
  for year in range(BEGIN_YEAR, END_YEAR):
    for ticket in listTickets[f'{year}']:
      datatxt.writelines([f'{ticket.get("date")}\t', f'{ticket.get("index")}\t', f'{ticket.get("num1")}\t', f'{ticket.get("num2")}\t', f'{ticket.get("num3")}\t', f'{ticket.get("num4")}\t', f'{ticket.get("num5")}\t', f'{ticket.get("str1")}\t', f'{ticket.get("str2")}\n'])
  datatxt.close()

  datatxt = open('data.txt', 'r')
  print(datatxt.read())
  datatxt.close()

  print('Data obtained successfully')