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
for x in os.listdir('firestarter/templates/pages'):
    PAGES.append((x[:-5], x[:-5].capitalize()))

def intWithCommas(x):
	if x < 0:
		return '-' + intWithCommas(-x)
	result = ''
	while x >= 1000:
		x, r = divmod(x, 1000)
		result = ",%03d%s" % (r, result)
	return "%d%s" % (x, result)

def get_numbers():
	goal = intWithCommas(settings.GOAL)
	total = Order.objects.all().aggregate(Sum('amount'))['amount__sum']
	backers = Order.objects.count()
	if total:
		pct = 100 * float(total) / float(settings.GOAL)
		pct_disp = int(pct)
		total = intWithCommas(int(total))
	else:
		pct = 0
		pct_disp = 0
		total = '0'
	days = (settings.DATE - datetime.datetime.now()).days
	return goal, total, backers, pct, pct_disp, days

def get_rewards():
	rewards = Reward.objects.all()
	rewards_disclaimer = settings.REWARDS_DISCLAIMER
	return rewards, rewards_disclaimer

def home(request):
	pages = PAGES
	proj_name = settings.PROJECT_NAME
	proj_addr = settings.PROJECT_ADDR
	slogan = settings.PROJECT_SLOGAN
	if settings.STOP and (settings.DATE - datetime.datetime.now()).days < 0:
		nopay = True
	goal, total, backers, pct, pct_disp, days = get_numbers()
	rewards, rewards_disclaimer = get_rewards()
	activepage = 'home'
	unum = Update.objects.all().count()
	qnum = Question.objects.all().count()
	return render(request, 'home.html', locals())

def questions(request):
	pages = PAGES
	proj_name = settings.PROJECT_NAME
	proj_addr = settings.PROJECT_ADDR
	slogan = settings.PROJECT_SLOGAN
	if settings.STOP and (settings.DATE - datetime.datetime.now()).days < 0:
		nopay = True
	goal, total, backers, pct, pct_disp, days = get_numbers()
	rewards, rewards_disclaimer = get_rewards()
	unum = Update.objects.all().count()
	qnum = Question.objects.all().count()
	activepage = 'questions'
	questions = Question.objects.filter(orig=None).order_by('created_at').reverse()
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			f = form.save(commit=False)
			if not f.email and f.notify:
				messages.error(request, "Please provide an email address to receive a notification.")
				return render(request, 'comments.html', locals())
			else:
				f.save()
		else:
			messages.error(request, "An error occurred in validation. Please make sure all fields are complete and correct.")
	else:
		form = QuestionForm()
	return render(request, 'comments.html', locals())

def updates(request):
	pages = PAGES
	proj_name = settings.PROJECT_NAME
	proj_addr = settings.PROJECT_ADDR
	slogan = settings.PROJECT_SLOGAN
	if settings.STOP and (settings.DATE - datetime.datetime.now()).days < 0:
		nopay = True
	goal, total, backers, pct, pct_disp, days = get_numbers()
	rewards, rewards_disclaimer = get_rewards()
	unum = Update.objects.all().count()
	qnum = Question.objects.all().count()
	activepage = 'updates'
	updates = []
	for u in Update.objects.all().order_by('created_at').reverse():
		updates.append((settings.PROJECT_ADDR+'/updates/#'+str(u.pk), u))
	return render(request, 'updates.html', locals())

def choose(request):
	pay_types = settings.PAY_TYPES
	if settings.STOP and (settings.DATE - datetime.datetime.now()).days < 0:
		msg = 'The funding campaign is complete and is no longer accepting new contributions.'
		return render(request, 'error.html', locals())
	else:
		return render(request, 'payment/choose.html', locals())

def page(request, pagename=''):
	pages = PAGES
	proj_name = settings.PROJECT_NAME
	proj_addr = settings.PROJECT_ADDR
	slogan = settings.PROJECT_SLOGAN
	if settings.STOP and (settings.DATE - datetime.datetime.now()).days < 0:
		nopay = True
	goal, total, backers, pct, pct_disp, days = get_numbers()
	rewards, rewards_disclaimer = get_rewards()
	unum = Update.objects.all().count()
	qnum = Question.objects.all().count()
	activepage = pagename
	return render(request, 'pages/'+pagename+'.html', locals())

@receiver(post_save, sender=Update)
def send_notif(sender, instance, **kwargs):
	proj_name = settings.PROJECT_NAME
	proj_addr = settings.PROJECT_ADDR
	for order in Order.objects.all():
		if order.notify:
			send_mail(subject=proj_name+' - New Update', 
				message=get_template('update.txt').render(Context({'update': sender, 'proj_name': proj_name, 'proj_addr': proj_addr})), 
				from_email=settings.NOTIFY_SENDER, 
				recipient_list=[order.email],
				fail_silently=True)
