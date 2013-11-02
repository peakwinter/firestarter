import datetime
import decimal

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template

from firestarter.currency import get_btc_rate
from firestarter.models import Order, Reward

def approve_payment(request):
	proj_name = settings.PROJECT_NAME

	if request.method == 'POST':
		fd = request.POST.copy()
		if fd['reward'] != 'none':
			fd['reward_name'] = fd['reward']
			fd['reward_short_desc'] = Reward.objects.get(name=fd['reward']).short_desc
			fd['reward'] = True
		else:
			fd['reward'] = False
			fd['reward_name'] = ''
		fd['ptype'] = 'BC'
		request.session['fd'] = fd
		btc_donate_to = settings.BTC_ADDR
		return render(request, 'payment/confirm.html', locals())
	elif settings.STOP and (settings.DATE - datetime.datetime.now()).days < 0:
		msg = 'The funding campaign is complete and is no longer accepting new contributions.'
		return render(request, 'error.html', locals())
	else:
		request.session['fd'] = {}
		rewards = sorted(Reward.objects.all(), key=lambda i: i.min_amount)
		return render(request, 'payment/bc.html', locals())

def complete_payment(request):
	proj_name = settings.PROJECT_NAME
	proj_addr = settings.PROJECT_ADDR
	time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
	if request.session['fd']:
		reward_desc = (Reward.objects.get(name=request.session['fd']['reward_name']).desc if request.session['fd']['reward'] else 'None')
		btc = True
		o = Order(
			name=(request.session['fd']['namecredit'] if request.session['fd']['namecredit'] else (request.session['fd']['sh_name'] if request.session['fd']['sh_name'] else 'Bitcoin User')),
			addr1=request.session['fd']['sh_addr1'],
			addr2=request.session['fd']['sh_addr2'],
			city=request.session['fd']['sh_city'],
			state=request.session['fd']['sh_state'],
			pcode=request.session['fd']['sh_post'],
			country=request.session['fd']['sh_country'],
			reward=(Reward.objects.get(name=request.session['fd']['reward_name']) if request.session['fd']['reward'] else None),
			amount=decimal.Decimal(float(get_btc_rate()) * float(request.session['fd']['amount'])),
			ptype='BC',
			pref=request.session['fd']['ref'],
			email=request.session['fd']['email'],
			namecredit=request.session['fd']['namecredit'],
			notes=request.session['fd']['notes']
		)
		try:
			o.notify = request.session['fd']['notify']
		except:
			pass
		o.save()
		if request.session['fd']['email']:
			send_mail(
				subject='Thank you for your contribution',
				message=get_template('notify.txt').render(Context({'order': request.session['fd'], 'proj_name': proj_name, 'proj_addr': proj_addr, 'time': time, 'reward_desc': reward_desc})),
				from_email=settings.NOTIFY_SENDER, 
				recipient_list=[request.session['fd']['email']],
				fail_silently=False)
		request.session['fd'] = {}
		return render(request, 'payment/success.html', locals())
	else:
		msg = 'Your session data could not be found. Please retry your submission again.'
		return render(request, 'error.html', locals())
