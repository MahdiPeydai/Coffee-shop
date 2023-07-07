import "../css/cart.css"


function price_text() {
    const priceElements = document.getElementsByClassName('price');
    for (let i = 0; i < priceElements.length; i++) {
        const priceValue = priceElements[i].innerHTML;
        priceElements[i].innerHTML = priceValue.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }
}

$(document).ready(function() {
    function cart_check(quantity, product_id) {
        if (quantity === null) {
            $('#' + product_id).addClass('d-none');
        }
    }

    function trash_icon(quantity, product_id) {
        if (quantity === 1) {
            $('#' + product_id).find('#trash_icon').removeClass('d-none');
            $('#' + product_id).find('#sub_icon').addClass('d-none');
        } else {
            $('#' + product_id).find('#trash_icon').addClass('d-none');
            $('#' + product_id).find('#sub_icon').removeClass('d-none');
        }
    }

    for (let product in products) {
        trash_icon(products[product].quantity, product)
    }

    function updateCartQuantity(quantity, product_id) {
        $('#' + product_id).find('.item_quantity').text(quantity);
    }

    function quantity_error(message, product_id) {
        if (message === 'error') {
            console.log($('#' + product_id).find("#quantity_error"))
            $('#' + product_id).find("#quantity_error").removeClass('d-none')
        } else {
            $('#' + product_id).find("#quantity_error").addClass('d-none')
        }
    }

    function cart() {
        let cart_total_price = 0
        let cart_total_discount = 0
        let cart_total_final_price = 0
        let quantity = 0
        products.forEach(function (product) {
            cart_total_price += product.price * product.quantity
            cart_total_discount += (product.price * (product.discount/100)) * product.quantity
            cart_total_final_price += cart_total_price - cart_total_discount
            quantity += product.quantity
        });
        $('#cart_total_price').text(cart_total_price);
        $('#cart_total_discount').text(cart_total_discount);
        $('#cart_total_final_price').text(cart_total_final_price);
        $("#cart_item_counter").text(quantity)
        price_text()
    }

    cart()

    $('.cart_item_store').click(function() {
        $.ajax({
            url: cart_item_store_url,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 'product_id': $(this).data('product_id') }),
            success: function(response) {
                let quantity = response.item_quantity;
                let product_id = response.id;
                products[product_id].quantity = quantity
                cart_check(quantity, product_id);
                updateCartQuantity(quantity, product_id);
                trash_icon(quantity, product_id);
                quantity_error(response.message, product_id);
                cart();
                },
            error: function(xhr) {
                alert('Error: ' + xhr.responseText);
            }
        });
    });

    $('.cart_item_destroy').click(function() {
        $.ajax({
            url: cart_item_destroy_url,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 'product_id': $(this).data('product_id') }),
            success: function(response) {
                let quantity = response.item_quantity;
                let product_id = response.id;
                products[product_id].quantity = quantity
                if (quantity ===null) {
                    delete products[product_id]
                }
                cart_check(quantity,product_id);
                updateCartQuantity(quantity,product_id);
                trash_icon(quantity,product_id);
                cart_items_number -= 1
                quantity_error(response.message, product_id);
                cart();
                },
            error: function(xhr) {
                alert('Error: ' + xhr.responseText);
            }
        });
    });
});