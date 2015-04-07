What is Polla?
==============

Ever wanted to run several sites using the same codebase and the same database without having to deploy (and maintain) several instances of your project? Than Polla is for you!

Polla is a tool to ease the burden of such development.

Features
--------

* ``SiteAlias``: Polla add site aliases (other domain names) to the sites framework to allow having several domain names pointing to the same site (eg: http://john-doe.my-shiny-cms-platform.com and http://john-doe.com)
* ``get_current_site``: Polla leverages the changed behaviour of `get_current_site <https://docs.djangoproject.com/en/1.8/ref/contrib/sites/#get-current-site-shortcut>`_ in Django 1.8 and patches it to extend lookups to site aliases
* ``setprimarydomain``: Polla provides a management command to change the first domain name in the database and optionally create an alias for 'localhost'
* ``SiteFilteredViewMixin``: Polla provides a view mixin, to use with Django's generic class based views, which filters results based on the current site
* Unique domains names: Polla patches the sites framework to ensure that domain names are unique.
* ``AllowedSites`` and ``CachedAllowedSites``: Polla provides 2 helper classes to use in your settings.py in order to fetch ``ALLOWED_HOSTS`` list from the database.

ToDo
----

* dependency django-allowedsites
* dependency django-threadlocals
* improve test coverage
* improve this doc


