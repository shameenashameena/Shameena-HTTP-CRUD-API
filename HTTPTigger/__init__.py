import logging
import azure.functions as func
import json
from cosmos_client import CosmosClientWrapper

client = CosmosClientWrapper()

def _bad_request(message="Bad Request"):
    return func.HttpResponse(json.dumps({"error": message}), status_code=400, mimetype="application/json")

def _not_found():
    return func.HttpResponse(status_code=404)

def _no_content():
    return func.HttpResponse(status_code=204)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing Products API request")
    method = req.method
    id = req.route_params.get('Id')

    try:
        if method == "POST":
            try:
                body = req.get_json()
            except Exception:
                return _bad_request("Invalid JSON")
            if not body.get("id") or "price" not in body:
                return _bad_request("id and price are required")
            item = client.create_item(body)
            return func.HttpResponse(json.dumps(item), status_code=201, mimetype="application/json")

        if method == "GET":
            if id:
                item = client.read_item(id)
                if not item:
                    return _not_found()
                return func.HttpResponse(json.dumps(item), status_code=200, mimetype="application/json")
            items = client.read_items()
            return func.HttpResponse(json.dumps(items), status_code=200, mimetype="application/json")

        if method == "PUT":
            if not id:
                return _bad_request("id path parameter required")
            try:
                body = req.get_json()
            except Exception:
                return _bad_request("Invalid JSON")
            updated = client.update_item(id, body)
            if not updated:
                return _not_found()
            return func.HttpResponse(json.dumps(updated), status_code=200, mimetype="application/json")

        if method == "DELETE":
            if not id:
                return _bad_request("id path parameter required")
            deleted = client.delete_item(id)
            if not deleted:
                return _not_found()
            return _no_content()

        return _bad_request("Unsupported method")
    except Exception as e:
        logging.exception(e)
        return func.HttpResponse(json.dumps({"error": "server error"}), status_code=500, mimetype="application/json")
