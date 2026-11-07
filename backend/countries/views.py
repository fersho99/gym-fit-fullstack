from drf_yasg.utils import swagger_auto_schema
from requests.exceptions import RequestException
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from zeep.exceptions import Error as ZeepError

from countries.services import PaisNoEncontrado, consultar_pais


class MonedaSerializer(serializers.Serializer):
    codigo = serializers.CharField()
    nombre = serializers.CharField()


class PaisSerializer(serializers.Serializer):
    """Solo documenta en Swagger la respuesta del servicio."""

    codigo = serializers.CharField()
    nombre = serializers.CharField()
    capital = serializers.CharField()
    moneda = MonedaSerializer()
    codigo_telefonico = serializers.CharField()
    bandera = serializers.URLField()
    fuente = serializers.CharField()


class PaisSoapView(APIView):
    """Consulta los datos de un país en un Web Service SOAP público usando zeep."""

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: PaisSerializer, 404: 'País no encontrado', 502: 'Servicio SOAP no disponible'})
    def get(self, request, codigo_iso):
        try:
            return Response(consultar_pais(codigo_iso))
        except PaisNoEncontrado:
            return Response({'detail': 'País no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except (ZeepError, RequestException):
            return Response({'detail': 'El servicio SOAP no está disponible.'}, status=status.HTTP_502_BAD_GATEWAY)
