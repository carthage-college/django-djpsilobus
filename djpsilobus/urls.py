# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path, reverse_lazy
from django.views.generic import RedirectView, TemplateView

from djpsilobus.core import views
from djauth.views import loggedout

admin.autodiscover()

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'


urlpatterns = [
    # django admin
    path('admin/', admin.site.urls),
    # auth
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(),
        {'template_name': 'registration/login.html'},
        name='auth_login',
    ),
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(),
        {'next_page': reverse_lazy('auth_loggedout')},
        name='auth_logout',
    ),
    path(
        'accounts/loggedout/',
        loggedout,
        {'template_name': 'registration/logged_out.html'},
        name='auth_loggedout',
    ),
    path(
        'accounts/',
        RedirectView.as_view(url=reverse_lazy('auth_login')),
    ),
    path(
        'denied/',
        TemplateView.as_view(template_name='denied.html'),
        name='access_denied',
    ),
    # downloads
    path(
        '<str:division>/<str:department>/<str:term>/<int:year>/download/',
        views.download,
        name='download_department',
    ),
    path(
        '<str:division>/<str:department>/download/',
        views.download,
        name='download_department',
    ),
    path(
        '<str:division>/download/',
        views.download,
        name='download_division',
    ),
    # OpenXML export
    path(
        '<str:division>/<str:department>/<str:term>/<int:year>/openxml/',
        views.openxml,
        name='openxml_department',
    ),
    path(
        '<str:division>/<str:department>/openxml/',
        views.openxml,
        name='openxml_department',
    ),
    path(
        '<str:division>/openxml/',
        views.openxml,
        name='openxml_division',
    ),
    # dspace API
    path(
        'dspace/file/search/',
        views.dspace_file_search,
        name='dspace_file_search',
    ),
    path(
        'dspace/<str:dept>/<str:term>/<int:year>/courses/',
        views.dspace_dept_courses,
        name='dspace_dept_courses',
    ),
    # home, with and without department code, term, year.
    path('<str:dept>/<str:term>/<int:year>/', views.home, name='home_all'),
    path('<str:dept>', views.home, name='home_dept'),
    path('', views.home, name='home'),
    #path('admin/', include('loginas.urls')),
]

