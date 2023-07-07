import '../css/product.css'

const priceElements = document.getElementsByClassName('price');
for (let i = 0; i < priceElements.length; i++) {
    const priceValue = priceElements[i].innerHTML;
    priceElements[i].innerHTML = priceValue.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

$(document).ready(function() {
    function cart_check(quantity) {
        if (quantity != null) {
            $('#in_cart').removeClass('d-none');
            $('#not_in_cart').addClass('d-none');
        } else {
            $('#in_cart').addClass('d-none');
            $('#not_in_cart').removeClass('d-none');
        }
    }
    cart_check(item_quantity)

    function trash_icon(quantity) {
        if (quantity === 1) {
            $('#trash_icon').removeClass('d-none');
            $('#sub_icon').addClass('d-none');
        } else {
            $('#trash_icon').addClass('d-none');
            $('#sub_icon').removeClass('d-none');
        }
    }

    trash_icon(item_quantity)

    function updateCartQuantity(quantity) {
        if (quantity != null){
            $('#item_quantity').text(quantity);
        }
    }

    function quantity_error(message) {
        if (message === 'error') {
            $("#quantity_error").removeClass('d-none')
        } else {
            $("#quantity_error").addClass('d-none')
        }
    }

    function cart_item_counter(quantity) {
        $("#cart_item_counter").text(quantity + other_items)
    }

    // $('#cart').on('click', '#cart_item_store',)
    $('#cart').on('click', '#cart_item_store', function() {
        $.ajax({
            url: cart_item_store_url,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 'product_id': product_id }),
            success: function(response) {
                cart_check(response.item_quantity);
                updateCartQuantity(response.item_quantity);
                trash_icon(response.item_quantity);
                cart_item_counter(response.item_quantity)
                quantity_error(response.message);
                },
            error: function(xhr) {
                alert('Error: ' + xhr.responseText);
            }
        });
    }).on('click', '#cart_item_destroy', function() {
        $.ajax({
            url: cart_item_destroy_url,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 'product_id': product_id }),
            success: function(response) {
                cart_check(response.item_quantity)
                updateCartQuantity(response.item_quantity);
                trash_icon(response.item_quantity);
                cart_item_counter(response.item_quantity)
                quantity_error(response.message)
                },
            error: function(xhr) {
                alert('Error: ' + xhr.responseText);
            }
        });
    });

});