#!/usr/bin/env python

import requests


def download(url):
    get_response = requests.get(url=url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


download("https://unsplash.com/photos/00SzLJ6yQOk/download?force=true&w=640")
