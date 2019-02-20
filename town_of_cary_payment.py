#!/usr/bin/python3

# Imports
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common import exceptions
from pyvirtualdisplay import Display
import sys, time, getopt

# Import login details from user defined file (stored in same directory as this script)
from town_of_cary_login import townOfCaryLogin

# Define variables
amount = ''
card = ''
cardRadioButtonLabels = {
        "mo_ofcu": "7203136",
        "mo_lmcu": "6273078",
        "lh_lmcu": "6273080"
}
helpText = """
town_of_cary_payment.py - v0.1

Created by Michael Oglesby for personal use.

DESCRIPTION:    Issues a payment to my Town of Cary (NC) utility bill.

USAGE:          python3 ./town_of_cary_payment.py -a <payment_amount_in_usd> -c <payment_card>
                    -- or --
                python3 ./town_of_cary_payment.py --amount <payment_amount_in_usd> --card <payment_card>

EXAMPLE USAGE:  python3 ./town_of_cary_payment.py -a 10.00 -c mo_ofcu

DEPENDENCIES:   Python3 Packages:   selenium, pyvirtualdisplay
                Applications:       Xvfb (X virtual framebuffer, used by pyvirtualdisplay)

NOTES:          

**<payment_card> must be a key in the cardRadioButtonLabels dictionary (stored in this script). This dictionary 
    matches a payment card to the corresponding radio button label on the Town of Cary's payment site.

**Current contents of cardRadioButtonLabels dictionary (for reference):
    """ + str(cardRadioButtonLabels) + """

**town_of_cary_login.py must be located in the same directory as town_of_cary_payment.py. Username and
    password must be filled in in town_of_cary_login.py. See town_of_cary_login.py for details.
"""

# Get command line arguments
try :
    opts, args = getopt.getopt(sys.argv[1:], "ha:c:", ["help", "amount=", "card="])
except :
    print(helpText)
    sys.exit(0)

# Parse command line arguments
for opt, arg in opts :
    if opt in ("-h", "--help") :
        print(helpText)
        sys.exit(0)
    elif opt in ("-a", "--amount") :
        amount = arg
    elif opt in ("-c", "--card") :
        card = arg

# Check command line arguments for validity
invalidArg = False
if card not in cardRadioButtonLabels :
    print("Invalid payment card...")
    invalidArg = True
try :
    if float(amount) < 1.0 :
        print("Payment amount must be greater than $1...")
        invalidArg = True
except :
    print("Invalid payment amount...")
    invalidArg = True
if invalidArg :
    sys.exit(0)

# Print command line arguments
print("Preparing to issue a $" + amount + " payment to the Town of Cary using payment card '" + card + "'...")

# Instantiate virtual display
print("Starting virtual display...")
display = Display(visible=0, size=(800, 600))
display.start()

# Instantiate Firefox driver
try :
    print("Instantiating Firefox selenium webdriver...")
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
except Exception as e :
    print("Error encountered (see below)... Stopping virtual display...")
    display.stop()
    print(str(e).strip())
    sys.exit(0)

# Execute payment
try :
    print("Executing payment...")
    driver.get("https://ipn.paymentus.com/cp/tcnc")
    driver.find_element_by_id("id_loginId").click()
    driver.find_element_by_id("id_loginId").clear()
    driver.find_element_by_id("id_loginId").send_keys(townOfCaryLogin["username"])
    driver.find_element_by_id("id_password").click()
    driver.find_element_by_id("id_password").clear()
    driver.find_element_by_id("id_password").send_keys(townOfCaryLogin["password"])
    driver.find_element_by_xpath("//*[@id=\"main-container\"]/div/div[2]/div/form/div/div[4]/div/input").click()
    driver.find_element_by_link_text("Pay Bill").click()
    driver.find_element_by_id("header.paymentAmount").click()
    driver.find_element_by_id("header.paymentAmount").clear()
    driver.find_element_by_id("header.paymentAmount").send_keys(amount)
    driver.find_element_by_xpath("//*[@id=\"carousel\"]/ul/li[1]").click()
    driver.find_element_by_xpath("//*[@id=\"label-pm-radio-pm-3-" + cardRadioButtonLabels[card] + "\"]/span").click()
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
    print("Error encountered (see below)... Closing webdriver and stopping virtual display...")
    driver.close()
    driver.quit()
    display.stop()
    print(str(e).strip())
    sys.exit(0)

# Close virtual display and Firefox
print("Closing webdriver and stoping virtualdisplay...")
driver.close()
driver.quit()
display.stop()

print("Success!")
