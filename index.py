from argparse import Action
import email
from email.policy import default
from enum import unique
from flask import Flask, render_template,flash,request,redirect
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#==============CONFIGURANDO LA CONEXION A LA BASE DE DATOS DE MYSQL=================================#
#https://wtforms.readthedocs.io/en/3.0.x/
app=Flask(__name__)
if __name__=='__main__':
    app.run(debug=True)
#Add Database
app.config['SQLALCHEMY_DATABASE_URI']='mysql://admin:oscar_123@dbacademico.cwl8pwi5cqbm.us-east-1.rds.amazonaws.com/bdacademico'
app.config['SQLALCHEMY_TRACK_MODEFICATIONS']=False
#secret key
app.config['SECRET_KEY']='My super secret that no one is supposed to know'
#Initialize the Databse
db=SQLAlchemy(app)

#==============================CREANDO LAS TABLAS PARA LA DB ACADEMICO===================================#

#CREANDO LA TABLA Escuela_Profesional
class Escuela_Profesional(db.Model):
    __tablename__ = 'Escuela_Profesional'
    codigo=db.Column(db.String(20), primary_key=True)
    nombre=db.Column(db.String(60),nullable=False)
    duracion=db.Column(db.Integer, nullable=False)

#CREANDO LA TABLA Estudiante    
class Estudiante(db.Model):
    __tablename__ = 'Estudiante'
    id=db.Column(db.Integer, primary_key=True)
    DNI=db.Column(db.Integer, nullable=False)
    apellidos=db.Column(db.String(60),nullable=False)
    nombres=db.Column(db.String(60),nullable=False)
    fecha_nacimiento=db.Column(db.String(30), nullable=False)
    sexo=db.Column(db.String(10),nullable=False)

#CREANDO LA TABLA Curso
class Curso(db.Model):
    __tablename__ = 'Curso'
    codigo=db.Column(db.String(20),primary_key=True)
    nombre=db.Column(db.String(40),nullable=False)
    credito=db.Column(db.Integer,nullable=False)

#CREANDO LA TABLA Matricula
class Matricula(db.Model):
    __tablename__ = 'Matricula'
    id=db.Column(db.Integer, primary_key=True)
    id_estudiante = db.Column(db.Integer, db.ForeignKey('Estudiante.id'))
    id_curso = db.Column(db.String(20), db.ForeignKey('Curso.codigo'))

    def __repr__(self):
        return '<id_estudiante %r>'% self.id_estudiante

with app.app_context():#cada vez que inicio el server me crea las tablas
    db.create_all()

#==============CREANDO EL FORMULARIO PARA AGREGAR CURSOS=================================#

#create form class
class UserForm(FlaskForm):
    #Action="registro.php"
    codigo=StringField("codigo", validators=[DataRequired()])
    nombre=StringField("nombre", validators=[DataRequired()])
    credito=StringField("credito", validators=[DataRequired()])
    submit=SubmitField('Submit')

@app.route('/')
def index():
    first_name='oscar trabajo en antabamba'
    stuff='This come bold text'
    flash("Welcome To Our Website!")
    favorite_pizza=['Hawaina', 'Especial','Italiana', 41]
    return render_template("index.html", 
    first_name=first_name,
    stuff=stuff,
    favorite_pizza=favorite_pizza)

#==============CREANDO LAS RUTAS PARA REALIZAR EL CRUD DE LA TABLA CURSO=================================#
#=CREANDO LA RUTA PARA AGREGAR=#
@app.route('/curso/add',methods=['GET','POST'])
def add_curso():
    name=None
    form=UserForm()
    # Validate form
    if form.validate_on_submit():
        curso=Curso.query.filter_by(codigo=form.codigo.data).first()
        if curso is None:
            curso=Curso(codigo=form.codigo.data, nombre=form.nombre.data,credito=form.credito.data)
            db.session.add(curso)
            db.session.commit()
        name=form.codigo.data
        form.codigo.data=''
        form.nombre.data=''
        form.credito.data=''
        flash("User Add Successfully!")
    our_users=Curso.query.order_by(Curso.nombre)
    return render_template('add_curso.html', form=form, name=name, our_users=our_users)

