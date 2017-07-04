import time
import re
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime 
from selenium import webdriver
from Helper import*

database = ""

class Stage1:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.max_num_of_tabs = 25 
        self.save_to_list = []
        self.starting_urls = []
        #***********************************************************************#
        f = open("stage1.txt")
        for line in f.readlines():
            self.starting_urls.append(line.strip())
        #***********************************************************************# 
        self.db = Database()     

    def close(self):
        self.driver.quit()

    def close_all_tabs(self):
        w_handles = self.driver.window_handles
        for i in range(1,len(w_handles)): 
            self.driver.switch_to_window(w_handles[i])
            self.driver.close()
        self.driver.switch_to_window(w_handles[0])     

    def question_ans_function(self):
        check = input('Please Enter 1111 to Clear the Database or Type 2222 to continue : ')
        if check == '1111':
            self.db.clear_db(database)
        else:
            print("\n>> Script is Resuming .... ")    

    def parse(self):
    	dic = {}     
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        #***********************************************************************#
            		# parse html here  
        #***********************************************************************#
        # insert to data base ==> self.db.insert_item(database,"Product_URLS",{"URL":link},"URL")
        #self.save_to_list ===> save in it for run time
         
    def send_async_requests(self,urls):
        for url in urls:
            myscript = 'window.open(\"' + url + '\");'
            print(myscript)
            self.driver.execute_script(myscript)#
            time.sleep(4)
        return            
    
    def parse_each_tab(self):
    	w_handles = self.driver.window_handles

    	for i in range(1,len(w_handles)):
            time.sleep(1.4)
            self.driver.switch_to_window(w_handles[i])#
            try:
                self.parse()
            except:
                print("Error: Parsing",self.driver.current_url) 
        return

    def process_tabs_until_end(self):# this lamda function is for clicking and stuff like that 
        def lamdafun(li):
            for item in li:
                if item == False:
                    return False
            return True  
        w_handles = self.driver.window_handles
        flag_list = []
        for w in w_handles: 
            flag_list.append(False)
        flag_list[0] = True
        #***********************************************************************#
        while lamdafun(flag_list) == False:
            time.sleep(3)
            self.parse_each_tab() # first parse also
            for i in range(0,len(w_handles)): 
                if flag_list[i] == True: 
                    continue
                self.driver.switch_to_window(w_handles[i])
        #***************************** put more logic above on process each tab func *********************
    def start_scraping(self):               
        # self.question_ans_function()
        lists_of_list_urls = make_lists_of_list(self.starting_urls,self.max_num_of_tabs)#
        for url_list in lists_of_list_urls: 
            self.send_async_requests(url_list)
            time.sleep(2)
            self.process_tabs_until_end()
            self.close_all_tabs()            
        
        save_links_to_text_file(list(set(self.save_to_list)))
        return  list(set(self.save_to_list))

if __name__ == "__main__":
	s1 = Stage1()
	s1.start_scraping()
	s1.close()
	print(">> Project 1 is working Fine")        

