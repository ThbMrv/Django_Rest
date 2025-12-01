from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework import permissions
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiResponse
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
        # Require authentication for POST (create)
        if not getattr(request, 'user', None) or not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ConcessionnaireSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save(owner=request.user)
            return Response(ConcessionnaireSerializer(obj).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConcessionnaireDetail(APIView):
    def get(self, request, pk):
        obj = get_object_or_404(Concessionnaire, pk=pk)
        serializer = ConcessionnaireSerializer(obj)
        return Response(serializer.data)

    def _check_owner(self, obj, user):
        if not user or not user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        if obj.owner_id != user.id:
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        return None

    def put(self, request, pk):
        obj = get_object_or_404(Concessionnaire, pk=pk)
        denied = self._check_owner(obj, request.user)
        if denied: return denied
        serializer = ConcessionnaireSerializer(obj, data=request.data)
        if serializer.is_valid():
            updated = serializer.save()
            return Response(ConcessionnaireSerializer(updated).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        obj = get_object_or_404(Concessionnaire, pk=pk)
        denied = self._check_owner(obj, request.user)
        if denied: return denied
        serializer = ConcessionnaireSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            updated = serializer.save()
            return Response(ConcessionnaireSerializer(updated).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = get_object_or_404(Concessionnaire, pk=pk)
        denied = self._check_owner(obj, request.user)
        if denied: return denied
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VehiculeList(APIView):
    def get(self, request, concession_id):
        concession = get_object_or_404(Concessionnaire, pk=concession_id)
        qs = Vehicule.objects.filter(concessionnaire=concession)
        serializer = VehiculeSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, concession_id):
        if not getattr(request, 'user', None) or not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

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

    def _check_owner_of_concession(self, concession, user):
        if not user or not user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        if concession.owner_id != user.id:
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        return None

    def put(self, request, concession_id, pk):
        veh = get_object_or_404(Vehicule, pk=pk, concessionnaire_id=concession_id)
        concession = veh.concessionnaire
        denied = self._check_owner_of_concession(concession, request.user)
        if denied: return denied
        serializer = VehiculeSerializer(veh, data=request.data)
        if serializer.is_valid():
            updated = serializer.save()
            return Response(VehiculeSerializer(updated).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, concession_id, pk):
        veh = get_object_or_404(Vehicule, pk=pk, concessionnaire_id=concession_id)
        concession = veh.concessionnaire
        denied = self._check_owner_of_concession(concession, request.user)
        if denied: return denied
        serializer = VehiculeSerializer(veh, data=request.data, partial=True)
        if serializer.is_valid():
            updated = serializer.save()
            return Response(VehiculeSerializer(updated).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, concession_id, pk):
        veh = get_object_or_404(Vehicule, pk=pk, concessionnaire_id=concession_id)
        concession = veh.concessionnaire
        denied = self._check_owner_of_concession(concession, request.user)
        if denied: return denied
        veh.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@ensure_csrf_cookie
def get_csrf(request):
    token = get_token(request)
    return JsonResponse({'csrf': token})


from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        email = validated_data.get('email', '')
        user = User(username=validated_data['username'], email=email)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserCreate(APIView):
    """Create a new user (POST /api/users/).

    Expected payload: {"username": "name", "password": "pw"}
    Returns the created user's `id` and `username` on success.
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
