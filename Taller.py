__author__ = 'jesus'
import datetime
import sqlite3 as dbapi
from gi.repository import Gtk
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle



class Entrada:
    #cargamos a interfaz de inicio

    def __init__(self):

        builder = Gtk.Builder()
        builder.add_from_file("inicio.glade")
    #recibimos el usuario y la contraseña 
        self.user = builder.get_object("user")
        self.password = builder.get_object("password")
        self.inicio = builder.get_object("inicio")

        signals = {"on_Entrada_clicked": self.entrada,
                   "delete-event": self.destruirVentana}

        builder.connect_signals(signals)
        self.inicio.set_title("Registrate")
        self.inicio.show_all()

    def entrada(self, widget):
      #si el usuario y la ocntraseña coinciden dejamos paso
        user = self.user.get_text();
        password = self.password.get_text();
        if user == "jesus" and passwor == "caba":
            MetodsTaller()
            self.inicio.destroy()
        else:
            self.ventanaEmergente("Datos incorrectos")

    def destruirVentana(self, widget):
       
        widget.destroy()

    def ventanaEmergente(self, texto):
      #creo la ventala emergente para futuros mensajes al usuario
        window = Gtk.Window(title="Advertencia")
        label = Gtk.Label(texto)
        label.set_padding(10, 10)
        window.add(label)
        window.connect("delete-event", self.destruirVentana)
        window.set_position(Gtk.PositionType.RIGHT)
        window.show_all()

class MetodsTaller():
#conexiones con la base de datos
    def __init__(self):
        self.correcto = bool
        self.elementos = []
        self.bd = dbapi.connect("basedatos.dat")
        self.cursor = self.bd.cursor()
#la primera vez que se ejecuta el programa se debe crear la base de datos de la siguiente manera
        #self.cursor.execute("CREATE TABLE taller (matricula VARCHAR(10) PRIMARY KEY NOT NULL,"
         #                   "vehiculo VARCHAR(20),"
          #                  "cliente VARCHAR(10),"
           #                 "dni VARCHAR(10),"
            #                "telefono INT,"
             #               "direccion VARCHAR(10))")
        self.builder2 = Gtk.Builder()
        self.builder2.add_from_file("Taller.glade")
        self.inicializar()
        self.ventana = self.builder2.get_object("Taller")
#creo las señales
        signals = {"on_insertar_clicked": self.on_Insertar_clicked,
                   "on_borrar_clicked": self.on_Delete_clicked,
                   "on_modificar_clicked": self.on_Modificar_clicked,
                   "on_ayuda_clicked": self.on_Ayuda_clicked,
                   "on_actualizar_clicked": self.actualizar,
                   "on_imprimir_clicked": self.crearpdf,
                   "delete-event": Gtk.main_quit}

        self.builder2.connect_signals(signals)
        self.ventana.set_title("Talleres Jesus")
        self.ventana.show_all()

    def destruirVentana(self, widget):
     
        widget.destroy()

    def ventanaEmergente(self, texto):
     #vetana emergente con el aviso
        window = Gtk.Window(title="Advertencia")
        label = Gtk.Label(texto)
        label.set_padding(10, 10)
        window.add(label)
        window.connect("delete-event", self.destruirVentana)
        window.set_position(Gtk.PositionType.RIGHT)
        window.show_all()

    def inicializar(self):

        self.box = self.builder2.get_object("box2")
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.vista = Gtk.TreeView()
        self.box.add(self.scroll)
        self.scroll.add(self.vista)
        self.scroll.set_size_request(400, 400)
        self.scroll.show()

        self.lista = Gtk.ListStore(str, str, str, str, int, str)

        self.lista.clear()
        self.cursor.execute("select * from taller")

        for coches in self.cursor:
            self.lista.append(coches)

        self.vista.set_model(self.lista)

        for i, title in enumerate(["matricula", "vehiculo", "cliente", "dni", "telefono", "direccion"]):
            render = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn(title, render, text=i)
            self.vista.append_column(columna)

    def on_Ayuda_clicked(self, widget):
       #ventana emergente de ayuda
        self.ventanaEmergente("ayuda")

    def on_Delete_clicked(self, widget):
       #metodo para borrar datos de la tabla
        seleccion = self.vista.get_selection()
        model, selec = seleccion.get_selected()
        if selec != None:
            self.matricula = model[selec][0]
            self.cursor.execute("delete from taller where matricula ='" + self.matricula + "'")

            self.bd.commit()
            self.ventanaEmergente("Borrado")

    def on_Modificar_clicked(self, modificar):
      #metodos para modificar datos de la tabla
        matricula = self.builder2.get_object("matricula").get_text()
        vehiculo = self.builder2.get_object("vehiculo").get_text()
        cliente = self.builder2.get_object("cliente").get_text()
        dni = self.builder2.get_object("dni").get_text()
        telefono = self.builder2.get_object("telefono").get_text()
        direccion = self.builder2.get_object("direccion").get_text()
