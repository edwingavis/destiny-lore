# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
import os
import time
import progressbar
import random
import re

COLLECT = False 
USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0'

def main():
    if COLLECT:
        collect_urls()
    else:
        #make_files("scraped")
        make_corpus("corpus")
    
def make_files(folder):   
    for url in url_gen("https://www.ishtar-collective.net"):
        text = scrape(url)
        path = build_path(url, folder)
        write_to_file(text, path)
        print("Scraped: " + url)
        time.sleep(random.random() * 10)

def build_path(url, folder):
    path = os.getcwd()
    url = url.replace("/", "_")
    path += "/" + folder + "/" + url + ".txt"
    return path

def url_gen(base_url):
    with open("links.txt") as f:
        for url in f.readlines():
            yield base_url + url.strip()

def scrape(url):
    headers = {'User-Agent': USER_AGENT}
    r = requests.get(url, headers=headers)
    return r.text

def write_to_file(text, file):
    with open(file, "w") as f:
        f.write(text)
        
def collect_urls():
    final=53
    base_url = "https://www.ishtar-collective.net/entries/"
    for i in progressbar.progressbar(range(1,final+1)):
        url = base_url
        if i > 1:
            url += "/page/" + str(i) 
        page_text = scrape(url)
        path = build_path(url, "entries")
        write_to_file(page_text, path)
        time.sleep(random.random() * 10)

def pull_entry_links():
    with open("links.txt", "w") as f1:
        entries_re = re.compile('"/entries/[\w-]+"')
        for fname in os.listdir("entries"):
            with open("entries/" + fname) as f2:
                text = f2.read()
                for match in entries_re.finditer(text):
                    url = match[0].strip('"')
                    f1.write(url + "\n")
 
def make_corpus(folder):
    for title,desc in get_texts("scraped"):
        with open(folder + "/" + title + ".txt", "w") as f:
            f.write(desc)
    
def get_texts(folder):
    '''
    generator
    '''
    files = os.listdir(folder)
    for fname in files:
        with open(folder + "/" + fname) as f:
            html = f.read()
        desc = pull_desc(html)
        title = pull_title(html)
        yield title,desc

def pull_title(html):
    start = html.index("<title>")
    end = html.index("</title>")
    title = html[start:end]
    title_start = title.index(">")
    title_end = title.index("—")
    title = title[title_start+1:title_end-1]
    title = title.replace("/","_").replace(" ","_")
    return title
    
def pull_desc(html):
    start = html.index("<p>")
    end = html.index("</div>", start)
    desc = html[start:end]
    desc = desc.replace("<p>","\n").replace("</p>", "")
    desc = desc.replace("<br />", " ")
    return desc

if __name__=="__main__":
    main()