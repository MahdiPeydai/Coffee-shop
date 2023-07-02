import flask
from flask import render_template, request, flash, redirect, url_for

from app import app, db, model
from sqlalchemy import and_, func

from app.middlewares.auth.login import user_login_require

from app.forms import Address


@user_login_require
def user_address(user_id):
    addresses = db.session.query(model.Address.id, model.Address.address_line,
                                 model.Address.postal_code, model.Address.transferee, model.Address.phone) \
        .join(model.User, model.Address.user_id == model.User.id) \
        .filter(and_(model.User.id == user_id,
                     model.Address.is_deleted == None)).all()
    user_address = []
    for address in addresses:
        user_address.append(
            {
                'id': address[0],
                'address_line': address[1],
                'postal_code': address[2],
                'transferee': address[3],
                'phone': address[4]
            }
        )
    return render_template('web/profile/address/address.html', user_address=user_address, user_id=user_id)


@user_login_require
def user_address_create(user_id):
    form = Address()
    flask.session["referrer_url"] = request.referrer
    return render_template('web/profile/address/address_create.html', form=form, user_id=user_id,
                           tinymce_key=app.config['TINYMCE_API_KEY'])


@user_login_require
def user_address_store(user_id):
    form = Address()
    if form.validate:
        new_address = model.Address(
            user_id=user_id,
            city=request.form['city'],
            address_line=request.form['address_line'],
            postal_code=request.form['postal_code'],
            phone=request.form['phone'],
            transferee=request.form['transferee']
        )
        db.session.add(new_address)
        db.session.commit()

        flash('ادرس با موفقیت ثبت شد ...', 'message')
        referrer_url = flask.session['referrer_url']
        del flask.session['referrer_url']
        return redirect(referrer_url)


@user_login_require
def user_address_edit(user_id, address_id):
    address = db.session.query(model.Address.city, model.Address.address_line, model.Address.postal_code,
                               model.Address.transferee, model.Address.phone).filter_by(id=address_id).first()
    placeholders = {
        'city': address[0],
        'address_line': address[1],
        'postal_code': address[2],
        'transferee': address[3],
        'phone': address[4]
    }
    form = Address(data=placeholders)
    return render_template('web/profile/address/address_edit.html', form=form, address_id=address_id,
                           tinymce_key=app.config['TINYMCE_API_KEY'])


@user_login_require
def user_address_update(user_id, address_id):
    form = Address()
    if form.validate:
        if request.form.get('_method') == 'PUT':
            address = db.session.query(model.Address).get(address_id)
            address.city = request.form['city']
            address.address_line = request.form['address_line']
            address.postal_code = request.form['postal_code']
            address.transferee = request.form['transferee']
            address.phone = request.form['phone']
            db.session.commit()
            flash('تغییرات با موفقیت ذخیره شد ...', 'message')
            return redirect(url_for('user_address_edit', address_id=address_id))


@user_login_require
def user_address_delete(user_id, address_id):
    address = db.session.query(model.Address).get(address_id)
    address.is_deleted = func.current_timestamp()
    db.session.commit()

    flash('ادرس با موفقیت حذف شد...', 'message')
    return redirect(url_for('user_address'))
