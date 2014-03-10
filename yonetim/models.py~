from django.db import models

class OgretimElemani(models.Model):
    unvansecenekleri = (('AG',u'Arastirma Gorevlisi'),
			('DR',u'Doktor'),
			('YD',u'Yardimci Docent Doktor'),
			('DD',u'Docent Doktor'),
			('PD',u'Profesor Doktor'),)
    unvani = models.CharField(max_length=2, choices = unvansecenekleri,
			      blank=True, verbose_name='Unvani')
    adi = models.CharField(max_length=50, verbose_name='Adi')
    soyadi = models.CharField(max_length=50, verbose_name='Soyadi')
    telefonu = models.CharField(max_length=10, blank=True, verbose_name='Telefonu')
    e_posta_adresi = models.EmailField(blank=True, verbose_name='E-Posta Adresi')
    
    def __unicode__(self):
      return u'%s,%s'%(self.soyadi, self.adi)
    
    class Meta:
      ordering = ['soyadi']
      
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
