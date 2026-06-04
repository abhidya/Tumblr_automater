# Tumblr_automater
Uses Reddit to scrape top and trending posts and reposts them onto tumblrs

## Archive status

This is an older social-media automation demo. It is preserved as a portfolio archive; Reddit/Tumblr APIs, auth flows, and platform automation policies may have changed.

## Credential hygiene and responsible use

Do not commit OAuth tokens, API keys, account credentials, cookies, or live account configuration. Run posting/follow automation only on accounts you control and in line with current platform terms and rate limits.

The current `main.py` is intentionally offline-first. It demonstrates how posts
would be classified from a local fixture and refuses live posting until the
project is rebuilt against current Reddit and Tumblr APIs.

## Offline demo

```bash
python3 main.py
```

Expected output includes three planned posts and `dry_run=true`.

I made a bot that automates managing the Tumblrs in one convenient program. it can handle multiple accounts

# What it does?

it for every tumblr account info you add, you also add a subreddit. now what the bot will do is once every 24 hours it will check the subreddit u specified. and scrape the top 10 "HOT" posts and post them to ur tumblr. 


Currently only supporting Videos, Images, and Links to articles.


# Features:

Python (can run on a linux vps)
Multi account support (Uses Tumblr's API)
Low memory


Found that following a ton of people 3 - 4 times increased the activity (likes and reblogs) on my blogs 
so i added a new update that will auto follow other people. 
Currently working on new features to remove double posts



# Historical requisites

import praw

from tumblpy import Tumblpy

import time

from random import randrange

from configparser import RawConfigParser

from threading import Thread

from robobrowser import RoboBrowser

import requests


The archived live implementation used `praw`, `tumblpy`, and `robobrowser`.
Those are not required for the current offline demo.



# Example of what it does, my tumblrs
http://staypositiveandstudy.tumblr.com/
http://mickisonthemoon.tumblr.com/
http://language-apfel.tumblr.com/
http://pillowtalkheaux.tumblr.com/
