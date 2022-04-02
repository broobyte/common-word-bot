import datetime
import config
import tweepy
import praw
import requests
from bs4 import BeautifulSoup

#---------------------------------------------------

# Date formatting for posts.

date = datetime.datetime.now()
formatted_date = date.strftime("%x") # Local format 04/01/2022.

results = [] # Common words gathered from all sites.

exclusions = ["the", "to", "of", "and", "&", "because", "in", "there", "there's", "for", "has", "that", "on", "with", "an", "say", "on", "i", "we", "know", "me", "who", "guardian", "uk", "us", "as", "a", "all", "–", "at", "us", "world", "exclusive", "it", "is", "stories", "from", "after", "over", "not", "how", "his", "was", "her", "he", "by", "be", "-", "says", "she", "ft", "will", "are", "into", "their", "have", "And", "its", "were", "—", "had", "said", "this", "when", "out", "you", "about", "About", "your", "up", "they", "been", "which", "while", "best", "the...", "here's", "or", "off", "before", "now", "want", "last", "also", "ukraine", "|"]

#---------------------------------------------------

def main(url, classID, ele):
    word_bank = [] # Storage for all non-excluded words.

    request = requests.get(url) # Fetch url.
    soup = BeautifulSoup(request.text, "html.parser")

    for child in soup.find_all(ele, class_ = classID, text=True):
        string = "".join(child.contents).strip() # Whitespace removed string of element inner text.
        list = string.split() # Separates the string into singular list items.

        for item in list:
            if item.lower() not in exclusions: # Exclusion check.
                word_bank.append(item)
    
    if word_bank:
        most_common = max(word_bank, key = word_bank.count).lower() # Common word from URL.
        print(most_common)
        results.append(most_common) # Add to list.
    else:
        print("Error in scraping: " + url)
        return

#---------------------------------------------------

def validate():
    word = max(set(results), key = results.count) # Common word from all words collected.
    print(f"{formatted_date}: {word}")
    confirm = input("Would you like to post this word to Twitter and Reddit?") # Double check validity.
    if confirm == "y":
        try:
            
            # Twitter Connection.

            client = tweepy.Client(consumer_key=config.API_KEY,
            consumer_secret=config.API_KEY_SECRET,
            access_token=config.ACCESS_TOKEN,
            access_token_secret=config.ACCESS_TOKEN_SECRET
            )

            client.create_tweet(text=f"{formatted_date}: {word}")

            #---------------------------------------------------

            # Reddit Connection.

            reddit = praw.Reddit(
            client_id = config.CLIENT_ID,
            client_secret = config.CLIENT_SECRET,
            username = config.USERNAME,
            password = config.PASSWORD,
            user_agent = config.USER_AGENT
            )

            reddit.subreddit("commonword").submit(f"{formatted_date}", f"{word}")

        except:
            print("Error caught in posting.")
        else:
            print("Successfully posted on both platforms.")
            print("----------")
            print("[[Reddit]] https://www.reddit.com/r/commonword")
            print("[[Twitter]] https://www.twitter.com/commonwordbot")
    else:
        print("NOT posting...")
        print("Exiting...")
        return

#---------------------------------------------------

main("https://www.theguardian.com/uk", "u-faux-block-link__overlay", "a")
main("https://www.theguardian.com/world", "u-faux-block-link__overlay", "a")
main("https://www.theguardian.com/us-news", "u-faux-block-link__overlay", "a")
main("https://www.theguardian.com/global-development", "u-faux-block-link__overlay", "a")
main("https://www.bbc.co.uk/news", "gs-c-promo-heading__title", "h3")
main("https://www.bbc.co.uk/news/uk", "gs-c-promo-heading__title", "h3")
main("https://www.bbc.co.uk/news/world", "gs-c-promo-heading__title", "h3")
main("https://www.dailymail.co.uk/home/index.html", "", "p")
main("https://www.dailymail.co.uk/ushome/index.html", "", "p")
main("https://www.dailymail.co.uk/sport/index.html", "", "p")
main("https://news.sky.com/uk", "sdc-site-tile__headline-text", "span")
main("https://news.sky.com/world", "sdc-site-tile__headline-text", "span")
main("https://news.sky.com/us", "sdc-site-tile__headline-text", "span")
main("https://www.thesun.co.uk/news/worldnews/", "rail__item-sub", "span")
main("https://uk.news.yahoo.com/", "Fw(600)", "span")
main("https://www.independent.co.uk/", "title", "a")
main("https://www.independent.co.uk/sport", "title", "a")
main("https://www.itv.com/news", "cp_heading _1J5yJ", "h3")
main("https://www.itv.com/news/world", "cp_heading _1J5yJ", "h3")
main("https://www.itv.com/news/topic/climate", "cp_heading _1J5yJ", "h3")
main("https://www.itv.com/news/politics", "cp_heading _1J5yJ", "h3")
main("https://www.mirror.co.uk/", "", "h2")
main("https://www.mirror.co.uk/news/", "", "h2")
main("https://www.mirror.co.uk/news/politics/", "", "h2")
main("https://www.mirror.co.uk/3am/", "", "h2")
main("https://www.thetimes.co.uk/", "u-showOnWide", "span")
main("https://www.huffingtonpost.co.uk/", "card__headline__text", "h3")
main("https://www.huffingtonpost.co.uk/", "card__description", "div")
main("https://www.huffingtonpost.co.uk/news/", "card__headline__text", "h3")
main("https://www.huffingtonpost.co.uk/news/", "card__description", "div")
main("https://www.huffingtonpost.co.uk/politics/", "card__headline__text", "h3")
main("https://www.huffingtonpost.co.uk/politics/", "card__description", "div")
main("https://www.ft.com/", "text", "span")
main("https://www.ft.com/world", "js-teaser-standfirst-link", "a")
main("https://www.ft.com/technology", "js-teaser-standfirst-link", "a")
main("https://www.ft.com/world/uk", "js-teaser-standfirst-link", "a")
main("https://www.ft.com/world/us", "js-teaser-standfirst-link", "a")
main("https://www.ft.com/markets", "js-teaser-standfirst-link", "a")
main("https://www.ft.com/companies", "js-teaser-standfirst-link", "a")

#---------------------------------------------------

validate()