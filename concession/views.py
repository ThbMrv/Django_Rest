from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Concessionnaire, Vehicule
from .serializers import ConcessionnaireSerializer, VehiculeSerializer
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie



class ConcessionnaireList(APIView):
    def get(self, request):
        qs = Concessionnaire.objects.all()
        serializer = ConcessionnaireSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ConcessionnaireSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(ConcessionnaireSerializer(obj).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConcessionnaireDetail(APIView):
    def get(self, request, pk):
        obj = get_object_or_404(Concessionnaire, pk=pk)
        serializer = ConcessionnaireSerializer(obj)
        return Response(serializer.data)


class VehiculeList(APIView):
    def get(self, request, concession_id):
        concession = get_object_or_404(Concessionnaire, pk=concession_id)
        qs = Vehicule.objects.filter(concessionnaire=concession)
        serializer = VehiculeSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, concession_id):
        # create a vehicule attached to the concessionnaire in the URL
        concession = get_object_or_404(Concessionnaire, pk=concession_id)
        data = request.data.copy()
        data['concessionnaire'] = concession_id
        serializer = VehiculeSerializer(data=data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(VehiculeSerializer(obj).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VehiculeDetail(APIView):
    def get(self, request, concession_id, pk):
        veh = get_object_or_404(Vehicule, pk=pk, concessionnaire_id=concession_id)
        serializer = VehiculeSerializer(veh)
        return Response(serializer.data)


@ensure_csrf_cookie
def get_csrf(request):
    """Return a JSON response with the CSRF token and ensure the CSRF cookie is set.

    Frontend should call this endpoint (GET /api/csrf/) before making POST requests.
    """
    token = get_token(request)
    return JsonResponse({'csrf': token})
