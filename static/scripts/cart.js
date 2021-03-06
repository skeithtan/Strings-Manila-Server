$(() => {
    const emptyState = $('#empty-state');
    const cartTable = $('#cart-table');
    const loadingIndicator = $('#loading-indicator');
    const rowClone = $('#row-clone');
    rowClone.remove();
    cartTable.hide();
    emptyState.hide();

    let itemPrice = [];

    $.post({
        url: window.location.href,
        data: localStorage.cart,
        beforeSend: authorizeXHR,
        success: response => {
            loadingIndicator.hide();

            if (response.length === 0) {
                emptyState.show();
                return;
            }

            cartTable.show();
            response.forEach(populateTable);
        },
        error: response => {
            $('#loading-indicator').hide();
            console.log(response);
        }
    });

    function populateTable(item) {
        const tierID = item.id.toString();
        itemPrice[tierID] = item.price;

        const row = rowClone.clone();

        $(row.find('img')[0]).attr('src', item.image);
        $(row.find('.product-name')[0]).text(item.name);
        $(row.find('.product-price')[0]).text("₱" + item.price);

        if (item.isSingular) {
            $(row.find('.product-tier')[0]).html("<small>N/A</small>");
        } else {
            $(row.find('.product-tier')[0]).text(item.tierName);
        }

        const select = $(row.find('.custom-select')[0]);
        const removeButton = $(row.find('.remove-button')[0]);

        select.val(item.quantity);

        select.change(() => {
            const cart = JSON.parse(localStorage.cart);
            const newQuantity = parseInt(select.val());
            cart.forEach((item, index) => {
                if (item.tier === tierID) {
                    cart[index].quantity = newQuantity;
                }
            });

            localStorage.cart = JSON.stringify(cart);
            calculateTotal();
        });

        removeButton.click(() => {
            let cart = JSON.parse(localStorage.cart);
            cart = cart.filter(item => {
                return item.tier !== tierID;
            });

            localStorage.cart = JSON.stringify(cart);
            row.remove();

            if (cart.length === 0) {
                cartTable.hide();
                emptyState.show();
            } else {
                calculateTotal();
            }
        });

        $('#cart-items').prepend(row);
        calculateTotal();
    }

    $('#proceed-to-checkout-button').click(() => {
        $.post({
            url: '/cart/review/',
            beforeSend: authorizeXHR,
            data: localStorage.cart,
            success: response => {
                $('body').html(response);
                $('#finalize-button').click(() => {
                    $.post({
                        url: '/cart/finalize/',
                        beforeSend: authorizeXHR,
                        data: localStorage.cart,
                        success: response => $('body').html(response),
                        error: response => console.log(response),
                    });
                });
            },
            error: response => console.log(response),
        });
    });


    function calculateTotal() {
        const cart = JSON.parse(localStorage.cart);
        let total = 0;
        cart.forEach(item => {
            const quantity = item.quantity;
            const tier = item.tier;
            const tierPrice = itemPrice[tier];

            total += quantity * tierPrice;
        });

        $('#total-price').text("₱" + total);
    }

    function authorizeXHR(xhr) {
        xhr.setRequestHeader('X-CSRFToken', getCSRF());
    }
})
;