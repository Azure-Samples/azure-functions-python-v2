import azure.functions as func
from emails import email_app
import utils

app = func.FunctionApp()

app.register_blueprint(email_app)

@app.route(route="aifred")
def main(req: func.HttpRequest) -> func.HttpResponse:
    req_body = req.get_json()
    if req_body:
        question = req_body.get('question')
        if question:
            answer = utils.get_response(question)
            return func.HttpResponse(answer)
        else:
            return func.HttpResponse(
                "Please pass a question in the request body",
                status_code=400
            )
    else:
        return func.HttpResponse(
            "Please pass a question in the request body",
            status_code=200
        )