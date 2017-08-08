#import schedule
#import time
import requests
#from bs4 import BeautifulSoup as soup
#import requests as req
#import re
#import html2text
#import os
#import errno
token='402534967:AAH-vMKfI1OlpNnusY0HD5kpWDGn2QJl3AA'
method='sendMessage'

        
            
response = requests.post(
            url='https://api.telegram.org/bot{0}/{1}'.format(token, method),
            data={'chat_id': '@testqw', 'text': 'hi'}
            ).json()
print('ddd')
print(response)

    
    
















    
