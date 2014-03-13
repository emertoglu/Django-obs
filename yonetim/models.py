from django.db import models
from django.contrib.auth.models import User

class OgretimElemani(User):
    unvansecenekleri = (('AG',u'Arastirma Gorevlisi'),
			('DR',u'Doktor'),
			('YD',u'Yardimci Docent Doktor'),
			('DD',u'Docent Doktor'),
			('PD',u'Profesor Doktor'),)
    unvani = models.CharField(max_length=2, choices = unvansecenekleri,
			      blank=True, verbose_name='Unvani')
    telefonu = models.CharField(max_length=10, blank=True, verbose_name='Telefon Numarasi')
    
    def __unicode__(self):
      return u'%s,%s'%(self.first_name, self.last_name)
    
    class Meta:
      ordering = ['last_name']
      
class Ders(models.Model):
    kodu = models.CharField(max_length=10)
    adi = models.CharField(max_length=50)
    ogretim_elemani = models.ForeignKey(OgretimElemani)
    tanimi = models.CharField(max_length=1000, blank=True)
    
class Ogrenci(models.Model):
    numarasi = models.IntegerField()
    adi = models.CharField(max_length = 50)
    soyadi = models.CharField(max_length=50)
    aldigi_dersler = models.ManyToManyField(Ders)
