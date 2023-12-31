
from sys import version
from PySide2 import QtWidgets , QtCore , QtGui
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMessageBox

import re

from datetime import datetime
from controllers.Modulo_utils.Funcion_validaciones import *
from controllers.Modulo_utils.funcion_efecto import Clase_Opacidad

from views.ui_vinculacion_nuevo import Ui_NuevaVinculacion




# importamos la clase de la base datos
from db.Modulo_base import BaseDatos


class Vinculacion(QtWidgets.QDialog):

    def __init__(self, vinculacion_id = None , nombre_estudiante = '', estado = '', modo="" , parent=None):
        
        super(Vinculacion, self).__init__(parent)
        self.vinculacion = Ui_NuevaVinculacion()
        self.vinculacion.setupUi(self)
        
        self.conec_base = BaseDatos()
        self.configuracion_ventana()

        self.parent = parent
        
        self.vinculacion_id = vinculacion_id 
        self.nombre_estudiante = nombre_estudiante
        self.estado = estado
        self.modo = modo

        if self.vinculacion_id and self.modo == "actualizar":
            self.cargar_datos_vinculacion(self.vinculacion_id)
            # self.vinculacion.vinculacion_titulo.setText(
            #     f'Actualizar Vinculación: {self.nombre_estudiante} '
            #     f'\nEstado: {self.estado}'
            # )
            self.vinculacion.axax.setText('Actualizar Vinculación: ')
            self.vinculacion.vinculacion_titulo.setText(self.nombre_estudiante)
            
            self.actualizar_titulo_estado()
            self.vinculacion.vinculacion_estado.setText(self.estado)
            self.vinculacion.btn_guardar.setText('Actualizar')
            
        else:
            self.vinculacion.vinculacion_estado.hide()
            self.vinculacion.vinculacion_titulo.hide()
            self.vinculacion.vinculacion_titulo_2.hide()
            
        # Evento Opacidad -----------------------
        self.raizOpacidad = Clase_Opacidad(self.parent)
        self.raizOpacidad.close()

        # Quitar fondo, transparencia
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint |QtCore.Qt.Tool | QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.vinculacion.btn_closeadmi.clicked.connect(lambda: self.cerrar_ui_vinculacion())
        

        self.vinculacion.line_identificacion.textChanged.connect(lambda: self.vinculacion.line_identificacion.setToolTip('Formato: 10 digitos\n Ejm: 992929394-9'))
        self.vinculacion.line_periodoacademico.textChanged.connect(lambda: self.vinculacion.line_periodoacademico.setToolTip('Ejm: P1-2023'))
        self.vinculacion.line_codigoies.textChanged.connect(lambda: self.vinculacion.line_codigoies.setToolTip('Formato: 4 digito númericos\n Ejm: 1003'))
        self.vinculacion.line_campoespecifico.textChanged.connect(lambda: self.vinculacion.line_campoespecifico.setToolTip('Ejm: 1-2A'))
        


        # Validaciones y mascaras para los inputs
        val_nombre_apellido(self, self.vinculacion.line_nombreapellidos)
        val_identifiacion(self, self.vinculacion.line_identificacion)
        val_periodo_academico(self, self.vinculacion.line_periodoacademico)
        val_codigo_campoespecifico(self, self.vinculacion.line_campoespecifico)
        val_codigo_ies(self, self.vinculacion.line_codigoies)


        # boton guardar
        self.vinculacion.btn_guardar.clicked.connect(lambda: self.obtener_campos_vinculacion())

                
    def actualizar_titulo_estado(self):
        if self.estado == "Pendiente":
            color_texto = "red"
        elif self.estado == "Culminado":
            color_texto = "green"

        estilo = f"color: {color_texto}; font-family: Roboto; font-style: normal; font-weight: 500; font-size: 17px; line-height: 40px; letter-spacing: 0.02em;"
        self.vinculacion.vinculacion_estado.setStyleSheet(estilo)


            
    def keyPressEvent(self, event):
  
        if event.key() == QtCore.Qt.Key_Escape:
            pass
    
    def cerrar_ui_vinculacion(self):
        self.parent.raizOpacidad.close()
        self.close()
        
    def keyPressEvent(self, qKeyEvent):
 
        if qKeyEvent.modifiers() & QtCore.Qt.AltModifier:
            qKeyEvent.ignore()
        elif qKeyEvent.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
            self.focusNextChild()
            self.window().setAttribute(QtCore.Qt.WA_KeyboardFocusChange)
        else:
            super().keyPressEvent(qKeyEvent)
            
    def llenar_combobox(self, combobox, lista, longitud_maxima):
        for elemento in lista:
            id_elemento, nombre_elemento = elemento
            texto_truncado = nombre_elemento[:longitud_maxima]
            combobox.addItem(texto_truncado, userData=id_elemento)
            combobox.setItemData(combobox.count() - 1, nombre_elemento, Qt.ToolTipRole)

    def configuracion_ventana(self):
        lista_carrera, lista_institucion, lista_proyectos, lista_tutores = self.conec_base.getDatosProcess("ObtenerDatos")
        
        self.llenar_combobox(self.vinculacion.cbox_carrera, lista_carrera, 30)
        self.llenar_combobox(self.vinculacion.cbo_institucion, lista_institucion, 30)
        self.llenar_combobox(self.vinculacion.cbo_proyectos, lista_proyectos, 100)
        self.llenar_combobox(self.vinculacion.cbo_tutor, lista_tutores, 30)

    def obtener_campos_vinculacion(self):
        
        nombre_apellidos = self.vinculacion.line_nombreapellidos.text().strip();
        tipo_identificacion = self.vinculacion.cbo_tipo_identificacion.currentText();
        identificacion = self.vinculacion.line_identificacion.text();
        carrera = self.vinculacion.cbox_carrera.itemData(self.vinculacion.cbox_carrera.currentIndex()); 
        institucion = self.vinculacion.cbo_institucion.itemData(self.vinculacion.cbo_institucion.currentIndex()); 
        periodo_academico = self.vinculacion.line_periodoacademico.text()
        fecha_inicio = self.vinculacion.fecha_inicio.date().toString("yyyy-MM-dd")
        fecha_final = self.vinculacion.fecha_final.date().toString("yyyy-MM-dd")
        codigo_ies = self.vinculacion.line_codigoies.text()
        campo_especifico = self.vinculacion.line_campoespecifico.text()
        tutor_asignado = self.vinculacion.cbo_tutor.itemData(self.vinculacion.cbo_tutor.currentIndex())
        proyecto  = self.vinculacion.cbo_proyectos.itemData(self.vinculacion.cbo_proyectos.currentIndex())


        # Realizar las validaciones
        mensaje_error = ""

        if not nombre_apellidos:
            mensaje_error += "- Ingrese el nombre y apellidos.\n"

        if not tipo_identificacion:
            mensaje_error += "- Seleccione un tipo de identificación.\n"

        if len(identificacion) != 11 or identificacion[9] != '-':
            mensaje_error += "- Ingrese una identificacion válido (ejemplo: 112233456-2).\n"

        if not carrera:
            mensaje_error += "- Seleccione una carrera.\n"

        if not institucion:
            mensaje_error += "- Seleccione una institución.\n"

        patron_periodo_academico = re.compile(r'^P[1-9]-\d{4}$')
        if not periodo_academico or not patron_periodo_academico.match(periodo_academico):
            mensaje_error += "- Ingrese un período académico válido (ejemplo: P1-1222).\n"


        if not fecha_inicio:
            mensaje_error += "- Ingrese una fecha de inicio válida.\n"

        if not fecha_final:
            mensaje_error += "- Ingrese una fecha final válida.\n"

        if not codigo_ies or len(codigo_ies) != 4:
            mensaje_error += "- El código de IES debe tener 4 dígitos.\n"


        formato_correcto = re.match(r'^[1-9]?\d-[1-9]?\d[A-Z]$', campo_especifico)
        if not campo_especifico or not formato_correcto:
            mensaje_error += "- Ingrese un campo específico válido (ejemplo: 1-6A).\n"


        if not tutor_asignado:
            mensaje_error += "- Seleccione un tutor.\n"

        if mensaje_error:
            # Si hay errores, muestra el mensaje de error en un QMessageBox
            QMessageBox.critical(self, "Error", "Revise los campos:\n" + mensaje_error)
        else:

            datos = [tipo_identificacion, identificacion, nombre_apellidos, carrera , periodo_academico,
                        codigo_ies, fecha_inicio, fecha_final, campo_especifico, tutor_asignado, institucion, proyecto]

            if self.modo == "actualizar":
                # Lógica para actualizar los datos de la vinculación existente
                datos.append(self.vinculacion_id)
                self.actualizar_vinculacion(datos)
            else:
                # Lógica para crear una nueva vinculación
                self.crear_nueva_vinculacion(datos)


            # Si no hay errores, continuar con el procesamiento
            QMessageBox.information(self, "Correcto", "Datos válidos. Continuar con el procesamiento...")

    def cargar_datos_vinculacion(self, vinculacion_id):
        datos = self.conec_base.getDatosProcess_condicion("ObtenerDatosVinculacion", (vinculacion_id,))
 
        if datos:
            datos = datos[0][0]

            self.vinculacion.line_nombreapellidos.setText(str(datos[0]))
            self.vinculacion.cbo_tipo_identificacion.setCurrentText(datos[1])
            self.vinculacion.line_identificacion.setText(str(datos[2]))
            self.vinculacion.line_periodoacademico.setText(str(datos[5]))
            self.vinculacion.fecha_inicio.setDate(datos[6])
            self.vinculacion.fecha_final.setDate(datos[7])
            self.vinculacion.spb_numerohoras.setValue(datos[8])
            self.vinculacion.line_codigoies.setText(str(datos[9]))
            self.vinculacion.line_campoespecifico.setText(str(datos[10]))

            # Obteniendo los identificadores de los datos
            codigo_carrera = datos[3]
            codigo_institucion = datos[4]
            identificacion_tutor = datos[11]
            id_proyecto = datos[12]

            # Buscando el índice correspondiente al identificador en los ComboBoxes
            self.set_combobox_by_user_data(self.vinculacion.cbox_carrera, codigo_carrera)
            self.set_combobox_by_user_data(self.vinculacion.cbo_institucion, codigo_institucion)
            self.set_combobox_by_user_data(self.vinculacion.cbo_tutor, identificacion_tutor)
            self.set_combobox_by_user_data(self.vinculacion.cbo_proyectos, id_proyecto)

    def set_combobox_by_user_data(self, combobox, user_data):
        index = combobox.findData(user_data, role=Qt.UserRole) 
        if index != -1:
            combobox.setCurrentIndex(index)


    def actualizar_vinculacion(self, dato_vinculacion):
        try:
            self.conec_base.setDatosProcess('ActualizarEstudianteYVinculacion', dato_vinculacion)
            QMessageBox.information(self, "Éxito", "Vinculación fue actualizado exitosamente.")
            self.parent.listar_vinculacion()
            self.parent.raizOpacidad.close()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar vinculación: {str(e)}")
        
    def crear_nueva_vinculacion(self, dato_vinculacion):
        try:
            self.conec_base.setDatosProcess('InsertarEstudianteYVinculacion', dato_vinculacion)
            QMessageBox.information(self, "Éxito", "Nueva vinculación creada exitosamente.")
            self.parent.listar_vinculacion()
            self.parent.raizOpacidad.close()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al crear la nueva vinculación: {str(e)}")



        
        
        
    