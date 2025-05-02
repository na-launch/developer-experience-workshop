from datetime import datetime
from flask import Blueprint, jsonify, request, abort, Response
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from flask import Flask
import base64

# OpenTelemetry setup
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

jaeger_exporter = JaegerExporter(
    agent_host_name="tempo-sample-query-frontend-observability.apps.<ocp-cluster>",
    agent_port=6831,
)

span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Flask app + instrumentation
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

main = Blueprint('main', __name__)

@main.route("/", methods=["GET"])
def index():
    return Response(f"200 OK", mimetype='text/plain')


@main.route('/api/check', methods=['POST'])
def check_json():
    span = trace.get_current_span()
    data = request.get_json()
    if not data or 'amount' not in data:
        span.set_attribute("http.status_code", 500)
        span.set_attribute("error.message", "'amount' key missing in JSON body")
        abort(500, description="'amount' key missing in JSON body")

    try:
        amt = float(data.get('amount'))
    except (ValueError, TypeError):
        span.set_attribute("http.status_code", 500)
        span.set_attribute("error.message", "Invalid amount format")
        abort(500, description="Sending ERROR 500")

    if amt == 1290 or amt == 190:
        span.set_attribute("http.status_code", 503)
        span.set_attribute("error.message", base64.b64decode("SWYgeW91IGNhbiBwcm9kdWNlIHRoaXMgbWVzc2FnZSBpbiBKYWVnZXIsIHlvdSd2ZSBmb3VuZCB0aGUgZWFzdGVyIGVnZwo=").decode("utf-8"))
        abort(503, description="Sending ERROR 503")

    if amt < 25000:
        span.set_attribute("http.status_code", 500)
        span.set_attribute("error.message", "Amount below minimum threshold")
        abort(500, description="Sending ERROR 500")

    return jsonify({"message": "SUCCESS VALID", "data": data}), 200


# Register blueprint and start app if needed
app.register_blueprint(main)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
