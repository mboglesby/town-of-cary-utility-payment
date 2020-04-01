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

USAGE:          python3 ./town_of_cary_payment.py -a <payment_amount_in_usd> -c <payment_card>
                    -- or --
                python3 ./town_of_cary_payment.py --amount <payment_amount_in_usd> --card <payment_card>
                    -- or --
                python3 ./town_of_cary_payment.py --amount <payment_amount_in_usd> --card-label <payment_card_radio_button_label>
                    -- or --
                python3 ./town_of_cary_payment.py -a <payment_amount_in_usd> -l <payment_card_radio_button_label>
                    -- or, if executed using docker image built from Dockerfile-town_of_cary_payment --
                docker run -it --rm town_of_cary_payment -a <payment_amount_in_usd> -c <payment_card>

EXAMPLE USAGE:  python3 ./town_of_cary_payment.py -a 10.00 -c mo_ofcu

DEPENDENCIES:   Python3 Packages:   selenium, pyvirtualdisplay
                Applications:       Firefox, Mozilla Geckodriver, Xvfb (X virtual framebuffer, used by pyvirtualdisplay)

NOTES:          

* If using the '-c'/'--card' option, <payment_card> must be a key in the cardRadioButtonLabels dictionary (stored in this script). This dictionary  matches a payment card 'nickname' (defined by you; can be anything) to the corresponding radio button label on the Town of Cary's payment site. You will have to get the radio button label from the payment site's html code.

* Current contents of cardRadioButtonLabels dictionary (for reference):
    """ + str(cardRadioButtonLabels) + """

* town_of_cary_login.py must be located in the same directory as town_of_cary_payment.py. Username and password must be filled in in town_of_cary_login.py. See town_of_cary_login.py for details.
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
    elif opt in ("-l", "--card-label") :
        cardLabel = arg

# Import login details from user defined file (stored in same directory as this script)
try :
    from town_of_cary_login import townOfCaryLogin
except :
    print("Error importing town_of_cary_login... Ensure that town_of_cary_login.py is located in the same directory as this script.")
    sys.exit(0)

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
    sys.exit(0)
if not cardLabel :
    print(helpText)
    sys.exit(0)

# Import selenium and pyvirtualdisplay
try :
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from selenium.common import exceptions
except :
    print("Error importing selenium... Perhaps the selenium python3 package is not installed?")
    print("Note: You can install this package with pip3.")
    sys.exit(0)
try :
    from pyvirtualdisplay import Display
except :
    print("Error importing pyvirtualdisplay... Perhaps the pyvirtualdisplay python3 package is not installed?")
    print("Note: You can install this package with pip3.")
    sys.exit(0)

# Print command line arguments
if card :
    print("Preparing to issue a $" + amount + " payment to the Town of Cary using payment card '" + card + "'...")
else :
    print("Preparing to issue a $" + amount + " payment to the Town of Cary using payment card with label '" + cardLabel + "'...")

# Instantiate virtual display
print("Starting virtual display...")
try :
    display = Display(visible=0, size=(1440, 900))
    display.start()
except Exception as e :
    print("Error starting virtual display (see 'Message' below)... Perhaps Xvfb is not installed?")
    print("Note: if you are running on ubuntu, you can install this with apt.")
    print(str(e).strip())
    sys.exit(0)

# Instantiate Firefox driver
try :
    print("Instantiating Firefox selenium webdriver...")
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
except Exception as e :
    print("Error instantiating Firefox selenium webdriver (see 'Message' below)... Perhaps geckodriver is not installed?")
    print("Note: you can find geckodriver here: https://github.com/mozilla/geckodriver")
    print("Stopping virtual display...")
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
    display.stop()
    print(str(e).strip())
    print(hintsText)
    sys.exit(0)

# Close virtual display and Firefox
print("Closing webdriver and stoping virtualdisplay...")
driver.close()
driver.quit()
display.stop()

print("Success!")
