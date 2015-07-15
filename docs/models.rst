Models
======

Airavata provides a ``SiteAlias`` model which allows you to create domain aliases. Even though serving the same content from different hostnames is not advisable it can be useful in at least 2 cases:

* local dev with live-ish data: simply create an alias to your existing site
* BitBucket-style case where main domain/address https://bitbucket.org/levit_scs/django-airavata has a convenience alias on http://bb.levit.be/django-airavata
