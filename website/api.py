import json

from constants import *
from Database import Database
from flask import Blueprint, jsonify, request

api = Blueprint("api", __name__)

"""
Ruta para retornar el poema solicitado.

Parámetro:
    <int:id> = El ID del poema.
"""


@api.route("/poem/<int:id>")
def get(id):
    # Verificar que el ID sea válido
    if id <= 0:
        return (
            jsonify({"msg": INVALID_PARAMETERS, "status": BAD_REQUEST_STATUS}),
            BAD_REQUEST_STATUS,
        )

    # Obtener el poema y verificar que exista.
    poem = Database().get_poem(id)
    if not poem:
        return (
            jsonify({"msg": POEM_NOT_FOUND, "status": NOT_FOUND_STATUS}),
            NOT_FOUND_STATUS,
        )

    # Remplazar la llave "_id" por "id".
    poem["id"] = poem.pop("_id")

    return jsonify(poem), OK_STATUS


"""
Ruta para crear un poema.

Parámetros:
    <string:author> = El nombre del autor.
    <string:title> = El titulo del poema.
    <array:poem> = El poema formateado dentro de un arreglo.
    <string:secret> = La clave secreta.
"""


@api.route("/poem", methods=["POST"])
def create():
    try:
        # Obtener los parámetros del cuerpo de la petición.
        args = request.get_json(force=True)

        # Asignar los valores a las variables.
        try:
            author, title, poem, secret = (
                args.get("author"),
                args.get("title"),
                args.get("poem"),
                args.get("secret"),
            )
        except:
            return (
                jsonify({"msg": INVALID_PARAMETERS, "status": BAD_REQUEST_STATUS}),
                BAD_REQUEST_STATUS,
            )

        # Verificar que los valores no estén vacíos
        if author == "" or title == "" or poem == []:
            return (
                jsonify({"msg": INVALID_PARAMETERS, "status": BAD_REQUEST_STATUS}),
                BAD_REQUEST_STATUS,
            )

        # Verificar que la clave secreta sea correcta.
        if secret != SECRET:
            return (
                jsonify({"msg": NOT_AUTHORIZED_MSG, "status": NOT_AUTHORIZED_STATUS}),
                NOT_AUTHORIZED_STATUS,
            )

        # Crear el poema y verificar si todo salió bien.
        created = Database().create_poem(author, title, poem)

        if created:
            return jsonify(), CREATED_STATUS
        else:
            raise Exception
    except:
        return (
            jsonify(
                {"msg": INTERNAL_SERVER_ERROR, "status": INTERNAL_SERVER_ERROR_STATUS}
            ),
            INTERNAL_SERVER_ERROR_STATUS,
        )


"""
Ruta para actualizar un poema.

Parámetros:
    <int:id> = El ID del poema.
    <string:autor> = El nombre del autor.
    <string:titulo> = El titulo del poema.
    <array:poema> = El poema formateado dentro de un arreglo.
    <string:secret> = La clave secreta.
"""


@api.route("/poem/<int:id>", methods=["PUT"])
def update(id):
    try:
        # Verificar que el ID sea válido
        if id <= 0:
            return (
                jsonify({"msg": INVALID_PARAMETERS, "status": BAD_REQUEST_STATUS}),
                BAD_REQUEST_STATUS,
            )

        # Verificar que el poema exista.
        if not Database().get_poem(id):
            return (
                jsonify({"msg": POEM_NOT_FOUND, "status": NOT_FOUND_STATUS}),
                NOT_FOUND_STATUS,
            )

        # Obtener los parámetros del cuerpo de la petición.
        args = request.get_json(force=True)
        # Asignar los valores a las variables.
        try:
            author, title, poem, secret = (
                args.get("author"),
                args.get("title"),
                args.get("poem"),
                args.get("secret"),
            )
        except:
            return (
                jsonify({"msg": INVALID_PARAMETERS, "status": BAD_REQUEST_STATUS}),
                BAD_REQUEST_STATUS,
            )

        # Verificar que los valores no estén vacíos
        if author == "" or title == "" or poem == []:
            return (
                jsonify({"msg": INVALID_PARAMETERS, "status": BAD_REQUEST_STATUS}),
                BAD_REQUEST_STATUS,
            )

        # Verificar que la clave secreta sea correcta.
        if secret != SECRET:
            return (
                jsonify({"msg": NOT_AUTHORIZED_MSG, "status": NOT_AUTHORIZED_STATUS}),
                NOT_AUTHORIZED_STATUS,
            )

        # Actualizar el poema y verificar si todo salió bien.
        updated = Database().update_poem(id, author, title, poem)

        if updated:
            return jsonify({"msg": POEM_UPDATED, "status": OK_STATUS}), OK_STATUS
        else:
            raise Exception
    except:
        return (
            jsonify(
                {"msg": INTERNAL_SERVER_ERROR, "status": INTERNAL_SERVER_ERROR_STATUS}
            ),
            INTERNAL_SERVER_ERROR_STATUS,
        )


