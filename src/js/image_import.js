function importAll(r) {
  return r.keys().map(r);
}

importAll(require.context('./../image/logo', false, /\.(png|jpg|jpeg|gif|svg)$/));
importAll(require.context('./../image/slideshow', false, /\.(png|jpg|jpeg|gif|svg)$/));
importAll(require.context('./../image/banner', false, /\.(png|jpg|jpeg|svg)$/));
importAll(require.context('./../image/category', false, /\.(png|jpg|jpeg|svg)$/));
importAll(require.context('./../image/product', false, /\.(png|jpg|jpeg|svg)$/));