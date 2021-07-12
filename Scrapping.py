from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait



'''
This function is used to scrape the name and hyperlinks of articles on factiva
It allows the user to input a text to search 
The function has 4 parameters:
path - the path of selenium chromedriver on your laptop
user - the HKU library username to log into your portal
passw - the HKU library password to log into your portal
text - the text you want to search on factiva 

Further Posibilities:
1. various other parameters of search can be added 
2. the scrapping can be widdened and details of articles other than name can be retrieved
'''
def scrapping_factiva(path, user, passw, search_text):

    
    driver = webdriver.Chrome(path)
    driver.get("https://julac-hku-a.alma.exlibrisgroup.com/view/action/uresolver.do?operation=resolveService&package_service_id=13999846060003414&institutionId=3414&customerId=3405")
    
    #find username and password for the login form
    username = driver.find_element_by_name("userid")
    password = driver.find_element_by_name("password")
    #send username and password for the login form
    username.send_keys(user)
    password.send_keys(passw)
    #click on submit to login
    driver.find_element_by_xpath("//button[@type='submit']").click()
    
    #wait 90 seconds for new page to load 
    wait = WebDriverWait(driver, 60)
    text = wait.until(EC.presence_of_element_located((By.NAME, 'ftx')))
    
    text.clear()
    #send text you want to search
    #CAN ADD OTHER PARAMETES HERE
    text.send_keys(search_text)
    #click on submit to search the text 
    driver.find_element_by_xpath("//input[@type='submit']").click()
    
    #wait 30 second for new page to load
    wait2 = WebDriverWait(driver, 30)
    present = wait2.until(EC.presence_of_element_located((By.CLASS_NAME, 'hitsCount')))
    #hisCount counts the total number of articles related to that text
    counts = driver.find_elements_by_class_name("hitsCount")
    print("Number of Dow Jones articles = " + counts[0].text)
    print("Number of total articles = " + counts[1].text)
    
    #enHeadline gives the title of each article
    title = driver.find_elements_by_class_name("enHeadline")
    headline=[]
    hyperlink=[]
    for tt in title:
        headline.append(tt.text)
        hyperlink.append(tt.get_attribute('href'))
    #add the title and hyperlinks of articles in a pandas dataframe
    article={"TITLE":headline, "LINK": hyperlink}
    df=pd.DataFrame(article)
    display(df)
    
if __name__ == "__main__" :
    chrome_path = r"/Users/varun/Desktop/factiva/chromedriver"
    username = ""
    password = ""
    text = "JP Morgan"
    scrapping_factiva(chrome_path, username, password, text)

