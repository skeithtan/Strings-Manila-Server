$(() => {
    const orderID = $('#order-id').val();

    $('#confirm-cancel-order-button').click(() => {
        $.post({
            url: `/api/orders/${orderID}/cancel/`,
            beforeSend: authorizeXHR,
            success: () => location.reload(),
            error: response => console.log(response)
        })
    });
});