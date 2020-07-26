#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup


def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass


target_url = "10.0.2.5/mutillidae/index.php?page=dns-lookup.php"
response = request(target_url)

parsed_html = BeautifulSoup(response.content, features="lxml")
forms_list = parsed_html.findAll("form")

for form in forms_list:
    action = form.get("action")
    method = form.get("method")
    inputs_list = form.findAll("input")
    for input in inputs_list:
        input_name = input.get("name")
        print input_name
    print action
    print method
