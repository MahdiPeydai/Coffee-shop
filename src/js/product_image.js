$(document).ready(function() {
    $('.order_upgrade').click(function() {
        $.ajax({
            url: order_upgrade_url,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 'product_id': product_id, 'order': $(this).data('order') }),
            success: function(response) {
            },
            error: function(xhr) {
                alert('Error: ' + xhr.responseText);
            }
        });
    });

    $('.order_downgrade').click(function() {
        $.ajax({
            url: order_downgrade_url,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 'product_id': product_id, 'order': $(this).data('order') }),
            success: function(response) {
                },
            error: function(xhr) {
                alert('Error: ' + xhr.responseText);
            }
        });
    });
})