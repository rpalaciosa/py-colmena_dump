import requests , os , json

from core.ColmenaLogic import ColmenaLogyc

l_colmena = ColmenaLogyc()

l_accessToken=l_colmena.get_access_token()

l_prestaciones_js = l_colmena.get_prestaciones()
l_fun = l_colmena.get_fun()
l_comunas = str(os.getenv("COMUNAS")).split(",")

l_comuna = int(l_comunas[0] )

with open("data/out_services.csv", mode="w", encoding="utf-8") as ar:
    ar.write("Prestacion;Comuna;Prestador;Rut;medico;copago\n")

    for p in l_prestaciones_js:
        l_servicios = l_colmena.get_servicios(l_fun , "00"+str(p["id"]) , l_comuna)

        for s in l_servicios :
            ar.write(f"{p["nombre"]};{s["prestador"]["comuna"]["nombre"]};{s["prestador"]["nombre"]};{s["medico"]["rut"]};{s["medico"]["nombre"]};{s["copago"]}\n")



print("Terminado!")