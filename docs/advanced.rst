Advanced usage
==============

.. warning::
    Those advanced usages are only available on the dev version (eg: not on the PyPi version) of Polla.

.. danger::
    These advanced usages all require to resort to *local threads* to be able to access the current request. Some people have `strong feeelings against local threads use in Django <https://groups.google.com/forum/?fromgroups=#!topic/django-users/5681nX0YPgQ>`_. Local threads in themselves (in our humble opinion) are not a security risk but may amplify some other security risks. So before you use them, make sure you know what you are getting into.

Extra requirement
-----------------

As said above ``threadlocals`` is an extra requirement for the advanced features, so go ahead and pip install it
::
    pip install django-threadlocals

Common Settings
---------------

To use any of the following features, make sure you enable the `LocalThreadMiddleware` (put it before ``django.middleware.common.CommonMiddleware``.
::
    ##settings.py
    MIDDLEWARE_CLASSES = (
        'polla.middleware.ThreadLocalMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        ...
    )


POLLA_SITES_DIR
~~~~~~~~~~~~~~~

Every site-specific feature (template, urls, static file) is hosted under a main directory (``BASE_DIR/sites`` by default), to override it, provide ``POLLA_SITES_DIR`` in your ``settings.py``

POLLA_REPLACE_DOTS_IN_DOMAINS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This setting is set to ``False`` by default. For people wanting to use Polla as or drop-in replacement for ``dynamicsites`` or would like to use the Urls feature, you shoud set it tu ``True``.

Setting ``POLLA_REPLACE_DOTS_IN_DOMAINS`` will change the default behaviour when it comes to looking for site specific features.

e.g: you are trying to load a template named ``base.html`` for the site ``example.com``. having ``POLLA_REPLACE_DOTS_IN_DOMAINS`` set to ``True`` django will try looking for it under ``sites/example_com/templates/base.html`` instead of the default ``sites/example.com/templates/base.html``

.. note::
    In any case directory names are lower-case


TemplateLoader
--------------

Polla provides a TemplateLoader allowing you to load different templates according to the requested host. Specific templates should be hosted in the special under the directory configured in ``POLLA_SITES_DIR`` under a sub-directory corresponding to the main domain name (the domain name in ``Site``).

To enable Polla's template loader, you have to make the following changes to your settings.py:
::
    TEMPLATES = [
        {
            ...
            ## Make sure APP_DIRS is set to False
            'APP_DIRS': False,
            'OPTIONS': {
                ...
                ## add a loaders option
                'loaders': (
                    'polla.template_loader.Loader',
                    ## Django uses the filesystem loader by default, I tend to try to avoid it
                    ## but it's up to you
                    # 'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader'
                ),
            },
        },
    ]

Now you can write ``example.com`` specific templates in ``sites/example.com/templates/``

.. note::
    As with the other loaders, you will have to restart runserver in order for Django to find newly added templates.


StaticFile Finder
-----------------

Polla provides a StaticFile Finder to allow you to host site specific static files (js, css, img, etc).

Site specific should be located under ``sites/<main domain name>/static/<file path>`` and they will be served under ``<STATIC_ROOT>/<main domain name>/<file path>``

To enable Polla's StaticFile Finder, you have to make the following changes to your settings.py:
::
    ## Add the STATICFILES_FINDERS directive
    STATICFILES_FINDERS = (
        "polla.staticfiles_finder.SiteFinder",
        ## Django uses the filesystem finder by default, I tend to try to avoid it.
        ## This one is up to you too
        # "django.contrib.staticfiles.finders.FileSystemFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    )

With this setting, ``collectstatic`` will collect files in ``sites/<domain name>`` for every domain listed in ``Site``

.. warning::
    Using this method will, by default, expose static files of **every** ``Site`` to **any** ``Site`` running under the same Django project.
    e.g: ``css/site.css`` sprcific to ``site-a.com`` wil be available on ``http://site-a.com/static/site-a.com/css/site.css`` as well as on ``http://site-b.com/static/site-a.com/css/site.css`` (provided ``site-b.com`` runs under the same django project).
    This side-effect might not be desirable and may be prevented using a clever configuration on your web server.

sitestatic templatetags library
-------------------------------

To go hand-in-hand with the StaticFile finder, Polla provides a replacement for ``staticfiles`` templatetags library. To use it, simply replace ``{% load staticfiles %}`` with ``{% load sitestatic %}`` in your templates.

The ``static`` templatetag from ``sitestatic`` will first try to find site-specific static files before defaulting to ``staticfiles`` behaviour.
::
    {% load sitestatic %}
    <html>
      <head>
        <link rel="stylesheet" href="{% static 'css/site.css' %}">
      </head>
      ...


UrlPatterns
-----------

.. note::
    To use this feature, make sure you set ``POLLA_REPLACE_DOTS_IN_DOMAINS`` to ``True`` in your ``settings.py``
    On Python 2 also make sure to include ``__init__.py`` in both ``sites`` and it's sub_directory

Polla allows you to define different urlpatterns for specific domains. To use this feature, update your main ``urls.py`` to look like this
::
    ...
    from polla import urls


    urlpatterns = urls.UrlPatterns([
        # Place your patterns here
        ...
        url(...),
    ])

Wrapping the ``urlpatterns`` list with ``UrlPattern`` will allow Polla to check for a urls.py files in ``sites/<your underscored domain name>/``. If it finds one, it will load it instead of the default provided ``urlpatterns``.

If you need common urls feel free to extend the ``UrlPattern`` wrapper with a list of common urls like this
::
    urlpatterns += [
        url(r'^' + settings.STATIC_URL[1:] + r'(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]
