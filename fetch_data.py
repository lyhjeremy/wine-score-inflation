"""
fetch_data.py - download the Wine Enthusiast review dataset (~130k reviews).

Source: the widely used "winemag-data-130k-v2" Kaggle dataset, here via a public
GitHub mirror. Columns include points (80-100), price, title (contains the vintage
year), variety, winery, and taster_name. Saved to ./data/ (git-ignored).
"""
import os
import urllib.request

URL = ("https://raw.githubusercontent.com/viannaandreBR/My-Data-Science-Journey/"
       "master/18-Kaggle/_DataSets/winemag-data-130k-v2.csv")
OUT = os.path.join(os.path.dirname(__file__), "data", "winemag-data-130k-v2.csv")


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    print(f"Downloading {URL}")
    urllib.request.urlretrieve(URL, OUT)
    print(f"Saved -> {OUT} ({os.path.getsize(OUT):,} bytes)")


if __name__ == "__main__":
    main()
