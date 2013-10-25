## Firestarter

A Django-based crowdfunding platform that you can host and run yourself. Firestarter allows you to set your own funding goals, and your own rules for collecting money, timing your campaign and rewarding your crowdfunders.

With Firestarter, you can:

 - Accept payments by credit card (Stripe), Bitcoin, or Paypal Account
 - Automatically converts values from BTC, EUR or GBP to USD for display purposes
 - Display campaign progress on the front page, with %, $ and days left to go
 - Quickly set up pages with explanations and info about your project, and have it automatically integrated into the site
 - Create rewards, set descriptions and prices for them, and showcase them on the front page
 - Post Updates about your campaign progress and automatically notify your prior funders by email
 - Allow potential funders to post to the Comments page, and respond to them in real-time
 - View your orders, shipping addresses and more from the admin panel
 - Create your own theme for the templates, based in Bootstrap

Firestarter is a work-in-progress, being developed for the [Fund arkOS](https://fund.arkos.io) campaign. It is in a very early stage so you solely are responsible for any problems you encounter. Firestarter is licensed under AGPLv3.

This project depends on `django-captcha`, `django-gravatar`, `django-widget-tweaks`, `paypalrestsdk` (for PayPal), `south`, and `stripe-python` (for Stripe). 

To use, clone the distro, open `settings.py` and customize the values that you see. Sync the db, then migrate with `manage.py migrate` (used for Captcha). Then you're ready to go!

Pull requests and suggestions welcome!


### Sample Screenshot
![][http://i.imgur.com/QbXAKp2.png]
