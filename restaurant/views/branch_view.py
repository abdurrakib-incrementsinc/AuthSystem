from io import BytesIO
import requests
from rest_framework import viewsets
from ..models import Branch, Floor, Table
from restaurant.serializers import BranchSerializer, FloorSerializer, TableSerializer
from PIL import Image
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action


class BranchViewSets(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        user = self.request.user
        slug = self.request.query_params.get('slug', None)
        if user.is_superuser:
            return self.queryset
        if user.is_anonymous:
            return Branch.objects.none()
        if user.is_owner:
            return Branch.objects.filter(restaurant__owner=user)
        if slug:
            return get_object_or_404(Branch, slug=slug)

    @action(detail=False, methods=['GET'])
    def download_qr_pdf(self, request, *args, **kwargs):
        slug = self.request.query_params.get('slug', None)
        branch = Branch.objects.get(slug=slug)
        image_url = request.build_absolute_uri(branch.qr_image.url)

        # Make a request to the image URL
        response = requests.get(image_url)
        if response.status_code == 200:
            # Open the image using PIL
            image = Image.open(BytesIO(response.content))

            # Now you can work with the 'image' object
            # For example, save it as PDF
            pdf_buffer = BytesIO()
            image.save(pdf_buffer, format='PDF')

            # Set the response headers for a PDF file
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="qr_image.pdf"'

            # Write the PDF content to the response
            pdf_buffer.seek(0)
            response.write(pdf_buffer.read())

            return response
        else:
            return HttpResponse(f"Failed to retrieve the image. Status code: {response.status_code}")

    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)


class FloorViewSets(viewsets.ModelViewSet):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        user = self.request.user
        slug = self.request.query_params.get('slug', None)

        if user.is_superuser:
            return self.queryset
        elif user.is_anonymous:
            return Floor.objects.none()
        elif slug:
            return get_object_or_404(Floor, slug=slug)

    def perform_create(self, serializer):
        branch = Branch.objects.get(manager=self.request.user)
        serializer.save(branch=branch)


class TableViewSets(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        user = self.request.user
        slug = self.request.query_params.get('slug', None)

        if user.is_superuser:
            return self.queryset
        elif user.is_anonymous:
            return Table.objects.none()
        elif slug:
            return get_object_or_404(Table, slug=slug)
