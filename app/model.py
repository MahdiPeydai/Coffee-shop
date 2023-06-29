from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, Column, Integer, SmallInteger, String, DateTime, ForeignKey, text
from sqlalchemy.orm import relationship, backref

db = SQLAlchemy()


user_role_association = db.Table(
    'user_role',

    Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('role_id', Integer, ForeignKey('role.id', ondelete="CASCADE"), nullable=False)
)


class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(60), nullable=False)
    lastname = Column(String(60))
    email = Column(String(50), nullable=False)
    phone = Column(String(14), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    is_deleted = Column(DateTime, default=None)

    address = relationship('Address', back_populates='user')
    role = relationship('Role', secondary=user_role_association, back_populates='user')
    cart = relationship('Cart', back_populates='user')
    order = relationship('Order', back_populates='user')

    def __repr__(self):
        return f"user:{self.id} email:{self.email}"


class Address(db.Model):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    city = Column(String(60), nullable=False)
    address_line = Column(String(400), nullable=False)
    postal_code = Column(String(10), nullable=False)
    transferee = Column(String(60), nullable=False)
    phone = Column(String(14), nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    is_deleted = Column(DateTime, default=None)

    user = relationship('User', back_populates='address')
    order = relationship('Order', back_populates='address')


role_permission_association = db.Table(
    'role_permission',

    db.Column('permission_id', Integer, ForeignKey('permission.id', ondelete="CASCADE"), nullable=False),
    db.Column('role_id', Integer, ForeignKey('role.id', ondelete="CASCADE"), nullable=False)
)


class Role(db.Model):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    user = relationship('User', secondary=user_role_association, back_populates='role')
    permission = relationship('Permission', secondary=role_permission_association, back_populates='role')


class Permission(db.Model):
    __tablename__ = 'permission'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(256))
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    role = relationship('Role', secondary=role_permission_association, back_populates='permission')


class Cart(db.Model):
    __tablename__ = 'cart'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), default=None)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    user = relationship('User', back_populates='cart')
    items = relationship('CartItem', back_populates='cart')


product_category_association = db.Table(
    'product_category',

    db.Column('product_id', Integer, ForeignKey('product.id'), nullable=False),
    db.Column('category_id', Integer, ForeignKey('category.id'), nullable=False)
)


class Product(db.Model):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    discount = Column(SmallInteger, default=None)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    is_deleted = Column(DateTime, default=None)

    cart_items = relationship('CartItem', back_populates='product')
    order = relationship('OrderItem', back_populates='product')
    image = relationship('ProductImage', back_populates='product')
    category = relationship('Category', secondary=product_category_association, back_populates='product')


class CartItem(db.Model):
    __tablename__ = 'cart_item'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cart_id = Column(Integer, ForeignKey('cart.id', ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    cart = relationship('Cart', back_populates='items')
    product = relationship('Product', back_populates='cart_items')


class OrderItem(db.Model):
    __tablename__ = 'order_item'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer(), nullable=False)
    price = Column(Integer(), nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    order = relationship('Order', back_populates='item')
    product = relationship('Product', back_populates='order')


class Order(db.Model):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    total = Column(Integer, nullable=False)
    discount = Column(Integer)
    address_id = Column(Integer, ForeignKey('address.id'), nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    is_deleted = Column(DateTime, default=None)

    item = relationship('OrderItem', back_populates='order')
    user = relationship('User', back_populates='order')
    address = relationship('Address', back_populates='order')


class ProductImage(db.Model):
    __tablename__ = 'product_image'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    path = Column(String(256), nullable=False)
    display_order = Column(Integer(), nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    product = relationship('Product', back_populates='image')


class Category(db.Model):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(Integer, ForeignKey('category.id'))
    name = Column(String(50), nullable=False)
    description = Column(String(255))
    image = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    children = relationship("Category", backref=backref('parent', remote_side=[id]))

    product = relationship('Product', secondary=product_category_association, back_populates='category')











