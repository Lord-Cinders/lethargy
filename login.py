import requests
from bs4 import BeautifulSoup as bs
from requests.models import HTTPBasicAuth

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
        print(redirect)

        if(redirect[0] != 'http://gitam.edu/'): # Unsuccessful Login
            print('----------Login Failed----------', end='\n\n')
            return

        # Successful login
        print('----------Login Successful----------', end='\n\n') 
        url = 'http://glearn.gitam.edu/student/welcome.aspx' 
        
        glearnheaders = {
            'Host': 'glearn.gitam.edu',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Cookie': 'ASP.NET_SessionId=a345flviyfxreke3xkquc1eg',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }

        req = s.get(url, headers = glearnheaders)
        print(req)

        return req