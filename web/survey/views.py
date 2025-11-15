from rest_framework.generics import CreateAPIView
from .models import SurveyRequest
from .serializers import SurveyRequestSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class SurveyCreateAPIView(CreateAPIView):
    queryset = SurveyRequest.objects.all()
    serializer_class = SurveyRequestSerializer

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
