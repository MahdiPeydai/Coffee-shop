import '@fortawesome/fontawesome-free/js/fontawesome'
import '@fortawesome/fontawesome-free/js/solid'
import '@fortawesome/fontawesome-free/js/regular'
import '@fortawesome/fontawesome-free/js/brands'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css';
import '../css/layout.css'
import '../image/logo.png'

const $ = require('jquery');


    $(document).ready(function() {
      $("#sidebar-toggle").click(function() {
        $(".sidebar").toggleClass("d-none d-inline");
      });
    });