from django.views.generic import ListView, DetailView
from .models import CV

# Create your views here.

class CVListView(ListView):
    model = CV
    template_name = 'main/cv_list.html'
    context_object_name = 'cvs'
    ordering = ['-created_at']  # Show newest CVs first

class CVDetailView(DetailView):
    model = CV
    template_name = 'main/cv_detail.html'
    context_object_name = 'cv'
