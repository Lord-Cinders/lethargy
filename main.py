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
    with open('meetings.csv', 'r') as f:
        for i in f:
            p = i.split(',')

            if p[0].strip(' ') > strdate: break
            
            if p[0].strip(' ') == strdate:
                Classes_available = True
                classes_info.append(p[1:])
                

    # If not founds fetches classes
    if not Classes_available:
        userid = '221910307033' #input("Enter your Pin No: ")
        password = 'qwerty@12' #input("Enter your password: ")

        welcome_page = login.Login(userid, password)

        # only successful login
        if welcome_page:
            links, date_times = scrape.ScrapeData(welcome_page)
            if links and date_times:
                meeting_data = scrape.Mergedata(links, date_times)

                # remove previous data
                if(os.path.exists('meetings.csv') and os.path.isfile('meetings.csv')): os.remove('meetings.csv')

                # write to file
                with open('meetings.csv', 'a', newline = '') as f:
                    writer = csv.writer(f)
                    writer.writerows(meeting_data) # Date - Time - Meeting id
                    print('----------Classes Successfully Saved----------', end='\n\n')

        # check for todays classes
        with open('meetings.csv', 'r') as f:
            for i in f:
                p = i.split(',')

                if p[0].strip(' ') > strdate: break
               
                if p[0].strip(' ') == strdate:
                    classes_info.append(p)
                    Classes_available = True

    i = 0
    no_classes = len(classes_info)
    
    # main loop
    while True:

        if not Classes_available: break

        localtime = time.localtime(time.time())
        hour = localtime[3]
        
        if hour > 17 or i == no_classes: break

        try: 
            if  hour == int(classes_info[i][0]):
                zoom.Openzoom()
                
                zoom.Openmeeting(classes_info[i][1])

                time.sleep(45 * 60)
            
                zoom.Closemeeting()
                
                i += 1
                print("Finished class", i)

            else:
                wait_hour = abs(int(classes_info[i][0]) - hour)
                wait_minutes = 60 - localtime[4] 
                total_wait = wait_hour * 3600 + wait_minutes * 60 
                
                time.wait(total_wait)
        
        except: print("---------An unknown error has occured----------")

    print("----------Done for the day!----------")


    

    
    


    



