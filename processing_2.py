#its main framework
import time
import re
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from MDatabase import Database
from Helper import*


database = "" # write the database name here

class Project2:
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.count = 1
        self.set_delay = 10
        self.max_num_of_tabs = 25       
        self.db = Database()
        self.store_results = []
        self.starting_urls = []
        #***********************************************************************#
        f = open("stage2.txt")
        temp_count = 0
        for line in f.readlines():
            temp_count += 1
            if temp_count > 100:
                break
            self.starting_urls.append(line.strip())
        self.starting_urls = list(set(self.starting_urls))
        print("len of urls :" + str(len(self.starting_urls)))
        #***********************************************************************#\
    def close(self):
        self.driver.quit()

    def close_all_tabs(self):
        w_handles = self.driver.window_handles
        for i in range(1,len(w_handles)): 
            self.driver.switch_to_window(w_handles[i])
            self.driver.close()
        self.driver.switch_to_window(w_handles[0]) 
    
    def parse(self,category): # this function will parse and store the data in database   
        dic = {}
        dic["name"] = ""
        dic["sku"] = ""
        dic["price"] = ""
        dic["category"] = category
        dic["image_url"] = ""        
        dic["available"]= ""
        dic["children"] = []
        dic["b1"] = ""
        dic["b2"] = ""
        dic["b3"] = ""
        dic["b4"] = ""
        dic["b5"] = ""
        dic["i1"] = ""
        dic["i2"] = ""
        dic["i3"] = ""
        dic["i4"] = ""
        dic["i5"] = ""
        dic["i6"] = ""
        dic["i7"] = ""
        dic["vr_theme"] = 1

        soup = BeautifulSoup(self.driver.page_source,"html.parser")
        
        #***********************************************************************#
        dic["name"] = soup.find("table",{"class":"productInfoTable"}).find_all("tr")[0].find_all("td")[1].getText().strip()        
        dic["sku"] = soup.find("table",{"class":"productInfoTable"}).find_all("tr")[1].find_all("td")[1].getText().strip()
        dic["price"] = soup.find("table",{"class":"productInfoTable"}).find_all("tr")[2].find_all("td")[1].getText().strip()
        text = soup.find_all("table",{"class":"productInfoTable"})[1].getText().strip()
        dic["available"] = "No"
        


        ## product info bullet points 
        try:
            table_list = soup.find_all("table",{"class":"productInfo"})[1].find_all("li") 
            for i in range(1,6):
                try:
                    dic["b"+str(i)] = table_list[i-1].getText().strip()
                except:
                    pass    
        except:
            pass

        # children
        children_list = []
        sizes_list = []
        other_urls_list = []
        tr_nodes = soup.find_all("table",{"class":"productInfoTable"})[1].find("tbody").find_all("tr",recursive=False)

        # getting sizes list 
        td_nodes = tr_nodes[0].find_all("td",recursive=False)        
        del td_nodes[0]
        for td in td_nodes:
            if len(td.getText().strip()) <= 2:
                sizes_list.append(td.getText().strip())
                dic["vr_theme"] = 2
            
            

        # getting child names like Multi etc
        del tr_nodes[0]
        temp_len =  len(sizes_list)
        option_flag = False
        if temp_len == 0:
            temp_len = 1   
            option_flag = True    
        for i in range(temp_len):
            for tr_node in tr_nodes:        
                child_dic = {}
                child_dic["image_url"] = ""
                td_nodes = tr_node.find_all("td",recursive=False)
                child_name = td_nodes[0].getText().strip()
                if len(sizes_list) >0:
                    child_dic["sku"] = dic["sku"] + "-"+ child_name + "-"+ sizes_list[i]
                else:
                    child_dic["sku"] = dic["sku"] + "-"+ child_name

                temp_text = ""
                if len(sizes_list) == 0:
                    temp_text = tr_node.getText().strip()
                else:    
                    temp_text = td_nodes[i+1].getText().strip()
                
                if temp_text.find("Out of Stock") > -1:
                    child_dic["available"] = "No"
                else:
                    dic["available"] = "yes"
                    child_dic["available"] = "yes"

                # finding image url
                td_images_list1 = soup.find_all("table",{"class":"productInfoTable"})[3].find_all("td")
                td_images_list2 = []
                try:
                    td_images_list2 = soup.find_all("table",{"class":"productInfoTable"})[4].find_all("td")
                except:
                    pass
                
                for temp_td_node in td_images_list1 +td_images_list2:
                    text = temp_td_node.getText().strip()
                    print("text  : " , text)
                    print("child_name : ",child_name)
                    if len(text) >2:
                        if child_name.find(text) > -1 or text.find(child_name) >-1:
                            child_dic["image_url"] = temp_td_node.find("img")["src"]
                            dic["image_url"] = temp_td_node.find("img")["src"]
                            break
                    else:
                        try:
                            dic["image_url"] = temp_td_node.find("img")["src"]
                            other_urls_list.append(temp_td_node.find("img")["src"])
                            other_urls_list=li(set(other_urls_list))
                        except:
                            pass

                children_list.append(child_dic)                

        
        for i in range(1,8):
            try:
                dic["i"+str(i)] = other_urls_list[i-1]
            except:
                dic["i"+str(i)] = ""   

        dic["children"] = children_list
        self.store_results.append(dic)
        
            
    def start_scraping(self):
        lists_of_list_urls = make_lists_of_list(self.starting_urls,self.max_num_of_tabs)
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
        for url_list in lists_of_list_urls:
            for url in url_list:
                category = url.split("***")[1] 
                script = "window.open('{}')".format(url.split("***")[0])
                self.driver.execute_script(script)
                
            
            time.sleep(15)

            w_handles = self.driver.window_handles
            
            for i in range(1,len(w_handles)):
                self.count = self.count + 1
                self.driver.switch_to_window(w_handles[i])
                
                try:
                    self.parse(category)
                    print("count : " + str(self.count))
                except:
                    soup = BeautifulSoup(self.driver.page_source,"html.parser")
                    # print(soup.prettify())
                    text=soup.getText().strip()
                    if text.find("YOUR IP ADDRESS HAS BEEN BANNED! @ WHOLESALE JEWELRY TOWN") > -1:
                        print("Your IP Has Been Blocked")
                        
                    self.parse(category)
                    print("\n\n=======> Error: Parsing",self.driver.current_url)    

            self.close_all_tabs()

        put_data_to_excel(self.store_results)
        return self.store_results  # you can return list of dic from here #self.db.get_all(database,"Products")



if __name__ == "__main__":
    proj = Project2()
    rslt =  proj.start_scraping()
    put_data_to_excel(rslt)
    # print("Result = ", rslt)
    proj.close()
    print(">>Program Ended Successfully")          
