.. Django Polla documentation master file, created by
   sphinx-quickstart on Sun Apr  5 14:11:15 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Django Polla's documentation!
========================================

Polla (πολλά - in Greek "lots of / multi") is a Django 1.8+ library that allows you to hosts multiple dynamic sites running on a single Django instance/db.

I have been using a customized version of `dynamicsites <https://bitbucket.org/uysrc/django-dynamicsites/overview>`_ for a while now. But with the new features from Django 1.7 and 1.8, there exists another simpler, and more pythonesque IMHO, way to achieve the same results. Polla is an attempt at that *other* way.


Getting started
===============

Install
-------

``pip install polla``

Configure
~~~~~~~~~

Add ``polla`` and ``django.contrib.sites`` to your installed apps
::
    ## settings.py
    INSTALLED_APPS = [
        ...
        'django.contrib.sites',
        'polla',
    ]

**Make sure SITE_ID in not set in** ``settings.py``

ALLOWED_HOSTS
~~~~~~~~~~~~~

Polla provides two wrapper classes to fetch ``ALLOWED_HOSTS`` from the database instead of hard-coding them.
These two classes were largely inspired by (read mostly copied from) `kezabelle's django-allowedsites <https://github.com/kezabelle/django-allowedsites>`_.
Namely they are ``polla.utils.AllowedSites`` and ``polla.utils.CachedAllowedSites``. Use either of those in your settings.py
::
    ## settings.py
    from polla.utils import AllowedSites
    ALLOWED_HOSTS = AllowedSites()

Cache invalidation
~~~~~~~~~~~~~~~~~~

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

Also note that cache is supposed to be shared among Django instances in order for this process to work. Read `more about cache <https://docs.djangoproject.com/en/1.8/topics/cache/#setting-up-the-cache>`_

Set the domain for your primary site
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once ``django.contrib.sites`` is added to your ``settings.py`` Django won't let you access your website unless one of teh following is true:

* ``SITE_ID`` is also set in your ``settings.py`` (which we don't want to do since this library is for hosting *multiple dynamic* sites)
* ``DEBUG`` is set to ``True`` which is ok for dev but not for live servers
* **Django finds a** ``Site`` **(or a** ``SiteAlias`` **with Polla) corresponding to the** ``host`` **you are requesting**

In order to set the correct domain on the first site in your database, Polla provides a management command. Simply run

``python manage.py setprimarydomain``


Models
======

Polla provides a ``SiteAlias`` model which allows you to create domain aliases. Even though serving the same content from different hostnames is not advisable it can be useful in at least 2 cases:

* local dev with live-ish data: simply create an alias to your existing site
* BitBucket-style case where main domain/address https://bitbucket.org/levit_scs/django-polla has a convenience alias on http://bb.levit.be/django-polla

Views
=====

Polla provides a mixin for filtering views. Originally ``SingleObjectMixin`` and ``MultipleObjectMixin`` subclasses but feel free to use it on any View which provides a ``get_queryset`` method.

``SiteFilteredViewMixin`` filters ``get_queryset`` by the current site. By default ``SiteFilteredViewMixin`` looks for a ``site`` field but you can override with the ``site_field`` parameter.
::

    from django.views.generic import DetailView, ListView
    from polla.views import SiteFilteredViewMixin
    
    from .models import MyModel
    
    
    class MyModelListView(SiteFilteredViewMixin, ListView):
    
      model = MyModel
    
    
    class MyModelDetailView(SiteFilteredViewMixin, DetailView):
    
      model = MyModel
      site_field = 'base_site'


Extras
======

As serving multiple dynamic sites is highly dependent on the requested host. Polla adds validators to ``Site`` and ``SiteAlias`` in order to make sure domain names are unique.


ToDo
====

* allow different name_based urlpatterns to be applied depending on the requested host
* allow to use a different set of temples depending on the requested host
* allow serving different static files depending on the requested host
* improve this doc


This project is licensed under the `BSD 2-Clause License <http://bb.levit.be/django-polla/src/default/LICENSE.txt>`_


.. toctree::
   :maxdepth: 2
