"""Cliente del servicio SOAP público CountryInfoService."""
from functools import lru_cache

from requests import Session
from zeep import Client
from zeep.helpers import serialize_object
from zeep.transports import Transport

WSDL_URL = 'http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL'
TIMEOUT_SEGUNDOS = 15
# El servicio responde 200 con este texto cuando el código no existe.
PAIS_NO_ENCONTRADO = 'Country not found in the database'


class PaisNoEncontrado(Exception):
    pass


@lru_cache(maxsize=1)
def obtener_cliente():
    # Descargar el WSDL es lento, por eso el cliente se reutiliza.
    transporte = Transport(session=Session(), timeout=TIMEOUT_SEGUNDOS, operation_timeout=TIMEOUT_SEGUNDOS)
    return Client(WSDL_URL, transport=transporte)


def consultar_pais(codigo_iso):
    servicio = obtener_cliente().service
    codigo = codigo_iso.upper()
    nombre = servicio.CountryName(codigo)
    if nombre == PAIS_NO_ENCONTRADO:
        raise PaisNoEncontrado(codigo)
    moneda = serialize_object(servicio.CountryCurrency(codigo))
    return {
        'codigo': codigo,
        'nombre': nombre,
        'capital': servicio.CapitalCity(codigo),
        'moneda': {'codigo': moneda['sISOCode'], 'nombre': moneda['sName']},
        'codigo_telefonico': servicio.CountryIntPhoneCode(codigo),
        'bandera': servicio.CountryFlag(codigo),
        'fuente': 'CountryInfoService (SOAP)',
    }
