#!/bin/env python3
import os
import pathlib
import audible
import httpx
import requests
import audible
import re
from bs4 import BeautifulSoup
from urllib.parse import urlsplit, parse_qs

#Functions
# get download link(s) for book
def _get_download_link(auth, asin, codec="LC_128_44100_stereo"):
    # need at least v0.4.0dev
    if auth.adp_token is None:
        raise Exception("No adp token present. Can't get download link.")

    try:
        content_url = ("https://cde-ta-g7g.amazon.com/FionaCDEServiceEngine/"
                       "FSDownloadContent")
        params = {
            'type': 'AUDI',
            'currentTransportMethod': 'WIFI',
            'key': asin,
            'codec': codec
        }
        r = httpx.get(
            url=content_url,
            params=params,
            allow_redirects=False,
            auth=auth
        )

        # prepare link
        # see https://github.com/mkb79/Audible/issues/3#issuecomment-518099852
        link = r.headers['Location']
        tld = auth.locale.domain
        new_link = link.replace("cds.audible.com", f"cds.audible.{tld}")
        return new_link
    except Exception as e:
        print(f"Error: {e}")
        return

def download_file(url):
    r = httpx.get(url)

    try:
        title = r.headers["Content-Disposition"].split("filename=")[1]
        filename = pathlib.Path.cwd() / "audiobooks" / title

        with open(filename, 'wb') as f:
            for chunk in r.iter_bytes():
                f.write(chunk)
        print(f"File downloaded in {r.elapsed}")
        return filename
    except KeyError:
        return "Nothing downloaded"

def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]
#Start-----------------------------------------
auth =  audible.Authenticator.from_file("login")
#Sync Books to Log file
from pathlib import Path
oldlog_file = Path('log.txt').read_text()
oldlog_file = open("log.txt","r")
oldlog = oldlog_file.read()
oldlog_file.close()
log= list()
dif = list()
isAAX=False
#Get book list
with audible.Client(auth=auth) as client:
    library = client.get(
        "1.0/library",
        num_results=100,
        response_groups="product_desc, product_attrs",
        sort_by="-PurchaseDate"
    )
    for book in library["items"]:
        log.append(book.get("asin","ERROR"))
#filter downloaded
    for bok in log:
        if bok not in oldlog:
            dif.append(bok)
#Download Section
#TODO add diff checker
    for asin in dif:
        dl_link = _get_download_link(auth, asin)

        if dl_link:
            r=requests.get(dl_link, allow_redirects=True)
            filename = get_filename_from_cd(r.headers.get('content-disposition'))
            open("cache/"+filename, 'wb').write(r.content)

            isAAX=True

#save to file
with open("log.txt","w") as file:
    for byte in log:
        file.write(byte)
        file.write('\n')
file.close()

if isAAX==True:
    os._exit(1)
