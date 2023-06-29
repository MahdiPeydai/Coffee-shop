from flask import make_response, redirect, url_for


def user_logout():
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('user_token', '', expires=0)
    return resp
