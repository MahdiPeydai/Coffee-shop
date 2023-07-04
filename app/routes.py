from flask import Blueprint

from app.controller.panel.panel import *
from app.controller.panel.information.information import *
from app.controller.panel.role.role import *
from app.controller.panel.permission.permission import *
from app.controller.panel.category.category import *
from app.controller.panel.product.product import *

from app.controller.auth.user_login import *
from app.controller.auth.user_logout import *
from app.controller.auth.user_signup import *

from app.controller.web.home.home import *

from app.controller.web.profile.profile import *
from app.controller.web.profile.information.information import *
from app.controller.web.profile.address.address import *
from app.controller.web.profile.order.order import *
from app.controller.web.profile.password_change.password_change import *

from app.controller.web.category.category import *

from app.controller.web.product.product import *

from app.controller.web.checkout.cart.cart import *

routes = Blueprint('routes', __name__,
                   template_folder='templates',
                   static_folder='static'
                   )

# auth

# login
app.add_url_rule('/auth/login', 'user_login', user_login, methods=['POST', 'GET'])
#

# signup
app.add_url_rule('/auth/signup', 'user_register', user_register, methods=['POST', 'GET'])
#

# logout
app.add_url_rule('/auth/logout', 'user_logout', user_logout)
#

#

# panel
app.add_url_rule('/panel', 'panel', panel)

# user

# information
app.add_url_rule('/panel/user', 'admin_user', admin_information)

# create
app.add_url_rule('/panel/user/store', 'admin_user_store', admin_user_store)
app.add_url_rule('/panel/user/create', 'admin_user_create', admin_user_create, methods=['POST'])
#

# update
app.add_url_rule('/panel/user/<int:id>/edit', 'admin_user_edit', admin_user_edit)
app.add_url_rule('/panel/user/<int:id>/update', 'admin_user_update', admin_user_update, methods=['POST', 'PUT'])

app.add_url_rule('/panel/user/<int:id>/password/edit', 'admin_user_password_edit', admin_user_password_edit)
app.add_url_rule('/panel/user/<int:id>/password/update', 'admin_user_password_update', admin_user_password_update,
                 methods=['POST'])
#

# delete
app.add_url_rule('/panel/user/<int:id>/destroy', 'admin_user_delete', admin_user_delete)
#

#

# role
app.add_url_rule('/panel/role', 'admin_role', admin_role)

# create
app.add_url_rule('/panel/role/store', 'role_store', role_store)
app.add_url_rule('/panel/role/create', 'role_create', role_create, methods=['POST'])
#

# update
app.add_url_rule('/panel/role/<int:role_id>/edit', 'role_edit', role_edit)
app.add_url_rule('/panel/role/<int:role_id>/update', 'role_update', role_update, methods=['POST'])
#

# delete
app.add_url_rule('/panel/role/<int:role_id>/destroy', 'role_delete', role_delete)
#

#

# permission
app.add_url_rule('/panel/permission', 'admin_permission', admin_permission)

# create
app.add_url_rule('/panel/permission/store', 'permission_store', permission_store)
app.add_url_rule('/panel/permission/create', 'permission_create', permission_create, methods=['POST'])
#

# update
app.add_url_rule('/panel/permission/<int:permission_id>/edit', 'permission_edit', permission_edit)
app.add_url_rule('/panel/permission/<int:permission_id>/update', 'permission_update', permission_update,
                 methods=['POST'])
#

# delete
app.add_url_rule('/panel/permission/<int:permission_id>/destroy', 'permission_delete', permission_delete)
#

#

#

# category
app.add_url_rule('/panel/category', 'admin_category', admin_category)

# create
app.add_url_rule('/panel/category/store', 'category_store', category_store)
app.add_url_rule('/panel/category/create', 'category_create', category_create, methods=['POST'])
#

# update
app.add_url_rule('/panel/category/<int:category_id>/edit', 'category_edit', category_edit)
app.add_url_rule('/panel/category/<int:category_id>/update', 'category_update', category_update,
                 methods=['POST'])
#

# delete
app.add_url_rule('/panel/category/<int:category_id>/destroy', 'category_delete', category_delete)
#

#

# product
app.add_url_rule('/panel/product', 'admin_product', admin_product)

# create
app.add_url_rule('/panel/product/store', 'product_store', product_store)
app.add_url_rule('/panel/product/create', 'product_create', product_create, methods=['POST'])
#

# update
app.add_url_rule('/panel/product/<int:product_id>/edit', 'product_edit', product_edit)
app.add_url_rule('/panel/product/<int:product_id>/update', 'product_update', product_update, methods=['POST'])
#

# delete
app.add_url_rule('/panel/product/<int:product_id>/destroy', 'product_delete', product_delete)
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
app.add_url_rule('/profile/destroy', 'user_delete', user_delete)
#

#

# address
app.add_url_rule('/profile/addresses', 'user_address', user_address)

# create
app.add_url_rule('/profile/addresses/create', 'user_address_create', user_address_create)
app.add_url_rule('/profile/addresses/store', 'user_address_store', user_address_store, methods=['POST'])
#

# update
app.add_url_rule('/profile/addresses/<int:address_id>/edit', 'user_address_edit', user_address_edit)
app.add_url_rule('/profile/addresses/<int:address_id>/update', 'user_address_update', user_address_update, methods=['POST'])
#

# delete
app.add_url_rule('/profile/addresses/<int:address_id>/destroy', 'user_address_delete', user_address_delete)
#

#

# orders
app.add_url_rule('/profile/orders', 'user_order', user_order)
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
app.add_url_rule('/checkout/cart', 'cart', cart)

# add item
app.add_url_rule('/checkout/cart/product/<int:product_id>/store', 'cart_item_store', cart_item_store)
#

# delete item
app.add_url_rule('/checkout/cart/product/<int:product_id>/destroy', 'cart_item_destroy', cart_item_destroy)
#
