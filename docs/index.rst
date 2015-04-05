.. Django Polla documentation master file, created by
   sphinx-quickstart on Sun Apr  5 14:11:15 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Django Polla's documentation!
========================================

.. |status27| image:: http://jenkins.lasolution.be/buildStatus/icon?job=Polla/PYTHON=System-CPython-2.7
.. |status32| image:: http://jenkins.lasolution.be/buildStatus/icon?job=Polla/PYTHON=System-CPython-3.2
.. |status34| image:: http://jenkins.lasolution.be/buildStatus/icon?job=Polla/PYTHON=CPython-3.4
.. |docs| image:: https://readthedocs.org/projects/django-polla/badge/?version=latest
.. |pypiv| image:: https://pypip.in/v/polla/badge.png
.. |pypid| image:: https://pypip.in/d/polla/badge.png

+-----------------------+-----------------------+-----------------------+
| Python 2.7 |status27| | Python 3.2 |status32| | Python 3.4 |status34| |
+-----------------------+-----------------------+-----------------------+
| Docs |docs|           | Version |pypiv|       | |pypid|               |
+-----------------------+-----------------------+-----------------------+

Polla (πολλά - in Greek "lots of / multi") is a Django 1.8+ library that allows you to hosts multiple dynamic sites running on a single Django instance/db.

I have been using a customized version of `dynamicsites <https://bitbucket.org/uysrc/django-dynamicsites/overview>`_ for a while now. But with the new features from Django 1.7 and 1.8, there exists another simpler, and more pythonesque IMHO, way to achieve the same results. Polla is an attempt at that *other* way.


This project is licensed under the `BSD 2-Clause License <http://bb.levit.be/django-polla/src/default/LICENSE.txt>`_


Content:

.. toctree::
   :maxdepth: 2
   
   about
   getting_started
   models
   views
   contributing
