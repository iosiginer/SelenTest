import time, re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def parse_tweet(tweets, hashtagList, mentionList):
    file = open('DTtweets.txt', 'w')
    for tweet in tweets:
        print(tweet.text)
        file.write(tweet.text)
    return tweets


def get_tweets(driver, num):
    action = ActionChains(driver)
    action.send_keys(Keys.PAGE_DOWN * 10)
    tweets = []
    while len(tweets) < num:
        action.perform()
        time.sleep(0.2)
        tweets = driver.find_elements_by_class_name("TweetTextSize")
    return tweets[:num]


def main():
    # open a chrome window and enter twitter
    url = "https://twitter.com/realDonaldTrump"
    driver = webdriver.Chrome()
    driver.get(url)

    tweets = get_tweets(driver, 100)
    hashtagList = ()
    mentionList = ()
    print(len(tweets))
    parse_tweet(tweets, hashtagList, mentionList)

    # close the window
    driver.close()


if __name__ == '__main__':
    main()
