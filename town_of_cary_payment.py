#!/usr/bin/python3

# Set user-defined variables (see README.md or helpText)
cardRadioButtonLabels = {
        "mo_cfcu": "10955444",
        "mo_ofcu": "7203136",
        "lh_ofcu": "9463946",
        "mo_lmcu": "6273078",
        "lh_lmcu": "6273080",
	"mo_ssb": "10246840"
}

# Set help text
helpText = """
town_of_cary_payment.py - v20.04

Created by Michael Oglesby for personal use.

DESCRIPTION:    Issues a payment to my Town of Cary (NC) utility bill.

USAGE:          docker run -it --rm town_of_cary_payment -a <payment_amount_in_usd> -c <payment_card>
                    -- or --
                docker run -it --rm town_of_cary_payment --amount <payment_amount_in_usd> --card <payment_card>
                    -- or --
                docker run -it --rm town_of_cary_payment --amount <payment_amount_in_usd> --card-label <payment_card_radio_button_label>
                    -- or --
                docker run -it --rm town_of_cary_payment -a <payment_amount_in_usd> -l <payment_card_radio_button_label>

EXAMPLE USAGE:  docker run -it --rm town_of_cary_payment -a 10.00 -c mo_ofcu

NOTES:          

* If using the '-c'/'--card' option, <payment_card> must be a key in the cardRadioButtonLabels dictionary (stored in this script). This dictionary  matches a payment card 'nickname' (defined by you; can be anything) to the corresponding radio button label on the Town of Cary's payment site. You will have to get the radio button label from the payment site's html code.

* Current contents of cardRadioButtonLabels dictionary (for reference):
    """ + str(cardRadioButtonLabels) + """
"""
hintsText = """\nHints:
* Ensure that town_of_cary_login.py contains your login details.")
* Ensure that for each key/value pair in cardRadioButtonLabels, the key is populated with a card 'nickname' (defined by you; can be anything), and the value is populated with the radio button label for the radio button corresponding to that specific card on the Town of Cary's payment site. You will have to get the radio button label from the payment site's html code."""

# Initial imports
import sys, time, getopt

# Define variables
amount = None
card = None
cardLabel = None

# Get command line arguments
try :
    opts, args = getopt.getopt(sys.argv[1:], "ha:c:l:", ["help", "amount=", "card=", "card-label="])
except :
    print(helpText)
    sys.exit(1)

# Parse command line arguments
for opt, arg in opts :
    if opt in ("-h", "--help") :
        print(helpText)
        sys.exit(0)
    elif opt in ("-a", "--amount") :
        amount = arg
    elif opt in ("-c", "--card") :
        card = arg
    elif opt in ("-l", "--card-label") :
        cardLabel = arg

# Import login details from user defined file (stored in same directory as this script)
try :
    from town_of_cary_login import townOfCaryLogin
except :
    print("Error importing town_of_cary_login... Ensure that town_of_cary_login.py is located in the same directory as this script.")
    sys.exit(1)

# Check command line arguments for validity
invalidArg = False
if card :
    if card not in cardRadioButtonLabels :
        print("Invalid payment card...")
        invalidArg = True
    else :
        cardLabel = cardRadioButtonLabels[card] 
try :
    if float(amount) < 1.0 :
        print("Payment amount must be greater than $1...")
        invalidArg = True
except :
    print("Invalid payment amount...")
    invalidArg = True
if invalidArg :
    sys.exit(1)
if not cardLabel :
    print(helpText)
    sys.exit(1)

# Import selenium and pyvirtualdisplay
try :
    from selenium import webdriver
    from selenium.common import exceptions
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
except :
    print("Error importing selenium... Perhaps the selenium python3 package is not installed?")
    print("Note: You can install this package with pip3.")
    sys.exit(1)

# Print command line arguments
if card :
    print("Preparing to issue a $" + amount + " payment to the Town of Cary using payment card '" + card + "'...")
else :
    print("Preparing to issue a $" + amount + " payment to the Town of Cary using payment card with label '" + cardLabel + "'...")

# Instantiate Chrome driver
try :
    print("Instantiating Chrome selenium webdriver...")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument("disable-dev-shm-usage")
    chrome_options.add_argument('no-sandbox')
    chrome_options.add_argument("start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-blink-features")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=chrome_options)
except Exception as e :
    print("Error instantiating Chrome selenium webdriver (see 'Message' below)... Perhaps geckodriver is not installed?")
    print("Note: you can find geckodriver here: https://github.com/mozilla/geckodriver")
    print(str(e).strip())
    sys.exit(1)

# Execute payment
try :
    print("Executing payment...")
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.get("https://ipn.paymentus.com/cp/tcnc")
    driver.get("https://ipn.paymentus.com/cp/tcnc")
    time.sleep(2)
    driver.find_element_by_id("id_loginId").click()
    time.sleep(2)
    driver.find_element_by_id("id_loginId").send_keys(townOfCaryLogin["username"])
    time.sleep(5)
    driver.find_element_by_id("id_password").click()
    time.sleep(2)
    driver.find_element_by_id("id_password").send_keys(townOfCaryLogin["password"])
    time.sleep(5)
    driver.find_element_by_xpath("//*[@id=\"main-container\"]/div/div[2]/div/form/div/div[4]/div/input").click()
    time.sleep(5)
    driver.find_element_by_link_text("Pay Bill").click()
    driver.find_element_by_id("header.paymentAmount").click()
    driver.find_element_by_id("header.paymentAmount").clear()
    driver.find_element_by_id("header.paymentAmount").send_keys(amount)
    driver.find_element_by_xpath("//*[@id=\"carousel\"]/ul/li[1]").click()
    driver.find_element_by_xpath("//*[@id=\"label-pm-radio-pm-3-" + cardLabel + "\"]/span").click()
    driver.find_element_by_link_text("Continue").click()
    time.sleep(5)
    try :
        driver.find_element_by_link_text("Continue").click()
    except exceptions.NoSuchElementException as e :
        print(str(e).strip())
        print("'Similar Payment' message not received... Continuing...")
    time.sleep(5)
    driver.find_element_by_link_text("Pay $" + amount).click()
    time.sleep(5)
except Exception as e :
    print("Error encountered (see 'Message' below)...")
    print("Closing webdriver and stopping virtual display...")
    driver.close()
    driver.quit()
    print(str(e).strip())
    print(hintsText)
    sys.exit(1)

# Close virtual display and Chrome
print("Closing webdriver and stoping virtualdisplay...")
driver.close()
driver.quit()

print("Success!")