#=CREANDO LA RUTA PARA EDITAR=#
@app.route('/curso_edit/<codigo>',methods=['GET','POST'])
def update_curso(codigo):
    user=Curso.query.get(codigo)
    form=UserForm()
    if form.validate_on_submit():
        user.codigo=form.codigo.data
        user.nombre=form.nombre.data
        user.credito=form.credito.data

        db.session.commit()

    name=form.nombre.data
    form.codigo.data=''
    form.nombre.data=''
    form.credito.data=''
    flash("From Submitted Successfully")
    our_users=Curso.query.order_by(Curso.nombre)
    return render_template('edit_curso.html',user=user,form=form,name=name,our_users=our_users)

#=CREANDO LA RUTA PARA ELIMNAR=#
@app.route('/delete_curso/<codigo>')
def delete_curso(codigo):
    deleteUser = Curso.query.get(codigo)
    db.session.delete(deleteUser)
    db.session.commit()
    return redirect('/curso/add')


#=======================CREANDO EL FORMULARIO PARA AGREGAR ESTUDIANTES=================================#

#create form class
class UserFormes(FlaskForm):
    id=StringField("Codigo", validators=[DataRequired()])
    DNI=StringField("DNI", validators=[DataRequired()])
    apellidos=StringField("Apellidos", validators=[DataRequired()])
    nombres=StringField("Nombres", validators=[DataRequired()])
    fecha_nacimiento=StringField("Fecha de Nacimiento", validators=[DataRequired()])
    sexo=StringField("Sexo", validators=[DataRequired()])
    submit=SubmitField('Submit')

#==============CREANDO LAS RUTAS PARA REALIZAR EL CRUD DE LA TABLA ESTUDIANTE=================================#
#=CREANDO LA RUTA PARA AGREGAR=#
@app.route('/estudiante/add',methods=['GET','POST'])
def add_estudiante():
    name=None
    form=UserFormes()
    # Validate form
    if form.validate_on_submit():
        estu=Estudiante.query.filter_by(DNI=form.DNI.data).first()
        if estu is None:
            estu=Estudiante(id=form.id.data,DNI=form.DNI.data, apellidos=form.apellidos.data,nombres=form.nombres.data,fecha_nacimiento=form.fecha_nacimiento.data,sexo=form.sexo.data)
            db.session.add(estu)
            db.session.commit()
        name=form.DNI.data
        form.id.data=''
        form.DNI.data=''
        form.apellidos.data=''
        form.nombres.data=''
        form.fecha_nacimiento.data=''
        form.sexo.data=''
        flash("User Add Successfully!")
    our_ests=Estudiante.query.order_by(Estudiante.nombres)
    return render_template('add_estudiante.html', form=form, name=name, our_ests=our_ests)

#=CREANDO LA RUTA PARA EDITAR=#
@app.route('/estudiante_edit/<id>',methods=['GET','POST'])
def update_estudiante(id):
    estu=Estudiante.query.get(id)
    form=UserFormes()
    if form.validate_on_submit():
        estu.id=form.id.data
        estu.DNI=form.DNI.data
        estu.apellidos=form.apellidos.data
        estu.nombres=form.nombres.data
        estu.fecha_nacimiento=form.fecha_nacimiento.data
        estu.sexo=form.sexo.data

        db.session.commit()

    name=form.nombres.data
    form.id.data=''
    form.DNI.data=''
    form.apellidos.data=''
    form.nombres.data=''
    form.fecha_nacimiento.data=''
    form.sexo.data=''
    flash("From Submitted Successfully")
    our_ests=Estudiante.query.order_by(Estudiante.nombres)
    return render_template('edit_estudiante.html',estu=estu,form=form,name=name,our_ests=our_ests)

#=CREANDO LA RUTA PARA ELIMNAR=#
@app.route('/delete_estudiante/<id>')
def delete_estudiante(id):
    deleteestudiante = Estudiante.query.get(id)
    db.session.delete(deleteestudiante)
    db.session.commit()
    return redirect('/estudiante/add')

#==============================================CREANDO EL FORMULARIO PARA AGREGAR ESCUELA PROFESIONAL=================================#

#create form class
class UserFormpro(FlaskForm):
    codigo=StringField("Codigo", validators=[DataRequired()])
    nombre=StringField("Nombre", validators=[DataRequired()])
    duracion=StringField("Duracion", validators=[DataRequired()])
    submit=SubmitField('Submit')

