import re, urllib, httplib

post_params = {"Cuenta_Empresarial": "0123456",
               "Costo_Productos_Comprar": 123.00,
               "URL_Salto": "/"}
campos = urllib.urlencode(post_params)
# url = "http://127.0.0.1:8000/test_urllib/"
# url = "http://10.56.8.132/Banco/Consumo/Consumo.php"
# sitio = urllib.urlopen(url, campos)
# print(sitio.read())
# parametros = urllib.urlencode(post_params)
url_port = "10.56.8.132:80"
# url_port = "127.0.0.1:8000"
file_to_consume = "/Banco/Consumo/Consumo.php"
# file_to_consume = "/test_urllib/"
cabeceras = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
abrir_conexion = httplib.HTTPConnection(url_port)
abrir_conexion.request("POST", file_to_consume, campos, cabeceras)
respuesta = abrir_conexion.getresponse()
print respuesta.status
ver_source = respuesta.read()
print ver_source
