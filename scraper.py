import requests
import pymysql
from bs4 import BeautifulSoup
import csv
from urllib.request import Request, urlopen

#connect to db
password = input("Enter Password: ")
conn = pymysql.connect(host = 'localhost', user='root', passwd=password,db='mysql')
cur = conn.cursor()
cur.execute("USE aquarium")

#drop table if currently exists
delete_table = "DROP TABLE IF EXISTS `Fish`;" 
cur.execute(delete_table)
conn.commit()

#create table to store data
create_table ="CREATE TABLE `Fish` ( `fish_id` int NOT NULL AUTO_INCREMENT, `name` varchar(50) NOT NULL, `genus` varchar(50), `species` varchar(50), PRIMARY KEY (`fish_id`) ) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;"
cur.execute(create_table)
conn.commit()

#set up beautiful soup for web scraping
site ='https://dwazoo.com/exhibit/aquarium/page/'
site_page = 1
hdr = {'User-Agent': 'Mozilla/5.0'}

while(site_page < 8):
    full_site = site + str(site_page)
    req = Request(full_site,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'html.parser') 

    #get elements with value class = entry-title
    fish = soup.find_all(class_="entry-title")

    #loop through fish and insert data into table
    for f in fish:
        val = f.get_text().split(", ")
        query = "INSERT INTO fish (name, genus, species) VALUES ('" + val[0] + "', '" + val[1].split(' ',1)[0] + "', '" + val[1].split(' ',1)[1] + "');"
        print(query)
        cur.execute(query)
        conn.commit()
    site_page+=1

cur.close()
conn.close()
