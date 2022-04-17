from flask import jsonify


class GlobalException:

    @staticmethod
    def handle(app):

        @app.errorhandler(404)
        def page_not_found(e):
            return jsonify({'message': 'route not found'}), 404

        @app.errorhandler(500)
        def server_error(e):
            return jsonify({'message': 'Internal server error'}), 500

        @app.errorhandler(503)
        def server_error(e):
            return jsonify({'message': 'Server unavailable'}), 503

        @app.errorhandler(422)
        def server_error(e):
            return jsonify({'message': 'Invalid data provided'}), 422
