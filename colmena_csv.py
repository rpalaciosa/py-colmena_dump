import requests , os , json


l_colmena = os.getenv("COLMENA_URL")
l_username = os.getenv("COLMENA_USERNAME")
l_password=os.getenv("COLMENA_PASSWORD")


def get_access_token(p_colmena , p_username , p_password) -> str:
        
    url = p_colmena+"authenticate"

    payload = {
        "username": p_username,
        "password": p_password
    }

    headers = {
        "sec-ch-ua-platform": "Windows",
        "Referer": "https://www.colmena.cl/afiliados/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": """Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24""",
        "Content-Type": "application/json",
        "sec-ch-ua-mobile": "?0"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    accessToken = response.json()["token"]

    return accessToken

def get_prestaciones(p_colmena , p_accessToken) -> dict :
    url = p_colmena + "private/prestaciones"

    payload = {
        "id": 1,
        "nombre": ""
    }
    headers = {
        "sec-ch-ua-platform": """Windows""",
        "Referer": """https://www.colmena.cl/afiliados/""",
        "sec-ch-ua": """Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24""",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "X-Auth-Token": p_accessToken
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    return response.json()

def get_fun(p_colmena , p_accessToken) -> dict :
    import requests

    url = p_colmena+"/private/contrato"

    payload = ""
    headers = {
        "X-Auth-Token": p_accessToken,
        "sec-ch-ua-platform": """Windows""",
        "Referer": "https://www.colmena.cl/afiliados/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": """Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24""",
        "sec-ch-ua-mobile": "?0"
    }

    response = requests.request("GET", url, data=payload, headers=headers)

    return response.json()

def get_servicios(p_colmena , p_accessToken , p_fun , p_prestacion) -> dict :


    url = p_colmena + "private/bonos/simulacion"

    payload = {
        "origen": 1,
        "fecha": "2025-01-01T00:00:01.000Z",
        "comuna2": 0,
        "comuna3": 0,
        "calce": "",
        "codigo": 1,
        "tipoAtencion": 1,
        "comuna1": {
            "codigoRetorno": 0,
            "id": 7201,
            "nombre": ""
        },
        "beneficiario": {            
        },
        "prestacion": {
            "nombre": F"{p_prestacion} 01 0000000 N",
        },
        "contrato": p_fun,
        "costoCero": "N"
    }
    headers = {
        "X-Auth-Token": p_accessToken,
        "sec-ch-ua-platform": """Windows""",
        "Referer": "https://www.colmena.cl/afiliados/",
        "sec-ch-ua": """Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24""",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    return response.json()



l_accessToken=get_access_token(l_colmena, l_username , l_password)
#print(l_accessToken)
#l_accessToken="eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3Mzc3NDMxNDAsInN1YiI6IntcImlkXCI6MCxcInVzZXJuYW1lXCI6XCIxNTEzNjA4MC03XCIsXCJlbmFibGVkXCI6ZmFsc2UsXCJlc3RhZG9cIjowLFwiaWRBcHBcIjoyNDgsXCJjb2RpZ29SZXRvcm5vXCI6MCxcImdsb3NhUmV0b3Jub1wiOlwiXCJ9IiwiaXNzIjoiaHR0cFwvXC9tcHJvZC5jb2xtZW5hLmNsb3VkOjgwXC9zZXJ2aWNlc1wvYWZpbGlhZG9zIiwiaWF0IjoxNzM3NzQxMzQwfQ.8ZG9W8SQGMhzlHJwtcEXGpI1_t7JFWYuokSMkbQvc18"

l_prestaciones_js = get_prestaciones(l_colmena , l_accessToken)
l_fun = get_fun(l_colmena,l_accessToken)

#print(json.dumps(l_prestaciones_js , indent=4))


with open("data/out_services.csv", mode="w", encoding="utf-8") as ar:
    ar.write("Prestación;Comuna;Prestador;Rut;medico;copago\n")

    for p in l_prestaciones_js:
        l_servicios = get_servicios(l_colmena,l_accessToken,l_fun , "00"+str(p["id"]))

        for s in l_servicios :
            ar.write(f"{p["nombre"]};{s["prestador"]["comuna"]["nombre"]};{s["prestador"]["nombre"]};{s["medico"]["rut"]};{s["medico"]["nombre"]};{s["copago"]}\n")

print("Terminado!")