import requests
from bs4 import BeautifulSoup
import json
import regex as re

headers = {
    "Referer": "https://www.amazon.com/",
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}

ASINS = ['B07FKX52DJ']

json_data = {}

for ASIN in ASINS:
    
    url = 'https://www.amazon.com/dp/{0}'.format(ASIN)

    # sin = re.findall(r"[A-Z0-9]{10}", url)[0]
    
    r = requests.get(url,  headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    print(r.status_code)
    


    # title
    try:
        title = soup.find('span', id='productTitle').text.strip() 
        price = soup.find('span', class_='a-offscreen').text.strip()
    except:
        # if fails to then try to grab from search
        try:
            url2 = 'https://www.amazon.com/s?k={0}'.format(ASIN)
            res = requests.get(url2,  headers=headers)
            soup2  =BeautifulSoup(res.text, 'html.parser')
            product = soup2.select('div[data-asin]')[1]
            try:
                    price = product.find('span', class_="a-offscreen").text
                    print(price)
            except:
                    price = 'N/A'
            try:    
                title = product.find('h2', class_='a-size-mini a-spacing-none a-color-base s-line-clamp-4').text
                print(title)
            except:
                title = 'N/A'
        except:
            pass


    if price[:5] == "Page ":
        price = "Currently unavailable"

        
    
    json_data["title"] = title
    json_data["price"] = price

    


        # size
    try:
        varioationSizesElem = soup.find('div', id='variation_size_name')
        varioationSizes = BeautifulSoup(str(varioationSizesElem), 'html.parser')
        sizes = varioationSizes.find_all('option')
        json_data["sizes"] = []
        for size in sizes[1:]:
            json_data["sizes"].append(size.text.strip())
    except:
        pass



        # Color
    try:
        varioationColorElem = soup.find('div', id='variation_color_name')
        varioationColors = BeautifulSoup(str(varioationColorElem), 'html.parser')
        colors = varioationColors.find_all('li')
        json_data["colors"] = []
        for color in colors:
            var = color['title']
            var = var.split(' ')
            json_data["colors"].append(var[-1])
    except:
        pass


        # Size
    try:
        varioationSizesElem = soup.find('div', id='variation_size_name')
        varioationSizes = BeautifulSoup(str(varioationSizesElem), 'html.parser')
        sizes = varioationSizes.find_all('li')
        for size in sizes:
           json_data["sizes"].append(size.text.strip())
    except:
        pass

        # Style
    try:
        variationStyles = soup.find('div', id='variation_style_name')
        varioationStyles = BeautifulSoup(str(variationStyles), 'html.parser')
        styles = varioationStyles.find_all('li')
        json_data["styles"] = []
        for style in styles:
           json_data["styles"].append(style.text.strip())
    except:
        pass


    # Configaration
    try:
        variationConfigurations = soup.find_all('div', id='variation_configuration')
        configuration = BeautifulSoup(str(variationConfigurations), 'html.parser')
        configurations = configuration.find_all('li')
        json_data["configurations"] = []
        for configuration in configurations:
            conf = configuration.text.strip()
            json_data["configurations"].append(conf)        
    except:
        pass


        # Description
    try:
        description = soup.find('div', id='feature-bullets').text.strip()
        json_data["description"] = description
    except:
        description = 'N/A'
    

    #  Features
    try:
        featuresElem = soup.find('div', id='productOverview_feature_div')
        all_features = featuresElem.find_all('tr')
        json_data["features"] = []
        for feature in all_features:
            json_data["features"].append(feature.text.strip())
    except:
        featuresElem = 'N/A'



    # all images related to product
    try:
        imageBlock = soup.find('div', id='altImages')
        all_images = imageBlock.find_all('img')
        json_data["image_urls"]  = []
        for image  in all_images:
            imageLink = image['src']
            json_data["image_urls"].append(imageLink)
    except:
        pass

json_data  = json.dumps(json_data)
print(json_data)


