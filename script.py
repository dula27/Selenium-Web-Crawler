import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("headless")
driver = webdriver.Chrome(options=chrome_options)
source_name = "INTERPOL Red Notices"
source_url = "https://www.interpol.int/How-we-work/Notices/View-Red-Notices"
source_code = "INTERPOL_RN"
driver.get(source_url)

# Wait for page to laod
driver.implicitly_wait(5)

# Get elements from page by class
links = driver.find_elements_by_class_name('redNoticeItem__labelLink')

url_list = []
persons = ""

for link in links:
    url_list.append(link.get_attribute('href'))

driver.close()

for url_id in url_list:
    driver = webdriver.Chrome(options=chrome_options)
    print(url_id)
    driver.get(url_id)
    driver.implicitly_wait(15)

    date_of_birth = driver.find_element_by_id('date_of_birth').text
    place_of_birth = driver.find_element_by_id('place_of_birth').text
    country_of_birth_id = driver.find_element_by_id('country_of_birth_id').text
    sex_id = driver.find_element_by_id('sex_id').text
    nationalities = driver.find_element_by_id('nationalities').text
    forename = driver.find_elements_by_id('forename')[1].text
    name = driver.find_elements_by_id('name')[1].text

    driver.close()
    persons += '''
        {
            "firstname": "%s",
            "lastname": "%s",
            "about": {
                "date_of_birth": "%s",
                "place_of_birth": "%s %s",
                "nationality": "%s",
                "gender": "%s"
            },
            "other": {}
        },
''' % (forename, name, date_of_birth, place_of_birth, country_of_birth_id, nationalities, sex_id)

persons = persons[:-2]
json =  '''{
    "source_code": "%s",
    "source_name": "%s",
    "source_url": "%s",
    "persons": [
    %s
    ]
}''' % (source_code, source_name, source_url,persons)

with open('data.json', 'w') as page:
    page.write(json)
    page.close()