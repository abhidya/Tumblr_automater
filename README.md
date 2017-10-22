# Tumblr_automater
Uses Reddit to scrape top and trending posts and reposts them onto tumblrs

I made a bot that automates managing the Tumblrs in one convenient program. it can handle multiple accounts

# What it does?

it for every tumblr account info you add, you also add a subreddit. now what the bot will do is once every 24 hours it will check the subreddit u specified. and scrape the top 10 "HOT" posts and post them to ur tumblr. 


Currently only supporting Videos, Images, and Links to articles.


# Features:

Python (can run on a linux vps)
Multi account support (Uses Tumblr's API)
Low memory


# Requisites

import praw

from tumblpy import Tumblpy

import time

from random import randrange

from configparser import RawConfigParser

from threading import Thread

from robobrowser import RoboBrowser

import requests


So u gotta install "praw", "tumblpy", and i believe configparser, threading, time, and random come preinstalled. 



# Example of what it does, my tumblrs
http://staypositiveandstudy.tumblr.com/
http://mickisonthemoon.tumblr.com/
http://language-apfel.tumblr.com/
http://pillowtalkheaux.tumblr.com/
