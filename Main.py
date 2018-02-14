#! python3
"""
    Script written to mine data from a twitter account.
    Takes a certain number of Tweets, counts the Hashtags and Mentions and
    makes a list of the most used words.

    Originally made to gather and parse Donald J. Trump's last 100 tweets.

    Written by Josef Ginerman as a homework/interview for Cellebrite.
"""

import re, time, argparse
from collections import Counter
from getpass import getpass, getuser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def word_count(file_name):
    words = []
    with open(file_name) as file:
        line = file.readline()
        while line:
            line_words = re.split(" ", line)
            words += [word for word in line_words if len(word) > 5]
            line = file.readline()

    print("The list of words is: ", words)
    counter = Counter(words)
    return counter.most_common(5)


def parse_tweet(tweets, hashtag_list, mention_list):
    hashtag = re.compile(r'(#[A-Za-z]+[A-Za-z0-9]+)')
    mention = re.compile(r'(@[A-Za-z]+[A-Za-z0-9]+)')

    for tweet in tweets:
        tweet = tweet.text
        print(tweet + '\n')
        hashtag_list += hashtag.findall(tweet)
        mention_list += mention.findall(tweet)
    return tweets


def get_tweets(driver, file_name, num):
    file = open(file_name, 'w+')
    action = ActionChains(driver)
    action.send_keys(Keys.PAGE_DOWN * 15)
    tweets = []
    while len(tweets) < num:
        action.perform()
        time.sleep(0.2)
        tweets = driver.find_elements_by_class_name("TweetTextSize")
    for tweet in tweets[:num]:
        file.write(tweet.text + '\n')

    return tweets[:num]


def login(driver):
    username = driver.find_element_by_name("username")
    password = driver.find_element_by_name("password")

    username.send_keys(getuser())
    password.send_keys(getpass())

    ##TODO actually log in (ask for username and password

    driver.find_element_by_css_selector("button.submit.btn.primary-btn").click()


def output(console_output, file_output):
    pass


def main():
    parser = argparse.ArgumentParser(description='Provide data about Trump\'s tweets.')
    parser.add_argument('integer', metavar='N', type=int,
                        help='the number of tweets to mine for.',
                        default=100)
    parser.add_argument('--f', dest='file_output', action='store_true',
                        help='output to a file')
    parser.add_argument('--c', dest='console_output', action='store_true',
                        help='output to the console')
    parser.add_argument('--no-c', dest='console_output', action='store_false',
                        help='no output to the console')
    parser.set_defaults(console_output=True)
    parser.set_defaults(file_output=False)
    args = parser.parse_args()

    # open a chrome window and enter twitter
    url = "https://twitter.com/realDonaldTrump"
    file_name = 'tweets_file.txt'

    hashtag_list = []
    mention_list = []

    driver = webdriver.Chrome()
    driver.get(url)
    assert 'Twitter' in driver.title

    # login(driver)

    tweets = get_tweets(driver, file_name, 100)

    parse_tweet(tweets, hashtag_list, mention_list)

    popular_words_dict = word_count(file_name)
    
    output(console_output, file_output)

    print("There were %d mentions and %d hashtags" % (len(set(mention_list)), len(set(hashtag_list))))
    print(mention_list)
    print(hashtag_list)
    print(popular_words_dict)
    # close the window
    driver.close()


if __name__ == '__main__':
    main()
