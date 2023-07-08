const path = require('path');
const { WebpackManifestPlugin } = require('webpack-manifest-plugin');


module.exports = {
  entry: {
    layout: "./src/js/layout.js",
    image_import: "./src/js/image_import",
    home: "./src/js/home.js",
    product: "./src/js/product.js",
    cart: "./src/js/cart.js",
    successful_payment: "./src/js/successful_payment.js",
    profile: "./src/js/profile.js",
    panel: "./src/js/panel.js",
    auth: "./src/js/auth.js",
    product_image: "./src/js/product_image.js"
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
          test: require.resolve("jquery"),
          loader: "expose-loader",
          options: {
            exposes: ["$", "jQuery"],
          },
        }
      ]
    },
};
