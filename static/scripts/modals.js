$(() => {
    $('#sign-out-button').click(onSignOutButtonClick);
    $('#product-card-modal').on('hidden.bs.modal', () => {
        $('#product-modal-quantity-selection').val('1');
    });
});

function onSignOutButtonClick() {
    $.post({
        url: "/accounts/logout/",
        beforeSend: authorizeXHR,
        success: () => {
            location.reload();
        },
        error: response => {
            console.log(response);
        }
    })
}

function tierInCart(tier) {
    let cart = [];
    try {
        cart = JSON.parse(localStorage.cart);
    } catch (e) {
        console.log(e);
        return false;
    }

    if (!Array.isArray(cart)) {
        return false;
    }

    cart = cart.map(item => {
        return item.tier;
    });

    let tierInCart = false;

    cart.forEach(tierID => {
        if (tierID === tier) {
            tierInCart = true;
        }
    });

    return tierInCart;
}

function onProductCardClick(product, addToCart) {
    $('#product-modal-product-name').text(product.name);
    $('#product-modal-product-price').text("₱" + product.producttierSet[0].currentPrice); //TODO
    $('#product-modal-product-description').text(product.description);
    $('#product-modal-main-product-img').attr('src', product.image);

    if (product.isSingular) {
        const tier = product.producttierSet[0];
        setUpSingularProduct(tier);
    } else {
        setUpTieredProduct(product.producttierSet)
    }

    const addToCartButton = $('#product-modal-add-to-cart-button');
    addToCartButton.off('click'); //Unbind previous add to carts

    addToCartButton.click(() => {
        iziToast.success({
            title: "Success",
            message: "Product added to cart",
            position: "bottomCenter",
            timeout: 2500,
            progressBar: false,
        });
        const quantity = parseInt($('#product-modal-quantity-selection').val());
        const tierID = $('#product-modal-selected-tier').val();

        addToCart(tierID, quantity);
        $('#product-modal-in-cart-message').show();
    });
}

function showAddToCart(tier) {
    const isOutOfStock = tier.quantity === 0;

    if (isOutOfStock) {
        $('#product-modal-in-cart-message').hide();
        $('#product-modal-add-to-cart').hide();
        $('#product-modal-out-of-stock-message').show();
        return;
    } else {
        $('#product-modal-add-to-cart').show();
        $('#product-modal-out-of-stock-message').hide();
    }

    if (tierInCart(tier.id)) {
        $('#product-modal-in-cart-message').show();
    } else {
        $('#product-modal-in-cart-message').hide();
    }
}

function setUpSingularProduct(tier) {
    $('#product-modal-tiers').hide();
    $('#product-modal-selected-tier').val(tier.id);
    showAddToCart(tier);
}

function setUpTieredProduct(tiers) {
    $('#product-modal-tiers').show();
    let isFirst = true;

    function setActiveTier(tier) {
        $('#product-modal-selected-tier').val(tier.id);
        $('#product-modal-product-price').text("₱" + tier.currentPrice);

        showAddToCart(tier);
    }

    $('#product-modal-tier-choices').text(''); //Clear first

    tiers.forEach(tier => {
        const clone = $('#product-modal-tier-button-clone').clone();
        clone.removeAttr('id');
        clone.append(tier.name);
        clone.click(() => {
            setActiveTier(tier);
        });

        const radioButton = $(clone.find('input')[0]);
        radioButton.val(tier.id);

        if (isFirst) {
            isFirst = false;
            clone.addClass('active');
            radioButton.attr('checked', true);
            setActiveTier(tier);
        }

        $('#product-modal-tier-choices').append(clone);
    })
}

function authorizeXHR(xhr) {
    xhr.setRequestHeader('X-CSRFToken', getCSRF());
}
