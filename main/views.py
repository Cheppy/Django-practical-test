from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError

from .models import CV, Language
from .utils import generate_pdf_sync
from .translation import translate_text
from rest_framework import viewsets, permissions
from .serializers import CVSerializer
import logging
import json

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['languages'] = Language.objects.all()
        return context

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

@require_POST
def translate_cv(request: HttpRequest, pk: int) -> JsonResponse:
    """Translate CV content to the selected language
    
    Args:
        request: The HTTP request containing the target language
        pk: The primary key of the CV
        
    Returns:
        JsonResponse: The translated CV content
    """
    try:
        cv = get_object_or_404(CV, pk=pk)
        data = json.loads(request.body)
        target_language = data.get('language')
        
        if not target_language:
            raise ValidationError("Language not specified")
            
        # Translate each field
        translated = {
            'firstname': cv.firstname,  # Keep names untranslated
            'lastname': cv.lastname,    # Keep names untranslated
            'bio': translate_text(cv.bio, target_language),
            'skills': translate_text(cv.skills, target_language),
            'projects': translate_text(cv.projects, target_language),
            'contacts': translate_text(cv.contacts, target_language)
        }
        
        return JsonResponse({
            'success': True,
            'translated': translated
        })
        
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

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
