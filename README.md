# Django Polla

Python 2.7 [![Build Status](http://jenkins.lasolution.be/buildStatus/icon?job=Polla/PYTHON=System-CPython-2.7)](http://jenkins.lasolution.be/view/Levit/job/Polla/PYTHON=System-CPython-2.7)
Python 3.2 [![Build Status](http://jenkins.lasolution.be/buildStatus/icon?job=Polla/PYTHON=System-CPython-3.2)](http://jenkins.lasolution.be/view/Levit/job/Polla/PYTHON=System-CPython-3.2/)
Python 3.4 [![Build Status](http://jenkins.lasolution.be/buildStatus/icon?job=Polla/PYTHON=CPython-3.4)](http://jenkins.lasolution.be/view/Levit/job/Polla/PYTHON=CPython-3.4/)


Polla (πολλά - in Greek "lots of / multi") is a Django 1.8+ library that allows you to hosts multiple dynamic sites running on a single Django instance/db.

I have been using a customized version of [dynamicsites](https://bitbucket.org/uysrc/django-dynamicsites/overview) for a while now. But with the new features form Django 1.7 and 1.8, there exists another simpler, and more pythonesque IMHO, way to achieve the same results. Polla is an attempt at that *other* way.

## Getting started
### Install

`pip install django_polla`

### Configure
Add `polla` and `django.contrib.sites` to your installed apps

```
## settings.py
INSTALLED_APPS = [
    ...
    'django.contrib.sites',
    'polla',
]
```

_Make sure SITE_ID in not set in_ `settings.py`

### ALLOWED_HOSTS

Polla provides two wrapper classes to fetch `ALLOWED_HOSTS` from the database instead of hard-coding them.
These two classes were largely inspired by (read mostly copied from) [kezabelle's django-allowedsites](https://github.com/kezabelle/django-allowedsites).
Namely they are `polla.utils.AllowedSites` and `polla.utils.CachedAllowedSites`. Use either of those in your settings.py

```
## settings.py
from polla.utils import CachedAllowedSites
ALLOWED_HOSTS = CachedAllowedSites()
```

### Set the domain for your primary site

Once `django.contrib.sites` is added to your `settings.py` Django won't let you access your website unless one of teh following is true:

* `SITE_ID` is also set in your `settings.py` (which we don't want to do since this library is for hosting _multiple dynamic_ sites)
* `DEBUG` is set to `True` which is ok for dev but not for live servers
* Django finds a `Site` (or a `SiteAlias` with Polla) corresponding to the `host` you are requesting

In order to set the correct domain on the first site in your database, Polla provides a management command. Simply run

`python manage.py setprimarydomain`


## Models

Polla provides a `SiteAlias` model which allows you to create domain aliases. Even though serving the same content from different hostnames is not advisable it can be useful in at least 2 cases:

* local dev with live-ish data: simply create an alias to your existing site
* BitBucket-style case where main domain/address https://bitbucket.org/levit_scs/django-polla has a convenience alias on http://bb.levit.be/django-polla

## Views

Polla provides a mixin for filtering views. Originally `SingleObjectMixin` and `MultipleObjectMixin` subclasses but feel free to use it on any View which provides a `get_queryset` method.

`SiteFilteredViewMixin` filters `get_queryset` by the current site. By default `SiteFilteredViewMixin` looks for a `site` field but you can override with the `site_field` parameter.

```
from django.views.generic import DetailView, ListView
from polla.views import SiteFilteredViewMixin

from .models import MyModel


class MyModelListView(SiteFilteredViewMixin, ListView):

  model = MyModel


class MyModelDetailView(SiteFilteredViewMixin, DetailView):

  model = MyModel
  site_field = 'base_site'
```


## Extras

As serving multiple dynamic sites is highly dependent on the requested host. Polla adds validators to `Site` and `SiteAlias` in order to make sure domain names are unique.


## ToDo

* allow different name_based urlpatterns to be applied depending on the requested host
* allow to use a different set of temples depending on the requested host
* allow serving different static files depending on the requested host
* improve this doc


This project is licensed under the [BSD 2-Clause License](http://bb.levit.be/django-polla/src/default/LICENSE.txt)
