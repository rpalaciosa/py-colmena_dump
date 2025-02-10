
import os , requests

class ColmenaLogyc :

    def __init__(self):
        self.colmena = os.getenv("COLMENA_URL")
        self.username = os.getenv("COLMENA_USERNAME")
        self.password=os.getenv("COLMENA_PASSWORD")
        self.accessToken = ''
    

    def get_access_token(self) -> str:
            
        url = self.colmena+"authenticate"

        payload = {
            "username": self.username,
            "password": self.password
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
        
        self.accessToken = accessToken

        return accessToken

    def get_prestaciones(self ) -> dict :
        url = self.colmena + "private/prestaciones"

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
            "X-Auth-Token": self.accessToken
        }

        response = requests.request("POST", url, json=payload, headers=headers)

        return response.json()

    def get_fun(self) -> dict :
        import requests

        url = self.colmena +"/private/contrato"

        payload = ""
        headers = {
            "X-Auth-Token": self.accessToken,
            "sec-ch-ua-platform": """Windows""",
            "Referer": "https://www.colmena.cl/afiliados/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "sec-ch-ua": """Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24""",
            "sec-ch-ua-mobile": "?0"
        }

        response = requests.request("GET", url, data=payload, headers=headers)

        return response.json()

    def get_servicios(self , p_fun , p_prestacion) -> dict :


        url = self.colmena + "private/bonos/simulacion"

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
            "X-Auth-Token": self.accessToken,
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
