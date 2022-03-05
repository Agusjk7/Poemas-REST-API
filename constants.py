from os import getenv

MONGO_URI = getenv("MONGO_URI")
SECRET = getenv("SECRET")
DEFAULT_QUANTITY = int(getenv("DEFAULT_QUANTITY"))
DEFAULT_PAGE = int(getenv("DEFAULT_PAGE"))
OK_STATUS = 200
CREATED_STATUS = 204
BAD_REQUEST_STATUS = 400
NOT_AUTHORIZED_STATUS = 403
NOT_FOUND_STATUS = 404
INTERNAL_SERVER_ERROR_STATUS = 500
INVALID_PARAMETERS = "Parámetros inválidos."
NO_ENOUGH_POEMS = "No hay suficientes poemas para mostrar en esta página."
POEM_NOT_FOUND = "Poema no encontrado."
NOT_AUTHORIZED_MSG = "Usted no está autorizado para realizar esta acción."
INTERNAL_SERVER_ERROR = "Ha ocurrido un error interno en el servidor."
POEM_UPDATED = "Poema actualizado satisfactoriamente."
POEM_DELETED = "Poema eliminado satisfactoriamente."
