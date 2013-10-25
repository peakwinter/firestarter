from django import forms
from django.contrib import admin
from django.db import models
from captcha.fields import CaptchaField

from firestarter.models import Order, Reward, Update, Question, Value


class AdminOrderForm(admin.ModelAdmin):
	model = Order
	list_display = ('name', 'amount', 'created_at')

	def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
		field = super(AdminOrderForm, self).formfield_for_foreignkey(
			db_field, request, **kwargs)
		if db_field.rel.to == Reward:
			field.label_from_instance = self.get_reward_name
		return field

	def get_reward_name(self, reward):
		return reward.name


class AdminRewardForm(admin.ModelAdmin):
	model = Reward
	list_display = ('name', 'min_amount')


class AdminUpdateForm(admin.ModelAdmin):
	model = Update
	list_display = ('created_at', 'subject', 'author')


class QuestionForm(forms.ModelForm):
	captcha = CaptchaField()
	class Meta:
		model = Question


class AdminQuestionForm(admin.ModelAdmin):
	model = Question
	list_display = ('created_at', 'name', 'orig')

	def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
		field = super(AdminQuestionForm, self).formfield_for_foreignkey(
			db_field, request, **kwargs)
		if db_field.rel.to == Question:
			field.label_from_instance = self.get_question_id
		return field

	def get_question_id(self, question):
		return '%s %s' % (str(question.created_at), question.name)


class AdminValueForm(admin.ModelAdmin):
	model = Value
	list_display = ('type', 'created_at', 'value')
