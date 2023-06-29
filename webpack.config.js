const path = require('path');
const { WebpackManifestPlugin } = require('webpack-manifest-plugin');


module.exports = {
  entry: {
    layout: "./src/js/layout.js",
    home: "./src/js/home.js",
    product: "./src/js/product.js",
    cart: "./src/js/cart.js",
    shipment: "./src/js/shipment.js",
    successful_payment: "./src/js/successful_payment.js",
    profile: "./src/js/profile.js",
    administrator: "./src/js/administrator.js",
    category_create: "./src/js/category_create.js",
    category_update: "./src/js/category_update.js",
    product_create: "./src/js/product_create.js",
    product_update: "./src/js/product_update.js",
    user_create: "./src/js/user_create.js",
    user_update: "./src/js/user_update.js",
    user_change_password: "./src/js/user_change_password.js",
    role_create: "./src/js/role_create.js",
    role_update: "./src/js/role_update.js",
    permission_create: "./src/js/permission_create.js",
    permission_update: "./src/js/permission_update.js",
    user_auth: "./src/js/user_auth.js",
    category: "./src/js/category.js"
  },
  output: {
    filename: '[name].js',
    publicPath: '/static/dist/',
    path: path.resolve(__dirname, 'app', 'static', 'dist'),
    clean: true,
    assetModuleFilename: '[name][ext]',
  },
  plugins: [
      new WebpackManifestPlugin()
  ],
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          'css-loader'
        ]
      },
      {
        test: /\.(png|jpg|jpeg|svg|gif)$/i,
        type: 'asset/resource'
      },
      {
        test: /\.(woff|woff2|ttf)$/i,
        type: 'asset/resource'
      },
    ]
  },
};
