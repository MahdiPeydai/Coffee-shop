# Coffee-shop
Coffee Shop is an online coffee shop that you can sell your all related products to coffee.
<br>
In admin panel you can create,update and delete users. you can set roles for them and set permission for each roll. You can manage your products in it and you can set each product in different categories.
<br>
Users have cart and are able to add to or remove products from it and after that can make orders and go for payment. Users also have a dashboard that they can manage their profile and can see their orders.
# Development
- Flask framework
- Mysql database
- SQLAlchemy for handling ORM
- WTForms for handling forms
- Webpack assets bundle
# How To Run
after cloning the repo you need first to install requirements:
<br>
<br>
<code>$ pip install -r requirements.txt</code>
<br>
<br>
then create a .env file in project directory and set these configs in it:
- MYSQL_USER
- MYSQL_PASSWORD
- MYSQL_HOST
- MYSQL_DB
- SQLALCHEMY_DATABASE_URI
- SECRET_KEY
- CATEGORY_IMAGE_FOLDER
- PRODUCT_IMAGE_FOLDER
<br>
after that, to initialize migration:
<br>
* assuming you have installed MySQL already*
<br>
<br>
<code>$ flask db init</code>
<br>
<code>$ flask db migrate -m "Initial migration."</code>
<br>
<code>$ flask db upgrade</code>
<br>
<br>
then bundle the asset files:
<br>
<br>
<code>$ npm run dev</code>
<br>
<br>
it's done. Now you can run it
<br>
<br>
<code>$ flask --app app --debug run </code>
<br>
<br>

# Have Fun
