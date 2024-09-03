import json
from app.intel import intel, handlers
from flask import request, Response
from werkzeug.exceptions import HTTPException

@intel.errorhandler(Exception)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "error": {
            "code": e.code,
            "name": e.name,
            "details": e.description,
        }
    })
    response.content_type = "application/json"
    return response

# books API
@intel.route('/books', methods=['GET'])
def fetch_books():
    resp = {}
    try:
        status_code, resp = handlers.get_books()
        if status_code != 200:
            return Response(status=status_code, response=json.dumps(resp))
        return resp
    except Exception as e:
        if isinstance(e, HTTPException):
            resp = handle_exception(e)
    return resp

@intel.route('/books', methods=['POST'])
def add_new_book():
    resp = {}
    try:
        data = request.get_json()
        status_code, resp = handlers.add_new_book(data)
        return Response(status=status_code, response=json.dumps(resp))
    except Exception as e:
        if isinstance(e, HTTPException):
            resp = handle_exception(e)
    return resp

@intel.route('/books/<id>', methods=['GET'])
def get_single_book(id):
    resp = {}
    try:
        status_code, resp = handlers.get_book_by_id(id)
        return Response(status=status_code, response=json.dumps(resp))
    except Exception as e:
        if isinstance(e, HTTPException):
            resp = handle_exception(e)
    return resp

@intel.route('/books/<id>', methods=['PUT'])
def update_single_book(id):
    resp = {}
    try:
        data = request.get_json()
        status_code, resp = handlers.update_book(id, data)
        return Response(status=status_code, response=json.dumps(resp))
    except Exception as e:
        if isinstance(e, HTTPException):
            resp = handle_exception(e)
    return resp

@intel.route('/books/<id>', methods=['DELETE'])
def single_book_delete(id):
    resp = {}
    try:
        status_code, resp = handlers.delete_book_by_id(id)
        return Response(status=status_code, response=json.dumps(resp))
    except Exception as e:
        if isinstance(e, HTTPException):
            resp = handle_exception(e)
    return resp

# reviews API
@intel.route('/books/<id>/reviews', methods=['GET'])
def book_reviews(id):
    resp = {}
    try:
        status_code, resp = handlers.get_book_review(id)
        return Response(status=status_code, response=json.dumps(resp))
    except Exception as e:
        if isinstance(e, HTTPException):
            resp = handle_exception(e)
    return resp

@intel.route('/books/<id>/reviews', methods=['POST'])
def add_book_reviews(id):
    resp = {}
    try:
        data = request.get_json()
        status_code, resp = handlers.add_new_review(id, data)
        return Response(status=status_code, response=json.dumps(resp))
    except Exception as e:
        if isinstance(e, HTTPException):
            resp = handle_exception(e)
    return resp

@intel.route('/books/<id>/summary', methods=['GET'])
def get_book_summary(id):
    resp = {}
    try:
        status_code, resp = handlers.book_summary(id)
        return Response(status=status_code, response=json.dumps(resp))
    except Exception as e:
        if isinstance(e, HTTPException):
            resp = handle_exception(e)
    return resp

@intel.route('/recommendations', methods=['GET'])
def book_recommendation():
    return "Get book recommendations based on user preferences"

@intel.route('/generate-summary', methods=['GET'])
def generate_summary():
    resp = {}
    try:
        content = request.get_json()['content']
        status_code, resp = handlers.generate_summary(content)
        return Response(status=status_code, response=json.dumps(resp))
    except Exception as e:
        if isinstance(e, HTTPException):
            resp = handle_exception(e)
    return resp