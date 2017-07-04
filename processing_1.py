import time
import re
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime 
from selenium import webdriver
from MDatabase import Database
from Helper import*

database = ""

class Project1:
    def __init__(self):
        self.driver = webdriver.PhantomJS()
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

    def question_ans_function(self):
        check = input('Please Enter 1111 to Clear the Database or Type 2222 to continue : ')
        if check == '1111':
            self.db.clear_db(database)
        else:
            print("\n>> Script is Resuming .... ")    

    def close_all_tabs(self):
        w_handles = self.driver.window_handles
        for i in range(1,len(w_handles)): 
            self.driver.switch_to_window(w_handles[i])
            self.driver.close()
        self.driver.switch_to_window(w_handles[0])    

    
    def parse(self):
        dic = {}     
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        #***********************************************************************#
        urls_list = []
        category = soup.find_all("a",{"class":"headerNavigation"})[-1].getText().strip()
        for a_node in soup.find_all("a",{"class":"iframe"}):
            try:
                url = "http://wholesalejewelrytown.com/product_info.php?manufacturers_id=&products_id=" + a_node["href"].strip().split("=")[-1]  
                urls_list.append((url,category))
                # print(url)
            except:
                continue    
           
        self.save_to_list = self.save_to_list + urls_list              
          
        #***********************************************************************#
        

    def parse_each_tab(self):
        w_handles = self.driver.window_handles

        for i in range(1,len(w_handles)):
            time.sleep(1.4)
            self.driver.switch_to_window(w_handles[i])#
            try:
                self.parse()
            except:
                 print("Error: Parsing",self.driver.current_url)                

    def start_scraping(self): 
        def send_async_requests(urls):
            for url in urls:
                myscript = 'window.open(\"' + url + '\");'
                print(myscript)
                self.driver.execute_script(myscript)#
                time.sleep(3.5)
        
        def lamdafun(li):
            for item in li:
                if item == False:
                    return False
        
            return True
        
        def process_tabs_until_end():# this lamda function is for clicking and stuff like that 
            w_handles = self.driver.window_handles
            flag_list = []
            for w in w_handles: 
                flag_list.append(False)
            flag_list[0] = True

            #***********************************************************************#
            
            while lamdafun(flag_list) == False:
                time.sleep(3)
                self.parse_each_tab()
                for i in range(0,len(w_handles)): 
                    if flag_list[i] == True: 
                        continue
                    self.driver.switch_to_window(w_handles[i])
                    soup = BeautifulSoup(self.driver.page_source,"html.parser")
                    flag = False
                    next_page_link = ""    
                    for a_node in soup.find_all("a",{"class":"pageResults"}):
                        if a_node["title"].strip().find("Next Page") > -1:
                            flag = True
                            next_page_link = a_node["href"].strip()

                    if flag == True:
                        url = next_page_link
                        myscript = "location.href = " + '\"' + url + '\";'
                        print(myscript)
                        self.driver.execute_script(myscript)
                        time.sleep(2)
                    else:
                        flag_list[i] = True            

            #***********************************************************************#

            
        #<=============================== LAMDA FUNCTIONS END ==============================>#        
       
        lists_of_list_urls = make_lists_of_list(self.starting_urls,self.max_num_of_tabs)#
        for url_list in lists_of_list_urls: 
            send_async_requests(url_list)
            process_tabs_until_end()
            self.close_all_tabs()            

        save_links_to_text_file(list(set(self.save_to_list)))

        return self.save_to_list


# if __name__ == "__main__":
    
#     proj = Project1()
#     urls_list = proj.start_scraping()
    
#     proj.close()


#     print(">> Project 1 is working Fine")        

