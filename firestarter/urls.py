import os
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from firestarter import paypal

admin.autodiscover()

urlpatterns = patterns('firestarter.views',
    # Examples:
    url(r'^$', 'home', name='home'),
    url(r'^questions/$', 'questions', name='questions'),
    url(r'^updates/$', 'updates', name='updates'),
    url(r'^c/choose$', 'choose', name='choose'),
    # url(r'^firestarter/', include('firestarter.foo.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^admin/', include(admin.site.urls))
)

for x in os.listdir(os.path.join(settings.PROJECT_PATH, '/templates/pages')):
    urlpatterns += patterns('firestarter.views',
        url(r'^p/'+x[:-5]+'$', 'page', {'pagename': x[:-5]})
    )

for x in settings.PAY_TYPES:
    if 'CC' in x[0]:
        urlpatterns += patterns('firestarter.cc_stripe',
            url(r'^c/CC$', 'approve_payment', name='approve_payment'),
            url(r'^c/CC/complete$', 'complete_payment', name='complete_payment'),
        )
    elif 'BC' in x[0]:
        urlpatterns += patterns('firestarter.bitcoin',
            url(r'^c/BC$', 'approve_payment', name='approve_payment'),
            url(r'^c/BC/complete$', 'complete_payment', name='complete_payment'),
        )
    elif 'PP' in x[0]:
        urlpatterns += patterns('firestarter.paypal',
            url(r'^c/PP$', 'approve_payment', name='approve_payment'),
            url(r'^c/PP/confirm$', 'handle_response', name='handle_response'),
            url(r'^c/PP/complete$', 'complete_payment', name='complete_payment'),
            url(r'^c/PP/cancel$', 'cancel', name='cancel')
        )
