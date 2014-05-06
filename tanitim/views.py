from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import *
from django.http import *
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect


def giris_sayfasi(request):
  if request.Get.get('cikis'):
    logout(request)
    return HttpResponseRedirect('/tanitim/')
  if request.Post.get('giris_yap'):
    giris_formu = AuthenticationForm('data=request.POST')
    if giris_formu.is_valid():
      username=request.POST['username']
      password=request.POST['password']
      kullanici=authenticate(username=username, password=password)
    if kullanici is not None:
      if kullanici.is_active:
	login(request, kullanici)
      else:
	giris_formu = AuthenticationForm()
      return render_to_response('tanitim_ana_sayfa.html',locals(),context_instance=RequestContext(request))

def register(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect("/tanitim/")
    else:
      form=UserCreationForm()
    return render_to_response('registration/register.html',locals(),context_instance=RequestContext(request))