#==============CREANDO LAS RUTAS PARA REALIZAR EL CRUD DE LA TABLA ESCUELA PROFESIONAL===========================#
#=CREANDO LA RUTA PARA AGREGAR=#
@app.route('/escuela/add',methods=['GET','POST'])
def add_escuela():
    name=None
    form=UserFormpro()
    # Validate form
    if form.validate_on_submit():
        escuela=Escuela_Profesional.query.filter_by(codigo=form.codigo.data).first()
        if escuela is None:
            escuela=Escuela_Profesional(codigo=form.codigo.data,nombre=form.nombre.data, duracion=form.duracion.data)
            db.session.add(escuela)
            db.session.commit()
        name=form.codigo.data
        form.codigo.data=''
        form.nombre.data=''
        form.duracion.data=''
        flash("User Add Successfully!")
    our_escuelas=Escuela_Profesional.query.order_by(Escuela_Profesional.nombre)
    return render_template('add_escuela.html', form=form, name=name, our_escuelas=our_escuelas)

#=CREANDO LA RUTA PARA EDITAR=#
@app.route('/escuela_edit/<codigo>',methods=['GET','POST'])
def update_escuela(codigo):
    escuela=Escuela_Profesional.query.get(codigo)
    form=UserFormpro()
    if form.validate_on_submit():
        escuela.codigo=form.codigo.data
        escuela.nombre=form.nombre.data
        escuela.duracion=form.duracion.data

        db.session.commit()

    name=form.nombre.data
    form.codigo.data=''
    form.nombre.data=''
    form.duracion.data=''
    flash("From Submitted Successfully")
    our_escuelas=Escuela_Profesional.query.order_by(Escuela_Profesional.nombre)
    return render_template('edit_escuela.html',escuela=escuela,form=form,name=name,our_escuelas=our_escuelas)

#=CREANDO LA RUTA PARA ELIMNAR=#
@app.route('/delete_escuela/<codigo>')
def delete_escuela(codigo):
    deleteescuela = Escuela_Profesional.query.get(codigo)
    db.session.delete(deleteescuela)
    db.session.commit()
    return redirect('/escuela/add')


#==============================================CREANDO EL FORMULARIO PARA AGREGAR MATRICULA=================================#

#create form class
class UserFormmatri(FlaskForm):
    id_estudiante=StringField("Codigo del estudiante", validators=[DataRequired()])
    id_curso=StringField("Codigo del curso", validators=[DataRequired()])
    submit=SubmitField('Submit')

#==============CREANDO LAS RUTAS PARA REALIZAR EL CRUD DE LA TABLA MATRICULA===========================#
#=CREANDO LA RUTA PARA AGREGAR=#
@app.route('/matricula/add',methods=['GET','POST'])
def add_matricula():
    name=None
    form=UserFormmatri()
    # Validate form
    if form.validate_on_submit():
        matri=Matricula.query.filter_by(id=form.id_estudiante.data).first()
        if matri is None:
            matri=Matricula(id_estudiante=form.id_estudiante.data, id_curso=form.id_curso.data)
            db.session.add(matri)
            db.session.commit()
        name=form.id_estudiante.data
        form.id_estudiante.data=''
        form.id_curso.data=''
        flash("User Add Successfully!")
    our_matriculas=Matricula.query.order_by(Matricula.id_estudiante)
    return render_template('add_matricula.html', form=form, name=name, our_matriculas=our_matriculas)

#=CREANDO LA RUTA PARA EDITAR=#
@app.route('/matricula_edit/<id>',methods=['GET','POST'])
def update_matricula(id):
    matri=Matricula.query.get(id)
    form=UserFormmatri()
    if form.validate_on_submit():
        matri.id_estudiante=form.id_estudiante.data
        matri.id_curso=form.id_curso.data

        db.session.commit()

    name=form.id_estudiante.data
    form.id_estudiante.data=''
    form.id_curso.data=''
    flash("From Submitted Successfully")
    our_matriculas=Matricula.query.order_by(Matricula.id_estudiante)
    return render_template('edit_matricula.html',matri=matri,form=form,name=name,our_matriculas=our_matriculas)

#=CREANDO LA RUTA PARA ELIMNAR=#
@app.route('/delete_matricula/<id>')
def delete_matricula(id):
    deletematri = Matricula.query.get(id)
    db.session.delete(deletematri)
    db.session.commit()
    return redirect('/matricula/add')