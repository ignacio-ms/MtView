$(document).ready(function () {
    $('#pae-div').on('plotly_selected', function (eventData) {
        $.ajax({
            url: '/pae',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                // Get data
            }),
            success: function (data) {

            }
        });
    })
})