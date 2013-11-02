import datetime
import decimal
import paypalrestsdk

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template

from firestarter.models import Reward, Order
from firestarter.currency import dollars_to_eur, dollars_to_gbp, eur_to_dollars, gbp_to_dollars


def approve_payment(request):
	proj_name = settings.PROJECT_NAME
	if request.method == 'POST':
		fd = request.POST.copy()
		fd['ptype'] = 'PP'
		if fd['reward'] != 'none':
			fd['reward_name'] = fd['reward']
			fd['reward_short_desc'] = Reward.objects.get(name=fd['reward']).short_desc
			fd['reward'] = True
		else:
			fd['reward'] = False
			fd['reward_name'] = 'None'
			fd['reward_short_desc'] = 'No reward'
		if fd['ctype'] == 'eur':
			fd['amount_eur'] = fd['amount']
			fd['amount'] = eur_to_dollars(fd['amount'])
		elif fd['ctype'] == 'gbp':
			fd['amount_gbp'] = fd['amount']
			fd['amount'] = gbp_to_dollars(fd['amount'])
		request.session['fd'] = fd

		paypalrestsdk.configure({
			'mode': settings.PAYPAL_MODE,
			'client_id': settings.PAYPAL_CLIENT_ID,
			'client_secret': settings.PAYPAL_CLIENT_SECRET
			})
		pmt = paypalrestsdk.Payment({
			'intent': 'sale',
			'payer': {
				'payment_method': 'paypal'
				},
			'redirect_urls': {
				'return_url': settings.PROJECT_ADDR + '/c/PP/confirm',
				'cancel_url': settings.PROJECT_ADDR + '/c/PP/cancel'
				},
			'transactions': [{
				'item_list': {
					'items': [{
						'name': request.session['fd']['reward_name'],
						'sku': request.session['fd']['reward_name'],
						'price': str(decimal.Decimal(request.session['fd']['amount']).quantize(decimal.Decimal(10) ** -2)),
						'currency': 'USD',
						'quantity': 1
						}]
					},
				'amount': {
					'total': str(decimal.Decimal(request.session['fd']['amount']).quantize(decimal.Decimal(10) ** -2)),
					'currency': 'USD'
					},
				'description': request.session['fd']['reward_name'] + ' - ' + request.session['fd']['reward_short_desc']
				}]
			})

		if pmt.create():
			request.session['paypal_id'] = pmt['id']
			for link in pmt.links:
				if link['method'] == 'REDIRECT':
					return HttpResponseRedirect(link.href)
		else:
			msg = 'There was an error in creating your payment. Please try again. If this problem persists, please contact the site operator.\n'+str(pmt.error)
			return render(request, 'error.html', locals())
	elif settings.STOP and (settings.DATE - datetime.datetime.now()).days < 0:
		msg = 'The funding campaign is complete and is no longer accepting new contributions.'
		return render(request, 'error.html', locals())
	else:
		request.session['fd'] = {}
		rewards = sorted(Reward.objects.all(), key=lambda i: i.min_amount)
		return render(request, 'payment/pp.html', locals())

def handle_response(request):
	proj_name = settings.PROJECT_NAME
	paypalrestsdk.configure({
		'mode': settings.PAYPAL_MODE,
		'client_id': settings.PAYPAL_CLIENT_ID,
		'client_secret': settings.PAYPAL_CLIENT_SECRET
	})
	if request.method == 'GET':
		data = paypalrestsdk.Payment.find(request.session['paypal_id'])
		request.session['paypal_pid'] = request.GET['PayerID']
		if data['state'] == 'created':
			return render(request, 'payment/confirm.html', locals())
		else:
			request.session['paypal_id'] = {}
			request.session['paypal_pid'] = {}
			msg = 'Your payment was not approved by PayPal. Please check your account.'
			return render(request, 'error.html', locals())
	else:
		request.session['paypal_id'] = {}
		request.session['paypal_pid'] = {}
		msg = 'An unexpected error has occurred. Please try again.'
		return render(request, 'error.html', locals())

def complete_payment(request):
	paypalrestsdk.configure({
		'mode': settings.PAYPAL_MODE,
		'client_id': settings.PAYPAL_CLIENT_ID,
		'client_secret': settings.PAYPAL_CLIENT_SECRET
	})
	if request.session['fd'] and request.session['paypal_id']:
		time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
		reward_desc = (Reward.objects.get(name=request.session['fd']['reward_name']).desc if request.session['fd']['reward'] else 'None')
		pmt = paypalrestsdk.Payment.find(request.session['paypal_id'])
		if pmt['state'] == 'created':
			if pmt.execute({"payer_id": request.session['paypal_pid']}):
				o = Order(
					name=(request.session['fd']['namecredit'] if request.session['fd']['namecredit'] else 'PayPal User'),
					addr1='',
					addr2='',
					city='',
					state='',
					pcode='',
					country='',
					reward=(Reward.objects.get(name=request.session['fd']['reward_name']) if request.session['fd']['reward'] else None),
					amount=decimal.Decimal(request.session['fd']['amount']),
					ptype='PP',
					pref=request.session['paypal_id'],
					email=request.session['fd']['email'],
					namecredit=request.session['fd']['namecredit'],
					notes=request.session['fd']['notes']
				)
				request.session['paypal_id'] = {}
				request.session['paypal_pid'] = {}
				try:
					o.notify = request.session['fd']['notify']
				except:
					pass
				o.save()
				if request.session['fd']['email']:
					send_mail(
						subject=settings.PROJECT_NAME+' - Thank you for your contribution',
						message=get_template('notify.txt').render(Context({'order': request.session['fd'], 'proj_name': settings.PROJECT_NAME, 'proj_addr': settings.PROJECT_ADDR, 'time': time, 'reward_desc': reward_desc})),
						from_email=settings.NOTIFY_SENDER, 
						recipient_list=[request.session['fd']['email']],
						fail_silently=True)
				request.session['fd'] = {}
				return render(request, 'payment/success.html', locals())
			else:
				request.session['paypal_id'] = {}
				request.session['paypal_pid'] = {}
				msg = 'There was an error with your payment.\n'+str(pmt.error)
				return render(request, 'error.html', locals())
		else:
			request.session['paypal_id'] = {}
			request.session['paypal_pid'] = {}
			msg = 'An unexpected error has occurred. Please try again.'
			return render(request, 'error.html', locals())
	else:
		msg = 'Your session data could not be found. Please retry your submission again.'
		return render(request, 'error.html', locals())

def cancel(request):
	msg = 'You cancelled your PayPal transaction. Please try again.'
	return render(request, 'error.html', locals())
