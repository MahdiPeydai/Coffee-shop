from app import app, db, model
from sqlalchemy import and_

from flask import request, redirect, render_template, url_for, flash

from app.forms import Category
from wtforms.validators import DataRequired

from app.middlewares.auth.login import user_login_require
from app.middlewares.auth.permissions import permission_require

import os
import uuid


@user_login_require
@permission_require(['category.index'])
def admin_category():
    category_alias = model.Category.__table__.alias('A')

    categories = db.session.query(category_alias.c.id, category_alias.c.name, category_alias.c.description,
                                  category_alias.c.image, model.Category.name.label('parent_name')) \
        .select_from(category_alias) \
        .join(model.Category, model.Category.id == category_alias.c.parent_id, isouter=True) \
        .order_by(category_alias.c.id)
    db.session.close()

    data = []

    for id, name, description, image, parent in categories:
        category = {
            'id': id,
            'name': name,
            'description': description,
            'image': image,
            'parent': parent
        }
        data.append(category)
    return render_template('panel/category/admin_category.html', data=data)


@user_login_require
@permission_require(['category.store'])
def category_store():
    form = Category()
    form.category_image.validators.append(DataRequired())

    categories = db.session.query(model.Category.id, model.Category.name)
    db.session.close()

    choices = [(0, 'بدون دسته بندی مادر')]

    for id, name in categories:
        choices.append((id, name))

    form.category_parent.choices = choices
    return render_template('panel/category/category_create.html', form=form, tinymce_key=app.config['TINYMCE_API_KEY'])


@user_login_require
@permission_require(['category.store'])
def category_create():
    form = Category()

    categories = db.session.query(model.Category.id, model.Category.name)
    db.session.close()

    choices = [(0, 'بدون دسته بندی مادر')]

    for id, name in categories:
        choices.append((id, name))

    form.category_parent.choices = choices
    if request.method == 'POST' and form.validate:
        category_check = db.session.query(model.Category.name) \
            .filter(model.Category.name == request.form['category_name']).first()

        if category_check:
            flash('دسته بندی با نام وارد شده قبلا ایجاد شده است', 'error')
            return redirect(url_for('category_store'))

        category_image = request.files['category_image']
        category_image_name = category_image.filename
        file_format = category_image_name[category_image_name.index('.'):]
        category_image_name = f'{str(uuid.uuid4())}{file_format}'
        category_image.save(os.path.join(app.config['CATEGORY_IMAGE_FOLDER'], category_image_name))

        if int(request.form['category_parent']) == 0:
            category_parent = None
        else:
            category_parent = int(request.form['category_parent'])

        new_category = model.Category(
            name=request.form['category_name'],
            description=request.form['category_description'],
            image=category_image_name,
            parent_id=category_parent
        )
        db.session.add(new_category)
        db.session.commit()

        flash('دسته بندی با موفقیت ایجاد شد', 'message')
        return redirect(url_for('admin_category'))


@user_login_require
@permission_require(['category.edit'])
def category_edit(category_id):
    category_model_alias = model.Category.__table__.alias('A')

    category = db.session.query(category_model_alias.c.name, category_model_alias.c.description,
                                category_model_alias.c.image, model.Category.id.label('parent_id')) \
        .select_from(category_model_alias) \
        .join(model.Category, model.Category.id == category_model_alias.c.parent_id, isouter=True) \
        .filter(category_model_alias.c.id == category_id) \
        .order_by(category_model_alias.c.id).first()
    db.session.close()

    placeholders = {
        'category_name': category[0],
        'category_description': category[1],
        'category_parent': str(category[3])
    }
    form = Category(data=placeholders)

    categories = db.session.query(model.Category.id, model.Category.name).filter(model.Category.id != category_id)
    db.session.close()

    choices = [(0, 'بدون دسته بندی مادر')]

    for id, name in categories:
        choices.append((id, name))

    form.category_parent.choices = choices

    return render_template('panel/category/category_edit.html', form=form, category_id=category_id,
                           tinymce_key=app.config['TINYMCE_API_KEY'])


@user_login_require
@permission_require(['category.edit'])
def category_update(category_id):
    form = Category()

    categories = db.session.query(model.Category.id, model.Category.name)
    db.session.close()

    choices = [(0, 'بدون دسته بندی مادر')]

    for id, name in categories:
        choices.append((id, name))

    form.category_parent.choices = choices
    print(form.errors)
    if form.validate:
        if request.form.get('_method') == 'PUT':
            category_check = db.session.query(model.Category.name).filter(
                and_(model.Category.name == request.form['category_name'],
                     model.Category.id != category_id)).first()
            if category_check:
                flash('دسته بندی با نام وارد شده وجود دارد ...', 'error')
                return redirect(url_for('category_edit', category_id=category_id))

            if int(request.form['category_parent']) == 0:
                category_parent = None
            else:
                category_parent = int(request.form['category_parent'])

            category = db.session.query(model.Category).get(category_id)
            category.name = request.form['category_name']
            category.description = request.form['category_description']
            category.parent_id = category_parent

            if request.files['category_image']:
                old_image = db.session.query(model.Category.image).filter(model.Category.id == category_id).first()

                os.remove(os.path.join(app.config['CATEGORY_IMAGE_FOLDER'], old_image[0]))

                category_image = request.files['category_image']
                category_image_name = category_image.filename
                file_format = category_image_name[category_image_name.index('.'):]
                category_image_name = f'{str(uuid.uuid4())}{file_format}'
                category_image.save(os.path.join(app.config['CATEGORY_IMAGE_FOLDER'], category_image_name))
                category.image = category_image_name
            db.session.commit()
            flash('نغییرات با موفقیت انجام شد', 'message')
            return redirect(url_for('category_edit', category_id=category_id))


@user_login_require
@permission_require(['category.destroy'])
def category_delete(category_id):
    parent = db.session.query(model.Category.parent_id).filter_by(id=category_id).first()
    if parent[0]:
        update_parent_query = model.product_category_association.update().filter_by(category_id=category_id) \
            .values(category_id=parent[0])
        db.session.execute(update_parent_query)
        db.session.commit()

        activity_image = db.session.query(model.Category.image).filter_by(id=category_id).first()
        print(activity_image)
        os.remove(os.path.join(app.config['CATEGORY_IMAGE_FOLDER'], activity_image[0]))

        db.session.query(model.Category).filter_by(id=category_id).delete()
        db.session.commit()
        flash('دسته بندی با موفقیت حذف شد', 'message')
        return redirect(url_for('admin_category'))
    else:
        flash('چون دسته‌بندی مادر هست امکان حذف وجود ندارد، ویرایش کنید', 'error')
        return redirect(url_for('category_edit', category_id=category_id))
