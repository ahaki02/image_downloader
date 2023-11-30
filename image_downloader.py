# IMPORTING LIBRARIES
from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import os
import time

# SENDING REQUEST FOR THE DESIRED WEB PAGE
try:
    url = input("INPUT THE URL: ")
    web_content = get(url).text
    soup = BeautifulSoup(web_content, "html.parser")
except Exception as e:
    print(e)
    print("By BY")
    time.sleep(5)

# CREATING A FOLDER TO SAVE IMAGES AND SAVING THEIR LINK ADDRESS IN A CSV FILE
try:
    new_folder = "Images"
    os.mkdir(new_folder)
except FileExistsError:
    print("Folder already exists")

# DOWNLOADING IMAGES AND SAVING THEIR LINKS INTO A CSV FILE
def download_image(image_url, name):
    base_path = os.getcwd().replace("\\", "/") + "/images/" + name.replace("\\", " ").replace("/", " ") + ".jpg"
    img_data = get(image_url).content
    with open(base_path ,'wb') as handler:
        handler.write(img_data)
    
image_list_alt, image_list_url, counter = [], [], 0
for item in soup.find_all("img"):
    try:
        image_list_alt.append(item['alt'])
    except:
        item['alt'] = f"None{counter+1}"
        image_list_alt.append(item['alt'])
    try:
        image_list_url.append(item['src'])
    except:
        image_list_url.append("None")
    try:
        counter += 1
        download_image(item['src'][item['src'].index("http"):], str(counter) + " - " + item['alt'].replace("|", " "))
    except Exception as e:
        print(e)
        print(f"{counter} - {item['alt']}")

data = {"NAME":image_list_alt, "URL":image_list_url}
df = pd.DataFrame(data)
df.to_csv(os.getcwd().replace("\\", "/")+"/Images/"+"Image_links.csv", encoding="utf-8-sig")