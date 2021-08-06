#!/bin/env python3
import audible
import pathlib
import audible
import httpx
import requests
import audible
from bs4 import BeautifulSoup
from urllib.parse import urlsplit, parse_qs

auth = audible.Authenticator.from_login(
    "<USERNAME>",
    "<Password>",
    locale="<LOCATOION>", ## amazon.de == "de", amazon.com == us, ...
    with_username=False,
    register=True)

auth.to_file("login", encryption=False)
