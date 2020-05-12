#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from bs4 import BeautifulSoup
from bs4.element import Comment
import math

import urllib
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

def wordPassingTimeInURL(url, keyword):
    #url = raw_input('URL girin: ')
    html = text_from_html(urllib.urlopen(url).read())
    #pattern = raw_input('Kelime girin: ')
    return len(re.findall('\\b'+keyword+'\\b', html.lower()))

def takeUrls():
    inputUrl = ""
    urls = []
    while (inputUrl != "-1"):
        inputUrl = raw_input("URL giriniz(bitirmek icin -1 girin): ")
        urls.append(inputUrl)
    urls = urls[:-1]
    resultsForUrls(urls)


def resultsForUrls(urls, keywordsNonSplit):
    wordList = keywordsNonSplit.split()
    wordPassingTimes = []
    for i in range(len(urls)):
        words = []
        for j in range(len(wordList)):
            words.append(wordPassingTimeInURL(urls[i], wordList[j].lower()))
        wordPassingTimes.append(words)
    return calculateRelation(wordPassingTimes, urls, wordList)

def calculateRelation(wordPassingTimes, urls, wordList):
    relationshipPoints = []
    for i in range(len(wordPassingTimes)):
        _sum = 0
        for j in range(len(wordPassingTimes[i])):
            _sum = _sum + math.pow(float(wordPassingTimes[i][j])/sum(wordPassingTimes[i]),2)
        relationshipPoints.append([1-_sum])
    for i in range(len(relationshipPoints)):
        relationshipPoints[i].append(urls[i])
        for j in range(len(wordList)):
            relationshipPoints[i].append(wordList[j])
            relationshipPoints[i].append(wordPassingTimes[i][j])

    relationshipPoints = sorted(relationshipPoints, key=lambda point: point[0], reverse=True)
    return relationshipPoints
