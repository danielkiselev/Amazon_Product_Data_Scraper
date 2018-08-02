"""
Developed by Daniel Kiselev

"""


import csv
import sys
import warnings
try:
    import bs4
except ImportError:
    warnings.warn("dependency not found, please install bs4")
try:
    import requests
except ImportError:
    warnings.warn("dependency not found, please install requests")

def name(soupDataLocal):
    productTitle = (soupDataLocal.find(attrs={"id": "productTitle"}))
    if productTitle is None:
        print("Item is Irregular-Naming")
        return None
    else:
        productTitleString = ''.join(productTitle)
        titleStripped = productTitleString.strip()
        print("Product: ",titleStripped)
        return str(titleStripped)


def parseMerchant(soupDataLocal):
    merchantInfo = (soupDataLocal.find(attrs={"id": "merchant-info"}))
    merchantInfoString = str(merchantInfo)
    if merchantInfoString.__contains__("sold by Amazon.com."):
        print("Vendor: ","Amazon.com")
        return "Amazon.com"
    elif merchantInfoString.__contains__("by"):
        merchantInfoA = (merchantInfo.find_all('a'))
        merchantData = ''.join(merchantInfoA[0])
        merchantString = str(merchantData.strip())
        print("Vendor: ",merchantString)
        return merchantString
    else:
        print("Item is Irregular-Merchant")


def standardPricing(soupDataLocal):
    unifiedPrice = (soupDataLocal.find(attrs={"data-feature-name": "unifiedPrice"}))
    if unifiedPrice is None:
        print("Item is Irregular-Pricing Standard")
        return None
    priceBlock = unifiedPrice.find(attrs={"class": "a-size-medium a-color-price"})
    priceString = ''.join(priceBlock)
    priceStripped = priceString.strip()
    print("Price: ",priceStripped)
    return str(priceStripped)

def alternativePricing(soupDataLocal):
    combinedBuyBox = (soupDataLocal.find(attrs={"id": "combinedBuyBox"}))
    if combinedBuyBox is None:
        print("Item is Irregular-Pricing alternative")
        return None
    priceBlock = combinedBuyBox.find(attrs={"class": "a-size-medium a-color-price offer-price a-text-normal"})
    priceString = ''.join(priceBlock)
    priceStripped = priceString.strip()
    print("Price: ",priceStripped)
    return str(priceStripped)

def gamePricing(soupDataLocal):
    mediaPrice = (soupDataLocal.find(attrs={"data-feature-name":"mediaPrice" }))
    if mediaPrice is None:
        print("Item is Irregular-Pricing Gaming")
        return None
    print(mediaPrice)
    priceBlock = mediaPrice.find(attrs={"id": "priceblock_ourprice"})
    priceDollar = priceBlock.find(attrs={"class": "buyingPrice"})
    priceCent = priceBlock.find(attrs={"class": "verticalAlign a-size-large priceToPayPadding"})
    priceDollarString = ''.join(priceDollar)
    priceDollarStripped = priceDollarString.strip()
    priceCentString = ''.join(priceCent)
    priceCentStripped = priceCentString.strip()
    priceString = ''.join(['$',priceDollarStripped,'.' ,priceCentStripped])
    priceStripped = priceString.strip()
    print("Price: ",priceStripped)
    return str(priceStripped)

def textBookPricing(soupDataLocal):
    mediaTab = (soupDataLocal.find(attrs={"id": "mediaTab_content_landing"}))
    if mediaTab is None:
        print("Item is Irregular-Pricing textBook")
        return None
    priceBlock = mediaTab.find(attrs={"class": "a-size-medium a-color-price header-price"})
    priceString = ''.join(priceBlock)
    priceStripped = priceString.strip()
    print("Price: ",priceStripped)
    return str(priceStripped)


def productCSV(localName, localPrice, localSeller):
    fieldNames = ['Name', 'Price', 'Seller']
    try:
        open('amazonProductData.csv', 'r')
        with open('amazonProductData.csv', 'a', newline='') as f:
            theWriter = csv.DictWriter(f, fieldnames=fieldNames)
            theWriter.writerow({'Name': localName, 'Price': localPrice, 'Seller': localSeller})
    except IOError:
        with open('amazonProductData.csv', 'w', newline='') as f:
            thewriter = csv.DictWriter(f, fieldnames=fieldNames)
            thewriter.writeheader()
            thewriter.writerow({'Name': localName, 'Price': localPrice, 'Seller': localSeller})



def main():
    url = None
    try:
        url = str(sys.argv[1])
        html_contents = requests.get(url,
                                     headers={
                                         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36',
                                         'Upgrade-Insecure-Requests': '1',
                                         'x-runtime': '148ms'},
                                     allow_redirects=True).content
        soupData = None
        try:
            soupData = bs4.BeautifulSoup(html_contents, 'lxml')
        except:
            warnings.warn("Error parsing the html contents of your page please ensure you have 'lxml' installed")

        nameFound = None
        pricingFound = None
        merchantFound = None
        nameFound = name(soupData)
        merchantFound = parseMerchant(soupData)
        pricingFound = standardPricing(soupData)
        while pricingFound is None:
            pricingFound = alternativePricing(soupData)
            if pricingFound is not None:
                break
            pricingFound = gamePricing(soupData)
            if pricingFound is not None:
                break
            pricingFound = textBookPricing(soupData)
            if pricingFound is not None:
                break
            print("Unable to fetch pricing")
        productCSV(nameFound, pricingFound, merchantFound)

    except IndexError:
        print("No argument found.")
        print("Pass in Amazon product page URL")
        print("Exiting")
        sys.exit()

if __name__ == "__main__":
    main()




