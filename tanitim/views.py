from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext


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
