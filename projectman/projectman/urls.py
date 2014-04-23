from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'projectman.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #
   url(r'^admindjango/', include(admin.site.urls)),
   url(r'^admin/', include('projectman.apps.admin.urls')),
    #punto de entrada al index
   url(r'^$', 'projectman.apps.desarrollo.views.view_oth.mostrar_panel') , 
   url(r'^desarrollo/',include('projectman.apps.desarrollo.urls')),
   url(r'^gestcambio/',include('projectman.apps.gestcambio.urls'))
)
