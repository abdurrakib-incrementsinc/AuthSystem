from rest_framework import viewsets
from ..models import Branch, Floor, Table, Restaurant
from restaurant.serializers import BranchSerializer, FloorSerializer, TableSerializer


class BranchViewSets(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        user = self.request.user
        slug = self.request.query_params.get('slug', None)

        if user.is_superuser:
            return self.queryset
        elif user.is_anonymous:
            return None
        elif slug:
            return Branch.objects.get(slug=slug)

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
            return None
        elif slug:
            return Floor.objects.get(slug=slug)

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
            return None
        elif slug:
            return Table.objects.get(slug=slug)
