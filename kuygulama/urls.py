from django.conf.urls import patterns, include, url


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kuygulama.views.home', name='home'),
    # url(r'^kuygulama/', include('kuygulama.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    url(r'^yonetim/listele$', 'yonetim.views.ogretim_elemanlari_listesi'),
    url(r'^yonetim/ogretim_elemani_ekle$', 'yonetim.views.ogretim_elemani_ekleme'),
    url(r'^yonetim/coklu-ogretim-elemani-ekleme$', 'yonetim.views.coklu_ogretim_elemani_ekleme'),
)