#los datos de matricula y telefono tiene que ser 9 digitos , sino saltara ua ventana emergente con el texto datos invalidos
        if len(matricula) == 9 and len(dni) == 9 and telefono.isdigit and len(telefono) == 9:
            self.correcto = True
        else:
            self.ventanaEmergente("Datos invalidos.")
            self.correcto = False
#si los datos son correctos modificamos el contenido
        if (self.correcto):
            try:
                self.cursor.execute("update taller set vehiculo ='" + vehiculo + "'"
                                                    ",cliente='" + cliente + "'"
                                                    ",dni='" + dni + "'"
                                                    ",telefono='" + telefono + "'"
                                                    ",direccion='" + direccion + "' where matricula='" + matricula + "'")
                self.ventanaEmergente("Modificado")
                self.bd.commit()
                self.actualizar()
            except dbapi.IntegrityError:
                self.ventanaEmergente("La matricula ya existe")

    def on_Insertar_clicked(self, control):
        #metodos para insertar
        matricula = self.builder2.get_object("matricula").get_text()
        vehiculo = self.builder2.get_object("vehiculo").get_text()
        cliente = self.builder2.get_object("cliente").get_text()
        dni = self.builder2.get_object("dni").get_text()
        telefono = self.builder2.get_object("telefono").get_text()
        direccion = self.builder2.get_object("direccion").get_text()
    #dni y telefono deben contener 9 digios
        if len(dni) == 9 and telefono.isdigit and len(telefono) == 9 and cliente.isalpha:
            self.correcto = True
        else:
#ventana con aviso de revisar ls datos
            Entrada.ventanaEmergente("Revise los datos")
            self.correcto = False

        if (self.correcto):
#si los datos son correctos los insertamos en la tabla
            try:
                self.cursor.execute(
                        "insert into taller values('" + matricula + "'"
                                                   ",'" + vehiculo + "'"
                                                   ",'" + cliente + "'"
                                                   ",'" + dni + "'"
                                                   ",'" + telefono + "'"
                                                   ",'" + direccion + "')")
                self.ventanaEmergente("Insertado")
                self.actualizar()
                self.bd.commit()
            except dbapi.IntegrityError:
                self.ventanaEmergente("La matricula esta repetida")

    def actualizar(self,widget):
       #metodo para actualizar la lista , simplemente volvemos a cargar los datos con un select
        self.lista.clear()
        self.cursor.execute("select * from taller")

        for coches in self.cursor:
            self.lista.append(coches)
        self.vista.set_model(self.lista)
        self.ventanaEmergente("Actualizado")

    def crearpdf(self,widget):
        #metodos para crear pdf, le damos un tamaño de A4 , el titulo de impresion de la base de datos ,  cargamos las etiquetas de cada campo
        historialpdf = "Vehiculos y clientes_.pdf"
        c = canvas.Canvas(historialpdf, pagesize=A4)
        c.drawString(20, 800, "Impresion de la Base de Datos")
        clientes = list(self.cursor.execute("select * from taller"))
        titulos = [["MATRICULA", "VEHICULO", "CLIENTE", "DNI", "TELEFONO", "DIRECCION"]]

        clientes = titulos + clientes
        tabla = Table(clientes)

        # self.elements.append(tabla)
        # doc.build(elements)
        tabla.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 2, colors.white),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.green),
                                   ('BACKGROUND', (0, 0), (-1, 0), colors.red)]))

        tabla.wrapOn(c, 20, 30)
        tabla.drawOn(c, 20, 600)
        c.save()
        self.ventanaEmergente("PDF Generado")


Entrada()
Gtk.main()
