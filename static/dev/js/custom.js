$(document).ready(function () {
    $("#header_havigation li a").each(function () {
        var location = window.location.href;
        var link = this.href;
        if (location === link) {
            $(this).parent("li").addClass("active");
        }
    });

    $("#search").submit(function () {
        $.ajax({
            type: $("#search").attr("method"),
            url: $("#search").attr("action"),
            data: $("#search").serialize(),
            success: function (data) {
                data = JSON.parse(data);
                for (var i = 0; i < success.length; ++i) {
                    $('#result_search').append(success[i].text);
                }
            },
            error: function (data) {

            }
        });
        return false;
    });
});