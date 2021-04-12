"""
File name: example_test.py
Description:  Example for Auto image downloader usage
OS:  Windows 
Author:  Tejas Anilkumar P.  <tpandara@andrew.cmu.edu>
Date:  04/11/2021
   
Carnegie Mellon University
"""

from auto_image_downloader import AutoImageDownloader
from time import sleep

def main():
   aid = AutoImageDownloader()
   aid.searchImage("Dog",2)
   sleep(0.5)
   aid.searchImage("Rabbit",2)
   sleep(0.5)
   aid.searchImage("Cat",2)

  
if __name__=='__main__':
    main()
