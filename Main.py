#! python3
"""
    Script written to mine data from a twitter account.
    Takes a certain number of Tweets, counts the Hashtags and Mentions and
    makes a list of the most used words.

    Originally made to gather and parse Donald J. Trump's last 100 tweets.

    Written by Josef Ginerman as a homework/interview for Cellebrite.
"""

import re, time
from collections import Counter
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

    counter = Counter(words)
    return dict(counter.most_common(5))


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


def output_data(mention_list, hashtag_list, popular_words, file_name, to_file):
    mentions_and_tags = "There were %d mentions and %d hashtags" % (len(set(mention_list)), len(set(hashtag_list)))
    mention_string = "The mentions are: " + str(mention_list)
    hashtag_string = "The hashtags are: " + str(hashtag_list)
    popular_words_string = "The 5 most used words are:\n"
    popular_words_dict = (
    [(key, popular_words[key]) for key in sorted(popular_words, key=popular_words.get, reverse=True)])
    for word, freq in popular_words_dict:
        popular_words_string += "\t \"" + word + "\" used " + str(freq) + " times\n"

    print(mentions_and_tags)
    print(mention_string)
    print(hashtag_string)
    print(popular_words_string)

    if to_file:
        with open(file_name) as file:
            file.write(mentions_and_tags)
            file.write(mention_string)
            file.write(hashtag_string)
            file.write(popular_words)


def main():
    # set the url, the user and the file name.
    url = "https://twitter.com/"
    twitterUser = "realDonaldTrump"
    file_name = 'tweets_file.txt'
    to_file = False
    num_of_tweets = 100

    # create the lists to store the data
    hashtag_list = []
    mention_list = []

    # open Google Chrome on the given url and user
    driver = webdriver.Chrome()
    driver.get(url + twitterUser)
    assert 'Twitter' in driver.title  # check if Twitter opened

    tweets = get_tweets(driver, file_name, num_of_tweets)  # get the tweets from the feed

    parse_tweet(tweets, hashtag_list, mention_list)  # get the data from the tweets

    popular_words_dict = word_count(file_name)  # determine and save the most used words

    output_data(mention_list, hashtag_list, popular_words_dict, file_name, to_file)

    # close the window
    driver.close()


if __name__ == '__main__':
    main()
