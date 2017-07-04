import time
import re
from bs4 import BeautifulSoup
from datetime import datetime 
from selenium import webdriver
from stage1 import*
from stage2 import*

def main():
   s1 = Stage1()
   s1.start_scraping()
   s1.close() 

   s2= Stage2()
   s2.start_scraping()
   s2.close()
   
if __name__ == "__main__":
    t1 = time.time()
    main()
    t2 = time.time()
    print('\n\n ********************* Program Ended Successfully. Time (sec) : {}  **************************************'.format(t2 - t1)) 
