from models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import *
from yonetim.forms import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms.models import modelformset_factory

def yonetim_anasayfa(request):
  return render_to_response('yonetim.html')

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