# personal-automation

This repo contains a Python script that can be used to issue a payment for a Town of Cary (NC) utility bill. This script can be built into a docker image that includes all required dependencies. 

To build the docker image, execute the following steps:

1. Replace the contents of 'town_of_cary_login.py' with your Town of Cary Utiilities login details.

2. Build the docker image.

`docker build -t town_of_cary_payment:20.04 -f Dockerfile-town_of_cary_payment .`
* Note: 'Dockerfile-town_of_cary_payment', 'town_of_cary_payment.py', and 'town_of_cary_login.py' must all be located in the same directory, and the build command must be run from within that directory.

Once the docker image is built, you can use it to to execute the town_of_cary_payment.py script as follows:

`docker run -it --rm town_of_cary_payment:20.04 -a <payment_amount_in_usd> -c <payment_card>` 

-- or --

`docker run -it --rm town_of_cary_payment --amount <payment_amount_in_usd> --card <payment_card>`

-- or --

`docker run -it --rm town_of_cary_payment --amount <payment_amount_in_usd> --card-label <payment_card_radio_button_label>`

-- or --

`docker run -it --rm town_of_cary_payment:20.04 -a <payment_amount_in_usd> -l <payment_card_radio_button_label>

..for example:
`docker run -it --rm town_of_cary_payment:20.04 -a 10.00 -c mo_ofcu`

