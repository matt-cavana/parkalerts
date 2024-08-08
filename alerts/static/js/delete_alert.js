// delete_alert.js
$(document).ready(function () {
    var deleteModal = $('#deleteModal');
    var confirmDeleteBtn = $('#confirmDelete');
    var alertIdInput = $('#alertId');

    $('.delete-btn').on('click', function () {
        var alertId = $(this).data('id');
        alertIdInput.val(alertId);
        deleteModal.show();
    });

    $('.close').on('click', function () {
        deleteModal.hide();
    });

    confirmDeleteBtn.on('click', function () {
        var alertId = alertIdInput.val();
        $.ajax({
            url: '/alerts/' + alertId + '/delete/',
            type: 'POST',
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                if (response.success) {
                    location.reload();
                } else {
                    alert(response.error);
                }
            },
            error: function (xhr, status, error) {
                console.error(error);
                alert('An error occurred while deleting the alert.');
            }
        });
    });

    $(window).on('click', function (event) {
        if ($(event.target).is(deleteModal)) {
            deleteModal.hide();
        }
    });
});

