from rest_framework import viewsets
from career.models import CareerPath
from career.serializers import careerPath_serializer
from utils.permissions import AdminOnlyPost

class CareerPathViewSet(viewsets.ModelViewSet):
    queryset = CareerPath.objects.all().select_related('career', 'course')
    permission_classes = [AdminOnlyPost]

    def get_serializer_class(self):
        if self.request.method in ['GET']: 
            return careerPath_serializer.CareerPathReadSerializer
        return careerPath_serializer.CareerPathCreateSerializer