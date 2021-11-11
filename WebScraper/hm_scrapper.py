"""
Data to scrape from H&M:
Tshirt = {
    "name" : name,
    "price" : price,   
    "description" : description,
    "length": length,
    "sleeve_length": sleeve_length,
    "fit" : fit,
    "neckline": neckline,
    "composition" : composition,
    "color": color,     
    "imported": imported,           
    "article_number" : article_number,
    "sustainability": sustainability,
    "supplier": supplier,    #NOTE: This one has trouble
    "reviews": reviews,    #NOTE: This one has trouble
    "rating": rating    #NOTE: This one has trouble
}
Total products for Men/T-shirts: 235
Total products for Women/T-shirts: 161
Total: 397
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime

def scrapping_pipeline(url):
    
    baseurl = "https://www2.hm.com"
    # avoid getting banned from website, used common headers from this website: https://developers.whatismybrowser.com/useragents/explore/software_type_specific/web-browser/1 
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko)"
    }
    # request website content and parse with beautifulsoup
    r = requests.get(url, headers = headers)
    soup = BeautifulSoup(r.content, 'lxml')

    #this variable will hold links to each product
    productLinks = []  
    imageUrls = [] 
    # find all the product links and store them in productLinks
    for product in soup.find_all('li', class_ = 'product-item'):
        link = product.find('a', href = True)
        productLinks.append(baseurl+link['href'])
        imageUrls.append(product.select('.item-image')[0]['data-altimage'])

    Tshirt_lst = []
    # visit each product page and scrapping information
    for idx, link in enumerate(productLinks):
        r = requests.get(link, headers = headers)
        soup = BeautifulSoup(r.content, 'lxml')

        Tshirt = {}
        Tshirt["title"] = soup.find('h1', class_ = "primary product-item-headline").text.strip()
        Tshirt["link"] = link
        Tshirt["supplier"] = soup.find_all("ul", class_ = "ProductBackground-module--sustainabilityList__9jGol")   # couldn't scrape       
        Tshirt["rating"] = soup.find('div', class_ = "star-average-number js-stars-number")   # couldn't scrape        
        Tshirt["reviews"] = soup.find("div", class_ = "sticky-footer pdp-details").find("button", \
                                            class_ = "label-copy js-open-reviews").text.strip() # return a reviewsLabel object
        Tshirt["price"] = soup.find('div', class_ = "inner").find("section", class_ = "name-price").find('span', class_ = "price-value").text.strip() 
        Tshirt["imageUrl"] = imageUrls[idx]
        try:
            Tshirt["description"] = soup.find("p", class_= "pdp-description-text").text.strip()
        except:
            Tshirt["description"] = 'unknown'

        attributes_lst = soup.find_all('div', class_ = "details-attributes-list-item")
        for attribute in attributes_lst:
            attribute_content = attribute.find('dd', class_ = 'details-list-item').text.strip()
            attribute_headline = attribute.find('dt', class_ = "details-headline").text.strip()    

            if attribute_headline == "messages.garmentLength":
                Tshirt["length"] = attribute_content
                continue
            elif attribute_headline == "messages.sleeveLength":
                Tshirt["sleeve_length"] = attribute_content
                continue
            elif attribute_headline == "Fit":
                Tshirt["fit"] = attribute_content
                continue
            elif attribute_headline == "messages.neckLineStyle":
                Tshirt["neckline"] = attribute_content
                continue
            elif attribute_headline == "Composition":
                Tshirt["composition"] = attribute_content
                continue
            elif attribute_headline == "Description":
                Tshirt["color"] = attribute_content
                continue
            elif attribute_headline == "Imported":
                Tshirt["imported"] = attribute_content
                continue
            elif attribute_headline == "Nice to know":
                Tshirt["sustainability"] = attribute_content
                continue
            elif attribute_headline == "Art. No.":
                Tshirt["article_number"] = attribute_content
                
        Tshirt_lst.append(Tshirt)
        print("Saving:", Tshirt["title"])

    df = pd.DataFrame(Tshirt_lst)
    print(df.head(15))
    print("-*"*70)
    print()

    return df


if __name__ == "__main__":

    # scrapping men's and women's T-shirt seperately, each link contains all the products, so no need to loop through pages
    menTshirtUrl = "https://www2.hm.com/en_us/men/products/t-shirts-tank-tops/short-sleeves.html?sort=stock&image-size=small&image=model&offset=0&page-size=235"
    womenTshirtUrl = "https://www2.hm.com/en_us/women/products/tops/t-shirts.html?sort=stock&image-size=small&image=model&offset=0&page-size=161"
    
    start_time = datetime.now()
    # getting men's and women's dataframe and also add gender column to each 
    print("\tCollecting H&M Men's Tshirt info...")
    men_df = scrapping_pipeline(menTshirtUrl)
    men_df["gender"] = "men"

    print("\tCollecting H&M Women's Tshirt info...")
    women_df = scrapping_pipeline(womenTshirtUrl)
    women_df["gender"] = "women"

    end_time = datetime.now()
    print(f"Duration: {end_time - start_time}")

    # combine two dataframe and save it in the local folder
    df = pd.concat([men_df, women_df], ignore_index = True)
    df.to_csv("./h&m_tshirt.csv")
