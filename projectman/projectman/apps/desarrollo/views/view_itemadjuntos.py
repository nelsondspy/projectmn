from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, render 
from django.views.generic import ListView
from django.views.generic import View
from ..models import Item
from ..forms import ItemAdjuntosForm
 

TEMPL_ADJUNTO = 'desarrollo/frmls_itemadjunto.html'

class LsCrAdjuntoView(View):
    """
    Lista y crea adjuntos del item.
    
    """
    template_name = TEMPL_ADJUNTO
    
    def get(self, request,iditem):
        item = get_object_or_404(Item, pk=iditem)
        form = ItemAdjuntosForm()
        form.initial = {'item':item }
        return render(request, TEMPL_ADJUNTO, {'form':form})
    
    def post(self, request, *args, **kwargs):
        print "holaaaa"
        form = ItemAdjuntosForm(request.POST, request.FILES)
        if form.is_valid():
            print "saveee!"
            form.save()
        return render(request, TEMPL_ADJUNTO, {'form':form})
    