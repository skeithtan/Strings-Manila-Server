function productIsInCart(product) {
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

    const tiers = product.producttierSet.map(tier => {
        return tier.id
    });

    cart = cart.map(item => {
        return item.tier;
    });

    let productIsInCart = false;

    cart.forEach(tierID => {
        tiers.forEach(tier => {
            if (tierID === tier) {
                productIsInCart = true;
            }
        });
    });

    return productIsInCart;
}

function onProductCardClick(product, addToCart) {
    $('#product-modal-product-name').html(product.name);
    $('#product-modal-product-price').html("₱" + product.producttierSet[0].currentPrice); //TODO
    $('#product-modal-product-description').html(product.description);
    $('#product-modal-main-product-img').attr('src', product.image);

    if (productIsInCart(product)) {
        $('#product-modal-in-cart-message').show();
    } else {
        $('#product-modal-in-cart-message').hide();
    }

    if (product.isSingular) {
        $('#product-modal-tiers').hide();
        $('#product-modal-selected-tier').val(product.producttierSet[0].id);
    } else {
        setUpTieredProduct(product.producttierSet)
    }

    const addToCartButton = $('#product-modal-add-to-cart');
    addToCartButton.off('click'); //Unbind previous add to carts

    addToCartButton.click(() => {
        const quantity = parseInt($('#product-modal-quantity-selection').val());
        const tierID = $('#product-modal-selected-tier').val();

        addToCart(tierID, quantity);
        $('#product-modal-in-cart-message').show();
    });
}

function setUpTieredProduct(tiers) {
    $('#product-modal-tiers').show();
    let isFirst = true;

    function setActiveTier(tier) {
        $('#product-modal-selected-tier').val(tier.id);
        $('#product-modal-product-price').html("₱" + tier.currentPrice);
    }

    $('#product-modal-tier-choices').html(''); //Clear first

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


