import datetime
import decimal
import json
import os

from django.core.mail import send_mail
from django.shortcuts import render
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.template import Context
from django.template.loader import get_template

from firestarter.currency import get_btc_rate, dollars_to_eur, dollars_to_gbp, eur_to_dollars, gbp_to_dollars
from firestarter.models import Order, Reward, Update, Question
from firestarter.forms import QuestionForm

PAGES = []
for x in os.listdir(os.path.join(settings.PROJECT_PATH, '/templates/pages')):
	PAGES.append((x[:-5], x[:-5].capitalize()))

def intWithCommas(x):
	if x < 0:
		return '-' + intWithCommas(-x)
	result = ''
	while x >= 1000:
		x, r = divmod(x, 1000)
		result = ",%03d%s" % (r, result)
	return "%d%s" % (x, result)

def get_context():
	total = Order.objects.all().aggregate(Sum('amount'))['amount__sum']
	pct = ((100 * float(total) / float(settings.GOAL)) if total else 0)
	c = Context({
		'activepage': 'home',
		'goal': intWithCommas(settings.GOAL),
		'backers': Order.objects.count(),
		'pct': pct,
		'pct_disp': (int(pct) if total else 0),
		'total': (intWithCommas(int(total)) if total else '0'),
		'pages': PAGES,
		'nopay': (True if settings.STOP and (settings.DATE - datetime.datetime.now()).days < 0 else False),
		'days': (settings.DATE - datetime.datetime.now()).days,
		'rewards': sorted(Reward.objects.all(), key=lambda i: i.min_amount),
		'rewards_disclaimer': settings.REWARDS_DISCLAIMER,
		'unum': Update.objects.all().count(),
		'qnum': Question.objects.all().count(),
		'proj_name': settings.PROJECT_NAME,
		'proj_addr': settings.PROJECT_ADDR
		})
	return c

def home(request):
	return render(request, 'home.html', get_context())

def questions(request):
	c = get_context()
	c['activepage'] = 'questions'
	c['questions'] = Question.objects.filter(orig=None).order_by('created_at').reverse()
	if request.method == 'POST':
		c['form'] = QuestionForm(request.POST)
		if c['form'].is_valid():
			f = c['form'].save(commit=False)
			if not f.email and f.notify:
				messages.error(request, "Please provide an email address to receive a notification.")
				return render(request, 'comments.html', c)
			else:
				f.save()
		else:
			messages.error(request, "An error occurred in validation. Please make sure all fields are complete and correct.")
	else:
		c['form'] = QuestionForm()
	return render(request, 'comments.html', c)

def updates(request):
	c = get_context()
	c['activepage'] = 'updates'
	c['updates'] = []
	for u in Update.objects.all().order_by('created_at').reverse():
		c['updates'].append((settings.PROJECT_ADDR+'/updates/#'+str(u.pk), u))
	return render(request, 'updates.html', c)

def choose(request):
	proj_name = settings.PROJECT_NAME
	pay_types = settings.PAY_TYPES
	if settings.STOP and (settings.DATE - datetime.datetime.now()).days < 0:
		msg = 'The funding campaign is complete and is no longer accepting new contributions.'
		return render(request, 'error.html', locals())
	else:
		return render(request, 'payment/choose.html', locals())

def page(request, pagename=''):
	c = get_context()
	c['activepage'] = pagename
	return render(request, 'pages/'+pagename+'.html', c)

@receiver(post_save, sender=Update)
def send_notif(sender, instance, **kwargs):
	proj_name = settings.PROJECT_NAME
	proj_addr = settings.PROJECT_ADDR
	for order in Order.objects.all():
		if order.notify:
			send_mail(subject=proj_name+' - New Update', 
				message=get_template('update.txt').render(Context({'update': instance, 'proj_name': proj_name, 'proj_addr': proj_addr})), 
				from_email=settings.NOTIFY_SENDER, 
				recipient_list=[order.email],
				fail_silently=True)
