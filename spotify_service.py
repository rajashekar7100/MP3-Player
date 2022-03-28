#!/usr/bin/env python3

import requests

url = "https://spotify-charts.p.rapidapi.com/dominican-republic-top-200"

headers = {
    'x-rapidapi-host': "spotify-charts.p.rapidapi.com",
    'x-rapidapi-key': "98d6066658msh44d1bdfca73af37p1f2dccjsna6b0f4115df6"
    }

response = requests.request("GET", url, headers=headers)

print(response.text)
