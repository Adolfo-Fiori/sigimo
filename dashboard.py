from flask import render_template
from database import get_next_patient_id
#from database import get_user_role
#from permissions import PERMISOS

def setup_dashboard_routes(app):

    @app.route('/asignar_permisos_roles')
    def asignar_permisos_roles():
        return render_template('asignar_permisos_roles.html')

    @app.route('/captura_expedientes')
    def captura_expedientes():
        next_patient_id = get_next_patient_id()
        return render_template('captura_expedientes.html',next_id=next_patient_id)

    @app.route('/asignaciones_especialistas')
    def asignaciones_especialistas():
        return render_template('asignaciones_especialistas.html')

    @app.route('/resultados_laboratorio')
    def resultados_laboratorio():
        return render_template('resultados_laboratorio.html')

    @app.route('/firma_digital')
    def firma_digital():
        return render_template('firma_digital.html')

