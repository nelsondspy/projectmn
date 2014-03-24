from django.conf.urls import patterns, url


urlpatterns = patterns('projectman.apps',
    url(r'^autenticar/$', 'admin.views.autenticar'),
    url(r'^cerrar_sesion/$', 'admin.views.cerrar_sesion'),
    url(r'^login/$', 'admin.views.login_form'),
    url(r'^proyectos/$', 'admin.views.proyectos_abm'),
    url(r'^proyectos/(?P<idproyecto>\d+)$', 'admin.views.proyectos_abm'),
    url(r'^proyectos/(?P<accion>[a-z]+)/(?P<idproyecto>\d+)$', 'admin.views.proyectos_abm'),
    url(r'^fases/(?P<accion>[a-z]+)/(?P<idelemento>\d+)$', 'admin.views.fases_abm'),
    url(r'^fases/$', 'admin.views.fases_abm')

)
