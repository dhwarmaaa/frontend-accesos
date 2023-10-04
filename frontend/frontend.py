import tkinter
import customtkinter

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x640")
        self.title('Control de accesos')
        # creamos dos columnas
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.crear_frame()
        
    def button_function(self):
        print("button pressed")
    
    def crear_frame(self):
        # Crear frame para inicio
        self.inicio_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.inicio_frame.grid_columnconfigure(0, weight=1)  # Columna 0 con peso 1
        self.inicio_frame.grid_columnconfigure(1, weight=1)  # Columna 1 con peso 1
        self.inicio_frame.grid_columnconfigure(2, weight=1)  # Columna 2 con peso 1
        self.btn_users = customtkinter.CTkButton(self.inicio_frame, text='Obtener usuarios', 
                                                 compound="right", fg_color="#17A1C9", hover_color="#10738E",
                                                 font=("Arial", 14, 'bold'), text_color="white",
                                                 command=self.button_function, anchor="center")
        self.btn_users.grid(row=1, column=0, padx=5, pady=10)


