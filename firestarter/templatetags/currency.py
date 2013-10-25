import decimal

from django.template import Library
from firestarter import currency

register = Library()

@register.filter
def dollars_to_btc(value):
	return currency.dollars_to_btc(value)

@register.filter
def btc_to_dollars(value):
	return currency.btc_to_dollars(value)

@register.filter
def dollars_to_eur(value):
	return currency.dollars_to_eur(value)

@register.filter
def eur_to_dollars(value):
	return currency.eur_to_dollars(value)

@register.filter
def dollars_to_gbp(value):
	return currency.dollars_to_gbp(value)

@register.filter
def gbp_to_dollars(value):
	return currency.gbp_to_dollars(value)
