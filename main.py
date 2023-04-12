from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

# EXTRACTION OF APP NAME
def get_appname(soup):
    try:
        # APP NAME
        name = soup.find("h1", attrs={'class': 'Fd93Bb F5UCq p5VxAd'}).find('span', recursive=False).get_text(strip=True)
    except AttributeError:
        name = "N/A"

    return name

# EXTRACTION OF APP MAKER NAME
def get_appmaker(soup):
    try:
        # APP MAKER NAME
        maker = soup.find("div", attrs={'class': 'Vbfug auoIOc'}).find('span').get_text(strip=True)
    except AttributeError:
        maker = "N/A"

    return maker

# EXTRACTION OF APP DOWNLOAD COUNT
def get_appdownloadcount(soup):
    try:
        # APP DOWNLOAD COUNT
        dcount = soup.find_all('div', attrs={'class': 'wVqUob'})
        for div in dcount:
            if "Downloads" in div.find('div', attrs={'class': 'g1rdde'}):
                dcount = div.find("div", attrs={'class': 'ClM7O'}).get_text(strip=True)
    except AttributeError:
        dcount = "N/A"

    return dcount

# EXTRACTION OF APP RATING
def get_apprating(soup):
    try:
        # APP RATING
        rating = soup.find('div', attrs={'class':'TT9eCd'}).get_text(strip=True)
    except AttributeError:
        rating = "N/A"

    return rating

# EXTRACTION OF APP REVIEW COUNT
def get_appreviewcount(soup):
    try:
        # APP REVIEW COUNT
        rcount = soup.find_all("div", attrs={'class': 'g1rdde'})[0].get_text(strip=True)
        if 'reviews' not in rcount:
            rcount = "N/A"
    except AttributeError:
        rcount = "N/A"

    return rcount

# EXTRACTION OF APP MAKER EMAIL (IF AVAILABLE)
def get_appemail(soup):
    try:
        # APP MAKER EMAIL
        email = soup.find("div", attrs={'jscontroller': 'lpwuxb'}).find('div', attrs={'class': 'bARER'}).get_text(strip=True)
        email = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", email)
        if len(email) == 0:
            email = "N/A"
        email = "".join(email)
    except AttributeError:
        email = "N/A"

    return email

# CREATION OF DATAFRAME
def app_infodataframe(d, soup):
    d["Name"].append(get_appname(soup))
    d["Maker"].append(get_appmaker(soup))
    d['Download Count'].append(get_appdownloadcount(soup))
    d['Rating'].append(get_apprating(soup))
    d['Review Count'].append(get_appreviewcount(soup))
    d['Email'].append(get_appemail(soup))

    return d

if __name__ == '__main__':
    HEADERS = ({'User-Agent':'', 'Accept-Language': 'en-US, en;q=0.5'})

    # GIVEN URL
    URL = "https://play.google.com/store/apps/details?id=com.galvanizetestprep.vocabbuilder"

    # HTTP REQUEST
    webpage = requests.get(URL, headers=HEADERS)

    # SOUP WITH HTML METADATA
    soup = BeautifulSoup(webpage.content, "html.parser")

    # LINKS OF AVAILABLE SIMILAR APPS
    links = soup.find_all('section', attrs={'class':'HcyOxe'})[6].find_all('a', attrs={'class': 'Si6A0c nT2RTe'})
    
    # STORING LINKS IN LIST
    links_list = []

    # EXTRACTION OF LINKS
    for link in links:
        links_list.append(link.get('href'))

    # DICTIONARY FOR STORING IN CSV
    d = {"Name": [], "Maker": [], "Download Count": [], "Rating": [], "Review Count": [], "Email": []}
    
    # FUNCTION CALLING FOR MAIN APP URL
    app_infodataframe(d, soup)

    # EXTRACTION OF APP INFORMATION
    for link in links_list:
        new_webpage = requests.get('https://play.google.com' + link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, 'html.parser')

        # FUNCTION CALLING FOR SIMILAR APPS
        app_infodataframe(d, new_soup)    

    # CONVERSION OF DICTIONARY TO CSV
    dataframe = pd.DataFrame(d)
    dataframe.to_csv("Data.csv", index=False)