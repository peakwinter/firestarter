import datetime
import decimal
import json
import urllib2

from django.conf import settings
from django.utils import timezone

from firestarter.models import Value


def dollars_to_btc(value):
	x = decimal.Decimal(value) / decimal.Decimal(get_btc_rate())
	return x.quantize(decimal.Decimal(10) ** -5)

def btc_to_dollars(value):
	x = decimal.Decimal(get_btc_rate()) / decimal.Decimal(value)
	return x.quantize(decimal.Decimal(10) ** -5)

def dollars_to_eur(value):
	x = decimal.Decimal(value) / decimal.Decimal(get_rate('EUR', 'USD'))
	return x.quantize(decimal.Decimal(10) ** -2)

def eur_to_dollars(value):
	x = decimal.Decimal(value) / decimal.Decimal(get_rate('USD', 'EUR')) 
	return x.quantize(decimal.Decimal(10) ** -2)

def dollars_to_gbp(value):
	x = decimal.Decimal(value) / decimal.Decimal(get_rate('GBP', 'USD'))
	return x.quantize(decimal.Decimal(10) ** -2)

def gbp_to_dollars(value):
	x = decimal.Decimal(value) / decimal.Decimal(get_rate('USD', 'GBP'))
	return x.quantize(decimal.Decimal(10) ** -2)

def get_btc_rate():
	current_time = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
	if not Value.objects.filter(type='BTC'):
		Value.objects.create(type='BTC', value=json.loads(urllib2.urlopen('https://api.bitcoinaverage.com/ticker/USD').read())['24h_avg'], update=True)
		return Value.objects.filter(type='BTC')[0].value
	elif ((current_time - Value.objects.filter(type='BTC')[0].created_at).days >= 1) and Value.objects.filter(type='BTC')[0].update:
		try:
			data = json.loads(urllib2.urlopen('https://api.bitcoinaverage.com/ticker/USD').read())
			v = Value.objects.filter(type='BTC')[0]
			v.value = data['24h_avg']
			v.created_at = current_time
			v.save()
		except:
			pass
		return Value.objects.filter(type='BTC')[0].value
	else:
		return Value.objects.filter(type='BTC')[0].value

def get_rate(src='', tgt=''):
	current_time = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
	key = settings.CURRENCY_API_KEY
	if not Value.objects.filter(type=src+'-'+tgt):
		try:
			data = json.loads(urllib2.urlopen('http://currency-api.appspot.com/api/'+src+'/'+tgt+'.json?key='+key).read())
			if data['success']:
				Value.objects.create(type=src+'-'+tgt, value=data['rate'], update=True)
			else:
				raise Exception('Currency API encountered an error: '+str(data))
		except Exception, e:
			raise Exception('An error occurred with Currency API check: '+str(e))
		return Value.objects.filter(type=src+'-'+tgt)[0].value
	elif ((current_time - Value.objects.filter(type=src+'-'+tgt)[0].created_at).days >= 1) and Value.objects.filter(type=src+'-'+tgt)[0].update:
		try:
			data = json.loads(urllib2.urlopen('http://currency-api.appspot.com/api/'+src+'/'+tgt+'.json?key='+key).read())
			if data['success']:
				v = Value.objects.filter(type=src+'-'+tgt)[0]
				v.value = data['rate']
				v.created_at = current_time
				v.save()
		except:
			pass
		return Value.objects.filter(type=src+'-'+tgt)[0].value
	else:
		return Value.objects.filter(type=src+'-'+tgt)[0].value
