try:
    from .Spotify import Spotify
except ImportError:
    from Spotify import Spotify

try:
    # Added 'request' to extract the incoming POST payload
    from flask import Flask, jsonify, request
except ImportError:
    print("Flask is not installed, please install it with 'pip install flask'")


class WebAPI(Spotify):
    """
    Creates a flask app with each endpoint being a class name, 
    returns the output from the function as the response to the POST request.
    """
    def __init__(self, app: Flask, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self._registerEndpoints()

    def _registerEndpoints(self):
        for attrName in dir(self):                          #< Look through all attributes
            if attrName.startswith('_'):                    #< Ignore private methods
                continue

            attr = getattr(self, attrName)

            if callable(attr):  
                routePath = f"/{attrName}"
                self.app.add_url_rule(
                    routePath,
                    endpoint=f"{attrName}",
                    view_func=self._createView(attr),
                    methods=['POST']                        #< Restricts endpoint to POST requests only
                )
                print(f"Registered POST route: {routePath}")

    def _createView(self, func):
        def viewWrapper(*args, **kwargs):
            """ Automatically extract list payload and return JSON """
            try:
                reqData = request.get_json(silent=True)
                argsList = reqData if isinstance(reqData, list) else []    #< if nothing is passed, assume no args

                responseData = func(*argsList)
                print(str(responseData)[:1000])

                return jsonify(responseData)
            except TypeError as te:
                print(f"Argument mismatch: {str(te)}")
                return jsonify({"error": f"Argument mismatch: {str(te)}"}), 400
            except Exception as e:
                print(f"error: {e}")
                return jsonify({"error": str(e)}), 500

        return viewWrapper

def runWebAPI():
    app = Flask(__name__)
    controller = WebAPI(app)
    app.run(debug=True, threaded=False, use_reloader=False)

if __name__ == "__main__":
    runWebAPI()
    # app.run(debug=True, threaded=False)