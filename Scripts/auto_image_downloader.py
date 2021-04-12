"""
File name:  auto_image)downloader.py
Description:  Download Images from Google Image Search using Selenium
OS:  Windows 
Author:  Tejas Anilkumar P.  <tpandara@andrew.cmu.edu>
Date:  04/11/2021
   
Carnegie Mellon University
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

from time import sleep
import requests
import os


class AutoImageDownloader():
    def __init__(self):
        self.initVariables()
        self.initDriver()
        self.initImgDir()
        
    def initVariables(self):
        self.image_size = " imagesize:1024x768"  #Image Size: 1024 x 768
        self.file_type = " filetype:jpg"         #Image Type: JPEG
        self.parent_dir = os.path.dirname(os.getcwd())
        self.google_driver = "chromedriver.exe"
        self.img_dir = "Images"
        self.search_xpath = '//*[@id="sbtc"]/div/div[2]/input'  #Search Box Xpath
        self.img_xpath = 'img'


    def initDriver(self):
        os.chdir(self.parent_dir)
        self.google_driver_path = os.path.join(os.getcwd(),"Drivers",self.google_driver)
        self.driver = webdriver.Chrome(executable_path=self.google_driver_path)
                
    def initImgDir(self):
        os.chdir(self.parent_dir) #Change directory to parent directory
        os.makedirs(self.img_dir,exist_ok = True) # Create Image Directory
        self.img_dir_path = os.path.join(os.getcwd(),self.img_dir) 

    def scrollDown(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #Scroll down the search result 
        sleep(0.5) #Interval between scrolling

        
    def searchImage(self,search_label,img_count):
        self.driver.get("https://www.google.com/imghp?hl=EN")
        self.searchbox = self.driver.find_element_by_xpath(self.search_xpath)  #Find Search Box using xpath
        self.searchbox.send_keys(search_label + self.image_size + self.file_type) # Send Search query with image size and type parameters
        self.searchbox.send_keys(Keys.ENTER)  #Hit Enter to search
        elements = self.driver.find_elements_by_class_name('rg_i') #List of matches/elements in search result
        count = 0
        #Loop till the no. of images requested is reached i.e. img_count
        while(count < img_count):
            self.scrollDown()
            img_name = search_label + "_" + str(count+1) +".jpg"   #Name for the image to be stored
            element = elements[count]                              #Move through the search result elements
            element.click()                                        #Click on the selected image thumbnail/element
            sleep(1)                                               #Wait for 1 sec
            final_path = os.path.join(self.img_dir_path,img_name)  #location for storing image
            element2 = self.driver.find_elements_by_class_name('v4dQwb')  #Find the expanded image element after click operation is performed
            
            #Chrome First image thumbnail
            if(count == 0):
                img = element2[0].find_element_by_class_name('n3VNCb')
                action = ActionChains(self.driver)
                action.move_to_element(img).perform() #Move/hover the mouse to center of the expanded image element
                
            #Rest of the Image thumbnails
            else:
                img = element2[1].find_element_by_class_name('n3VNCb')
            
            count+=1    
            sleep(0.5)
            #Internet speeds can vary and result in slower loading
            #can cause wrong url to be read
            #Loop till the image is loaded
            loading = True
            while(loading):
                img_url = img.get_attribute("src")
                if('data:image/jpeg;base64' not in img_url):
                    loading = False
                    
            #Send request using the image url obtained above
            try:
                response = requests.get(img_url)   
            except requests.exceptions.InvalidSchema as exception:
                print("Connection Error/Invalid Url")
                
            #Write the image file is response is 200 (OK)
            if(response.status_code == 200):
                with open(final_path,"wb") as file:
                    file.write(response.content)
            
        


