# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 21:28:23 2018

@author: Uxío
"""

import re
import requests
from lxml import html

# This URL will be the URL that your login form points to with the "action" tag.
# Login URL might not be obvious. An advanced trick to find it:
# 1. Open developer tools (F12)
# 2. Go to "network" tab and watch it while you log in the page
# 3. An item should be active while you do this. Click on its name.
# 4. In the new menu, go to "Headers" tab. Here you can get the field
# "Request URL" as well as "Form data" (useful in defining the payload)"
POST_LOGIN_URL = 'https://www.example.es/lib/login.php'

#This URL is the page you actually want to pull down with requests.
REQUEST_URL = 'https://www.example.es/data'

# Check the info you need to supply in "Form data" and substitute the names of
# the fields ('usr', 'pwd-login'). USERNAME and PASS are your own credentials
payload = {
	'usr': 'USERNAME', 
	'pwd-login': 'PASS' 
	#"csrfmiddlewaretoken": "" # Field might be needed
}

# Using a session lets us use the autentification cookie for subsequential
# requests:
with requests.Session() as session:
    
    post = session.post(POST_LOGIN_URL, data=payload) # Cookie saved
    r = session.get(REQUEST_URL)
    
    # Get HTML content from the page of interest
    tree = html.fromstring(r.content)
    
    # Look for the field of interest. We can inspect the element in the webpage
    # (right click -> inspect, on the element), then right click over the html 
    #line in developer tools -> Copy -> Copy Xpath
    price = tree.xpath("//div[@id='Price']/text()")
    
    # String has weird formatting. Using regex expression to get a substring 
    # until the "€" character is found    
    p = re.compile( '(.*)(?:€)' )
    price_string = p.match( price[0]).group()
    
    print('Saldo: ',price_string)
