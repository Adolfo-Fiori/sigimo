# expedientes.py

from flask import Flask, request, jsonify
#from flask_cors import CORS
import random
import datetime
import string
import os
from database import get_db_connection
from dotenv import load_dotenv
load_dotenv()

def generar_codigo_anonimato():
    # Obtener la fecha en formato 'yy-mm-dd'
    fecha = datetime.datetime.now().strftime('%y%m%d')
    
    # Generar dos caracteres aleatorios del abecedario
    letras = ''.join(random.choices(string.ascii_lowercase, k=2))
    
    # Generar un número aleatorio entre 0000 y 9999
    numero = str(random.randint(0, 9999)).zfill(4)
    
    # Combinar todo para formar el código
    codigo = f'{fecha}_{letras}_{numero}'
    
    return codigo


def setup_expedientes_routes(app):
    @app.route('/api/insertExp', methods=['POST'])
    def insert_data():
        data = request.json
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            paciente_id = data['paciente']['pacienteId']
            codigo_anonimato = generar_codigo_anonimato()  # Generar el código
            # Insertar en Pacientes
            cursor.execute("""INSERT INTO Pacientes(PacienteID,Nombre,ApellidoPaterno,ApellidoMaterno,FechaNacimiento,Direccion,Telefono,Email,Genero,codigoAnonimato)
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", 
                            (paciente_id, data['paciente']['nombre'], data['paciente']['apellidoPaterno'], data['paciente']['apellidoMaterno'], 
                            data['paciente']['fechaNacimiento'], data['paciente']['direccion'], data['paciente']['telefono'], 
                            data['paciente']['email'], data['paciente']['genero'],codigo_anonimato))

            # Insertar en AntecedentesClinicos
            cursor.execute("""INSERT INTO AntecedentesClinicos(PacienteID,TipoAntecedente,Descripcion,Fecha)
                            VALUES(%s,%s,%s,CURDATE())""", 
                            (paciente_id, data['antecedente']['tipoAntecedente'], data['antecedente']['descripcion']))  # AntecedenteID es random en este caso

            # Insertar en Diagnosticos
            cursor.execute("""INSERT INTO Diagnosticos(PacienteID,Sintomatologia,Diagnostico,FechaDiagnostico)
                            VALUES(%s,%s,%s,CURDATE())""", 
                            (paciente_id, data['diagnostico']['sintomatologia'], "",))  # Diagnóstico es vacío en este caso

            # Insertar en Estudios
            cursor.execute("""INSERT INTO Estudios(PacienteID,NombreEstudio,FechaEmision)
                            VALUES(%s,%s,CURDATE())""", 
                            (paciente_id, data['estudio']['nombreEstudio']))

            connection.commit()

            return jsonify({'message': 'Datos insertados exitosamente'})

        except Exception as e:
            connection.rollback()
            return jsonify({'message': 'Error al insertar los datos: ' + str(e)})

        finally:
            cursor.close()
            connection.close()
    
    @app.route('/api/insertCert', methods=['POST'])
    def insert_certificado():
        data = request.json
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            paciente_id = data['certificado']['pacienteId']
            fecha_emision = data['certificado']['fechaEmision']
            motivo = data['certificado']['motivo']

            cursor.execute("""INSERT INTO CertificadosMedicos(PacienteID, FechaEmision, Motivo)
                            VALUES(%s,%s,%s)""", 
                            (paciente_id, fecha_emision, motivo))

            connection.commit()

            return jsonify({'message': 'Certificado insertado exitosamente'})

        except Exception as e:
            connection.rollback()
            return jsonify({'message': 'Error al insertar el certificado: ' + str(e)})

        finally:
            cursor.close()
            connection.close()
