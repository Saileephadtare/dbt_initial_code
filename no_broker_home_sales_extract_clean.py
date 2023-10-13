from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import requests as req
from itertools import zip_longest

def get_property_name(new_soup):
    try:
        all_details=new_soup.find('div',attrs={'class':'nb__2RSJy'})
        Property_Name=all_details.div.div.h1.text
    except:
        Property_Name=''
    return Property_Name

def get_property_price(new_soup):
    try:
        house_cost=new_soup.find('div',attrs={'class':'font-semi-bold heading-5 flex items-center justify-center nb__3h7Fo'})
        House_Price=house_cost.span.text
        House_Price=House_Price.replace(" ₹ ","")
    except:
        House_Price='' 
    return House_Price

def get_property_area(new_soup):
    try:
        sqft_detail=all_details.find('div',class_='nb__1sFxw' )
        sqft=sqft_detail.div.text
    except:
        sqft=''
    return sqft

def get_property_details(new_soup):
    try:
        property_details=new_soup.find('div',attrs={'class':'nb__1oYzq nb__1O4x_'})  

        for data in property_details.find_all('div',class_='nb__3vD7l'):
               data_1=data.find_all('h4',attrs={'id':'details-summary-typeDesc'})
               for i in data_1:
                    bedroom=i.get_text()
                
               data_2=data.find_all('h4',attrs={'id':'details-summary-bathroom'}) 
               for i in data_2:
                    bathroom=i.get_text()

               data_3=data.find_all('h4',attrs={'id':'details-summary-availableFrom'}) 
               for i in data_3:
                    availability=i.get_text()     

               data_4=data.find_all('h4',attrs={'id':'details-summary-society'}) 
               for i in data_4:
                    society=i.get_text() 

               data_5=data.find_all('h4',attrs={'id':'details-summary-parkingDesc'}) 
               for i in data_5:
                    parking=i.get_text() 

               data_6=data.find_all('h4',attrs={'id':'details-summary-balconies'}) 
               for i in data_6:
                    balcony=i.get_text()  

               data_7=data.find_all('h4',attrs={'id':'details-summary-lastUpdateDate'}) 
               for i in data_7:
                    ad_posted=i.get_text()     

               data_8=data.find_all('h4',attrs={'id':'details-summary-powerBackup'}) 
               for i in data_8:
                    power_backup=i.get_text()      

    except:
          bedroom='NA'
          bathroom='NA'
          availability='NA'
          society='NA'
          parking='NA'
          balcony='NA'
          ad_posted='NA'
          power_backup='NA'
    return [bedroom,bathroom,availability,society,parking,balcony,ad_posted,power_backup]

########################### overview details ###################################
def get_property_overview(new_soup):
     try:
           for overview_detail in new_soup.find_all('div', attrs={'class': 'nb__33JWL'}):
               data_1_elements = overview_detail.findAll('div', class_='nb__2vvM7')
               data_elements = overview_detail.findAll('div', class_='nb__2xbus')

               record_dict = {}  # Initialize the dictionary outside the loop

               for data_1, data in zip_longest(data_1_elements, data_elements, fillvalue=None):
                    house_data_1 = data_1.find('h5', attrs={'class': 'nb__1IoiM'}).get_text() if data_1 else None
                    house_data = data.find('h5', attrs={'class': 'font-semi-bold nb__1IoiM'}).get_text() if data else None

                    # Add the data to the record_dict
                    if house_data_1 and house_data:
                              record_dict[house_data_1] = house_data

     except:
         record_dict='NA'

     return record_dict


##############################################################################################################################################
if __name__ == '__main__':
     CHROMEDRIVER_PATH = 'C:/Users/username/Downloads/chromedriver-win64/chromedriver'
     URL='https://www.nobroker.in/property/sale/pune/Wakad?searchParam=W3sibGF0IjoxOC42MDEwOTIxLCJsb24iOjczLjc2NDEyNDUsInBsYWNlSWQiOiJDaElKN1J0WHIzcTV3anNSYzJhbnBXczBad3ciLCJwbGFjZU5hbWUiOiJXYWthZCIsInNob3dNYXAiOmZhbHNlfV0=&isMetro=false&radius=2.0'
     HEADERS=({'User_Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36','Accept-Language':'en-US,en;q=0.5'})
     res=req.get(URL,headers=HEADERS)

     options = Options()
