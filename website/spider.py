#!/usr/bin/env python

import requests
import re
import urlparse


def extract_links(url):
    response = requests.get(url)
    return re.findall('(?:href=")(.*?)"', response.content)


target_url = "https://zsecurity.org"
href_links = extract_links(target_url)
for link in href_links:
    link = urlparse.urljoin(target_url, link)

    if target_url in link:
        print(link)
