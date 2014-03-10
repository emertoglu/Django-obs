from models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import *
from yonetim.forms import *
from django.core.paginator import Paginator
from django.db.models import Q


def ogretim_elemanlari_listesi(request):
  siralama='soyadi'
  olcut=request.GET.get('sirala')
  sayfa = request.GET.get('sayfa',1)
  if olcut:
    siralamaolcutleri={'1':'adi',
		      '2':'soyadi',
		      '3':'e_posta_adresi'}
    if olcut in siralamaolcutleri:
      siralama=siralamaolcutleri[olcut]
  
  ogretim_elemanlari_tumu = OgretimElemani.objects.order_by(siralama)
  arama_formu = AramaFormu()
  if request.GET.get('aranacak_kelime'):
    arama_formu = AramaFormu(request.GET)
    if arama_formu.is_valid():
      aranacak_kelime = arama_formu.cleaned_data['aranacak_kelime']
      ogretim_elemanlari_tumu = OgretimElemani.objects.filter(
	  Q(adi__contains=aranacak_kelime) | Q(soyadi__contains=aranacak_kelime))
  ogretim_elemanlari_sayfalari = Paginator(ogretim_elemanlari_tumu, 5)
  ogretim_elemanlari = ogretim_elemanlari_sayfalari.page(int(sayfa))
  
  for ogrelm in ogretim_elemanlari:
    verdigi_dersler = Ders.objects.filter(ogretim_elemani = ogrelm)
    ogrelm.verdigi_dersler = verdigi_dersler
  
  return render_to_response('listele.html', locals())

def ogretim_elemani_ekleme(request):
  ogrelmid=request.GET.get('id')
  if ogrelmid:
    try:
      ogrelm=OgretimElemani.objects.get(id = ogrelmid)
    except:
      return HttpResponse(u'Aradiginiz ogretim elemani bulunamiyor: ID=%s'%ogrelmid)
  if request.GET.get('sil'):
    ogrelm.delete()
    return HttpResponseRedirect('/yonetim/listele')
  
  if request.method=='POST':
    form=OgretimElemaniFormu(request.POST)
    if form.is_valid():
      temiz_veri=form.cleaned_data
      if not ogrelmid: ogrelm=OgretimElemani()
      ogrelm=OgretimElemani(
		    adi=temiz_veri['adi'],
		    soyadi=temiz_veri['soyadi'],
		    telefonu=temiz_veri['telefonu'],
		    e_posta_adresi=temiz_veri['e_posta_adresi'])
		    
      ogrelm.unvani = temiz_veri['unvani']
      ogrelm.save()
      return HttpResponseRedirect('/yonetim/listele')
  else:
      if ogrelmid: form=OgretimElemaniFormu(initial = ogrelm.__dict__)
      else: form=OgretimElemaniFormu()
  
  return render_to_response('genel_form.html',{'form':form,'baslik':'Ogretim Elemani Ekleme','ID':ogrelmid},
						context_instance=RequestContext(request))