Advanced usage
==============

.. warning::
    Those advanced usages are only available on the dev version (eg: not on the PyPi version) of Polla.

.. danger::
    These advanced usages all require to resort to *local threads* to be able to access the current request. Some people have `strong feeelings against local threads use in Django <https://groups.google.com/forum/?fromgroups=#!topic/django-users/5681nX0YPgQ>`_. Local threads in themselves (in our humble opinion) are not a security risk but may amplify some other security risks. So before you use them, make sure you know what you are getting into.

Extra requirement
-----------------

As said above threadlocals is an extra requirement for the advanced features, so go ahead and pip install it
::
    pip install django-threadlocals

Common Settings
---------------

To use any of the following features, make sure you enable the `LocalThreadMiddleware`.
::
    ##settings.py
    MIDDLEWARE_CLASSES = (
        ...
        'polla.middleware.ThreadLocalMiddleware',
    )


POLLA_SITES_DIR
~~~~~~~~~~~~~~~

Every site-specific feature (template, urls, static file) is hosted under a main directory (``BASE_DIR/sites`` by default), to override it, provide ``POLLA_SITES_DIR`` in your ``settings.py``

POLLA_REPLACE_DOTS_IN_DOMAINS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This setting is set to ``False`` by default. For people wanting to use Polla as or drop-in replacement for ``dynamicsites``, you shoud set it tu ``True``.

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

Site specific should be hosted under ``sites/<main domain name>/static/<main domain name>``

.. warning
    This will probably change in V0.9.1, the second ``<main domain name>`` will likely get dropped

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


