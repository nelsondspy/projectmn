from django.shortcuts import get_object_or_404, render 
from django.views.generic import View
from ..models import Item
from ..forms import ItemAdjuntosForm
from ..models import ItemAdjuntos 
 

TEMPL_ADJUNTO = 'desarrollo/frmls_itemadjunto.html'

class LsCrAdjuntoView(View):
    """
    Lista y crea adjuntos del item.
    
    """
    template_name = TEMPL_ADJUNTO
    
    def get(self, request,iditem):
        item = get_object_or_404(Item, pk=iditem)
        form = ItemAdjuntosForm()
        lista_adjuntos = ItemAdjuntos.objects.filter(item=item)
        form.initial = {'item':item }
        
        return render(request, TEMPL_ADJUNTO, {'form':form, 'lista_adjuntos': lista_adjuntos})
    
    def post(self, request, *args, **kwargs):
        form = ItemAdjuntosForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return render(request, TEMPL_ADJUNTO, {'form':form})
    