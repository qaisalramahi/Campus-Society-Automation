import time
import sys
import PyPDF2
import re
from datetime import datetime, date
import pywhatkit as pwk

# Reconfigure stdout encoding
sys.stdout.reconfigure(encoding='utf-8')

def extract_prayer_times_from_pdf(pdf_path):
    try:
        # Open the PDF file
        with open(pdf_path, 'rb') as file:
            
            reader = PyPDF2.PdfReader(file)
            
            text = reader.pages[0].extract_text()
        
        lines = text.strip().split('\n')
        
        today = date.today()
        today_day = today.day
        today_month = today.month
            
        target_date = f"March {today_day}"
        today_prayer_times = None
        
        for line in lines:
            if target_date in line:
                parts = line.split()
                if len(parts) >= 8:
                    ramadan_day = parts[0]
                    # Format: "1 March 1 5:17 12:42 15:28 18:09 19:44"
                    fajr_pos = -5
                    dhuhur_pos = -4
                    asr_pos = -3
                    maghrib_pos = -2
                    isha_pos = -1
                    
                    today_prayer_times = {
                        'Fajr': parts[fajr_pos],
                        'Dhuhur': parts[dhuhur_pos],
                        'Asr': parts[asr_pos],
                        'Maghrib': parts[maghrib_pos],
                        'Isha': parts[isha_pos]
                    }
                    break
        
        if not today_prayer_times:
            print(f"Could not find prayer times for {target_date}")
            # Return empty dict if no times found
            return {}
            
        return today_prayer_times
        
    except Exception as e:
        print(f"Error extracting prayer times from PDF: {e}")
        return {}

def format_prayer_times(prayer_times):
    """
    Format prayer times into a WhatsApp message.
    
    Args:
        prayer_times (dict): Dictionary of prayer times
        
    Returns:
        str: Formatted message
    """
    today = date.today()
    message = f"📅 Prayer Times for Bremen, Germany - {today.strftime('%d %B %Y')}:\n\n"
    
    # Define prayer order for consistent display
    prayer_order = ['Fajr', 'Dhuhur', 'Asr', 'Maghrib', 'Isha']
    
    for prayer in prayer_order:
        if prayer in prayer_times:
            message += f"{prayer}: {prayer_times[prayer]}\n"
    
    message += "\nMay your day be blessed! 🌙"
    return message

def send_whatsapp_message(recipient, message, wait_time=50, tab_close=True, close_time=15):
    """
    Send WhatsApp message using pywhatkit.
    
    Args:
        recipient (str): WhatsApp group ID or phone number
        message (str): Message to send
        wait_time (int): Time to wait before sending
        tab_close (bool): Whether to close tab after sending
        close_time (int): Time to wait before closing tab
    """
    try:
        # Check if recipient is a group ID (no +)
        if not recipient.startswith('+'):
            pwk.sendwhatmsg_to_group_instantly(
                recipient, message, wait_time, tab_close, close_time
            )
        else:
            # Individual message
            pwk.sendwhatmsg_instantly(
                recipient, message, wait_time, tab_close, close_time
            )
        print("WhatsApp message sent successfully!")
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")

def main():
    pdf_path = "Ramadan_schedule.pdf"
    
    prayer_times = extract_prayer_times_from_pdf(pdf_path)
    
    if prayer_times:

        prayer_times_formatted = format_prayer_times(prayer_times)
        
        recipient = "Izg7UIoa3QN2fEqqUJUMx8"  
        
        send_whatsapp_message(recipient, prayer_times_formatted)
    else:
        print("No prayer times found for today.")

if __name__ == "__main__":
    main()

'''
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from time import sleep

def scheduled_main():
    main()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.start()

    # Run every day at 3:00:05 AM
    trigger = CronTrigger(
        year="*", month="*", day="*", hour="3", minute="0", second="5"
    )
    scheduler.add_job(
        scheduled_main,
        trigger=trigger,
        name="daily prayer times",
    )
    
    print("Scheduler started. Press Ctrl+C to exit.")
    try:
        # Keep the script running
        while True:
            sleep(5)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler stopped.")

if __name__ == "__main__":
    # Uncomment to use scheduler instead of one-time execution
    # start_scheduler()
    main()
'''