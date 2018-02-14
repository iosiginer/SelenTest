import time, re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def parse_tweet(tweets, hashtag_list, mention_list):
    hashtag = re.compile(r'(#[A-Za-z]+[A-Za-z0-9]+)')
    mention = re.compile(r'(@[A-Za-z]+[A-Za-z0-9]+)')

    for tweet in tweets:
        text = tweet.text
        print(text + '\n')
        tags = hashtag.findall(text)
        mentions = mention.findall(text)
        hashtag_list += tags
        mention_list += mentions

    print("There were <%d> mentions and <%d> hashtags" % (len(mention_list), len(hashtag_list)))
    print(mention_list)
    print(hashtag_list)
    return tweets


def get_tweets(driver, file, num):
    action = ActionChains(driver)
    action.send_keys(Keys.PAGE_DOWN * 10)
    tweets = []
    while len(tweets) < num:
        action.perform()
        time.sleep(0.2)
        tweets = driver.find_elements_by_class_name("TweetTextSize")
    for tweet in tweets[:num]:
        file.write(tweet.text + '\n')

    return tweets[:num]


def main():
    # open a chrome window and enter twitter
    url = "https://twitter.com/realDonaldTrump"
    file = open('tweets_file.txt', 'w+')
    hashtag_list = []
    mention_list = []

    driver = webdriver.Chrome()
    driver.get(url)

    tweets = get_tweets(driver, file, 10)

    parse_tweet(tweets, hashtag_list, mention_list)

    # close the window
    driver.close()


if __name__ == '__main__':
    main()
