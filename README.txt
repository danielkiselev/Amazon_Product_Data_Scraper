Developed by Daniel Kiselev

File:Beautiful_Parser.py

The purpose of this script is to take an amazon url and to record the name price and seller into a csv file. 

Required Dependencies(It should throw you warnings and instruct you to install them if they are unavailable)
beautifulsoup4
requests
lxml

To run please pass in an amazon page URL as a parameter.
Below is an example for Window's Powershell

python C:\Users\danie\Desktop\Beautiful_Parser.py "https://www.amazon.com/dp/B01G3WMPII/ref=sspa_dk_detail_2?psc=1&pd_rd_i=B01G3WMPII&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=1713835751726239774&pf_rd_r=VZC21SVHJ01RE8BHBXZ5&pd_rd_wg=0I2CU&pf_rd_s=desktop-dp-sims&pf_rd_t=40701&pd_rd_w=mUeOU&pf_rd_i=desktop-dp-sims&pd_rd_r=f8a1fdd3-6543-11e8-bab5-6f0e79bbd50f"

You will get a few outputs in the console and the resulting data will be properly formatted and saved to "amazonProductData.csv"
The csv file is located in your terminal path. If a csv file doesn't exist in the path then one will be created, otherwise it will
append the existing data.

The console print out in this example is:

Product:  Coravin Model Two Elite Wine Preservation System, Silver
Vendor:  Amazon.com
Price:  $318.91


I tested it on a variety of pages and it SHOULD work on all physical items. Digital items like kindle books and music were not tested and are presumed to not work and may throw errors.