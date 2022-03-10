from django.urls import include, path, re_path

from jsonrpc.site import jsonrpc_site
from jsonrpc import views

urlpatterns = (
    path("^json/browse/", views.browse, name="jsonrpc_browser"),
    path("^json/", jsonrpc_site.dispatch, name="jsonrpc_mountpoint"),
    re_path(r"^json/(?P<method>[a-zA-Z0-9.-_]+)$", jsonrpc_site.dispatch),
)
