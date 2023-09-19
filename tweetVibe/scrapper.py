import selenium
import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

def initilaize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # runs browser in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-gpu')
    options.add_argument('--log-level=3')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-popup-blocking')
    driver = webdriver.Chrome(options= options, )
    return driver

def login(driver,uname="tweetAsis_2023",pswd="tweetAsis_2023@123"):
    #driver Initilaizing
    driver=driver
    time.sleep(3)
    #Login to Twitter
    driver.get("https://twitter.com/i/flow/login")
    time.sleep(3)
    username=driver.find_element(By.XPATH,"//input[@name='text']")
    username.send_keys(f"{uname}")
    next=driver.find_element(By.XPATH,"//span[contains(text(),'Next')]")
    next.click()
    time.sleep(2)
    passwrd=driver.find_element(By.XPATH,"//input[@name='password']")
    passwrd.send_keys(f"{pswd}")
    log_in=driver.find_element(By.XPATH,"//span[contains(text(),'Log in')]")
    log_in.click()
    return driver

def scrap_tweets(driver,url,no_scroll,time):
    drive = driver
    drive.get(url)
    ################################################## 
    ################## GET   SUCCES ##################
    ##################################################
    tweets = []
    userids=[]
    likes=[]
    retweets=[]
    replies=[]
    links=[]
    views=[]
    time.sleep(3) 
    # Start Scroll Tweets
    for i in range(no_scroll):
        ## scroll down 
        SCROLL_PAUSE_TIME = 2
        # Get scroll height
        drive.execute_script("window.scrollBy(0,2000)", "")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        tweet = driver.find_element(By.XPATH,".//div[@data-testid='tweetText']").text
        userid=driver.find_element(By.XPATH,"//div[@data-testid='User-Name']").text.split("\n")[1]
        group=driver.find_element(By.XPATH,".//div[@role='group']")
        try:
            like=group.text.split("\n")[2]
        except:
            like=0
        try:
            reply=group.text.split("\n")[0]
        except:
            reply=0
        try:
            retweet=group.text.split("\n")[1]
        except:
            retweet=0
        try:
            view=group.text.split("\n")[3]
        except:
            view=0
        # time=driver.find_element(By.XPATH,"//time']").get_attributes("datetime")
        link=group.find_element(By.TAG_NAME,"a").get_attribute("href").split("/")
        link.pop(-1)
        tweet=[word for word in tweet.split() if word]
        tweets.append(" ".join(tweet))
        links.append("/".join(link))
        userids.append(userid)
        replies.append(reply)
        retweets.append(retweet)
        likes.append(like)
        views.append(view)       
    return list(zip(userids,tweets,likes,replies,retweets,views,links))


#Making a Driver Object
def scrap(keyword):
    driver=initilaize_driver()
    #logging into it
    driver=login(driver)
    time.sleep(3)
    query=keyword
    driver.get("https://twitter.com/explore")
    time.sleep(1)
    search_1=driver.find_element(By.XPATH,"//input[@placeholder='Search']")
    search_1.send_keys(f"{query}")
    search_1.send_keys(Keys.ENTER)
    time.sleep(3)
    tweets_text=scrap_tweets(driver,driver.current_url,10,time)
    df=pd.DataFrame(tweets_text)
    df.columns="userids,tweets,likes,replies,retweets,views,links".split(",")
    df.drop_duplicates(inplace=True)
    return df