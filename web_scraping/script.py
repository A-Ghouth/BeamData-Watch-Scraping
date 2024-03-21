from bs4 import BeautifulSoup
import pandas as pd
import requests
from tqdm import tqdm
import os

# --> Initial Variables ---------------------------------------------------------------------
global data
global images

# Define The Columns 
df = pd.DataFrame(columns=['reference_number', 'watch_URL', 'type', 'brand', 'year_introduced', 'parent_model', 'specific_model', 'nickname', 'marketing_name', 'style', 'currency', 'price', 'image_URL', 'made_in', 'case_shape', 'case_material', 'case_finish', 'caseback', 'diameter', 'between_lugs', 'lug_to_lug', 'case_thickness', 'bezel_material', 'bezel_color', 'crystal', 'water_resistance', 'weight', 'dial_color', 'numerals', 'bracelet_material', 'bracelet_color', 'clasp_type', 'movement', 'caliber', 'power_reserve', 'frequency', 'jewels', 'features', 'description', 'short_description'])

benu = {
    "name": "Benu",
    "url": "https://en.grossmann-uhren.com/collection/benu",
    "collections": ".collection-title a",
}

tefnut = {
    "name": "Tefnut",
    "url": "https://en.grossmann-uhren.com/collection/tefnut",
    "collections": ".collection-title a",
}

sold_out = {
    "name": "",
    "url": "https://en.grossmann-uhren.com/collection/sold-out-pieces",
    "collections": ".single-collection .item-1",
}

# --> HelpFul Functions ---------------------------------------------------------------------
# Insert a Row to Data        
def add_data(data):
    data["parent_model"] = category["name"]
    data["brand"] = "Moritz Grossman"
    data["made_in"] = "Germany"
    
    data["case_thickness"] = data.get("diameter", None)
    data["numerals"] = data.get("dial_color", None)
    data["bracelet_color"] = data.get("bracelet_material", None)
    data["clasp_type"] = data.get("bracelet_material", None)
    data["caliber"] = data.get("movement", None)

    
    df.loc[len(df)] = data
    
# Filter Collection Specification
def filter_watches_specs(key, value):
    key = key.strip().split(":")[0].lower()
    items = {
        "movement": "movement", "atum 37 hommage - movement": "movement",
        "functions": "features", "functions / features": "features", "atum 37 hommage - functions": "features",
        "no. of jewels": "jewels", "jewels": "jewels", "atum 37 hommage - no. of jewels": "jewels",
        "balance": "frequency", "balance diameter": "frequency", "frequency": "frequency", "atum 37 hommage - balance": "frequency",
        "power reserve": "power_reserve", "atum 37 hommage - power reserve": "power_reserve",
        "case dimensions": "diameter", "atum 37 hommage - case dimensions": "diameter",
        "crystal / display back": "crystal", "crystal and display back": "crystal", "glass and caseback": "crystal", "crystal/display back": "crystal", "glass / display back": "crystal", "atum 37 hommage - crystal / display back": "crystal",
        "strap": "bracelet_material", "atum 37 hommage - strap": "bracelet_material", "case": "case_material",        
        "dial": "dial_color",
    }
    if key in items:
        if not data.__contains__(items[key]):  # For Duplicate Specification( Movement, ...)
            data[items[key]] = value.strip()
            
# Filter Watch Specification
def filter_tech_specs(key, value):
    key = key.split(":")[0].strip().lower()
    items = {
        "reference": "reference_number", "referencnr.": "reference_number", "referenc": "reference_number",
        "case": "case_material", "atum 37 hommage - case": "case_material", "atum 37 hommage - dial": "dial_color",
        "dial": "dial_color", "dial disc": "dial_color",
    }

    if key in items:
        data[items[key]] = value.strip()

# --> Main Functions ---------------------------------------------------------------------
# Get Html Page Content & Extract Some Columns 
def parse_html_page(url):
    global images
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")

    data["specific_model"] = (category["name"] if category['name'] != 'Tefnut' else '') + ' ' + soup.select_one(".watch-title").text
    images = [image.get("src") for image in soup.select(".watch-models__image img")]
    data["description"] = "\n".join([paragraph.text for paragraph in soup.select(".wpb_wrapper >  p")])

    tech_specs = soup.select_one(".specifications").select(".specification-item")
    watches = soup.select(".watch-models__content")
    
    return tech_specs, watches

# Get Each Collection Specification
def get_tech_specs(specs):
    for spec in specs:
        items = spec.select("p")
        key = items[0].text
        value = items[1].text

        filter_watches_specs(key, value)
            
# Get Each Watch Specification
def get_watch_specs(watches, url):
    global data
    temp_data  = data.copy()

    # Loop for Each Watch in Collection Watches
    for watch in watches:
        data = temp_data.copy()  # Clear Previous Data

        data["nickname"] = watch.select_one("h3").text
        data["image_URL"] = images.pop(0)
        data["watch_URL"] = url + f'#{data["nickname"].replace(" ", "-").lower()}'

        top = watch.select_one("h4").text if watch.select_one("h4") != None else ""
        bot = watch.select_one(".accent").text if watch.select_one(".accent") != None else ""
        data["marketing_name"] = top + " " + bot
        
        # Loop for Each Watch Specification in Single Watch
        for spec in watch.select("p:not(.accent)"):
            
            key = spec.select_one("strong").text
            value = spec.select_one("span").text

            filter_tech_specs(key, value)
        add_data(data)

# --> Main Code ---------------------------------------------------------------------
categories = [benu, tefnut, sold_out]

# Loop through the categories
for category in categories : 
    html = requests.get(category["url"])
    soup = BeautifulSoup(html.content, "html.parser")

    # Loop through each collection in the category
    for collection in tqdm(soup.select(category["collections"])):
        data = dict()
        url = collection["href"]

        tech_specs, watches = parse_html_page(url)
        
        get_tech_specs(tech_specs)
        get_watch_specs(watches, url)
    
df.to_csv("data/dataSet.csv", index=False)