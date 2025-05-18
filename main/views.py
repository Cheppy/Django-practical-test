from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, HttpRequest
from django.urls import reverse

from .models import CV
from .utils import generate_pdf_sync
from rest_framework import viewsets, permissions
from .serializers import CVSerializer
import logging

logger = logging.getLogger(__name__)

class CVListView(ListView):
    model = CV
    template_name = 'main/cv_list.html'
    context_object_name = 'cvs'
    ordering = ['-created_at']  # Show newest CVs first

class CVDetailView(DetailView):
    model = CV
    template_name = 'main/cv_detail.html'
    context_object_name = 'cv'

def cv_pdf(request: HttpRequest, pk: int) -> HttpResponse:
    """Generate PDF for a CV
    
    Args:
        request: The HTTP request
        pk: The primary key of the CV
        
    Returns:
        HttpResponse: The PDF response
    """
    logger.info(f"Starting PDF generation for CV {pk}")
    
    cv: CV = get_object_or_404(CV, pk=pk)
    
    url: str = request.build_absolute_uri(reverse('cv_detail', args=[pk]))
    logger.debug(f"Generated URL: {url}")
    
    try:
        pdf: bytes = generate_pdf_sync(url)
        logger.info("PDF generated successfully")
        
        response: HttpResponse = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{cv.firstname}_{cv.lastname}_CV.pdf"'
        return response
        
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        raise

class CVViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CVs to be viewed or edited.
    """
    queryset = CV.objects.all().order_by('-created_at')
    serializer_class = CVSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self) -> list[CV]:
        queryset = CV.objects.all().order_by('-created_at')
        logger.info(f"Retrieved {queryset.count()} CVs from database")
        for cv in queryset:
            logger.debug(f"CV: {cv.firstname} {cv.lastname} (ID: {cv.id})")
        return queryset

    def perform_create(self, serializer) -> None:
        logger.info("Creating new CV")
        serializer.save()
        logger.info(f"Created CV: {serializer.instance.firstname} {serializer.instance.lastname} (ID: {serializer.instance.id})")

    def list(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        logger.info(f"Listing CVs. User: {request.user}, Authenticated: {request.user.is_authenticated}")
        return super().list(request, *args, **kwargs)
