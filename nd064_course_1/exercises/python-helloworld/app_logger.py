from flask import Flask
import logging  #import logging library


app = Flask(__name__)
logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format=f'%(asctime)s %(module)s : %(message)s'
    )

@app.route("/")
def hello():
    app.logger.debug("/ endpoint was reached!")  #logs a message
    return "Hello World!"

@app.route("/status")  #adds a route /status to the flask application
def status():  #defines a function that is called when the app route is /status
    app.logger.debug("/status endpoint was reached!")  #logs a message
    healthz = {"result": "OK - healthy"}
    return healthz, 200  #returns the variable along with status code 200


@app.route("/metrics")  #adds a route /metrics to the flask application
def metrics():  #defines a function that is called when the app route is /metrics
    app.logger.debug("/metrics endpoint was reached!")  #logs a message
    metrics = {"UserCount": 140, "UserCountActive": 23}
    return metrics, 200  #returns the variable along with status code 200

if __name__ == "__main__":
    app.run(host='0.0.0.0')