options.add_argument('--headless')
options.add_argument('--log-level=3')
driver = webdriver.Chrome(options=options)

driver.get(URL)

soup=BeautifulSoup(driver.page_source,'html.parser')


flats_links=soup.find_all('a',attrs={'class':'overflow-hidden overflow-ellipsis whitespace-nowrap max-w-80pe po:max-w-full'})
links=[]
for flat_link in flats_links:
     links.append(flat_link.get('href'))


d = {"Name":[],"House_Price":[],"Area":[],"property_details":[],"overview_details":[],"Apartment_Name":[],
    "Bedroom":[],"Bathroom":[],"Balcony":[], "Age of Building":[], "Ownership Type":[],"Avability":[],
     "Maintenance Charges":[], "Floor":[], "Builtup Area":[],
      "Carpet Area":[],"Parking":[],"Power_Supply":[],"Furnishing Status":[], "Facing":[], "Gated Security":[],"Ad_posted":[]
                 }
 

for link in links:
    product_link='https://nobroker.in'+link
    res_1=req.get(product_link,headers=HEADERS)
#     print(res_1)
    driver.get(product_link)
    new_soup=BeautifulSoup(driver.page_source,'html.parser')
    all_details=new_soup.find('div',attrs={'class':'nb__2RSJy'})  
    d['Name'].append(get_property_name(new_soup))
    d['House_Price'].append(get_property_price(new_soup))
    d['Area'].append(get_property_area(new_soup))
    d['property_details'].append(get_property_details(new_soup))
    d['overview_details'].append(get_property_overview(new_soup))

for data in d['property_details']:

       d['Bedroom'].append(data[0].replace("Bedroom","")),d['Bathroom'].append(data[1].replace("Bathroom","")),d['Avability'].append(data[2]),
       d['Balcony'].append(data[5]),
       d['Apartment_Name'].append(data[3]),d['Parking'].append(data[4]),
       d['Ad_posted'].append(data[6]),d['Power_Supply'].append(data[7])
      

for data in d['overview_details']:       
            if 'Age of Building' in data:
                 d['Age of Building'].append(data['Age of Building'])
            else:
                 d['Age of Building'].append('NA')     
            if 'Ownership Type' in data:
                 d['Ownership Type'].append(data['Ownership Type'])
            else:
                  d['Ownership Type'].append('NA')    
            if 'Maintenance Charges' in data:
                 d['Maintenance Charges'].append(data['Maintenance Charges'].replace(" ₹",""))
            else:
                 d['Maintenance Charges'].append('NA')     
            if 'Floor'  in data:
                 d['Floor'].append(data['Floor'])
            else:
                  d['Floor'].append('NA')    
            if 'Builtup Area' in data:
                 d['Builtup Area'].append(data['Builtup Area'])
            else:
                  d['Builtup Area'].append('NA')    
            if 'Carpet Area' in data:
                 d['Carpet Area'].append(data['Carpet Area'])
            else:
                  d['Carpet Area'].append('NA')          
            if 'Furnishing Status' in data:
                 d['Furnishing Status'].append(data['Furnishing Status'])
            else:
                  d['Furnishing Status'].append('NA')     
            if 'Facing' in data:
                 d['Facing'].append(data['Facing'])   
            else:
                  d['Facing'].append('NA')      
            if data['Gated Security']:
                 d['Gated Security'].append(data['Gated Security'])  
            else:
                  d['Gated Security'].append('NA')                                                    


sale_df=pd.DataFrame.from_dict(d)
sale_df.to_csv('C:/Users/username/Downloads/folder/file_name.csv',index=False)
