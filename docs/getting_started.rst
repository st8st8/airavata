Getting started
===============

Install
-------

``pip install polla``

Configure
---------

Add ``polla`` and ``django.contrib.sites`` to your installed apps
::
    ## settings.py
    INSTALLED_APPS = [
        ...
        'django.contrib.sites',
        'polla',
    ]

.. danger::
   Make sure SITE_ID in not set in ``settings.py``

ALLOWED_HOSTS
-------------

Polla provides two wrapper classes to fetch ``ALLOWED_HOSTS`` from the database instead of hard-coding them.
These two classes were largely inspired by (read mostly copied from) `kezabelle's django-allowedsites <https://github.com/kezabelle/django-allowedsites>`_.
Namely they are ``polla.utils.AllowedSites`` and ``polla.utils.CachedAllowedSites``. Use either of those in your settings.py
::
    ## settings.py
    from polla.utils import AllowedSites
    ALLOWED_HOSTS = AllowedSites()

Cache invalidation
------------------

If you are planning on using CachedAllowedSites, don't forget to register cache invalidation signals in your `AppConfig <https://docs.djangoproject.com/en/1.8/ref/applications/#django.apps.AppConfig.ready>`_.
::
    ## apps.py
    from django.apps import AppConfig
    from polla.utils import register_signals
    
    class MyAppConfig(AppConfig):
      name = 'my_app'
      verbose_name = "My app"
    
      def ready(self):
            from django.contrib.sites.models import Site
            from polla.models import SiteAlias
            for model in [Site, SiteAlias]:
                register_signals(model)
    
    ## __init__.py
    default_app_config = 'my_app.apps.MyAppConfig'

.. note::
   Cache is supposed to be shared among Django instances in order for this process to work. Read `more about cache <https://docs.djangoproject.com/en/1.8/topics/cache/#setting-up-the-cache>`_

Set the domain for your primary site
------------------------------------

Once ``django.contrib.sites`` is added to your ``settings.py`` Django won't let you access your website unless one of teh following is true:

* ``SITE_ID`` is also set in your ``settings.py`` (which we don't want to do since this library is for hosting *multiple dynamic* sites)
* ``DEBUG`` is set to ``True`` which is ok for dev but not for live servers
* **Django finds a** ``Site`` **(or a** ``SiteAlias`` **with Polla) corresponding to the** ``host`` **you are requesting**

In order to set the correct domain on the first site in your database, Polla provides a management command. Simply run

``python manage.py setprimarydomain``

