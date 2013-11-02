import datetime
import decimal
import stripe

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template

from firestarter.currency import eur_to_dollars, gbp_to_dollars
from firestarter.models import Order, Reward


def approve_payment(request):
	proj_name = settings.PROJECT_NAME
	stripe_public_key = settings.STRIPE_PUBLIC_KEY

	if request.method == 'POST':
		fd = request.POST.copy()
		if fd['reward'] != 'none':
			fd['reward_name'] = fd['reward']
			fd['reward_short_desc'] = Reward.objects.get(name=fd['reward']).short_desc
			fd['reward'] = True
		else:
			fd['reward'] = False
			fd['reward_name'] = ''
		if fd['ctype'] == 'eur':
			fd['amount_eur'] = fd['amount']
			fd['amount'] = eur_to_dollars(fd['amount'])
		elif fd['ctype'] == 'gbp':
			fd['amount_gbp'] = fd['amount']
			fd['amount'] = gbp_to_dollars(fd['amount'])
		request.session['fd'] = fd
		return render(request, 'payment/confirm.html', locals())
	elif settings.STOP and (settings.DATE - datetime.datetime.now()).days < 0:
		msg = 'The funding campaign is complete and is no longer accepting new contributions.'
		return render(request, 'error.html', locals())
	else:
		request.session['fd'] = {}
		rewards = sorted(Reward.objects.all(), key=lambda i: i.min_amount)
		return render(request, 'payment/cc.html', locals())

def complete_payment(request):
	if request.session['fd']:
		stripe.api_key = settings.STRIPE_PRIVATE_KEY
		proj_name = settings.PROJECT_NAME
		proj_addr = settings.PROJECT_ADDR
		time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
		reward_desc = (Reward.objects.get(name=request.session['fd']['reward_name']).desc if request.session['fd']['reward'] else 'None')

		# amount in cents
		amount = int(request.session['fd']['amount']) * 100
		token = request.session['fd']['stripeToken']
		desc = request.session['fd']['email']

		try:
			o = Order(
				name=(request.session['fd']['sh_name'] if request.session['fd']['sh_name'] else request.session['fd']['cc_name']),
				addr1=request.session['fd']['sh_addr1'],
				addr2=request.session['fd']['sh_addr2'],
				city=request.session['fd']['sh_city'],
				state=request.session['fd']['sh_state'],
				pcode=request.session['fd']['sh_post'],
				country=request.session['fd']['sh_country'],
				reward=(Reward.objects.get(name=request.session['fd']['reward_name']) if request.session['fd']['reward'] else None),
				amount=decimal.Decimal(request.session['fd']['amount']),
				ptype='CC',
				pref=request.session['fd']['cc_type'] + ' x-'+ request.session['fd']['cc_last4'],
				email=request.session['fd']['email'],
				namecredit=request.session['fd']['namecredit'],
				notes=request.session['fd']['notes']
			)
		except:
			msg = "There was a problem saving your order details to the database. Your card has NOT been charged. Please notify the site operator."
			return render(request, 'error.html', locals())

		try:
			charge = stripe.Charge.create(
				amount=amount,
				currency="usd",
				card=token,
				description=desc
			)
			try:
				o.notify = request.session['fd']['notify']
			except:
				pass
			o.save()
			send_mail(
				subject=proj_name+' - Thank you for your contribution',
				message=get_template('notify.txt').render(Context({'order': request.session['fd'], 'proj_name': proj_name, 'proj_addr': proj_addr, 'time': time, 'reward_desc': reward_desc})),
				from_email=settings.NOTIFY_SENDER, 
				recipient_list=[request.session['fd']['email']],
				fail_silently=False)
			request.session['fd'] = {}
			return render(request, 'payment/success.html', locals())
		except stripe.CardError, e:
			msg = "Your card has been declined. Please choose a new card or a new payment method and restart your order."
			return render(request, 'error.html', locals())
		except:
			msg = "There was a problem saving your order. Please contact the site operator immediately to confirm your order completion."
			return render(request, 'error.html', locals())
	else:
		msg = 'Your session data could not be found. Please retry your submission again.'
		return render(request, 'error.html', locals())
