from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def material_scrapping_selenium(link):
    """
    potentail problem when using selenium:
        1. The web element was not present as it could not load due to the runtime issues.
        2. The usage of AJAX techniques in the web applications has introduced uncertainty 
            in the sense that loading of the web page and the web elements present in it may 
            happen at a different time span. 
        3. Many times, due to peak traffic or network latency, our application may behave 
            differently than it does at normal, optimal conditions.
    """
    # to avoid getting "DeprecationWarning: executable_path has been deprecated, please pass in a Service object"
    # s = Service("/Users/Claude/Desktop/GraduateStudy/Fall21/DSCI591/web_scrapping/chromedriver")
    driver = webdriver.Chrome("/Users/Claude/Desktop/GraduateStudy/Fall21/DSCI591/web_scrapping/chromedriver")
    driver.get(link)
    # Elements on the web application may not be recognized by the selenium if the browser is not maximized and thereby making framework fail.
    driver.maximize_window()
    # use CLASS_NAME strategy to find the all the locator
    paragraphs = driver.find_elements(By.CLASS_NAME, "structured-component-text-block-paragraph")

    paragraphs_lst = []
    for i in range(len(paragraphs)):
        try:
            # print("------------------------")
            # print(paragraphs[i])
            # print(paragraphs[i].get_attribute("textContent"))
            paragraphs_lst.append(paragraphs[i].get_attribute("textContent"))
        except:
            continue

    driver.close()

    return paragraphs_lst


def scrapping_pipeline(gender):
    
    # avoid getting banned from website, used common headers from this website: https://developers.whatismybrowser.com/useragents/explore/software_type_specific/web-browser/1  
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko)"
    }
    # links to each product product
    productLinks = []

    if gender == "men":
        # iterate through each page, as of 10/18/21, there are 10 pages for men's T-shirt on Zara
        for i in range(1, 11):
            # request website content and parse with beautifulsoup
            r = requests.get(f"https://www.zara.com/us/en/man-tshirts-l855.html?v1=1886142&page={i}", headers = headers)
            soup = BeautifulSoup(r.content, 'lxml')
            # find all the products in the current page
            products = soup.find("ul", class_ = "product-grid__product-list").find_all("li", class_ = "product-grid-product")
            for product in products:
                try:
                    link = product.find("a", href = True)["href"]  
                    productLinks.append(link)
                except:
                    continue

    elif gender == "women":
        # iterate through each page, as of 10/18/21, there are 22 pages for women's T-shirt on Zara
        for i in range(1, 23):
            # request website content and parse with beautifulsoup
            r = requests.get(f"https://www.zara.com/us/en/woman-tshirts-l1362.html?v1=1882929&page={i}", headers = headers)
            soup = BeautifulSoup(r.content, 'lxml')
            # find all the products in the current page
            products = soup.find("ul", class_ = "product-grid__product-list").find_all("li", class_ = "product-grid-product")
            for product in products:
                try:
                    link = product.find("a", href = True)["href"]  
                    productLinks.append(link)
                except:
                    continue

    # observed that there are lots of duplicates in product links, some product is listed for multiple times
    productLinks = list(set(productLinks))
    Tshirt_lst = []
    # visit each product page and scrapping information
    for link in productLinks:

        # NOTE: materails is a list of text, the real T-shirt composition is inside the text, need to process text to extract text
        materials = material_scrapping_selenium(link)

        r = requests.get(link, headers = headers)
        soup = BeautifulSoup(r.content, "lxml")

        Tshirt = {}
        Tshirt["link"] = link
        Tshirt["composition"] = materials
        try:
            Tshirt["imageUrl"] = soup.find_all("li", class_ = "product-detail-images__image-wrapper")[0].find("picture", class_ = "media-image").find("source", srcset = True)["srcset"].split(" ")[0]
        except:
            Tshirt["imageUrl"] = "unknown"
        try:
            Tshirt["title"] = soup.find("h1", class_ = "product-detail-info__name").text.strip()
        except:
            continue
        try:
            Tshirt["description"] = soup.find("div", class_ = "expandable-text__inner-content").text.strip()
        except:
            Tshirt["description"] = "unknown"
        try:
            Tshirt["price"] = soup.find("span", class_ = "price__amount-current").text.strip()
        except:
            Tshirt["price"] = "unknown"
        try:
            try:
                Tshirt["color"] = soup.find("p", class_ = "product-detail-selected-color product-detail-info__color").text.strip()
            except:
                Tshirt["color"] = soup.find("p", class_ = "product-detail-selected-color product-detail-color-selector__selected-color-name").text.strip()
        except:
            Tshirt["color"] = "unknown"
        Tshirt["sustainability"] = soup.find("div", class_ = "product-detail-extra-detail") # need help

        Tshirt_lst.append(Tshirt)
        print("Saving:", Tshirt["title"])

    df = pd.DataFrame(Tshirt_lst)
    print(df.head(15))
    print("-*"*70)
    print()

    return df


if __name__ == "__main__":

    start_time = datetime.now()
    # getting men's and women's dataframe and also add gender column to each 
    print("\tCollecting Zara Men's Tshirt info...")
    men_df = scrapping_pipeline("men")
    men_df["gender"] = "men"

    print("\tCollecting Zara Women's Tshirt info...")
    women_df = scrapping_pipeline("women")
    women_df["gender"] = "women"

    end_time = datetime.now()
    print(f"Duration: {end_time - start_time}")

    # combine two dataframe and save it in the local folder
    df = pd.concat([men_df, women_df], ignore_index = True)
    df.to_csv("./zara_tshirt.csv")







