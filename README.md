# airbnb_automation
Automation for airbnb.com website
reservation is selected in home page and validates: Check-in and checkout date, number of guests, elements in page such as reserve button and attempt of make reservation

Pages are implemented with POM design
listing page assertion are collected and printed at the end

in order to run the automation, please install all in install.txt 
to run from cmd from downloaded repo folder: pytest -s -vv

in conftest.py you can change the headless to False if you don't want to see the browser during tests

**Bugs found in automation of airbnb.com**
- When searching on 2-4/5/25 in Tel Aviv for 2 adults, results show listing not from Tel Aviv
- Input of phone is not always found when clicking on reserve in listing page
