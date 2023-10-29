from flask import Flask, request, jsonify
#from flask_cors import CORS
from config.config import DB_CONFIG
import smtplib
import random
import os
import bcrypt
from database import get_db_connection
from dotenv import load_dotenv
load_dotenv()

smtp_password = os.getenv("SMPT_PASSWORD")



def setup_routes(app):
    def get_verification_code(email):
        """Obtiene el código de verificación para un email específico."""
        try:
            cnx = get_db_connection()
            cursor = cnx.cursor(dictionary=True)
            query = "SELECT verification_code FROM usuarios WHERE email = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            return result['verification_code'] if result else None
        except Exception as e:
            print(f"Error obteniendo el código de verificación: {e}")
            return None
        finally:
            cursor.close()
            cnx.close()

    def store_user(username, email, password, verification_code):
        """Almacena un nuevo usuario en la base de datos con un estado no verificado."""
        try:
            # Cifrar la contraseña antes de guardarla en la base de datos
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cnx = get_db_connection()
            cursor = cnx.cursor()
            query = """INSERT INTO usuarios (username, email, password, verification_code, is_verified) 
                    VALUES (%s, %s, %s, %s, FALSE)"""
            cursor.execute(query, (username, email, hashed_password, verification_code))
            cnx.commit()
        except Exception as e:
            print(f"Error almacenando el usuario: {e}")
            return False
        finally:
            cursor.close()
            cnx.close()
        return True

    @app.route('/create-account', methods=['POST'])
    def create_account():
        data = request.get_json() #Por data se refiere a lo siguiente: { username, email, password }
        
        # Validar datos del usuario
        
        # Generar un código de verificación
        verification_code = random.randint(100000, 999999)
        
        # Intenta guardar el usuario y el código de verificación
        if not store_user(data['username'], data['email'], data['password'], verification_code):
            return jsonify(success=False, message="Error al guardar el usuario en la base de datos")
        
        # Enviar el código de verificación por correo electrónico
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('alfonsolimalimon@gmail.com', smtp_password)
            
            subject = 'Código de Verificación'
            body = f'Tu código de verificación es: {verification_code}'
            message = f'Subject: {subject}\n\n{body}'
            message = message.encode('utf-8')

            server.sendmail('alfonsolimalimon@gmail.com', data['email'], message)
            server.quit()
        except Exception as e:
            print(f"Error al enviar correo electrónico: {e}")
            return jsonify(success=False, error=str(e))
        
        return jsonify(success=True)


    @app.route('/verify-account', methods=['POST'])
    def verify_account():
        data = request.get_json() #Por data se refiere a lo siguiente: { email, verificationCode }
        email = data['email']
        input_verification_code = data['verificationCode']
        
        # Obtener el código de verificación asociado al email desde la base de datos
        stored_verification_code = get_verification_code(email)

        if not stored_verification_code:
            # Si no hay un código asociado a ese email, o hubo un error al obtenerlo
            return jsonify(success=False, message="El email no está asociado a un código de verificación.")

        
        # Validar el código de verificación
        if input_verification_code == stored_verification_code:
            # Si los códigos coinciden, cambiar el estado del usuario a verificado
            if set_user_verified(email):
                return jsonify(success=True)
            else:
                return jsonify(success=False, message="Hubo un error al verificar la cuenta.")
        else:
            # Si los códigos no coinciden, enviar un mensaje de error
            print(input_verification_code)
            print(stored_verification_code)
            return jsonify(success=False, message="El código de verificación no es correcto.")
        

    # Función auxiliar para obtener el código de verificación asociado a un email
    def set_user_verified(email):
        """Cambia el estado del usuario a verificado en la base de datos."""
        try:
            cnx = get_db_connection()
            cursor = cnx.cursor()
            query = "UPDATE usuarios SET is_verified = 1 WHERE email = %s"
            cursor.execute(query, (email,))
            cnx.commit()
        except Exception as e:
            print(f"Error verificando el usuario: {e}")
            return False
        finally:
            cursor.close()
            cnx.close()
        return True
    
def check_password(email, password):
#Valida la contraseña del usuario con la almacenada en la base de datos.
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT password FROM usuarios WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result and bcrypt.checkpw(password.encode('utf-8'), result['password'].encode('utf-8')):
            return True
        return False
    except Exception as e:
        print(f"Error comprobando la contraseña: {e}")
        return False
    finally:
        cursor.close()
        cnx.close()