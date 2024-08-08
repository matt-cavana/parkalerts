// Check if jQuery is loaded
if (typeof jQuery !== 'undefined') {
    console.log('jQuery is loaded');
} else {
    console.log('jQuery is not loaded');
}

$(document).ready(function () {
    console.log('Document is ready');

    const bothButton = $('#bothButton');
    const mapButton = $('#mapButton');
    const listButton = $('#listButton');

    if (bothButton.length) {
        bothButton.on('click', function () {
            window.location.href = bothButton.data('url');
        });
    }

    if (mapButton.length) {
        mapButton.on('click', function () {
            window.location.href = mapButton.data('url');
        });
    }

    if (listButton.length) {
        listButton.on('click', function () {
            window.location.href = listButton.data('url');
        });
    }

    const currentPage = window.location.pathname;
    if (currentPage.includes('/map/')) {
        if (mapButton.length) mapButton.addClass('active');
    } else if (currentPage.includes('/list/')) {
        if (listButton.length) listButton.addClass('active');
    } else {
        if (bothButton.length) bothButton.addClass('active');
    }

    // Search box functionality
    $('#searchBox').on('input', function () {
        var searchTerm = $(this).val().toLowerCase();

        console.log('Search Term:', searchTerm); // Debug log for search term

        // Check if tbody tr elements exist
        var rows = $('tbody tr');
        if (rows.length > 0) {
            console.log('Rows found:', rows.length); // Debug log for number of rows
        } else {
            console.log('No rows found'); // Debug log if no rows found
        }

        // Filter table rows
        rows.each(function () {
            var title = $(this).find('td:nth-child(2)').text().toLowerCase();
            var details = $(this).find('td:nth-child(3)').text().toLowerCase();
            var startDate = $(this).find('td:nth-child(4)').text().toLowerCase();
            var endDate = $(this).find('td:nth-child(5)').text().toLowerCase();
            var published = $(this).find('td:nth-child(6)').text().toLowerCase();

            console.log('Row Data:', title, details, startDate, endDate, published); // Debug log for row data

            if (title.includes(searchTerm) || details.includes(searchTerm) || startDate.includes(searchTerm) || endDate.includes(searchTerm) || published.includes(searchTerm)) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

    // Add CSRF token to the form
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
            }
        }
    });

    $('.unpublish-button').click(function () {
        var alertId = $(this).data('id');
        $.ajax({
            url: '{% url "unpublish_alert" %}',
            method: 'POST',
            data: {
                'id': alertId,
                'csrfmiddlewaretoken': '{{ csrf_token }}'
            },
            success: function (response) {
                if (response.success) {
                    location.reload();
                } else {
                    alert('Failed to unpublish the alert.');
                }
            }
        });
    });
});
