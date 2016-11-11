$(function ($) {
    "use strict";

    // Find all pagination controls.
    $(".pagination").each(function (i, el) {
        var pagination = $(el);
        pagination.find(".pagination-prev > a").click(function () {
            $(this).parent().siblings(".active").prevUntil(".pagination-prev").first().find("a").trigger("click");
        });
        pagination.find(".pagination-next > a").click(function () {
            $(this).parent().siblings(".active").nextUntil(".pagination-next").first().find("a").trigger("click");
        });

        return true;
    });
});
