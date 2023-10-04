import os, sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import firebase_admin
from firebase_admin import credentials, db
import tkinter.messagebox as messagebox

import requests
import json
import datetime
import tracemalloc
import aiohttp
import timeit
from datetime import datetime, timedelta
class Base_datos():
    def __init__(self):
        self.path_datosjson = self.resolver_ruta('datos.json')
        self.path_controlAcceso = self.resolver_ruta('control-de-accesos-9bcbc-firebase-adminsdk-dpums-752fb96c44.json')
        self.cred = credentials.Certificate(self.path_controlAcceso)
        firebase_admin.initialize_app(self.cred,
                                      {'databaseURL': 'https://control-de-accesos-9bcbc-default-rtdb.firebaseio.com/'})
        self.ref = db.reference('/Users')
        self.usuarios_diccionario = {}
        self.person_codes_set = set()
        self.person_cambio = {}
        self.primera_vez = True
        self.morosos = ""
        self.acceso = ""
        self.fecha_hoy = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.etiqueta_estado = ""

    def resolver_ruta(self, ruta_relativa):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, ruta_relativa)
        return os.path.join(os.path.abspath('.'), ruta_relativa)

    def registrosUsuarios(self):
        print('self.db')

    def lee_usuarios(self):
        users_data = self.ref.get()
        if users_data is not None:
            users = [user_data for user_data in users_data.values()]
            #print(users)
            return json.dumps(users)

    def agrega_api(self, registro):
        user_id = registro['personCode']

        # Verificar si el usuario ya existe
        users = self.ref.get()
        if users is None:
            self.ref.push(registro)
            return

        global bandera
        bandera = False
        for key, value in users.items():
            if value['personCode'] == user_id:
                print('ya existe')
                bandera = True
                break

        user_ref = self.ref.get()
        if bandera == False:
            self.ref.push(registro)


    def fetch_data_usuarios(self, url, pageNo, headers):
        body = {
            'pageNo': pageNo,
            'pageSize': 500
        }
        myString = json.dumps(body)
        response = requests.post(url, data=myString, headers=headers, verify=False)
        response.raise_for_status()  # Lanzar una excepción en caso de error

        data = response.json()
        # Agregar datos a un diccionario
        for registro in data['data']['list']:
            person_code = registro['personCode']
            registro['estatus'] = ""
            registro['fechaActualizacion'] = ""
            registro['index_bd'] = ""
            if person_code not in self.person_codes_set:
                self.agrega_api(registro)
                self.usuarios_diccionario[person_code] = registro
                self.person_codes_set.add(person_code)

        return response.json()

    def obtener_usuarios(self):
        with open(self.path_datosjson) as archivo:
            datos = json.load(archivo)

        url = 'https://127.0.0.1:444/artemis/api/resource/v1/person/personList'
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'x-ca-key': datos["key"],
            'x-ca-signature': datos["getUsers"],
            'x-ca-signature-headers': 'x-ca-key'
        }

        batch_size = 100
        page_no = 1
        sum_registros = 0

        messagebox.showinfo("Mensaje",
                            "Leyendo informacion de Hikcentral, una vez finalizado se le notificará")

        while True:
            data = self.fetch_data_usuarios(url, page_no, headers)
            usuariosConsulta = len(data['data']['list'])
            totalUsuarios = data['data']['total']
            sum_registros += usuariosConsulta
            print(f"Van {sum_registros} de {totalUsuarios} usuarios")
            # Si ya se han obtenido todos los registros, salimos del ciclo
            if usuariosConsulta < batch_size:
                break

            page_no += 1
        print("Proceso de lectura finalizado.")
        messagebox.showinfo("Mensaje",
                            "Proceso de lectura finalizado.")

    def accessLevelID(self):
        global morosos_id, acceso_id
        with open(self.path_datosjson) as archivo:
            datos = json.load(archivo)

        if "key" not in datos or not datos["key"] or "accessLevel" not in datos or not datos["accessLevel"]:
            print("Los campos 'key' y 'accessLevel' deben estar presentes y no estar vacíos.")
            return

        url = 'https://127.0.0.1:444/artemis/api/acs/v1/privilege/group'

        body = {
            "pageNo": 1,
            "pageSize": 10,
            "type": 1
        }

        body_json = json.dumps(body)

        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'x-ca-key': datos["key"],
            'x-ca-signature': datos["accessLevel"],
            'x-ca-signature-headers': 'x-ca-key'
        }

        response = requests.post(url, data=body_json, headers=headers, verify=False)

        print(response.status_code)
        print(response.json)

        valor = response.json()
        print(valor)
        groups = valor['data']['list']

        for group in groups:
            group_name = group['privilegeGroupName']
            privilege_group_id = group['privilegeGroupId']

            if group_name == 'Morosos':
                morosos_id = privilege_group_id
                print(f"Grupo: {group_name}")
                print(f"privilegeGroupId: {privilege_group_id}")
            if group_name == 'Acceso Total':
                acceso_id = privilege_group_id
                print(f"Grupo: {group_name}")
                print(f"privilegeGroupId: {privilege_group_id}")

            # Agregar los campos privilegeGroupId
        datos["morososId"] = morosos_id
        datos["accesoTotalid"] = acceso_id
        self.morosos = morosos_id
        self.acceso = acceso_id

            # Escribir los datos actualizados en el archivo JSON
        with open(self.path_datosjson, "w") as archivo:
            json.dump(datos, archivo)

    def llena_diccionario(self):
        users = self.ref.get()
        print('llena diccionario')
        for key, value in users.items():
            personCode = value['personCode']
            personId = value['personId']
            estatus = value['estatus']
            print(estatus)
            fechaActualizacion = value['fechaActualizacion']
            indiceBD = key

            data = {
                'personCode': personCode,
                'personId': personId,
                'estatus': estatus,
                'fechaActualizacion': fechaActualizacion,
                'indiceBD': indiceBD,
                "personFamilyName": value["personFamilyName"],
                "personGivenName": value["personGivenName"],
                "orgIndexCode": value["orgIndexCode"],
                "gender": value['gender'],
                "phoneNo": value["phoneNo"],
                "remark": value["remark"],
                "email": value['email'],
                "beginTime": value["beginTime"],
                "endTime": value['endTime']
            }
            self.usuarios_diccionario[personCode] = data
            self.person_codes_set.add(personCode)

    async def actualizar_diccionario(self):
        with open(self.path_datosjson) as archivo:
            config = json.load(archivo)

        # Código para enviar las solicitudes al API y actualizar los registros
        async with aiohttp.ClientSession() as session:
            for person_code in self.usuarios_diccionario:
                dato = self.usuarios_diccionario[person_code]
                registroFecha = dato['fechaActualizacion']
                registroEstado = dato['estatus']
                if self.compara_fecha(registroFecha):
                    url = f"{config['webServer']}?id={person_code}"
                    async with session.get(url) as resp:
                        web_server_response = await resp.json()
                        # print(web_server_response)
                        self.revisa_estado(person_code, web_server_response, registroEstado)
        self.realiza_cambios()

    def cambio_grupo(self, accion, grupo_id, person_id):
        with open(self.path_datosjson) as archivo:
            datos = json.load(archivo)
        clave = ""
        url = ""
        if accion == 'agregar':
            url = 'https://127.0.0.1:444/artemis/api/acs/v1/privilege/group/single/addPersons'
            clave = datos["addGroup"]
        elif accion == 'eliminar':
            url = 'https://127.0.0.1:444/artemis/api/acs/v1/privilege/group/single/deletePersons'
            clave = datos["deleteGroup"]
        print('accion: ', accion)
        print('clave: ', clave)
        print('url: ', url)
        body = {
            "privilegeGroupId": grupo_id,
            "type": 1,
            "list": [
                {
                    "id": person_id
                }
            ]
        }

        body_json = json.dumps(body)

        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'x-ca-key': datos["key"],
            'x-ca-signature': clave,
            'x-ca-signature-headers': 'x-ca-key'
        }
        response = requests.post(url, data=body_json, headers=headers, verify=False)
        print(response.status_code)
    def realiza_cambios(self):
        print('en realiza: ')
        #print(self.person_cambio)
        for clave, valor in self.person_cambio.items():
            print(f'Clave: {clave}, Valor: {valor}')
            grupo_id_eliminar = self.acceso if valor['eliminar'] == 'accesos' else self.morosos
            grupo_id_agregar = self.acceso if valor['agregar'] == 'accesos' else self.morosos
            #cambio_grupo(self, accion, grupo_id, person_id):
            eliminar = valor['eliminar']
            agregar = valor['agregar']
            self.cambio_grupo('eliminar', grupo_id_eliminar, clave)
            self.cambio_grupo('agregar', grupo_id_agregar, clave)
            primer_dia_siguiente_mes = (datetime.now().replace(day=1) + timedelta(days=32)).replace(day=1)
            new_end_date = datetime.now().strftime('%Y-%m-%dT23:59:59-06:00') if agregar == 'morosos' else primer_dia_siguiente_mes.strftime('%Y-%m-%dT23:59:59-06:00')
            self.actualiza_usuario(clave, new_end_date)

    def actualiza_bd(self, person_code, nuevo_estatus, nueva_fecha):
        #recibe person_code y lo busca en la bd
        # actualiza el campo estatus
        # actualiza campo fechaActualizacion
        data = self.ref.get()

        if data:
            bandera = False
            # print('data: ', data)
            for item in data:
                # print('data: ', item)
                if item == 'id:':
                    continue
                if person_code == data[item]['personCode']:
                    print('en db: ', data[item]['personCode'])
                    #data[item]['estatus'] = nuevo_estatus
                    #data[item]['fechaActualizacion'] = nueva_fecha
                    self.ref.child(f"{item}/estatus").set(nuevo_estatus)
                    self.ref.child(f"{item}/fechaActualizacion").set(nueva_fecha)
                    break
    def revisa_estado(self, person_code, web_server_response, registro_estado):

        if web_server_response != registro_estado:
            valor = self.usuarios_diccionario[person_code]
            valor['estatus'] = web_server_response
            valor['fechaActualizacion'] = self.fecha_hoy
            self.actualiza_bd(person_code, web_server_response, self.fecha_hoy)
            person_id = valor['personId']
            grupo_agregar = "accesos" if web_server_response else "morosos"
            grupo_eliminar = "morosos" if web_server_response else "accesos"
            self.person_cambio[person_code] = {'person_id': person_id, 'agregar': grupo_agregar,
                                               'eliminar': grupo_eliminar}

    def actualiza_usuario(self, clave, new_end_date):
        with open(self.path_datosjson) as archivo:
            datos = json.load(archivo)
        user = self.usuarios_diccionario[clave]
        url = 'https://127.0.0.1:444/artemis/api/resource/v1/person/single/update'
        # print(user)
        print('-----')
        body = {
            "personId": user["personId"],
            "personCode": user["personCode"],
            "personFamilyName": user["personFamilyName"],
            "personGivenName": user["personGivenName"],
            "orgIndexCode": user["orgIndexCode"],
            "gender": user['gender'],
            "phoneNo": user["phoneNo"],
            "remark": user["remark"],
            "email": user['email'],
            "beginTime": user["beginTime"],
            "endTime": new_end_date
        }
        # "endTime": "2030-05-26T15:00:00-06:00"
        body_json = json.dumps(body)

        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'x-ca-key': datos["key"],
            'x-ca-signature': datos["updateUser"],
            'x-ca-signature-headers': 'x-ca-key'
        }

        response = requests.post(url, data=body_json, headers=headers, verify=False)
        print(response.status_code)
        # print(response.json())

    def compara_fecha(self, fechaActualizacion):
        # Comprobar si la fecha está vacía
        if not fechaActualizacion:
            return True

        fecha1 = datetime.strptime(fechaActualizacion, '%Y-%m-%d %H:%M:%S')
        hoy = datetime.now()

        # Comparar las fechas
        if fecha1 < hoy:
            # print("La fecha 1 es anterior a la fecha 2.")
            return True
        else:
            # print("Las fechas son iguales.")
            return False
    async def web_server(self):
        if not self.usuarios_diccionario:
            print("El diccionario está vacío.")
            self.llena_diccionario()
        else:
            print("El diccionario no está vacío.")
        print(len(self.usuarios_diccionario))
       # inicio = timeit.default_timer()
        with open(self.path_datosjson) as archivo:
            config = json.load(archivo)
        await self.actualizar_diccionario()
        self.actualiza_biometrico()
        #fin = timeit.default_timer()

        # Cálculo del tiempo total de ejecución
        #tiempo_total = fin - inicio
        #print("Tiempo total de ejecución:", tiempo_total, "segundos")

        # messagebox.showinfo("Confirmación", "Los registros han sido actualizados.")

    def actualiza_biometrico(self):
        with open(self.path_datosjson) as archivo:
            datos = json.load(archivo)

        url = 'https://127.0.0.1:444/artemis/api/visitor/v1/auth/reapplication'

        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'x-ca-key': datos["key"],
            'x-ca-signature': datos["updateBio"],
            'x-ca-signature-headers': 'x-ca-key'
        }

        response = requests.post(url, headers=headers, verify=False)

        print('biometrico: ', response.status_code)