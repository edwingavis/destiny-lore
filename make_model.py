#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 14:44:26 2020

@author: jg
"""

import markovify
import os

corpus = ""
files = os.listdir("corpus")
for fname in files:
    with open("corpus/" + fname) as f:
        corpus += f.read()#.replace("\n"," ")

text_model = markovify.NewlineText(corpus)
with open("model.json", "w") as f:
    f.write(text_model.to_json())
