from django.core.urlresolvers import reverse_lazy
from django.conf.urls import include, url
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth import views as auth_views
from django.contrib import admin

from djauth.views import loggedout

admin.autodiscover()

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'

from djpsilobus.core import views

urlpatterns = [
    url(
        r'^admin/', include(admin.site.urls)
    ),
    # auth
    url(
        r'^accounts/login/$',auth_views.login,
        {'template_name': 'accounts/login.html'},
        name='auth_login'
    ),
    url(
        r'^accounts/logout/$',auth_views.logout,
        {'next_page': reverse_lazy('auth_loggedout')},
        name='auth_logout'
    ),
    url(
        r'^accounts/loggedout/$',loggedout,
        {'template_name': 'accounts/logged_out.html'},
        name='auth_loggedout'
    ),
    url(
        r'^accounts/$',
        RedirectView.as_view(url=reverse_lazy('auth_login'))
    ),
    url(
        r'^denied/$',
        TemplateView.as_view(
            template_name='denied.html'
        ), name='access_denied'
    ),
    # downloads
    url(
        r'^(?P<division>[A-Z_]+)/(?P<department>[A-Z_]+)/(?P<term>[-\w]+)/(?P<year>\d+)/download/$',
        views.download, name='download_department'
    ),
    url(
        r'^(?P<division>[A-Z_]+)/(?P<department>[A-Z_]+)/download/$',
        views.download, name='download_department'
    ),
    url(
        r'^(?P<division>[A-Z_]+)/download/$',
        views.download, name='download_division'
    ),
    # OpenXML export
    url(
        r'^(?P<division>[A-Z_]+)/(?P<department>[A-Z_]+)/(?P<term>[-\w]+)/(?P<year>\d+)/openxml/$',
        views.openxml, name='openxml_department'
    ),
    url(
        r'^(?P<division>[A-Z_]+)/(?P<department>[A-Z_]+)/openxml/$',
        views.openxml, name='openxml_department'
    ),
    url(
        r'^(?P<division>[A-Z_]+)/openxml/$',
        views.openxml, name='openxml_division'
    ),
    # dspace API
    url(
        r'^dspace/file/search/$',
        views.dspace_file_search, name='dspace_file_search'
    ),
    url(
        r'^dspace/(?P<dept>[-\w]+)/(?P<term>[-\w]+)/(?P<year>\d+)/courses/$',
        views.dspace_dept_courses, name='dspace_dept_courses'
    ),
    # home, with and without department code, year, term.
    url(
        r'^(?P<dept>[A-Z_]+)/(?P<term>[-\w]+)/(?P<YEAR>\d+)/$', views.home, name='home_all'
    ),
    url(
        r'^(?P<dept>[A-Z_]+)/$', views.home, name='home_dept'
    ),
    url(
        r'^$', views.home, name='home'
    )
]
