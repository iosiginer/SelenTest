#! python3
"""
    Script written to mine data from a twitter account.
    Takes a certain number of Tweets, counts the Hashtags and Mentions and
    makes a list of the most used words.

    Originally made to gather and parse Donald J. Trump's last 100 tweets.

    Written by Josef Ginerman.
"""

import re, time
from collections import Counter
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def find_most_used_words(tweets):
    words = []
    # loop through the tweets and add the words to a list ( for the counting ).
    for line in tweets:
        line_words = re.split(" ", line.text)
        words += [word for word in line_words if len(word) > 5]

    # use the Counter to quickly find the most common words and their frequency.
    counter = Counter(words)
    return dict(counter.most_common(5))


def find_special_items_in_tweet(tweets, hashtag_list, mention_list):  # finds hastags and mentions in the tweets
    hashtag = re.compile(r'(#[A-Za-z]+[A-Za-z0-9]+)')
    mention = re.compile(r'(@[A-Za-z]+[A-Za-z0-9]+)')

    # loop one time though all the tweet's text, to find mentions and hash-tags.
    for tweet in tweets:
        tweet = tweet.text
        hashtag_list += hashtag.findall(tweet)
        mention_list += mention.findall(tweet)
    return tweets


def get_tweets_from_server(driver, num_of_tweets):
    action = ActionChains(driver)
    action.send_keys(Keys.PAGE_DOWN * 15)  # scroll down to find the desired ammount of tweets.
    action.perform()
    tweets = []
    while len(tweets) < num_of_tweets:
        action.perform()
        time.sleep(0.2)  # wait for the page to fully load.
        tweets = driver.find_elements_by_class_name("TweetTextSize")  # find the tweets by their class name.

    return tweets[:num_of_tweets]  # return only num ammout of tweets.


def output_data(mention_list, hashtag_list, popular_words, file_name, to_file):
    # create the strings
    mentions_and_tags = "There were %d mentions and %d hashtags" % (len(set(mention_list)), len(set(hashtag_list)))
    mention_string = "\nThe mentions are: "
    hashtag_string = "\nThe hashtags are: "
    popular_words_string = "\nThe 5 most used words are:"

    for mention in set(mention_list):
        mention_string += "\n\t" + mention

    for hash in set(hashtag_list):
        hashtag_string += "\n\t" + hash

    # sort the most popular words before outputting.
    popular_words_dict = (
        [(key, popular_words[key]) for key in sorted(popular_words, key=popular_words.get, reverse=True)])
    # form a string out of the most popular words
    for word, freq in popular_words_dict:
        popular_words_string += "\n\t \"" + word + "\" used " + str(freq) + " times"

    # print the data to the console
    print(mentions_and_tags)
    print(mention_string)
    print(hashtag_string)
    print(popular_words_string)

    # write the data to a file (if the boolean is true).
    if to_file:
        file = open(file_name, "w")
        file.write(mentions_and_tags)
        file.write(mention_string)
        file.write(hashtag_string)
        file.write(popular_words_string)


def main():
    # set the url, the user and the file name.
    url = "https://twitter.com/"
    twitter_user = "realDonaldTrump"
    file_name = 'tweets_file.txt'
    to_file = True
    num_of_tweets = 100

    # create the lists to store the data
    hashtag_list = []
    mention_list = []

    # open Google Chrome on the given url and user
    driver = webdriver.Chrome()
    driver.get(url + twitter_user)
    assert 'Twitter' in driver.title  # check if Twitter opened

    tweets = get_tweets_from_server(driver, num_of_tweets)  # get the tweets from the feed

    find_special_items_in_tweet(tweets, hashtag_list, mention_list)  # get the data from the tweets

    popular_words_dict = find_most_used_words(tweets)  # determine and save the most used words

    output_data(mention_list, hashtag_list, popular_words_dict, file_name, to_file)

    # close the window
    driver.close()


if __name__ == '__main__':
    main()
