from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import requests  as req
import re


def get_property_name(new_soup):
    try:
        all_details=new_soup.find('div',attrs={'class':'nb__2RSJy'})
        Property_Name=all_details.div.div.h1.text
    except:
            Property_Name=""

    return Property_Name

def get_property_rent(new_soup):
     try:
        rent_details=new_soup.find('div',attrs={'class':'font-semi-bold heading-5 nb__3h7Fo'})
        rent=rent_details.span.span.text
        rent=rent.replace('₹',"")
     except:
            rent=""
     return rent

def get_propert_deposit(new_soup):
     try:
          deposit_details=all_details.find('div',attrs={'class':'nb__3zfm-'})
          deposit=deposit_details.span.text
          deposit=deposit.replace(' ₹ ',"")
     except:
          deposit=""
     return deposit

def get_property_area(new_soup):
     try:
          sqft_detail=all_details.find('div',class_='nb__Og576' )
          sqft=sqft_detail.div.text
     except:
         sqft=""
     return sqft

def get_property_bedroom(new_soup):
     try:
          property_details=new_soup.find('div',attrs={'class':'nb__1oYzq nb__1O4x_'})
          for data in property_details.find_all('div',class_='nb__3vD7l'):
               data_1=data.find_all('h4',attrs={'id':'details-summary-typeDesc'})
               for i in data_1:
                    bedroom=i.get_text()
                
               data_2=data.find_all('h4',attrs={'id':'details-summary-leaseType'}) 
               for i in data_2:
                    type=i.get_text()

               data_3=data.find_all('h4',attrs={'id':'details-summary-availableFrom'}) 
               for i in data_3:
                    availability=i.get_text()     

               data_4=data.find_all('h4',attrs={'id':'details-summary-parkingDesc'}) 
               for i in data_4:
                    parking=i.get_text() 

               data_5=data.find_all('h4',attrs={'id':'details-summary-propertyAge'}) 
               for i in data_5:
                    property_age=i.get_text() 

               data_6=data.find_all('h4',attrs={'id':'details-summary-balconies'}) 
               for i in data_6:
                    balcony=i.get_text()  

               data_7=data.find_all('h4',attrs={'id':'details-summary-lastUpdateDate'}) 
               for i in data_7:
                    ad_posted=i.get_text()     

     except:
          bedroom=''
          type=''
          availability=''
          parking=''
          balcony=''
     return [bedroom,type,availability,parking,property_age,balcony,ad_posted]

def get_property_overview(new_soup):
     try:
          overview_detail=new_soup.find('div',attrs={'class':'nb__33JWL'})
          house_details=[]

          for data in overview_detail.findAll('div',class_='nb__2xbus'):
               house_data=data.find('h5',attrs={'class':'font-semi-bold nb__1IoiM'})
               for data in house_data:
                   house_details.append(data.get_text())
     except:
         house_details=''

     return house_details
########################################################################
if __name__ == '__main__':
     CHROMEDRIVER_PATH = 'C:/Users/username/Downloads/chromedriver-win64/chromedriver'
URL='https://www.nobroker.in/property/rent/pune/Wakad?searchParam=W3sibGF0IjoxOC42MDEwOTIxLCJsb24iOjczLjc2NDEyNDUsInBsYWNlSWQiOiJDaElKN1J0WHIzcTV3anNSYzJhbnBXczBad3ciLCJwbGFjZU5hbWUiOiJXYWthZCJ9XQ==&radius=2.0&sharedAccomodation=0&city=pune&locality=Wakad'
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



d = {"Name":[],"House_Rent":[],"Area":[],"Deposit":[],"property_details":[],"overview_details":[],
     "Bedroom":[],"Bathroom":[],"Balcony":[],"Building_age":[],"Avability":[],"Tenant":[],"Parking":[],
     "Water_Supplier":[],"Floor":[],"Furniture_Status":[],"Facing":[],"Gate_Security":[],"Ad_posted":[]}

for link in links:
    product_link='https://nobroker.in'+link
    res_1=req.get(product_link,headers=HEADERS)
    driver.get(product_link)
    new_soup=BeautifulSoup(driver.page_source,'html.parser')
    all_details=new_soup.find('div',attrs={'class':'nb__2RSJy'})  
    d['Name'].append(get_property_name(new_soup))
    d['House_Rent'].append(get_property_rent(new_soup))
    d['Deposit'].append(get_propert_deposit(new_soup))
    d['Area'].append(get_property_area(new_soup))
    d['property_details'].append(get_property_bedroom(new_soup))
    d['overview_details'].append(get_property_overview(new_soup))


for data in d['property_details']:
       d['Bedroom'].append(data[0].replace("Bedroom","")),d['Tenant'].append(data[1]),d['Avability'].append(data[2]),
       d['Parking'].append(data[3]),d['Building_age'].append(data[4]),
       d['Balcony'].append(data[5]),d['Ad_posted'].append(data[6])
 
for data in d['overview_details']:
       d['Furniture_Status'].append(data[0]), d['Facing'].append(data[1]), d['Water_Supplier'].append(data[2]),
       d['Floor'].append(data[3]),d['Bathroom'].append(data[4]),d['Gate_Security'].append(data[6])




rent_df = pd.DataFrame.from_dict(d) 

rent_df.to_csv('C:/Users/username/Downloads/folder/filename.csv',index=False)



         

