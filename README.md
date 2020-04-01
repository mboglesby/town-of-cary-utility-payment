# personal-automation
Personal automation scripts/programs.

### Dockerfile-town_of_cary_payment
This Dockerfile can be used to build a docker image containing the town_of_cary_payment.py script and all dependencies. This eliminates the need to install the dependencies within your local environment.

To build the docker image, run:

`docker build -t town_of_cary_payment:20.04 -f Dockerfile-town_of_cary_payment .`
* Note: 'Dockerfile-town_of_cary_payment', 'town_of_cary_payment.py', and 'town_of_cary_login.py' must all be located in the same directory, and the build command must be run from within that directory.

Once the docker image is built, you can use it to to execute the town_of_cary_payment.py script as follows:

`docker run -it --rm town_of_cary_payment:20.04 -a <payment_amount_in_usd> -c <payment_card>` 

-- or --

`docker run -it --rm town_of_cary_payment:20.04 -a <payment_amount_in_usd> -l <payment_card_radio_button_label>

..for example:
`docker run -it --rm town_of_cary_payment:20.04 -a 10.00 -c mo_ofcu`


### town_of_cary_payment.py
DESCRIPTION:    Issues a payment to my Town of Cary (NC) utility bill.

USAGE:          

`python3 ./town_of_cary_payment.py -a <payment_amount_in_usd> -c <payment_card>`

-- or --

`python3 ./town_of_cary_payment.py --amount <payment_amount_in_usd> --card <payment_card>`

..for example:
`python3 ./town_of_cary_payment.py -a 10.00 -c mo_ofcu`

DEPENDENCIES:   
* Python3 Packages:   selenium, pyvirtualdisplay
  * Note: You can install these via pip3.
* Applications:       Firefox, Mozilla Geckodriver, Xvfb (X virtual framebuffer, used by pyvirtualdisplay)
  * Note: If you are running ubuntu, you can install Firefox and Xvfb via apt.
  * Note: geckodriver can be installed from here: https://github.com/mozilla/geckodriver/releases

NOTES:          
* <payment_card> must be a key in the cardRadioButtonLabels dictionary (stored in this script). This dictionary matches a payment card 'nickname' (defined by you; can be anything) to the corresponding radio button label on the Town of Cary's payment site. You will have to get the radio button label from the payment site's html code.
* 'town_of_cary_login.py' must be located in the same directory as 'town_of_cary_payment.py'. Username and password must be filled in in 'town_of_cary_login.py'. See 'town_of_cary_login.py' for details.


### town_of_cary_login.py
This file contains Town of Cary login details in python dictionary format.  It is used by 'town_of_cary_payment.py'.
