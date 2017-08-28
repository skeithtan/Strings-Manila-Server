$(() => {
    const emptyState = $('#empty-state');
    const cartTable = $('#cart-table');
    const loadingIndicator = $('#loading-indicator');
    const rowClone = $('#row-clone');
    rowClone.remove();
    cartTable.hide();
    emptyState.hide();

    let totalPrice = 0;
    let itemPrice = [];

    $.post({
        url: window.location.href,
        data: localStorage.cart,
        beforeSend: xhr => {
            xhr.setRequestHeader('X-CSRFToken', csrf);
        },
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
        $(row.find('.product-name')[0]).html(item.name);
        $(row.find('.product-price')[0]).html("₱" + item.price);
        $(row.find('.product-tier')[0]).html(item.isSingular ? "<small>N/A</small>" : item.tierName);

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

    function calculateTotal() {
        const cart = JSON.parse(localStorage.cart);
        let total = 0;
        cart.forEach(item => {
            const quantity = item.quantity;
            const tier = item.tier;
            const tierPrice = itemPrice[tier];

            total += quantity * tierPrice;
        });

        $('#total-price').html("₱" + total);

    }
});