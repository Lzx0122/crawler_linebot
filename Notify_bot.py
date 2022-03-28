
import requests as req
from bs4 import BeautifulSoup


def notifybot():
    headers = {
        "Authorization": "Bearer " + "r4J0BaYHj4yruCRVdO490gxrrUhkjaYQQegqKwi2cBP",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    params = {"message": "測試"}
    r = req.post("https://notify-api.line.me/api/notify",
                 headers=headers, params=params)


notifybot()
