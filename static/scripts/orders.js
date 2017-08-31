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

    const uploadSlipButton = $('#upload-deposit-slip-button');
    const slipInput = $('#upload-deposit-slip-input');

    slipInput.change(() => {
        const noImage = slipInput[0].files.length === 0;

        //Disable when no image is added
        uploadSlipButton.attr('disabled', noImage);
    });

    uploadSlipButton.click(() => {
        const image = slipInput[0].files[0];
        uploadImage({
            image: image,
            success: response => {
                const link = response.data.link;
                uploadPayment(link);
            },
            error: response => console.log(response),
        });
    });

    function uploadPayment(imageLink) {
        $.post({
            url: `/orders/${orderID}/submit-payment/`,
            data: {
                image: imageLink
            },
            success: () => location.reload(),
            error: response => console.log(response),
            beforeSend: authorizeXHR
        })
    }

    function uploadImage(data) {
        const form = new FormData();
        form.append('image', data.image);

        iziToast.info({
            title: 'Uploading image...',
            message: 'Do not refresh or leave this page.',
            timeout: false,
            position: 'bottomCenter'
        });

        $.post({
            url: 'https://api.imgur.com/3/image',
            async: true,
            data: form,
            contentType: false,
            processData: false,
            // We don't have to hide uploading message since we're still uploading anyway
            // Plus we'll refresh the page after, so really no need to hide it
            success: response => data.success(response),
            error: response => {
                iziToast.destroy();
                iziToast.error({
                    title: 'Error',
                    message: 'Unable to upload photo.'
                });
                data.error(response);
            },
            beforeSend: xhr => {
                xhr.setRequestHeader('Authorization', 'Client-ID 715b55f24db9cd2')
            }
        });
    }
});