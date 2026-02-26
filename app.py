import os
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.secret_key = "clave_secreta_segura"

# ==========================
# Configuración Base de Datos
# ==========================
database_url = os.getenv('DATABASE_URL')

if database_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estudiantes.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==========================
# Modelo
# ==========================
class Estudiante(db.Model):
    __tablename__ = 'estudiantes'

    no_control = db.Column(db.String(20), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ap_paterno = db.Column(db.String(100), nullable=False)
    ap_materno = db.Column(db.String(100), nullable=False)
    semestre = db.Column(db.Integer, nullable=False)

# Crear tablas automáticamente
with app.app_context():
    db.create_all()

# ==========================
# Rutas
# ==========================

@app.route('/')
@app.route('/estudiantes')
def index():
    estudiantes = Estudiante.query.all()
    return render_template('index.html', estudiantes=estudiantes)

@app.route('/estudiantes/new', methods=['GET', 'POST'])
def create_estudiante():
    if request.method == 'POST':
        nuevo = Estudiante(
            no_control=request.form['no_control'],
            nombre=request.form['nombre'],
            ap_paterno=request.form['ap_paterno'],
            ap_materno=request.form['ap_materno'],
            semestre=int(request.form['semestre'])
        )

        db.session.add(nuevo)
        db.session.commit()

        flash('Estudiante agregado correctamente', 'success')
        return redirect(url_for('index'))

    return render_template('create_estudiante.html')

@app.route('/estudiantes/update/<string:no_control>', methods=['GET', 'POST'])
def update_estudiante(no_control):
    estudiante = Estudiante.query.get_or_404(no_control)

    if request.method == 'POST':
        estudiante.nombre = request.form['nombre']
        estudiante.ap_paterno = request.form['ap_paterno']
        estudiante.ap_materno = request.form['ap_materno']
        estudiante.semestre = int(request.form['semestre'])

        db.session.commit()
        flash('Estudiante actualizado correctamente', 'info')
        return redirect(url_for('index'))

    return render_template('update_estudiante.html', estudiante=estudiante)

@app.route('/estudiantes/delete/<string:no_control>')
def delete_estudiante(no_control):
    estudiante = Estudiante.query.get_or_404(no_control)

    db.session.delete(estudiante)
    db.session.commit()

    flash('Estudiante eliminado correctamente', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)