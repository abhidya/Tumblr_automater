__author__ = 'Abdulrehman_Bhidya'
import praw
from tumblpy import Tumblpy
import time
from random import randrange
from configparser import RawConfigParser
from threading import Thread
from robobrowser import RoboBrowser
import requests

requests.packages.urllib3.disable_warnings()


class Reddit2Tumblr():
    def __init__(self, consumer_key, consumer_secret, oauth_token, oauth_secret, subreddit, site_link, ):
        self.client = Tumblpy(
            consumer_key,
            consumer_secret,
            oauth_token,
            oauth_secret
        )
        self.blog_url = self.client.post('user/info')
        self.blog_url = self.blog_url['user']['blogs'][0]['url']
        self.agent = 'PyEng version: ' + str(randrange(1, 200, 1))
        self.r = praw.Reddit(user_agent=self.agent)
        self.subreddit = self.r.get_subreddit(subreddit)
        self.site_link = site_link

    def watch(self, count):
        for submission in self.subreddit.get_hot(limit=10):
            try:
                # print(submission.title)
                # print(submission.url)
                # print(submission.selftext)
                if "This Sub" or "Text" not in submission.title:

                    if "Article" in submission.title:
                        print("Article")
                        print("Title Article: ", submission.title.replace("[Article]", "", 1))
                        print("Url: ", submission.url)
                        text = submission.title.replace("[Article]", "", 1) + ' ' + self.site_link
                        print("Text: ", text)
                        post = self.client.post('post', blog_url=self.blog_url,
                                                params={'type': 'link', 'caption': text, 'source': submission.url})
                        print(post)

                    if ("youtube" not in submission.url) and ('youtu.be' not in submission.url):
                        if ("jpg" or "png" or "gif" or "jpeg") and ('reddit.com' or "redd.it") not in submission.url:
                            if "imgur" not in submission.url:
                                print("Article")
                                print("Title Article: ", submission.title.replace("[Article]", "", 1))
                                print("Url: ", submission.url)
                                text = submission.title.replace("[Article]", "", 1) + ' ' + self.site_link
                                print("Text: ", text)
                                post = self.client.post('post', blog_url=self.blog_url,
                                                        params={'type': 'link', 'caption': text,
                                                                'source': submission.url})
                                print(post)
                        else:
                            pass

                    if ("Video" in submission.title) or ("youtube" in submission.url) or ('youtu.be' in submission.url):
                        print("Video")
                        print("Title Article: ", submission.title.replace("[Video]", "", 1))
                        print("Url: ", submission.url)
                        print("Text: ", submission.selftext)
                        text = submission.title.replace("[Video]", "", 1) + ' ' + self.site_link
                        print("Text: ", text)
                        post = self.client.post('post', blog_url=self.blog_url,
                                                params={'type': 'video', 'caption': text, 'embed': submission.url})
                        print(post)

                    if ("jpg" or "png" or "gif" or "jpeg") in submission.url:
                        print("Image")
                        print("Title: ", submission.title.replace("[Image]", "", 1))
                        print("Image Url: ", submission.url)
                        text = submission.title.replace("[Image]", "", 1) + ' ' + self.site_link
                        print("Text: ", text)
                        post = self.client.post('post', blog_url=self.blog_url,
                                                params={'type': 'photo', 'caption': text, 'source': submission.url})
                        print(post)
            except:
                pass
        else:
            pass

    def follower(self, count):
        tc = requests.session()
        tc.verify = False
        tbrowser = RoboBrowser(session=tc)
        tbrowser.open('https://www.tumblr.com/tagged/trending-topics')
        links = tbrowser.find_all("a", {"class": "post_info_link"})
        for link in links:
            try:
                self.client.post('user/follow', params={'url': link['href']})
                print("following " + link['href'] + "On account: " + self.blog_url)
            except:
                print("boo")


def bot(account, count):
    bot = Reddit2Tumblr(
        consumer_key=account['consumer_key'],
        consumer_secret=account['consumer_secret'],
        oauth_token=account['oauth_token'],
        oauth_secret=account['oauth_secret'],
        subreddit=account['subreddit'],
        site_link=account['site_link'],

    )

    while True:
        bot.watch(count)
        bot.follower(count)
        print('Taking a break for 24 Hours')
        time.sleep(86400)


if __name__ == "__main__":
    config = RawConfigParser(allow_no_value=True)
    config.read('accounts.ini')
    count = 0
    for account in config.sections():
        user = {i: config[account][i] for i in config[account]}
        Thread(target=bot, args=(user, count)).start()
        count += 1
