$(() => {
    $('.remove-waitlist-button').each((index, button) => {
        const waitlistButton = $(button);
        const tierID = $(waitlistButton).data("tier-id");

        waitlistButton.click(() => {
            $('#remove-waitlist-tier-id').val(tierID);
        })
    });

    $('#confirm-remove-waitlist').click(() => {
        const tierID = $('#remove-waitlist-tier-id').val();
        $.ajax({
            url: `/waitlist/${tierID}/`,
            method: 'DELETE',
            beforeSend: xhr => {
                xhr.setRequestHeader('X-CSRFToken', getCSRF());
            },
            success: () => {
                $(`#row-${tierID}`).remove()
            },
            error: response => {
                console.log(response);
            }
        });
    });
});