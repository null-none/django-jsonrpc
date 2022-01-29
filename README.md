Django JSON-RPC
===============

A basic JSON-RPC Implementation for your Django-powered sites.

Features:

* Simple, pythonic API</li>
* Support for Django authentication</li>
* Supports JSON-RPC 1.0, 1.1, 1.2 and 2.0 Spec
* Proxy to test your JSON Service
* Run-time type checking
* Graphical JSON-RPC browser and web console
* Provides `system.describe`


The basic API:

**myproj/myapp/views.py**

    from jsonrpc import jsonrpc_method

    @jsonrpc_method('myapp.sayHello')
    def whats_the_time(request, name='Lester'):
      return "Hello %s" % name

    @jsonrpc_method('myapp.gimmeThat', authenticated=True)
    def something_special(request, secret_data):
      return {'sauce': ['authenticated', 'sauce']}


**myproj/urls.py**

    from django.urls import include, path, re_path

    from jsonrpc.site import jsonrpc_site
    from jsonrpc import views

    urlpatterns = (
      path('^json/browse/', views.browse, name='jsonrpc_browser'),
      path('^json/', jsonrpc_site.dispatch, name='jsonrpc_mountpoint'),
      re_path(r'^json/(?P<method>[a-zA-Z0-9.-_]+)$', jsonrpc_site.dispatch),
    )


**To test your service:**
You can test your service using the provided graphical browser and console,
available at http://YOUR_URL/json/browse/ (if using the url patterns from above) or with the included ServiceProxy:

    >>> from jsonrpc.proxy import ServiceProxy

    >>> s = ServiceProxy('http://localhost:8080/json/')

    >>> s.myapp.sayHello('Sam')
    {u'error': None, u'id': u'jsonrpc', u'result': u'Hello Sam'}

    >>> s.myapp.gimmeThat('username', 'password', 'test data')
    {u'error': None, u'id': u'jsonrpc', u'result': {u'sauce': [u'authenticated', u'sauce']}}

We add the `jsonrpc_version` variable to the request object. It be either '1.0', '1.1' or '2.0'. Arg.

Guide
=====

### Adding JSON-RPC to your application

#### 1. Install django-json-rpc

    git clone git://github.com/samuraisam/django-json-rpc.git
    cd django-json-rpc
    python setup.py install

    # Add 'jsonrpc' to your INSTALLED_APPS in your settings.py file

#### 2. Write JSON-RPC methods

    from jsonrpc import jsonrpc_method

    @jsonrpc_method('app.register')
    def register_user(request, username, password):
      u = User.objects.create_user(username, 'internal@app.net', password)
      u.save()
      return u.__dict__

    @jsonrpc_method('app.change_password', authenticated=True)
    def change_password(request, new_password):
      request.user.set_password(new_password)
      request.user.save()
      return u.__dict__

#### 3. Add the JSON-RPC mountpoint and import your views

    from jsonrpc import jsonrpc_site
    import app.views

    urlpatterns = patterns('',
      url(r'^json/$', jsonrpc_site.dispatch, name='jsonrpc_mountpoint'),
      # ... among your other URLs
    )


### The jsonrpc_method decorator
Wraps a function turns it into a json-rpc method. Adds several attributes to the function speific to the JSON-RPC machinery and adds it to the default jsonrpc_site if one isn't provided. You must import the module containing these functions in your urls.py.

`jsonrpc.jsonrpc_method(name, authenticated=False, safe=False, validate=False)`
<ul>
<li>
`name`

The name of your method. IE: `namespace.methodName`
</li>
<li>
`authenticated=False`

Adds `username` and `password` arguments to the beginning of your method if the user hasn't already been authenticated. These will be used to authenticate the user against `django.contrib.authenticate` If you use HTTP auth or other authentication middleware, `username` and `password` will not be added, and this method will only check against `request.user.is_authenticated`.

You may pass a callablle to replace `django.contrib.auth.authenticate` as the authentication method. It must return either a User or `None` and take the keyword arguments `username` and `password`.
</li>
<li>
`safe=False`

Designates whether or not your method may be accessed by HTTP GET. By default this is turned off.
</li>
<li>
`validate=False`

Validates the arguments passed to your method based on type information provided in the signature. Supply type information by including types in your method declaration. Like so:

      @jsonrpc_method('myapp.specialSauce(Array, String)', validate=True)
      def special_sauce(self, ingredients, instructions):
        return SpecialSauce(ingredients, instructions)

Calls to `myapp.specialSauce` will now check each arguments type before calling `special_sauce`, throwing an `InvalidParamsError` when it encounters a discrepancy. This can significantly reduce the amount of code required to write JSON-RPC services.

*NOTE:* Type checking is only available on Python versions 2.6 or greater.
</li>
<li>
`site=default_site`

Defines which site the jsonrpc method will be added to. Can be any
object that provides a `register(name, func)` method.
</li>
</ul>
