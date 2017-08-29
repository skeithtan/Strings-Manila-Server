$(() => {
    $('#finalize-button').click(() => {
        $.post({
            url: '/cart/finalize/',
            beforeSend: xhr => xhr.setRequestHeader('X-CSRFToken', getCSRF()),
            data: localStorage.cart,
            success: response => {
                const body = $('body');
                body.html(response);
                body.removeAttr('class').attr('class', 'bg-dark');
            },
            error: response => console.log(response)
        })
    })
});