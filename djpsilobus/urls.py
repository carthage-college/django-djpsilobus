from django.core.urlresolvers import reverse_lazy
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth import views as auth_views
from django.contrib import admin

from djauth.views import loggedout

admin.autodiscover()

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'

urlpatterns = patterns('djpsilobus.core.views',
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
        {'next_page': reverse_lazy("auth_loggedout")},
        name="auth_logout"
    ),
    url(
        r'^accounts/loggedout/$',loggedout,
        {'template_name': 'accounts/logged_out.html'},
        name="auth_loggedout"
    ),
    url(
        r'^accounts/$',
        RedirectView.as_view(url=reverse_lazy("auth_login"))
    ),
    url(
        r'^denied/$',
        TemplateView.as_view(
            template_name="denied.html"
        ), name="access_denied"
    ),
    # dspace API
    url(
        r'^dspace/file/search/$',
        'dspace_file_search', name="dspace_file_search"
    ),
    # home, with and without department code set
    url(
        r'^(?P<dept>[A-Z_]+)/$', 'home', name="home_dept"
    ),
    url(
        r'^$', 'home', name="home"
    ),
)
