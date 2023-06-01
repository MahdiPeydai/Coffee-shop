from flask import render_template, Blueprint, url_for, flash, redirect, request, make_response
from app import app, db, curs

shop = Blueprint('shop', __name__,
                 template_folder='templates',
                 static_folder='static'
                 )


@shop.route('/product')
def product():
    return render_template('product.html')


@shop.route('/card')
def card():
    return render_template('card.html')


@shop.route('/card/shipment')
def shipment():
    return render_template('shipment.html')


@shop.route('/card/payment/successful')
def successful_payment():
    return render_template('successful_payment.html')
