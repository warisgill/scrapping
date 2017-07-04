import time
import re
from bs4 import BeautifulSoup
from datetime import datetime 
from selenium import webdriver
from processing_1 import*
from processing_2 import*

def main():
    proj1 = Project1()
    proj1.start_scraping()
    proj1.close() 

    proj2= Project2()
    proj2.start_scraping()
    proj2.close()

   

if __name__ == "__main__":
    t1 = time.time()
    main()
    t2 = time.time()
    print('\n\n ********************* Program Ended Successfully. Time (sec) : {}  **************************************'.format(t2 - t1)) 
