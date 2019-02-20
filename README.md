# personal-automation
Personal automation scripts/programs.


### town_of_cary_payment.py
DESCRIPTION:    Issues a payment to my Town of Cary (NC) utility bill.

USAGE:          `python3 ./town_of_cary_payment.py -a <payment_amount_in_usd> -c <payment_card>` or
                `python3 ./town_of_cary_payment.py --amount <payment_amount_in_usd> --card <payment_card>`

EXAMPLE USAGE:  `python3 ./town_of_cary_payment.py -a 10.00 -c mo_ofcu`

DEPENDENCIES:   
* Python3 Packages:   selenium, pyvirtualdisplay
  * Note: You can install these via pip3.
* Applications:       Xvfb (X virtual framebuffer, used by pyvirtualdisplay)
  * Note: If you are running ubuntu, you can install this via apt.

NOTES:          
* <payment_card> must be a key in the cardRadioButtonLabels dictionary (stored in this script). This dictionary matches a payment card 'nickname' (defined by you; can be anything) to the corresponding radio button label on the Town of Cary's payment site. You will have to get the radio button label from the payment site's html code.
* 'town_of_cary_login.py' must be located in the same directory as 'town_of_cary_payment.py'. Username and password must be filled in in 'town_of_cary_login.py'. See 'town_of_cary_login.py' for details.


### town_of_cary_login.py
Town of Cary login details used by 'town_of_cary_payment.py'.
