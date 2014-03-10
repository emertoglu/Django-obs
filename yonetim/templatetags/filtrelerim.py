from django import template
from yonetim.models import *

register = template.Library()

@register.filter
def ders_bul(ogrelm_id):
   verdigi_dersler = Ders.objects.filter(ogretim_elemani = ogrelm_id)
   ders_listesi=[]
   for ders in verdigi_dersler:
     ders_listesi.append(ders.adi)
   
   return ders_listesi