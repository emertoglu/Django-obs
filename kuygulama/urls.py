from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kuygulama.views.home', name='home'),
    # url(r'^kuygulama/', include('kuygulama.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    url(r'^cerez-deneme/$', 'yonetim.views.cerez_deneme'),
    url(r'^yonetim/$', 'yonetim.views.yonetim_anasayfa'),
    url(r'^yonetim/listele$', 'yonetim.views.ogretim_elemanlari_listesi'),
    url(r'^yonetim/ogretim_elemani_ekle$', 'yonetim.views.ogretim_elemani_ekleme'),
    #url(r'^yonetim/ogretim_elemani_ekle$', login_required('yonetim.views.ogretim_elemani_ekleme')),
    #eger istersek url i de gizleyebiliyoruz login_required ile
    url(r'^yonetim/coklu-ogretim-elemani-ekleme$', 'yonetim.views.coklu_ogretim_elemani_ekleme'),
    
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name':'login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page':'/accounts/login/'}),
    
)
