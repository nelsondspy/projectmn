from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from views.view_comite import CrearComiteProyectoView

urlpatterns = patterns('projectman.apps',
    #gestion de tipos de items 
    url(r'^comite/crear/$', login_required(CrearComiteProyectoView.as_view()), name="comite_crear"),

)
