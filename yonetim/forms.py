from django import forms
from django.forms import ModelForm
from models import *
from django.forms import Textarea
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group


class OgretimElemaniFormu(ModelForm):
  parolasi=forms.CharField(label="Parolasi",
		    help_text='Parola yazilmazsa onceki parola gecerlidir',
		    required=False)
  
  class Meta:
    model = OgretimElemani
    fields = ('unvani','first_name','last_name',
	       'username','parolasi','email','telefonu')
    def save(self,commit=True):
      instance = super(OgretimElemaniFormu,self).save(commit=False)
      if self.cleaned_data.get('parolasi'):
	instance.password=make_password(self.cleaned_data['parolasi'])
      if commit:
	instance.save()
	if instance.group.filter(name='ogretimelemanlari'):
	  grp = Group.objects.get(name='ogretimelemanlari')
	  instance.group.add(grp)
      return instance
    
  

class DersFormu(ModelForm):
  class Meta:
    model = Ders
    widgets = {
	  'tanimi':Textarea(attrs={'cols':35, 'rows':5}),
      }

#class OgretimElemaniAltFormu(ModelForm):
#  class Meta:
#    model = OgretimElemani
#    fields = ('username','parolasi','email')
    #exclude=('unvani','telefonu') bu da ayni gorevi gorur
    # fields kullanarak hangi sirada gozukmesini istiyorsak ayarlayabiliriz
    # yada exclude diyerek istemedigimiz alanlari formdan cikartabiliriz

class AramaFormu(forms.Form):
  aranacak_kelime = forms.CharField()
  def clean_aranacak_kelime(self):
    kelime=self.cleaned_data['aranacak_kelime']
    if len(kelime) < 3:
      raise forms.ValidationError('Aranacak kelime 3 harften az olamaz')
    return kelime