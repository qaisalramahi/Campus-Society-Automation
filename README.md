When I received the task of automating the sending of a certain type of data - before running any code I decided to use the divide and conquer approach to split this problem into smaller ones so that I can eventually come up with the final
solution. 

1. Where do I get this data from?
2. How to extract it? 
3. How to format it in a way to send to people professionally?
4. How to access WhatsApp's API to send the message?
5. How to schedule a daily reminder to send at regular intervals each day? 


## What adhan.py does: 

I was using BeautifulSoup and Requests libraries to scrape dynamic content from a specific website. Then I applied techniques to extract the content that was relevant to me - getting rid of all the rest of the data that was not needed. 
I had a function that was responsible for formatting the message in a neat and concise way so as to be sent on a WhatsApp group chat. 

What really helped making this happen is the pywhatkit library and I am extremely grateful for [Ankit404butfound](https://github.com/Ankit404butfound) for creating this library because without it - I would not have been able to make this. 
WhatsApp have a real problem sharing their API and finding it for free was a pain for the longest time. 

## What ramadan.py does: 

Here, the only difference was that instead of following the website that I was scraping data from - I was given a pdf document and told to follow the contents that were on there instead for a specific month of the year.
But once again due to the availability of a library that eases these things, in this case PyPDF2 which have a .extract_text() method - extracting the data and placing it in a specific format by splitting the text was an easy solution to implement. 

## How I schedule the message

Right now I am trying to make this project without spending money on it although I know that I can put this script on the cloud and it can run automatically that way. However, for the time being I am using Microsoft's task scheduler which does it for me. I know this is somewhat of a limitation right now but can definitely be imporved in the future. That is also why I have the part for APscheduler commented because that could also be an option if I wanted to use code to automate this procedure as well. 
