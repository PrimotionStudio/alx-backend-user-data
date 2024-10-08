#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ GET /api/v1/stats
    Return:
      - the number of each objects
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized/', strict_slashes=False)
def unauthorized():
    """
    This endpoint must raise a 401 error by using abort
    Return:
    - 401 Unauthorized
    """
    abort(401, description="Unauthorized Access")


@app_views.route('/forbidden/', strict_slashes=False)
def forbidden():
    """
    This endpoint must raise a 403 error by using abort
    Return:
    - 401 Forbidden
    """
    abort(403, description="Forbidden Access")
