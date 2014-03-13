from models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import *
from yonetim.forms import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import *

import random
import time


def yonetici_kontrol(user):
  if user:
    if user.groups.filter(name='yoneticiler').count() > 0:
      return True
  return False

#@login_required
@user_passes_test(yonetici_kontrol)
def yonetim_anasayfa(request):
  if request.GET.get('cikis'):
    logout(request)
    return HttpResponseRedirect('/yonetim/')
  
  if request.POST.get('giris_yap'):
    giris_formu = AuthenticationForm(data =request.POST)
    if giris_formu.is_valid():
      username = request.POST['username']
      password = request.POST['password']
      kullanici = authenticate(username=username, password=password)
      
      if kullanici is not None:
	if kullanici.is_active:
	  login(request, kullanici)
  else:
    giris_formu = AuthenticationForm()
  
  return render_to_response('yonetim.html', locals(), context_instance=RequestContext(request))

def cerez_deneme(request):
  cerez_listesi = ['Findik','Fistik','Ceviz','Badem','Leblebi','Misir Kavurgasi']
  if not 'sevdigim_cerez' in request.COOKIES:
    sevdigim_cerez = random.choice(cerez_listesi)
    gun = 7
    son_kullanma_tarihi = time.strftime('%a, %d-%b-%Y %H:%M:%S GMT',
			    time.localtime(time.time()+gun*24*60*60))
    response = HttpResponse(
		  u'Sevdigin cerez yoktu, sana bu cerezi sevdirdim: <b>%s</b>' %
		  sevdigim_cerez.decode('utf-8'))
    response.set_cookie('sevdigim_cerez',sevdigim_cerez, expires=son_kullanma_tarihi)
    return response
  else:
    sevdigim_cerez = request.COOKIES['sevdigim_cerez']
    return HttpResponse(
	      u'Sevdigin cerez budur: <b>%s</b>' %sevdigim_cerez.decode('utf-8'))

@login_required
def ogretim_elemanlari_listesi(request):
  #session yapisina gecildi
  #kullanici oturumlarini kaydedebilmek icin bir sozluk gibi kullanacagim.
  if request.GET.get('sirala'):
    request.session['ogretim_elemani_siralama']=request.GET['sirala']
  if not 'ogretim_elemani_siralama' in request.session:
    request.session['ogretim_elemani_siralama']='1'
  
  olcut = request.session['ogretim_elemani_siralama']
  #sayfa = request.GET.get('sayfa',1) 
  # hangi sayfada kaldigini da kaydetmek icin bu satiri degistiriyorum
  
  if request.GET.get('sayfa'):
    request.session['ogretim_elemani_sayfa']=request.GET['sayfa']
  if not 'ogretim_elemani_sayfa' in request.session:
    request.session['ogretim_elemani_sayfa']='1'
  sayfa = request.session['ogretim_elemani_sayfa']
  
  if olcut:
    siralamaolcutleri={'1':'first_name',
		      '2':'last_name',
		      '3':'email'}
    if olcut in siralamaolcutleri:
      siralama=siralamaolcutleri[olcut]
  
  ogretim_elemanlari_tumu = OgretimElemani.objects.order_by(siralama)
  
  if request.GET.get('aranacak_kelime'):
    arama_formu = AramaFormu(request.GET)
    if arama_formu.is_valid():
      aranacak_kelime = arama_formu.cleaned_data['aranacak_kelime']
      ogretim_elemanlari_tumu = OgretimElemani.objects.filter(
	  Q(first_name__contains=aranacak_kelime) | Q(last_name__contains=aranacak_kelime))
  
  ogretim_elemanlari_sayfalari = Paginator(ogretim_elemanlari_tumu, 5)
  ogretim_elemanlari = ogretim_elemanlari_sayfalari.page(int(sayfa)) 
  
  #for ogrelm in ogretim_elemanlari:
  #  verdigi_dersler = Ders.objects.filter(ogretim_elemani = ogrelm)
  #  ogrelm.verdigi_dersler = verdigi_dersler
  
  return render_to_response('listele.html', locals())

@login_required
def ogretim_elemani_ekleme(request):
  
  ogrelmid=request.GET.get('id')
  if ogrelmid:
    try:
      ogrelm=OgretimElemani.objects.get(id = ogrelmid)
      form = OgretimElemaniFormu(instance=ogrelm)
    except:
      return HttpResponse(u'Aradiginiz ogretim elemani bulunamiyor: ID=%s'%ogrelmid)
  else:
    form = OgretimElemaniFormu()
    
    
  if request.GET.get('sil'):
    ogrelm.delete()
    return HttpResponseRedirect('/yonetim/listele')
  
  if request.method=='POST':
    if ogrelmid:
      form = OgretimElemaniFormu(request.POST, instance=ogrelm)
    else:
      form = OgretimElemaniFormu(request.POST)
    
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/yonetim/listele')
  
  return render_to_response('genel_form.html',{'form':form,'baslik':'Ogretim Elemani Ekleme','ID':ogrelmid},
						context_instance=RequestContext(request))
@login_required
def coklu_ogretim_elemani_ekleme(request):
   OgretimElemaniFormuKumesi = modelformset_factory(OgretimElemani,fields=('unvani','adi','soyadi'),can_delete=True)
   
   if request.method == 'POST':
     formkumesi = OgretimElemaniFormuKumesi(request.POST)
     if formkumesi.is_valid():
       formkumesi.save()
       return HttpResponseRedirect('/yonetim/coklu-ogretim-elemani-ekleme')
     
   else:
       formkumesi = OgretimElemaniFormuKumesi()
   return render_to_response(
		'coklu_ogretim_elemani.html',
		locals(),
		context_instance = RequestContext(request))