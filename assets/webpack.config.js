const path = require('path');
const { WebpackManifestPlugin } = require('webpack-manifest-plugin');


module.exports = {
  entry: {
    layout: "./src/js/layout.js",
    home: "./src/js/home.js",
    product: "./src/js/product.js",
    card: "./src/js/card.js",
    shipment: "./src/js/shipment.js",
    successful_payment: "./src/js/successful_payment.js",
    profile: "./src/js/profile.js",
    administrator: "./src/js/administrator.js",
    category_update: "./src/js/category_update.js"
  },
  output: {
    filename: '[name].js',
    publicPath: '/static/dist/',
    path: path.resolve(__dirname, '..','app', 'static', 'dist'),
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
