from rest_framework import viewsets
from career.models import Career
from career.serializers import career_serializer
from utils.permissions import AdminOnlyPost

class CareerViewSet(viewsets.ModelViewSet):
    queryset = Career.objects.all()
    permission_classes = [AdminOnlyPost]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return career_serializer.CareerReadSerializer
        return career_serializer.CareerCreateSerializer