from flask import Blueprint

from app.controller.panel.panel import *
from app.controller.panel.information.information import *
from app.controller.panel.role.role import *
from app.controller.panel.permission.permission import *
from app.controller.panel.category.category import *
from app.controller.panel.product.product import *
from app.controller.panel.auth.login import *

from app.controller.auth.user_login import *
from app.controller.auth.user_logout import *
from app.controller.auth.user_signup import *

from app.controller.home.home import *

from app.controller.profile.profile import *
from app.controller.profile.information.information import *
from app.controller.profile.address.address import *
from app.controller.profile.order.order import *
from app.controller.profile.password_change.password_change import *

from app.controller.category.category import *

from app.controller.product.product import *

from app.controller.order.cart.cart import *

routes = Blueprint('routes', __name__,
                   template_folder='templates',
                   static_folder='static'
                   )


# panel
app.add_url_rule('/panel/admin', 'panel', panel)

# auth

# login
app.add_url_rule('/panel/admin/auth/user/login', 'admin_login', admin_login, methods=['POST', 'GET'])
#

# logout
app.add_url_rule('/panel/admin/auth/user/logout', 'admin_logout', admin_logout)
#

# user

# information
app.add_url_rule('/panel/admin/user', 'admin_user', admin_information)

# create
app.add_url_rule('/panel/admin/user/create', 'admin_user_create', admin_user_create)
app.add_url_rule('/panel/admin/user/store', 'admin_user_store', admin_user_store, methods=['POST'])
#

# update
app.add_url_rule('/panel/admin/user/<int:user_id>/edit', 'admin_user_edit', admin_user_edit)
app.add_url_rule('/panel/admin/user/<int:user_id>/update', 'admin_user_update', admin_user_update, methods=['POST'])

app.add_url_rule('/panel/admin/user/<int:user_id>/password/edit', 'admin_user_password_edit', admin_user_password_edit)
app.add_url_rule('/panel/admin/user/<int:user_id>/password/update', 'admin_user_password_update', admin_user_password_update,
                 methods=['POST'])
#

# delete
app.add_url_rule('/panel/admin/user/<int:user_id>/delete', 'admin_user_delete', admin_user_delete)
#

#

# role
app.add_url_rule('/panel/admin/role', 'admin_role', admin_role)

# create
app.add_url_rule('/panel/admin/role/create', 'role_create', role_create)
app.add_url_rule('/panel/admin/role/store', 'role_store', role_store, methods=['POST'])
#

# update
app.add_url_rule('/panel/admin/role/<int:role_id>/edit', 'role_edit', role_edit)
app.add_url_rule('/panel/admin/role/<int:role_id>/update', 'role_update', role_update, methods=['POST'])
#

# delete
app.add_url_rule('/panel/admin/role/<int:role_id>/delete', 'role_delete', role_delete)
#

#

# permission
app.add_url_rule('/panel/admin/permission', 'admin_permission', admin_permission)

# create
app.add_url_rule('/panel/admin/permission/create', 'permission_create', permission_create)
app.add_url_rule('/panel/admin/permission/store', 'permission_store', permission_store, methods=['POST'])
#

# update
app.add_url_rule('/panel/admin/permission/<int:permission_id>/edit', 'permission_edit', permission_edit)
app.add_url_rule('/panel/admin/permission/<int:permission_id>/update', 'permission_update', permission_update,
                 methods=['POST'])
#

# delete
app.add_url_rule('/panel/admin/permission/<int:permission_id>/delete', 'permission_delete', permission_delete)
#

#

#

# category
app.add_url_rule('/panel/admin/category', 'admin_category', admin_category)

# create
app.add_url_rule('/panel/admin/category/create', 'category_create', category_create)
app.add_url_rule('/panel/admin/category/store', 'category_store', category_store, methods=['POST'])
#

# update
app.add_url_rule('/panel/admin/category/<int:category_id>/edit', 'category_edit', category_edit)
app.add_url_rule('/panel/admin/category/<int:category_id>/update', 'category_update', category_update,
                 methods=['POST'])
#

# delete
app.add_url_rule('/panel/admin/category/<int:category_id>/delete', 'category_delete', category_delete)
#

#

# product
app.add_url_rule('/panel/admin/product', 'admin_product', admin_product)

# create
app.add_url_rule('/panel/admin/product/create', 'product_create', product_create)
app.add_url_rule('/panel/admin/product/store', 'product_store', product_store, methods=['POST'])
#

# update
app.add_url_rule('/panel/admin/product/<int:product_id>/edit', 'product_edit', product_edit)
app.add_url_rule('/panel/admin/product/<int:product_id>/update', 'product_update', product_update, methods=['POST'])
#

# delete
app.add_url_rule('/panel/admin/product/<int:product_id>/delete', 'product_delete', product_delete)
#

#

# auth

# login
app.add_url_rule('/auth/user/login', 'user_login', user_login, methods=['POST', 'GET'])
#

# signup
app.add_url_rule('/auth/user/signup', 'user_register', user_register, methods=['POST', 'GET'])
#

# logout
app.add_url_rule('/auth/user/logout', 'user_logout', user_logout)
#

#

# home
app.add_url_rule('/', 'home', home)
#

# profile
app.add_url_rule('/profile', 'user_profile', profile)

# information
app.add_url_rule('/profile/information', 'user_information', user_information)

# update
app.add_url_rule('/profile/information/edit', 'user_information_edit', user_information_edit)
app.add_url_rule('/profile/information/update', 'user_information_update', user_information_update, methods=['POST'])
#

#

# password change
app.add_url_rule('/profile/password/edit', 'user_password_edit', user_password_edit)
app.add_url_rule('/profile/password/update', 'user_password_update', user_password_update, methods=['POST'])
#

# delete
app.add_url_rule('/profile/delete', 'user_delete', user_delete)
#

#

# address
app.add_url_rule('/profile/address', 'user_address', user_address)

# create
app.add_url_rule('/profile/address/create', 'user_address_create', user_address_create)
app.add_url_rule('/profile/address/store', 'user_address_store', user_address_store, methods=['POST'])
#

# update
app.add_url_rule('/profile/address/<int:address_id>/edit', 'user_address_edit', user_address_edit)
app.add_url_rule('/profile/address/<int:address_id>/update', 'user_address_update', user_address_update, methods=['POST'])
#

# delete
app.add_url_rule('/profile/address/<int:address_id>/delete', 'user_address_delete', user_address_delete)
#

#

# orders
app.add_url_rule('/profile/order', 'user_order', user_order)
#

#

# category
app.add_url_rule('/category', 'category_all', category_all)
app.add_url_rule('/category/<int:category_id>', 'category', category)

#

# product
app.add_url_rule('/product/<int:product_id>', 'product', product)

#

# order

# cart
app.add_url_rule('/order/cart', 'cart', cart)

# add item
app.add_url_rule('/order/cart/product/<int:product_id>/store', 'cart_item_store', cart_item_store)
#

# delete item
app.add_url_rule('/order/cart/product/<int:product_id>/delete', 'cart_item_delete', cart_item_delete)
#
