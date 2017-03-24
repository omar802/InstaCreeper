from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
import urllib
import urlparse
import re
import time
import os
import sys



#  Enter username of the user who's images you want to download at the end of the url

url = 'https://www.instagram.com/USER_NAME_GOES_HERE/'
path = urlparse.urlparse(url).path
folder_name = path.replace('/', '')
folder_path = 'images/{}/'.format(folder_name)

if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print 'Folder path created'

# Using webdriver to open our Chrome and navigate to the url
driver = webdriver.Chrome('C:\Users\Alex8\Documents\Visual Studio 2015\Projects\Instascrapper\chromedriver.exe')
driver.get(url)
driver.set_window_size(300, 6000)
# delay = 3  # seconds
# driver.execute_script("window.scrollTo(0, 1000)")

# Find the Load more button and click it to load more images
clickin = driver.find_element_by_link_text('Load more')

if clickin.click():
    print 'The load more button was clicked'
    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight)"
    )

scroll_counter = 0
# edit this to get the number of scroll downs for about 1000 images you need to use 90 and so on do the math
while scroll_counter <= 90:
    time.sleep(5)
    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight)"
    )
    scroll_counter += 1
    print 'Scroll Counter = {}'.format(scroll_counter)

soup = BeautifulSoup(driver.page_source, "lxml")
print 'We have hot delicios soup'

image_list = []
for link in soup.find_all('img'):
    print 'Gathering your images be patient...'
    # Finding all images
    m = re.search('src="(.+?)"', str(link))
    image_list.append(m.group(1))

counter = 0
for image in image_list:
    print 'Saving images'
    counter = counter + 1
    extension = '.jpg'
    path = folder_path + str(counter) + extension
    print path
    urllib.urlretrieve(image, path)
