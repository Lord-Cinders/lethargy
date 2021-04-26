import login
import scrape
import csv
import time
import datetime as dt
import zoom
import os

if __name__ == '__main__':

    date = dt.date.today()
    strdate = str(date.day) + '-' + date.strftime('%b') + '-' + str(date.year)
    
    Classes_available = False
    classes_info = []

    # checks for classes
    try:
        with open('meetings.csv', 'r') as f:
            for i in f:
                p = i.split(',')

                if p[0].strip(' ') > strdate: break
            
                if p[0].strip(' ') == strdate:
                    Classes_available = True
                    classes_info.append(p[1:])
    except:
        open('meetings.csv', 'x') # creates file if it doesnt exist
                
    # If not founds fetches classes
    if not Classes_available:
        userid = input("Enter your Pin No: ")
        password = input("Enter your password: ")

        welcome_page = login.Login(userid, password)

        # only successful login
        if welcome_page:
            links, date_times = scrape.ScrapeData(welcome_page)
            if links and date_times:
                meeting_data = scrape.Mergedata(links, date_times)

                # write to file
                with open('meetings.csv', 'w', newline = '') as f:
                    writer = csv.writer(f)
                    writer.writerows(meeting_data) # Date - Time - Meeting id
                    print('----------Classes Successfully Saved----------', end='\n\n')

        # check for todays classes
        with open('meetings.csv', 'r') as f:
            for i in f:
                p = i.split(',')

                if p[0].strip(' ') > strdate: break
               
                if p[0].strip(' ') == strdate:
                    classes_info.append(p[1:])
                    Classes_available = True

    i = 0
    no_classes = len(classes_info)
    
    # main loop
    while True:

        if not Classes_available: break

        localtime = time.localtime(time.time())
        hour = localtime[3]
        
        if hour > 17 or i == no_classes: break

        if hour > int(classes_info[i][0]):
            i += 1
            continue

        try: 
            if  hour == int(classes_info[i][0]):
                zoom.Openzoom()
                zoom.Openmeeting(classes_info[i][1])

                time.sleep(48 * 60)
            
                zoom.Closemeeting()
                
                i += 1
                print("Finished class", i)

            else:
                wait_hour = abs(int(classes_info[i][0]) - hour - 1) 
                wait_minutes = 60 - localtime[4] 
                total_wait = wait_hour * 3600 + wait_minutes * 60 
                
                print("No class until", total_wait/60, "minutes")
                time.sleep(total_wait)
                
        
        except: print("---------An unknown error has occured----------")

    print("----------Done for the day!----------")
