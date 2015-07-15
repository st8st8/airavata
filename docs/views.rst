Views
=====

Polla provides a mixin for filtering views. Originally ``SingleObjectMixin`` and ``MultipleObjectMixin`` subclasses but feel free to use it on any View which provides a ``get_queryset`` method.

``SiteFilteredViewMixin`` filters ``get_queryset`` by the current site. By default ``SiteFilteredViewMixin`` looks for a ``site`` field but you can override this with the ``site_field`` parameter.
::

    from django.views.generic import DetailView, ListView
    from polla.views import SiteFilteredViewMixin
    
    from .models import MyModel
    
    
    class MyModelListView(SiteFilteredViewMixin, ListView):
    
      model = MyModel
    
    
    class MyModelDetailView(SiteFilteredViewMixin, DetailView):
    
      model = MyModel
      site_field = 'base_site'

