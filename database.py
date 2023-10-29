import mysql.connector
from config.config import DB_CONFIG

def get_db_connection():
    """Retorna una nueva conexión a la base de datos."""
    return mysql.connector.connect(**DB_CONFIG) 

def get_user_role(email):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT rol_id FROM usuarios WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        return result['rol_id'] if result else None
    except Exception as e:
        print(f"Error obteniendo rol del usuario: {e}")
        return None
    finally:
        cursor.close()
        cnx.close()

def get_next_patient_id():
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)
        
        # Consultar el máximo ID de pacientes
        query = "SELECT MAX(PacienteID) as max_id FROM Pacientes"
        cursor.execute(query)
        
        result = cursor.fetchone()
        if result and result['max_id']:
            return result['max_id'] + 1
        else:
            # Si la tabla está vacía, devolver 1
            return 1
    except Exception as e:
        print(f"Error obteniendo el próximo ID de paciente: {e}")
        return None
    finally:
        cursor.close()
        cnx.close()
