pageSize = 2
showPage = function(page) {
    $(".post").hide();
    $(".post").each(function(n) {
        if (n >= pageSize * (page - 1) && n < pageSize * page)
            $(this).show();
    });
}

showPage(1);

$("#page-item li a").click(function() {
    $("#page-item li a").removeClass("current");
    $(this).addClass("current");
    showPage(parseInt($(this).text()))
});
