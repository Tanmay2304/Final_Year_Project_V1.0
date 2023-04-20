dropdownItems.forEach(function (item) {
    item.addEventListener("click", function (event) {
        console.log('in table');
        var selectedMallId = $(this).data('mall-id');
        fetch_slot(selectedMallId);
        fetch_floor(selectedMallId);
    });
});

function fetch_slot(mallId) {

    console.log(mallId);
    // Send AJAX request to the server to get the slot values
    $.ajax({
        url: "/get_slots",
        type: "POST",
        data: { mall_id: mallId },

        success: function (response) {
            var data = response;
            $("#available-slots").text(data.available_slots);
            $("#occupied-slots").text(data.occupied_slots);
            $("#total-slots").text(data.total_slots);
            // Update the series data of the chart object with new occupancy value
            chart.updateSeries([data.occupied_slots * 100 / data.total_slots]);
        },

        error: function (jqXHR, textStatus, errorThrown) {
            console.log(textStatus, errorThrown);
        }
    });
}

function fetch_floor(mallId) {
    $.ajax({
        url: '/get-data/' + mallId,
        type: 'GET',
        success: function (data) {
            $('#data-table tbody').empty();
            $.each(data, function (index, item) {
                var row = $('<tr>').appendTo('#data-table tbody');
                $('<td>').text(item.floor).appendTo(row);
                $('<td>').text(item.available).appendTo(row);
                $('<td>').text(item.occupied).appendTo(row);
                $('<td>').text(item.total).appendTo(row);
            });
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log('Error: ' + textStatus + ' ' + errorThrown);
        }
    });
}
