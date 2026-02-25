from flask_restx import Resource
from flask import current_app

class BaseResource(Resource):

    def handle_not_found(self, entity, entity_id):
        current_app.logger.warning(f"{entity} with id {entity_id} not found")
        return {"error": f"{entity} with id {entity_id} not found"}, 404

    def handle_conflict(self, message):
        current_app.logger.warning(f"Conflict: {message}")
        return {"error": message}, 409

    def handle_server_error(self, e):
        current_app.logger.error(f"Server error: {str(e)}")
        return {"error": "An unexpected error occurred"}, 500