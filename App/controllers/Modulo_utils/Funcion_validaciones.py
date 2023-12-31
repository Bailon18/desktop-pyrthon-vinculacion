
# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/ RESTRICCION DE INGRESO /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
from PySide2.QtCore import QRegExp
from PySide2.QtGui import QRegExpValidator,QIntValidator
from PySide2.QtCore import QDate # para fechas

def val_nombre_apellido(parent, objeto):
    valNombreApellido = QRegExpValidator(parent)
    valNombreApellido.setRegExp(QRegExp("^[a-zA-ZÀ-ÿ ]+$"))  # Permitir letras y espacios y acentos
    objeto.setValidator(valNombreApellido) 


def val_identifiacion(parent, objeto):
    valCadenaNum = QRegExpValidator(parent)
    valCadenaNum.setRegExp(QRegExp("^\d{9}-\d{1}$"))
    objeto.setValidator(valCadenaNum)  # Aplicar el validador al QLineEdit
    
def mascara_identificacion(objeto):
    """Máscara de ingreso"""
    objeto.setInputMask("999999999\-9")

def val_periodo_academico(parent, objeto):
    # Validador para el formato P1-2023 o P2-2023
    valPeriodoAcademico = QRegExpValidator(parent)
    valPeriodoAcademico.setRegExp(QRegExp("^P[1-2]-\d{4}$"))
    objeto.setValidator(valPeriodoAcademico)  # Aplicar el validador al QLineEdit

def mascara_periodo_academico(objeto):
    """Máscara de ingreso"""
    objeto.setInputMask("P9-9999")
    

def val_codigo_campoespecifico(parent, objeto):
    # Validador para el formato 1-6A
    valcampoespecifico = QRegExpValidator(parent)
    valcampoespecifico.setRegExp(QRegExp("^[1-9]-[1-9][A-Z]$"))
    objeto.setValidator(valcampoespecifico) 

def mascara_campoespecifico(objeto):
    """Máscara de ingreso"""
    objeto.setInputMask("9-9A")  # Esto limita la entrada al formato específico 1-6A


def val_codigo_ies(parent, objeto):
    # Validador para el formato de 4 dígitos del 1 al 9
    valCodigoIES = QRegExpValidator(parent)
    valCodigoIES.setRegExp(QRegExp("^[1-9]{4}$"))
    objeto.setValidator(valCodigoIES) 

def mascara_codigo_ies(objeto):
    """Máscara de ingreso"""
    objeto.setInputMask("9999") 
    
    
def borrar_caracteres(objeto, mascara_actual):
    # Obtener el cursor del QLineEdit
    cursor = objeto.cursorPosition()
    
    # Obtener el texto actual
    texto = objeto.text()
    
    # Verificar si hay algo seleccionado
    if objeto.selectedText():
        # Si hay texto seleccionado, eliminar el texto seleccionado
        objeto.insert("")
    else:
        # Si no hay texto seleccionado, eliminar el carácter a la izquierda del cursor
        texto = texto[:cursor - 1] + texto[cursor:]
        objeto.setText(texto)
        objeto.setCursorPosition(cursor - 1)  # Restaurar la posición del cursor
    
    # Aplicar la máscara y la validación nuevamente
    mascara_actual(objeto)


def borrar_caracteres_identificacion(objeto, mascara_identificacion):
    cursor = objeto.cursorPosition()
    texto = objeto.text()
    
    if objeto.selectedText():
        objeto.insert("")
    else:
        # Verificar si el cursor está en una posición que no puede ser eliminada
        if cursor > 0 and texto[cursor - 1] == '-':
            # Si el cursor está justo antes del guión, mover el cursor un paso a la izquierda
            objeto.setCursorPosition(cursor - 1)
        else:
            # Si no está justo antes del guión, eliminar el carácter a la izquierda del cursor
            texto = texto[:cursor - 1] + texto[cursor:]
            objeto.setText(texto)
            objeto.setCursorPosition(cursor - 1)

    mascara_identificacion(objeto)




