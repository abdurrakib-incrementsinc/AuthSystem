from django.urls import path
from .views import PdfExtractionView

urlpatterns = [
    path('', PdfExtractionView.as_view(), name='PdfExtraction'),
]
