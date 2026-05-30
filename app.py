from flask import Flask, render_template, request, redirect
import boto3

app = Flask(__name__)

# CONEXIÓN AWS
dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-2'
)

# TABLA
tabla = dynamodb.Table('Usuarios')

# READ
@app.route('/')
def inicio():

    datos = tabla.scan()

    usuarios = datos['Items']

    return render_template(
        'index.html',
        usuarios=usuarios
    )

# CREATE
@app.route('/guardar', methods=['POST'])
def guardar():

    try:

        id = request.form['id']
        nombre = request.form['nombre']
        correo = request.form['correo']

        # VALIDACIÓN
        if id == '' or nombre == '' or correo == '':
            return "Todos los campos son obligatorios"

        tabla.put_item(
            Item={
                'id': id,
                'nombre': nombre,
                'correo': correo
            }
        )

        return redirect('/')

    except Exception as e:
        return f"Error guardando: {e}"

# FORM EDITAR
@app.route('/editar/<id>')
def editar(id):

    respuesta = tabla.get_item(
        Key={'id': id}
    )

    usuario = respuesta['Item']

    return render_template(
        'editar.html',
        usuario=usuario
    )

# UPDATE
@app.route('/actualizar', methods=['POST'])
def actualizar():

    try:

        id = request.form['id']
        nombre = request.form['nombre']
        correo = request.form['correo']

        tabla.update_item(

            Key={
                'id': id
            },

            UpdateExpression=
            "set nombre=:n, correo=:c",

            ExpressionAttributeValues={
                ':n': nombre,
                ':c': correo
            }

        )

        return redirect('/')

    except Exception as e:
        return f"Error actualizando: {e}"

# DELETE
@app.route('/eliminar/<id>')
def eliminar(id):

    try:

        tabla.delete_item(
            Key={'id': id}
        )

        return redirect('/')

    except Exception as e:
        return f"Error eliminando: {e}"

if __name__ == '__main__':
    app.run(debug=True)