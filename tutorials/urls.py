from django.conf.urls import url 
from tutorials import views 
from django.views.generic import RedirectView
 
urlpatterns = [ 
    url(r'^api/tutorials$', views.tutorial_list),
    url(r'^api/tutorials/(?P<pk>[0-9]+)$', views.tutorial_detail),
    url(r'^api/tutorials/published$', views.tutorial_list_published),
    url(r'^api/admin$', views.admin_index),
    url('', RedirectView.as_view(url='/api/admin', permanent=True))
]