import '@fortawesome/fontawesome-free/js/fontawesome'
import '@fortawesome/fontawesome-free/js/solid'
import '@fortawesome/fontawesome-free/js/regular'
import '@fortawesome/fontawesome-free/js/brands'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css';
import '../css/layout.css'

const $ = require('jquery');


function price_text() {
    const priceElements = document.getElementsByClassName('price');
    for (let i = 0; i < priceElements.length; i++) {
        const priceValue = priceElements[i].innerHTML;
        priceElements[i].innerHTML = priceValue.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }
}

$(document).ready(function() {
    price_text()
})