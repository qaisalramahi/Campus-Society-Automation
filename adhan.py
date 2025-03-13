import time 
from bs4 import BeautifulSoup
import requests
import pywhatkit as pwk
from selenium import webdriver

import sys
sys.stdout.reconfigure(encoding='utf-8')


def fetch_prayer_times():

    r = requests.get('https://www.islamicfinder.org/world/germany/2944388/bremen-prayer-times/')
    r.encoding = 'utf-8'
    
    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(r.text, 'html.parser')

    meta_tag = soup.find('meta',attrs={'name': 'description'})

    if meta_tag:
        content = meta_tag.get('content', '')
        with open("description.txt","w",encoding='utf-8') as f:
            f.write(content)
       # print("Meta Description Content written on description.txt")
        
    with open("description.txt","r",encoding='utf-8') as file:
        content = file.read()

    prayer_times = {}
    segments = content.split(',')

    for segment in segments:
    
        if 'Prayer Time' in segment:
            if '&' in segment:

                main_part, extra_part = segment.split('&', 1)

                # processing the main part - maghrib
                parts = main_part.split('Prayer Time')
                name = parts[0].strip()
                time = parts[1].strip()
                prayer_times[name] = time
                # Isha
                parts = extra_part.split('Prayer Prayer Time')
                if len(parts) == 2:  # ensuring it splits into two parts
                    name = parts[0].strip()
                    time = parts[1].strip()
            
               # name = name.replace('&', '').strip()
                
                if name =='Isha':
                    time = time.split('.',1)[0].strip()
                prayer_times[name] = time
            else:
                # all other prayers
                parts = segment.split('Prayer Time')
                if len(parts) == 2:
                    name = parts[0].strip()
                    time = parts[1].strip()
                    prayer_times[name] = time
        
    prayer_times.pop('Today',None)

    for key in list(prayer_times.keys()):
        if "Bremen Germany are" in key:
            new_key=key.replace("Bremen Germany are","").strip()
            prayer_times[new_key]=prayer_times.pop(key)
            
    return prayer_times 

def format_prayer_times(prayer_times):
    message = "📅 Daily Prayer Times for Bremen, Germany:\n\n"
    for prayer,time in prayer_times.items():
        message+= f"{prayer}: {time}\n"
        
    message+= "\nMay your day be blessed! 🌙"
    return message
        
def send_whatsapp_message(recipient,message,wait_time=50,tab_close=True,close_time=15):
    pwk.sendwhatmsg_to_group_instantly(recipient,message,wait_time,tab_close,close_time)
#from apscheduler.schedulers.background import BackgroundScheduler
#from apscheduler.triggers.cron import CronTriggersend_whatsapp_message()
def main():
    prayer_times = fetch_prayer_times()
    prayer_times_formatted = format_prayer_times(prayer_times)
    recipient= "Izg7UIoa3QN2fEqqUJUMx8"
    send_whatsapp_message(recipient,prayer_times_formatted)
if __name__ == "__main__":
    main()

'''def foo(bar):
    print(bar)


def main():
    scheduler = BackgroundScheduler()
    scheduler.start()

    trigger = CronTrigger(
        year="*", month="*", day="*", hour="3", minute="0", second="5"
    )
    scheduler.add_job(
        foo,
        trigger=trigger,
        args=["hello world"],
        name="daily foo",
    )
    while True:
        sleep(5)


if __name__ == "__main__":
    main()'''