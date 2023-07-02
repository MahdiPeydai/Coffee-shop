import '@fortawesome/fontawesome-free/js/fontawesome'
import '@fortawesome/fontawesome-free/js/solid'
import '@fortawesome/fontawesome-free/js/regular'
import '@fortawesome/fontawesome-free/js/brands'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css';
import '../css/administrator.css'

function importAll(r) {
  r.keys().forEach(r);
}

importAll(require.context('../image/category_image/', true, /\.(png|jpg|jpeg|svg|gif)$/));