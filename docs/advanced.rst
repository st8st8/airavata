Advanced usage
==============

.. danger::
    These advanced usages all require to resort to *local threads* to be able to access the current *requested domain name*. Some people have `strong feeelings against local threads variables use in Django <https://groups.google.com/forum/?fromgroups=#!topic/django-users/5681nX0YPgQ>`_. Local threads in themselves (in our humble opinion) are not a security risk but may amplify some other security risks if you use them to store sensitive information.
    
    Airavata uses local threads to store the *requested host name*. If you feel this is sensitive information, make sure you know what you are getting into.

Extra requirement
-----------------

As said above ``threadlocals`` is an extra requirement for the advanced features to work, so go ahead and pip install it
::
    pip install django-threadlocals

Common Settings
---------------

To use any of the following features, make sure you enable `LocalThreadMiddleware` (put it before ``django.middleware.common.CommonMiddleware``.
::
    ##settings.py
    MIDDLEWARE_CLASSES = (
        'airavata.middleware.ThreadLocalMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        ...
    )


AIRAVATA_SITES_DIR
~~~~~~~~~~~~~~~

Every site-specific feature (template, urls, static file) is hosted under a main directory (``BASE_DIR/sites`` by default), to override it, provide ``AIRAVATA_SITES_DIR`` in your ``settings.py``

AIRAVATA_REPLACE_DOTS_IN_DOMAINS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This setting is set to ``False`` by default. For people wanting to use Airavata as a drop-in replacement for ``dynamicsites`` or who would like to use the **Urls** feature, you shoud set it to ``True``.

Setting ``AIRAVATA_REPLACE_DOTS_IN_DOMAINS`` will change the default behaviour when it comes to looking for site specific features.

e.g: you are trying to load a template named ``base.html`` for the site ``example.com``. having ``AIRAVATA_REPLACE_DOTS_IN_DOMAINS`` set to ``True`` django will try looking for it under ``sites/example_com/templates/base.html`` instead of the default ``sites/example.com/templates/base.html``

.. note::
    In any case directory names are lower-case


TemplateLoader
--------------

Airavata provides a TemplateLoader allowing you to load different templates according to the requested host. Specific templates should be placed under the directory configured in ``AIRAVATA_SITES_DIR`` under a sub-directory corresponding to the main domain name (the domain name in ``Site``).

To enable Airavata's template loader, you have to make the following changes to your settings.py:
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
                    'airavata.template_loader.Loader',
                    ## Django uses the filesystem loader by default, I tend to try to avoid it
                    ## but it's up to you
                    # 'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader'
                ),
            },
        },
    ]

Now you can write ``example.com`` specific templates in ``sites/example.com/templates/`` (or ``sites/example_com/templates/`` depending on your settings)

.. note::
    As with the other loaders, you will have to restart the web server in order for Django to find newly added templates.


StaticFile Finder
-----------------

Airavata provides a StaticFile Finder to allow you to host site specific static files (js, css, img, etc).

Site specific should be located under ``sites/<main domain name>/static/<file path>`` and they will be served under ``<STATIC_ROOT>/<main domain name>/<file path>``

To enable Airavata's StaticFile Finder, you have to make the following changes to your settings.py:
::
    ## Add the STATICFILES_FINDERS directive
    STATICFILES_FINDERS = (
        "airavata.staticfiles_finder.SiteFinder",
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

To go hand-in-hand with the StaticFile finder, Airavata provides a replacement for ``staticfiles`` templatetags library. To use it, simply replace ``{% load staticfiles %}`` with ``{% load sitestatic %}`` in your templates.

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
    To use this feature, make sure you set ``AIRAVATA_REPLACE_DOTS_IN_DOMAINS`` to ``True`` in your ``settings.py``
    On Python 2 also make sure to include ``__init__.py`` in both ``sites`` and it's sub_directory

Airavata allows you to define different urlpatterns for specific domains. To use this feature, update your main ``urls.py`` to look like this
::
    ...
    from airavata import urls


    urlpatterns = urls.UrlPatterns([
        # Place your patterns here
        ...
        url(...),
    ])

Wrapping the ``urlpatterns`` list within ``UrlPattern`` will allow Airavata to check for a ``urls.py`` file in ``sites/<your underscored domain name>/``. If it finds one, it will load it instead of the default provided ``urlpatterns``.

If you need common urls feel free to extend the ``UrlPattern`` wrapper with a list of common urls like this
::
    urlpatterns += [
        url(r'^' + settings.STATIC_URL[1:] + r'(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]
