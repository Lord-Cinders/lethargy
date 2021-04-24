import requests
from bs4 import BeautifulSoup as bs

def Login(userid, password):
    # constant POST Parameters
    payload = { 'txtusername' : userid,
                'password' : password,
                '__EVENTTARGET' : "",
                '__EVENTARGUMENT' : "",
                'Submit' : 'Login'
            }

    # browser headers
    headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0' }

    with requests.Session() as s: 
        req = s.get('https://login.gitam.edu/login.aspx', headers = headers)

        soup = bs(req.content, 'html5lib')
        
        # get additional POST parameters
        payload['__VIEWSTATE'] = soup.find('input', attrs = {'name' : '__VIEWSTATE' })['value']
        payload['__VIEWSTATEGENERATOR'] = soup.find('input', attrs = {'name' : '__VIEWSTATEGENERATOR' })['value']
        payload['__EVENTVALIDATION'] = soup.find('input', attrs = {'name' : '__EVENTVALIDATION' })['value']  
        
        # POST- for logging in
        req = s.post('https://login.gitam.edu/login.aspx', data = payload, headers = headers)
        soup = bs(req.content, 'html5lib')

        # To enter Glearn
        redirect = [a['href'] for a in soup.find_all('a', href=True)]

        if(redirect[0] == 'Signage_Images.aspx'): # Unsuccessful Login
            print('----------Login Failed----------', end='\n\n')
            return

        # Successful login
        print('----------Login Successful----------', end='\n\n') 
        url = 'http://login.gitam.edu/' + redirect[2]
        req = s.get(url, headers = headers)

        return req
        