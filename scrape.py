from bs4 import BeautifulSoup as bs
import re

# returns a dict with date: {time: meeting ids} 
def ScrapeData(webpage):
    # accessing welcome page

    soup = bs(webpage.content, 'html5lib')
    table_zoom = soup.find('table', attrs={'id': 'ContentPlaceHolder1_GridViewonline'}) # table with zoom links

    try:
        zoom_links = table_zoom.find_all("a") # finding links
        link_info = table_zoom.find_all("h6") # finding meeting details

    except:
        print("---------No Classes Found----------")
        return 0, 0

    dates_times = [str(i) for i in link_info]   
    links = [str(i.get('href')) for i in zoom_links]

    # getting meeting ids
    # for i in range(len(links)):
    #     m = re.search('/j/(.+?)?pwd=', links[i])
    #     links[i] = m.group(1).rstrip('?')
    return links, dates_times

# seperating text from tags and seperating date and time
def Mergedata(links, dates_times):
    meeting_info = []

    for i in range(len(dates_times)):

        start = dates_times[i].find('>')
        end = dates_times[i].rfind('<')
        dates_times[i] = dates_times[i][start + 1:end]

        p = dates_times[i].split(':')
        date = p[1].split('-')[0]

        # converting to 24 hour format
        if  int(p[4]) < 9: time = int(p[4]) + 12 
        else: time = int(p[4]) 

        meeting_info.append((date, time, links[i]))

    meeting_info.sort()

    return meeting_info