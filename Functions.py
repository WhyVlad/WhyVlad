import requests
import datetime
import math
import json
import secrets

datatime = math.trunc(datetime.datetime.now().timestamp()*1000)

#Change this variable to link to the YellowFin domain
staticUrl = "http://127.0.0.1:8083/api/"

def getZTMAGIC():
  #Change this variable for the production Zertic domain 
  url = 'https://master.ez2xs.com/call/api.Auth.Login.login?login=jos&password=..'

  # Request an authorization token from the server
  response = requests.get(url).json()

  # Get the MAGIC from the response
  return response['MAGIC']

def getYFSecurityToken():
  url = "{}refresh-tokens".format(staticUrl)
  nonce = secrets.token_urlsafe()
  payload = json.dumps({
    "userName": "admin@yellowfin.com.au",
    "password": "test",
    "clientOrgRef": ""
  })
  headers = {
    'Authorization': 'YELLOWFIN ts={}, nonce={}'.format(datatime,nonce),
    'Accept': 'application/vnd.yellowfin.api-v1+json',
    'Content-Type': 'application/json'
  }
  response = (requests.request("POST", url, headers=headers, data=payload)).json()
  tokenYF = response['_embedded']['accessToken']['securityToken']
  print(datatime,tokenYF)
  return tokenYF

def getYFJSonDataSourcesList(tokenYF):
  nonce = secrets.token_urlsafe()
  url = "{}data-sources".format(staticUrl)
  headers = {
          'Authorization': 'YELLOWFIN ts={}, nonce={}, token={}'.format(datatime,nonce,tokenYF),
          'Accept': 'application/vnd.yellowfin.api-v1+json',
          'Content-Type': 'application/json'
                }
  payload = ""

  response = (requests.request("GET", url, headers=headers, data=payload)).json()

  mylist = []
  for x in response['items'] :
      
    for key, value in x.items():
          if (key == 'sourceType' and value == 'JData'):
              mylist.append(x['sourceId'])
  return mylist;



def updateYFDataSources(tokenZT,tokenYF,mylist):
  nonce = secrets.token_urlsafe()
  headers = {
          'Authorization': 'YELLOWFIN ts={}, nonce={}, token={}'.format(datatime,nonce,tokenYF),
          'Accept': 'application/vnd.yellowfin.api-v1+json',
          'Content-Type': 'application/json'
                }
  payload = ""
  objectlist = []
  for i in mylist:
    url = "{}data-sources/".format(staticUrl) + str(i)
    response = (requests.request("GET", url, headers=headers, data=payload)).json()
    for key in response['sourceOptions']:
      if key['optionKey'] == 'EndURL' and key['optionValue'] != '':
        urllist = key['optionValue'].split('MAGIC')
        key['optionValue'] = urllist[0] + 'MAGIC=' + tokenZT
      if key['optionKey'] == 'JsonPath' and key['optionValue'] != '':
        urllist = key['optionValue'].split('MAGIC')
        key['optionValue'] = urllist[0] + 'MAGIC=' + tokenZT
      objectlist.append(key)
    YFdata = json.dumps({
      "sourceName": response['sourceName'],
      "sourceDescription": response['sourceDescription'],
      "sourceType": response['sourceType'],
      "connectionType": response['connectionType'],
      "connectionTypeCode": response['connectionTypeCode'],
      "connectionDriver": response['connectionDriver'],
      "connectionTimeout": response['connectionTimeout'],
      "minimumConnections": response['minimumConnections'],
      "maximumConnections": response['maximumConnections'],
      "refreshTime": response['refreshTime'],
      "timezone": response['timezone'],
      "accessLevelCode": response['accessLevelCode'],
      "maxRows": response['maxRows'],
      "maxAnalysisRows": response['maxAnalysisRows'],
      "inheritChildSourceFilters": response['inheritChildSourceFilters'],
      "sourceOptions": objectlist
    })
    objectlist = []
    response = requests.request("PATCH", url, headers=headers, data=YFdata)
    YFdata = []
    print(response)