from flask import request, jsonify


def search():
    return "555"


def get_song():
    s = request.args.get('name')
    a = request.args.get('artist')
    return jsonify({'name': s, 'artist': a})