"""
Ruta para eliminar un poema.

Parámetros:
    <int:id> = El ID del poema.
    <string:secret> = La clave secreta.
"""


@api.route("/poem/<int:id>", methods=["DELETE"])
def delete(id):
    try:
        # Verificar que el ID sea válido
        if id <= 0:
            return (
                jsonify({"msg": INVALID_PARAMETERS, "status": BAD_REQUEST_STATUS}),
                BAD_REQUEST_STATUS,
            )

        # Verificar que el poema exista.
        if not Database().get_poem(id):
            return (
                jsonify({"msg": POEM_NOT_FOUND, "status": NOT_FOUND_STATUS}),
                NOT_FOUND_STATUS,
            )

        # Obtener parámetros del cuerpo de la petición.
        args = request.get_json(force=True)

        # Verificar que la clave secreta sea correcta.
        if "secret" not in args or args.get("secret") != SECRET:
            return (
                jsonify({"msg": NOT_AUTHORIZED_MSG, "status": NOT_AUTHORIZED_STATUS}),
                NOT_AUTHORIZED_STATUS,
            )

        # Elimina el poema y verificar si todo salió bien.
        deleted = Database().delete_poem(id)

        if deleted:
            return jsonify({"msg": POEM_DELETED, "status": OK_STATUS}), OK_STATUS
        else:
            raise Exception
    except:
        return (
            jsonify(
                {"msg": INTERNAL_SERVER_ERROR, "status": INTERNAL_SERVER_ERROR_STATUS}
            ),
            INTERNAL_SERVER_ERROR_STATUS,
        )


"""
Ruta para retornar los poemas con limites que el usuario proponga.

Parámetros:
    <int:quantity> (opt) = Cantidad de poemas a retornar
    <int:page> (opt) = Número de página de poemas.
"""


@api.route("/poems")
def get_all():
    try:
        # Verificar los parámetros de la petición y añadirlos a variables.
        try:
            args = json.loads(json.dumps(request.args))

            quantity = (
                DEFAULT_QUANTITY
                if "quantity" not in args or int(args.get("quantity")) <= 0
                else int(args.get("quantity"))
            )
            page = (
                DEFAULT_PAGE
                if "page" not in args or int(args.get("page")) <= 0
                else int(args.get("page"))
            )
        except:
            return (
                jsonify({"msg": INVALID_PARAMETERS, "status": BAD_REQUEST_STATUS}),
                BAD_REQUEST_STATUS,
            )

        # Inicializar la base de datos y verificar que haya suficientes registros.
        db = Database()
        min_records = (page - 1) * quantity + 1
        if db.records < min_records:
            return (
                jsonify({"msg": NO_ENOUGH_POEMS, "status": BAD_REQUEST_STATUS}),
                BAD_REQUEST_STATUS,
            )

        # Obtener y filtrar los poemas segun la página y la cantidad.
        poems = db.get_poems(limit=quantity * page)[min_records - 1 :]

        # Remplazar la llave "_id" por "id".
        for poem in poems:
            poem["id"] = poem.pop("_id")

        # Definir si hay próxima página y cuál es.
        next_page = None if db.records < min_records + quantity else page + 1

        return jsonify({"poems": poems, "next_page": next_page}), OK_STATUS
    except:
        return (
            jsonify(
                {"msg": INTERNAL_SERVER_ERROR, "status": INTERNAL_SERVER_ERROR_STATUS}
            ),
            INTERNAL_SERVER_ERROR_STATUS,
        )
