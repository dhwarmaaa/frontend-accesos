import tkinter
import tkinter as tk
from tkinter import ttk
import json
import datetime
import customtkinter
import os, sys
import threading
import tkinter.messagebox as messagebox
from backend import Base_datos
import schedule
import time
import asyncio
from PIL import Image

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        # identificamos el separador de un directorio
        separador = os.path.sep
        # obtenemos la ubicacion del archivoactual
        dir_actual = os.path.dirname(os.path.abspath(__file__))
        # obtenemos la ubicacion anterior a la actual

        dire = separador.join(dir_actual.split(separador)[:-1])
        print(dir_actual)
        basedir = os.path.dirname(__file__)
        # la unimos al nombre del archivo a leer
        #self.path_json = os.path.join(basedir, 'datos.json')
        self.path_json = self.resolver_ruta('datos.json')
        self.title("Control de Accesos")
        self.geometry("1000x640")
        self.bd = Base_datos()

        # creamos dos columnas
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.cargar_img()
        # creamos el Menú vertical
        self.crear_menu_vertical()
        self.crearFrameConfig()
        # creamos el frame Inicio
        self.crearFrameInicio()
        # cargar informacion actual
        self.event_informacionactual()
        # seleccionamos el frame por default
        self.select_frame_by_name("inicio")
        self.bd.accessLevelID()
        # Iniciamos el hilo del temporizador
        #self.inicia_temporizador()
        #asyncio.create_task(self.otra_funcion_asincronica())
        #self.temporizador_thread = threading.Thread(target=self.temporizador)
        #self.temporizador_thread.daemon = True  # El hilo se detendrá cuando el programa principal termine
        #self.temporizador_thread.start()
        self.schedule_async_call()

    async def my_async_function(self):
        await self.bd.web_server()
        self.event_obtener_users()
            # Aquí va la función asíncrona que quieres llamar cada 10 minutos
       # await asyncio.sleep(1)  # Simulamos algo que toma tiempo

            # Cuando termina, actualizamos la etiqueta con un mensaje
        print("Llamada asíncrona completada.")
        hora_actual = datetime.datetime.now()
        formato_hora = hora_actual.strftime("%H:%M:%S")
        texto = "Actualización completada a las {}".format(formato_hora)
        self.label.configure(text=texto)
        self.schedule_async_call()  # Programamos la próxima llamada

    def schedule_async_call(self):
            # Programamos la próxima llamada en 10 minutos
        self.after(10 * 60 * 1000, self.run_async_function)

    def run_async_function(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        threading.Thread(target=loop.run_until_complete, args=(self.my_async_function(),)).start()


    def inicia_temporizador(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.temporizador())
        #asyncio.create_task(self.lectura_web_service())
        # Configurar el temporizador para que se llame cada 10 minutos
        #self.after(10 * 60 * 1000, self.inicia_temporizador)

    def temporizador(self):
        # Programa la función para que se ejecute cada 10 minutos
        schedule.every(10).minutes.do(self.on_actualizar_click())

        # Bucle principal para ejecutar las tareas programadas
        while True:
            schedule.run_pending()
            time.sleep(1)

    def cargar_img(self):
        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets/img")
        home_light = self.resolver_ruta("assets/home_light.png")
        config = self.resolver_ruta("assets/Config.png")

        self.home_image = customtkinter.CTkImage(light_image=Image.open(home_light),
                                                 dark_image=Image.open(home_light),
                                                 size=(30, 30))
        self.config_image = customtkinter.CTkImage(light_image=Image.open(config),
                                                   dark_image=Image.open(config),
                                                   size=(30, 30))


    def lectura_web_service(self):
        # llama a web service
        print('ya pasaron 10min')
        self.on_actualizar_click()
        #self.event_obtener_users()
    async def mi_funcion_asincronica(self):
        # await self.bd.web_server()
        await self.bd.web_server()
        self.event_obtener_users()

    def on_actualizar_click(self):
        # Ejecuta la función asincrónica dentro del bucle de eventos de asyncio
        # asyncio.create_task(self.mi_funcion_asincronica())
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Ejecuta la tarea asincrónica dentro del bucle de eventos de asyncio
            asyncio.create_task(self.mi_funcion_asincronica())
        else:
            # Si no hay un bucle de eventos en ejecución, creamos uno nuevo y ejecutamos la tarea
            loop.run_until_complete(self.mi_funcion_asincronica())
    def resolver_ruta(self, ruta_relativa):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, ruta_relativa)
        return os.path.join(os.path.abspath('.'), ruta_relativa)
    def crear_menu_vertical(self):
        # Se crea el menú de navegación
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0, bg_color='#36486C')
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=0)

        # boton para configuración
        self.config_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, width=95,
                                                     border_spacing=10, text="Configuración",
                                                     fg_color="transparent", bg_color='#36486C', text_color='white',
                                                     hover_color="#314056", image=self.config_image, command=self.config_button_event,
                                                     compound="top")
        self.config_button.grid(row=1, column=0, sticky="ew", padx=0, pady=0)

        # boton para inicio
        self.inicio_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, width=95,
                                                     border_spacing=10, text="Inicio",
                                                     fg_color="transparent", bg_color='#36486C',
                                                     text_color="white", hover_color="#314056", image=self.home_image,
                                                      command=self.inicio_button_event,
                                                     compound="top")
        self.inicio_button.grid(row=2, column=0, sticky="ew")
        # label para completar el espacio en la barra lateral
        self.appearance_mode_label = customtkinter.CTkLabel(self.navigation_frame, text="", bg_color='#36486C',
                                                            height=590, width=100)
        self.appearance_mode_label.grid(row=5, column=0, padx=0, pady=0)
    def crearFrameConfig(self):

        # Crear el frame para config
        self.config_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.config_frame.grid_columnconfigure(0, weight=1, minsize=155)
        self.config_frame.grid_columnconfigure(1, weight=1, minsize=550)
        # Titulo información actual
        self.labelInfoActual = customtkinter.CTkLabel(self.config_frame, text="Información Actual",
                                                      font=("Arial", 18, 'bold'))
        self.labelInfoActual.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        # Label Key
        self.labelKey = customtkinter.CTkLabel(self.config_frame, text="Key:", font=("Arial", 14, 'bold'), anchor="w",
                                               width=150)
        self.labelKey.grid(row=3, column=0, padx=1, pady=1)
        # label para mostrar la Key actual
        self.Key = customtkinter.CTkLabel(self.config_frame, text="", font=("Arial", 14, 'normal'), anchor="w",
                                          width=550)
        self.Key.grid(row=3, column=1, padx=1, pady=1)
        # Label añadir al grupo
        self.labelanadir = customtkinter.CTkLabel(self.config_frame, text="Añadir a grupo:", font=("Arial", 14, 'bold'),
                                                  width=155, anchor="w")
        self.labelanadir.grid(row=4, column=0, padx=1, pady=1)
        # Label para mostrar la información actual en addGroup
        self.anadir = customtkinter.CTkLabel(self.config_frame, text="", font=("Arial", 14, 'normal'),
                                             anchor="w", width=550)
        self.anadir.grid(row=4, column=1, padx=1, pady=1)
        # Label Eliminar de un grupo
        self.labeleliminar = customtkinter.CTkLabel(self.config_frame, text="Eliminar de un grupo:",
                                                    font=("Arial", 14, 'bold'), width=155, anchor="w")
        self.labeleliminar.grid(row=5, column=0, padx=1, pady=1)
        # Label para mostrar la información actual en deleteGroup
        self.eliminar = customtkinter.CTkLabel(self.config_frame, text="2312341564", font=("Arial", 14, 'normal'),
                                               anchor="w", width=550)
        self.eliminar.grid(row=5, column=1, padx=1, pady=1)
        # Label Obtener usuario
        self.labelobtener = customtkinter.CTkLabel(self.config_frame, text="Obtener Usuario:",
                                                   font=("Arial", 14, 'bold'), width=155, anchor="w")
        self.labelobtener.grid(row=6, column=0, padx=1, pady=1)
        # Label para mostrar la información actual en getUsers
        self.obtener = customtkinter.CTkLabel(self.config_frame, text="", font=("Arial", 14, 'normal'),
                                              anchor="w", width=550)
        self.obtener.grid(row=6, column=1, padx=1, pady=1)
        # Label Obtener IP
        self.labelIP = customtkinter.CTkLabel(self.config_frame, text="IP:",
                                              font=("Arial", 14, 'bold'), width=155, anchor="w")
        self.labelIP.grid(row=7, column=0, padx=1, pady=1)
        # Label para mostrar la información actual en WEBSERVER
        self.ip = customtkinter.CTkLabel(self.config_frame, text="", font=("Arial", 14, 'normal'),
                                         anchor="w", width=550)
        self.ip.grid(row=7, column=1, padx=1, pady=1)
        # Label Obtener ACTUALIZAR BIOMETRICOS
        self.labelBiometrico = customtkinter.CTkLabel(self.config_frame, text="Actualizar Biométricos:",
                                              font=("Arial", 14, 'bold'), width=155, anchor="w")
        self.labelBiometrico.grid(row=8, column=0, padx=1, pady=1)
        # Label para mostrar la información actual en updateBio
        self.biometrico = customtkinter.CTkLabel(self.config_frame, text="", font=("Arial", 14, 'normal'),
                                         anchor="w", width=550)
        self.biometrico.grid(row=8, column=1, padx=1, pady=1)
        # Label Obtener ACTUALIZAR USUARIO
        self.labelUser = customtkinter.CTkLabel(self.config_frame, text="Actualizar Usuario:",
                                              font=("Arial", 14, 'bold'), width=155, anchor="w")
        self.labelUser.grid(row=9, column=0, padx=1, pady=1)
        # Label para mostrar la información actual en updateUser
        self.user = customtkinter.CTkLabel(self.config_frame, text="", font=("Arial", 14, 'normal'),
                                         anchor="w", width=550)
        self.user.grid(row=9, column=1, padx=1, pady=1)
        # Label Obtener id grupos de acceso
        self.labelGrupoAcceso = customtkinter.CTkLabel(self.config_frame, text="ID grupos de acceso:",
                                                font=("Arial", 14, 'bold'), width=155, anchor="w")
        self.labelGrupoAcceso.grid(row=10, column=0, padx=1, pady=1)
        # Label para mostrar la información actual en grupo de acceso
        self.grupoacceso = customtkinter.CTkLabel(self.config_frame, text="", font=("Arial", 14, 'normal'),
                                           anchor="w", width=550)
        self.grupoacceso.grid(row=10, column=1, padx=1, pady=1)

        # Titulo Información a actualizar
        self.labelInfoform = customtkinter.CTkLabel(self.config_frame, text="Información a actualizar",
                                                    font=("Arial", 18, 'bold'))
        self.labelInfoform.grid(row=11, column=0, columnspan=2, padx=10, pady=10)
        # Label key
        self.labelKey1 = customtkinter.CTkLabel(self.config_frame, text="Key:", font=("Arial", 14, 'bold'), anchor="w",
                                                width=155)
        self.labelKey1.grid(row=12, column=0, padx=1, pady=1)
        # Campo para ingresar el valor de key
        self.inputKey = customtkinter.CTkEntry(self.config_frame, font=("Arial", 14, 'normal'), width=550)
        self.inputKey.grid(row=12, column=1, padx=1, pady=1)
        # Label añadir a grupo
        self.labelAnadir1 = customtkinter.CTkLabel(self.config_frame, text="Añadir a grupo:",
                                                   font=("Arial", 14, 'bold'), anchor="w", width=155)
        self.labelAnadir1.grid(row=13, column=0, padx=1, pady=1)
        # Campo para ingresar el valor en addGroup
        self.inputAnadir = customtkinter.CTkEntry(self.config_frame, font=("Arial", 14, 'normal'), width=550)
        self.inputAnadir.grid(row=13, column=1, padx=1, pady=1)
        # Label Eliminar de un grupo
        self.labelEliminar1 = customtkinter.CTkLabel(self.config_frame, text="Eliminar de un grupo:",
                                                     font=("Arial", 14, 'bold'), anchor="w", width=155)
        self.labelEliminar1.grid(row=14, column=0, padx=1, pady=1)
        # Campo para ingresar el valor en deleteGroup
        self.inputEliminar = customtkinter.CTkEntry(self.config_frame, font=("Arial", 14, 'normal'), width=550)
        self.inputEliminar.grid(row=14, column=1, padx=1, pady=1)
        # Label Obtener usuario
        self.labelObtener1 = customtkinter.CTkLabel(self.config_frame, text="Obtener Usuario:",
                                                    font=("Arial", 14, 'bold'), anchor="w", width=155)
        self.labelObtener1.grid(row=15, column=0, padx=1, pady=1)
        # Campo para ingresar el valor en getUser
        self.inputObtener = customtkinter.CTkEntry(self.config_frame, font=("Arial", 14, 'normal'), width=550)
        self.inputObtener.grid(row=15, column=1, padx=1, pady=1)
        # Label IP
        self.labelIP1 = customtkinter.CTkLabel(self.config_frame, text="IP:",
                                               font=("Arial", 14, 'bold'), anchor="w", width=155)
        self.labelIP1.grid(row=16, column=0, padx=1, pady=1)
        # Campo para ingresar el valor de la IP
        self.inputIP = customtkinter.CTkEntry(self.config_frame, font=("Arial", 14, 'normal'), width=550)
        self.inputIP.grid(row=16, column=1, padx=1, pady=1)
        # Label actualizar biometricos
        self.labelBiometrico1 = customtkinter.CTkLabel(self.config_frame, text="Actualizar biometricos:",
                                               font=("Arial", 14, 'bold'), anchor="w", width=155)
        self.labelBiometrico1.grid(row=17, column=0, padx=1, pady=1)
        # Campo para ingresar el valor de la key actualizar biometricos
        self.inputBiometrico = customtkinter.CTkEntry(self.config_frame, font=("Arial", 14, 'normal'), width=550)
        self.inputBiometrico.grid(row=17, column=1, padx=1, pady=1)
        # Label actualizar usuario
        self.labelUser1 = customtkinter.CTkLabel(self.config_frame, text="Actualizar usuario:",
                                                      font=("Arial", 14, 'bold'), anchor="w", width=155)
        self.labelUser1.grid(row=18, column=0, padx=1, pady=1)
        # Campo para ingresar el valor de la key actualizar biometricos
        self.inputUser = customtkinter.CTkEntry(self.config_frame, font=("Arial", 14, 'normal'), width=550)
        self.inputUser.grid(row=18, column=1, padx=1, pady=1)

        # Label grupo acceso
        self.labelgrupo_acceso = customtkinter.CTkLabel(self.config_frame, text="ID grupos de acceso:",
                                                 font=("Arial", 14, 'bold'), anchor="w", width=155)
        self.labelgrupo_acceso.grid(row=19, column=0, padx=1, pady=1)
        # Campo para ingresar el valor de la key actualizar biometricos
        self.inputgrupo_acceso = customtkinter.CTkEntry(self.config_frame, font=("Arial", 14, 'normal'), width=550)
        self.inputgrupo_acceso.grid(row=19, column=1, padx=1, pady=1)

        # Boton para actualizar la información
        self.btn_actualizar = customtkinter.CTkButton(self.config_frame, text='Actualizar información',
                                                      fg_color="#17A1C9", hover_color="#10738E",
                                                      font=("Arial", 14, 'bold'), text_color="white",
                                                      command=self.event_btnactualizar)
        self.btn_actualizar.grid(row=20, column=0, columnspan=2, padx=0, pady=10)
    def crearFrameInicio(self):
        # Crear frame para inicio
        self.inicio_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.inicio_frame.grid_columnconfigure(0, weight=1)  # Columna 0 con peso 1
        self.inicio_frame.grid_columnconfigure(1, weight=1)  # Columna 1 con peso 1
        self.inicio_frame.grid_columnconfigure(2, weight=1)  # Columna 2 con peso 1

        # boton para obtener usuarios y mostrarlo en la tabla
        self.btn_users = customtkinter.CTkButton(self.inicio_frame, text='Obtener usuarios',
                                                 compound="right", fg_color="#17A1C9", hover_color="#10738E",
                                                 font=("Arial", 14, 'bold'), text_color="white",
                                                 command=self.event_obtener_users, anchor="center")
        self.btn_users.grid(row=1, column=0, padx=5, pady=10)

        # boton para leer web service
        """""""""
        self.btn_actualizar = customtkinter.CTkButton(self.inicio_frame, text='Actualizar', fg_color="#17A1C9",
                                                      hover_color="#10738E", font=("Arial", 14, 'bold'),
                                                      text_color="white", command=self.on_actualizar_click)
        self.btn_actualizar.grid(row=1, column=1, padx=5, pady=10)
        """""""""
        # boton para obtener usuarios de hikcentral
        self.btn_obtenerUsuarios = customtkinter.CTkButton(self.inicio_frame, text='Leer Biometrico', fg_color="#17A1C9",
                                                      hover_color="#10738E", font=("Arial", 14, 'bold'),
                                                      text_color="white", command=self.leer_hikcentral)
        self.btn_obtenerUsuarios.grid(row=1, column=1, padx=5, pady=10, columnspan=2)

        self.label = customtkinter.CTkLabel(self, text="Esperando la próxima lectura al web service...")
        self.label.grid(row=2, column=0, columnspan=2, padx=0,pady=20)

        self.etiqueta_total = customtkinter.CTkLabel(self.inicio_frame, text="Total de registros:   ",
                                                     font=("Arial", 14, 'bold'), compound="right", width=780,
                                                     anchor="e")
        self.etiqueta_total.grid(row=4, column=0, columnspan=2, padx=0, pady=10)
        # Crear la tabla
        self.tabla = ttk.Treeview(self.inicio_frame, show='headings')
        # Agregar las columnas con los encabezados
        self.tabla['columns'] = ('personCode', 'personName', 'endTime', 'estado', 'fechaActualizacion')

        # Formatear los encabezados
        self.tabla.heading('personCode', text='ID')
        self.tabla.heading('personName', text='Nombre')
        self.tabla.heading('endTime', text='Fecha de vencimiento')
        self.tabla.heading('estado', text='Estado')
        self.tabla.heading('fechaActualizacion', text='Fecha Actualización')

        # Ajustar el ancho de las columnas
        self.tabla.column('personCode', width=100, anchor='center')
        self.tabla.column('personName', width=300)
        self.tabla.column('endTime', width=150, anchor='center')
        self.tabla.column('estado', width=150, anchor='center')
        self.tabla.column('fechaActualizacion', width=150, anchor='center')
        self.tabla.grid(row=3, column=0, columnspan=2, padx=25, pady=10)
        self.tabla.configure(height=22)

    def actualizar_etiqueta(self):
        mensaje = self.bd.etiqueta_estado
        self.contenido_variable.set(mensaje)
        self.etiqueta_estado.configure(text=mensaje)
        self.inicio_frame.after(1000, self.actualizar_etiqueta)
    def select_frame_by_name(self, name):
        # establece el color del botón para el botón seleccionado
        self.config_button.configure(fg_color="#314056" if name == "config" else "transparent")
        self.inicio_button.configure(fg_color="#314056" if name == "inicio" else "transparent")
        # muestra el frame seleccionado
        if name == "config":
            self.label.grid_forget()
            self.config_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.config_frame.grid_forget()
        if name == "inicio":
            self.label.grid(row=2, column=0, columnspan=2, padx=0, pady=20)
            self.inicio_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.inicio_frame.grid_forget()

    def event_informacionactual(self):
        # Leer el archivo JSON
        with open(self.path_json) as archivo:
            datos = json.load(archivo)
        # insertamos en los label los valores correspondientes
        self.Key.configure(text=datos['key'])
        self.anadir.configure(text=datos['addGroup'])
        self.eliminar.configure(text=datos['deleteGroup'])
        self.obtener.configure(text=datos['getUsers'])
        self.ip.configure(text=datos['webServer'])
        self.biometrico.configure(text= datos['updateBio'])
        self.user.configure(text=datos['updateUser'])
        self.grupoacceso.configure(text=datos['accessLevel'])
    def inicio_button_event(self):
        self.select_frame_by_name("inicio")

    def config_button_event(self):
        self.select_frame_by_name("config")


    def leer_hikcentral(self):
        self.bd.obtener_usuarios()

    def event_obtener_users(self):
        print('event_obtener')

        self.tabla.delete(*self.tabla.get_children())
        # los obtiene de la bd
        registros = json.loads(self.bd.lee_usuarios())

        num_reg = 0
        for registro in registros:
            person_code = registro['personCode']
            person_name = registro['personName']
            end_time = registro['endTime']
            estado = registro['estatus']
            estatus = "Con Acceso" if estado == 'true' or estado == 'True' else "Sin Acceso"
            fechaactuali = registro['fechaActualizacion']
            self.tabla.insert(parent='', index='end',
                              values=(person_code, person_name, end_time, estatus, fechaactuali))
            num_reg += 1
        self.etiqueta_total.configure(text='Total de registros: ' + str(num_reg))


    def event_btnactualizar(self):
        with open(self.path_json, "r") as archivo:
            datos_existentes = json.load(archivo)
            # recuperamos el valor de los input y los almacenamos
        key = self.inputKey.get()
        add_group = self.inputAnadir.get()
        delete_group = self.inputEliminar.get()
        get_users = self.inputObtener.get()
        web_server = self.inputIP.get()
        update_biome = self.inputBiometrico.get()
        update_user = self.inputUser.get()
        access_group = self.inputgrupo_acceso.get()
        datos = {
            "key": key if key else datos_existentes.get("key"),
            "addGroup": add_group if add_group else datos_existentes.get("addGroup"),
            "deleteGroup": delete_group if delete_group else datos_existentes.get("deleteGroup"),
            "getUsers": get_users if get_users else datos_existentes.get("getUsers"),
            "webServer": web_server if web_server else datos_existentes.get("webServer"),
            "updateBio": update_biome if update_biome else datos_existentes.get("updateBio"),
            "updateUser": update_user if update_user else datos_existentes.get("updateUser"),
            "accessLevel": access_group if access_group else datos_existentes.get("accessLevel")
        }
        # limpiamos los input
        self.inputKey.delete(0, len(self.inputKey.get()))
        self.inputAnadir.delete(0, len(self.inputAnadir.get()))
        self.inputEliminar.delete(0, len(self.inputEliminar.get()))
        self.inputObtener.delete(0, len(self.inputObtener.get()))
        self.inputIP.delete(0, len(self.inputIP.get()))
        self.inputBiometrico.delete(0, len(self.inputBiometrico.get()))
        self.inputUser.delete(0, len(self.inputUser.get()))
        self.inputgrupo_acceso.delete(0, len(self.inputgrupo_acceso.get()))
        # abrimos el archivo en modo escritura
        with open(self.path_json, "w") as archivo:
            json.dump(datos, archivo)
        # actualizamos informacion actual
        self.event_informacionactual()
        # Mostrar ventana emergente de confirmación
        messagebox.showinfo("Confirmación", "Los cambios han sido guardados correctamente.")

#def main():
#    ventana = VentanaPrincipal()
#    ventana.mainloop(())

#if __name__ == "__main__":
#    main()
if __name__ == "__main__":
    ventana = VentanaPrincipal()
    asyncio.run(ventana.mainloop())
    #ventana.mainloop(())

# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
#    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
