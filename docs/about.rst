What is Polla?
==============

Ever wanted to run several sites using the same codebase and the same database without having to deploy (and maintain) several instances of your project? Than Polla is for you!
The new (Django 1.8+) implementation of ``django.contrib.sites`` already makes things easier but is still missing (probably by design) some usefull features.

Polla is a tool providing those features.

Features
--------

* ``SiteAlias``: Polla adds site aliases (other domain names) to the sites framework to allow having several domain names pointing to the same site (eg: http://john-doe.my-shiny-cms-platform.com and http://john-doe.com)
* ``get_current_site``: Polla leverages the changed behaviour of `get_current_site <https://docs.djangoproject.com/en/1.8/ref/contrib/sites/#get-current-site-shortcut>`_ in Django 1.8 and patches it to extend lookups to site aliases
* ``setprimarydomain``: Polla provides a management command to change the first domain name in the database and optionally create an alias for 'localhost'
* ``SiteFilteredViewMixin``: Polla provides a view mixin, to use with Django's generic class based views, which filters results based on the current site
* Unique domains names: Polla patches the sites framework to ensure that domain names are unique across ``Site`` and ``SiteAlias``.
* ``AllowedSites`` and ``CachedAllowedSites``: Polla provides 2 helper classes extended from `django-allowedsites <https://github.com/kezabelle/django-allowedsites>`_ to use in your settings.py in order to fetch ``ALLOWED_HOSTS`` list from the database.

ToDo
----

* improve test coverage
* improve this doc
* Media file "finder" and upload_path builder
* provide a SiteFilteredModelAdmin


