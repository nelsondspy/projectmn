from django.conf.urls import patterns, url


urlpatterns = patterns('projectman.apps',
    url(r'^$', 'desarrollo.views.mostrar_panel'),
    url(r'^componentes/(?P<idproyecto>\d+)/$', 'desarrollo.views.editor_componentes', name='editor_componentes'),
    url(r'^componentes/(?P<idproyecto>\d+)/(?P<idfase>\d+)$', 'desarrollo.views.editor_componentes'),
    url(r'^procesaitem/(?P<accion>[a-z]+)/(?P<idelemento>\d+)$', 'desarrollo.views.procesa_item'),
    url(r'^procesaitem/$', 'desarrollo.views.procesa_item'),
    #url(r'^procesatipoitem/(?P<accion>[a-z]+)/(?P<idelemento>\d+)$')
    
)
