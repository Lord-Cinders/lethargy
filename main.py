import login
import scrape
import csv
import time
import datetime as dt
import zoom

if __name__ == '__main__':

    date = int(dt.date.today().day)

    Classes_available = False
    classes_info = []

    # checks for classes
    try:
        with open('meetings.csv', 'r') as f:
            for i in f:
                p = i.split(',')

                if int(p[0]) > date: break
            
                if int(p[0]) == date:
                    Classes_available = True
                    classes_info.append(p[1:])
    except:
        open('meetings.csv', 'x') # creates file if it doesnt exist

    # If not founds fetches classes
    if not Classes_available:
        userid =  input("Enter ID: ")
        password = input("Password: ")

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

                if int(p[0]) > date: break
            
                if int(p[0]) == date:
                    Classes_available = True
                    classes_info.append(p[1:])

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
            if  hour == int(classes_info[i][0]) and localtime[4] < 50:
                zoom.Openzoom()
                zoom.Openmeeting(classes_info[i][1])
                wait_minutes = (50 -localtime[4])*60
                time.sleep(wait_minutes)
                zoom.Closemeeting()
                i += 1
                print("Finished class", i)

            else:
                wait_hour = abs(int(classes_info[i][0]) - hour - 1) 
                wait_minutes = 60 - localtime[4] 
                total_wait = wait_hour * 3600 + wait_minutes * 60 
                print("No class until", total_wait/60, "minutes")
                time.sleep(total_wait)
                

        except: print("Unable to open zoom")

    print("----------Done for the day!----------")
