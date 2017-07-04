import time
import re
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime 
from selenium import webdriver
from Helper import*

database = "" # write the database name here

class Stage2:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.count = 1
        self.set_delay = 10
        self.max_num_of_tabs = 25       
        self.db = Database()
        self.store_results = []
        self.starting_urls = []
        #***********************************************************************#
        f = open("stage2.txt")
        for line in f.readlines():
            self.starting_urls.append(line.strip())
        self.starting_urls = list(set(self.starting_urls))
        print("len of urls :" + str(len(self.starting_urls)))
        #***********************************************************************# 
    
    def close(self):
        self.driver.quit()
    
    def close_all_tabs(self):
        w_handles = self.driver.window_handles
        for i in range(1,len(w_handles)): 
            self.driver.switch_to_window(w_handles[i])
            self.driver.close()
        self.driver.switch_to_window(w_handles[0])      
    
    def parse(self): # this function will parse and store the data in database
        dic = {}
        soup = BeautifulSoup(self.driver.page_source,"html.parser")
        #***********************************************************************#
            		# parse html here  
        #***********************************************************************#
        # store data into database or to list ===> self.db.insert_item(database,"Products",dic,"Product_URL")
            
    def start_scraping(self):
        def login():
            self.driver.get("https://wholesalejewelrytown.com/login.php")
            time.sleep(2)
            elem = self.driver.find_element_by_id("email_address")
            elem.send_keys("waris.gill@outlook.com")
            elem = self.driver.find_element_by_id("password")
            elem.send_keys("9175963258")
            elem.send_keys(Keys.RETURN)
            time.sleep(5)
        #login()   
        lists_of_list_urls = make_lists_of_list(self.starting_urls,self.max_num_of_tabs)
        
        for url_list in lists_of_list_urls:
            for url in url_list:
                script = "window.open('{}')".format(url)
                self.driver.execute_script(script)
                time.sleep(3)
            
            time.sleep(4)

            w_handles = self.driver.window_handles
            
            for i in range(1,len(w_handles)):
                time.sleep(1.4)
                self.driver.switch_to_window(w_handles[i])
                try:
                    self.parse()
                except:
                    #self.parse()
                    print("Error: Parsing",self.driver.current_url)    
            self.close_all_tabs()

        self.store_results = list(set(self.store_results))    
        
        return self.store_results # return the results

if __name__ == "__main__":
    proj = Stage2()
    rslt =  proj.start_scraping()
    proj.close()
    put_data_to_excel(rslt)
    print("Result = ", rslt)
    print(">>Program Ended Successfully")           
