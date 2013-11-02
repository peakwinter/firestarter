from django.conf import settings
from django.db import models


class Reward(models.Model):
	name = models.CharField(max_length=255, default="", verbose_name='Reward Name')
	min_amount = models.DecimalField(max_digits=8, decimal_places=2, default="", verbose_name="Minimum Amount")
	desc = models.CharField(max_length=255, default="", verbose_name='Reward Description')
	short_desc = models.CharField(max_length=255, default="", verbose_name='Short Reward Description')
	fine_print = models.CharField(max_length=255, default="", verbose_name='Fine Print', blank=True)
	icon_class = models.CharField(max_length=255, default="", verbose_name='Icon Classes', blank=True)
	img = models.URLField(default="", verbose_name='Image URL', blank=True)


class Update(models.Model):
	created_at = models.DateTimeField(auto_now=True)
	subject = models.CharField(max_length=255)
	author = models.CharField(max_length=255, verbose_name="Author Name")
	email = models.EmailField(verbose_name="Author Email")
	text = models.TextField()


class Question(models.Model):
	created_at = models.DateTimeField(auto_now=True)
	name = models.CharField(max_length=255, verbose_name="Name")
	email = models.EmailField(verbose_name="Email", blank=True)
	text = models.TextField()
	orig = models.ForeignKey('self', related_name='replies', verbose_name='In reply to', blank=True, null=True)
	notify = models.BooleanField(default=True, verbose_name="Notify me on replies")
	team_response = models.BooleanField(default=False, verbose_name="Add the Team Response flag")


class Order(models.Model):
	PAY_TYPES = (
		('CC', 'Credit Card'),
		('BC', 'Bitcoin'),
		('PP', 'PayPal'),
		('BT', 'Bank Transfer'),
	)

	created_at = models.DateTimeField(auto_now=True)

	name = models.CharField(max_length=255, default="", verbose_name='Name')
	addr1 = models.CharField(max_length=255, default="", verbose_name='Address 1')
	addr2 = models.CharField(max_length=255, default="", verbose_name='Address 2', blank=True)
	city = models.CharField(max_length=255, default="", verbose_name='City')
	state = models.CharField(max_length=255, default="", verbose_name='State/Province')
	pcode = models.CharField(max_length=255, default="", verbose_name='Postal Code')
	country = models.CharField(max_length=255, default="", verbose_name='Country')
	reward = models.ForeignKey(Reward, related_name='+', verbose_name='Reward Level', blank=True, null=True)
	amount = models.DecimalField(max_digits=8, decimal_places=2, default="", verbose_name='Amount')
	ptype = models.CharField(max_length=2, choices=PAY_TYPES, verbose_name='Payment Type')
	pref = models.CharField(max_length=255, default="", verbose_name='Payment Reference', blank=True)
	email = models.EmailField(verbose_name='Email')
	notify = models.BooleanField(verbose_name="Notify me if the project team posts an update?")
	namecredit = models.CharField(max_length=255, default="", verbose_name='Credit Name', blank=True)
	notes = models.CharField(max_length=255, default="", verbose_name='Notes', blank=True)


class Value(models.Model):
	created_at = models.DateTimeField(auto_now=True)
	type = models.CharField(max_length=7, verbose_name="Currency Abbreviation")
	value = models.FloatField(verbose_name="USD to currency")
	update = models.BooleanField(verbose_name="Update value from API?")
