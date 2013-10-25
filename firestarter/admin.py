from django.contrib import admin
from firestarter.models import Order, Reward, Update, Question, Value
from firestarter.forms import AdminOrderForm, AdminRewardForm, AdminUpdateForm
from firestarter.forms import AdminQuestionForm, AdminValueForm

admin.site.register(Order, AdminOrderForm)
admin.site.register(Reward, AdminRewardForm)
admin.site.register(Update, AdminUpdateForm)
admin.site.register(Question, AdminQuestionForm)
admin.site.register(Value, AdminValueForm)
