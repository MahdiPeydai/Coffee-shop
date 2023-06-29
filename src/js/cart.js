import "../css/cart.css"

const priceElements = document.getElementsByClassName('price');
for (let i = 0; i < priceElements.length; i++) {
    const priceValue = priceElements[i].innerHTML;
    priceElements[i].innerHTML = priceValue.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}