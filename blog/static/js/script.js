$(function () {
    function render_time() {
        return moment($(this).data('timestamp')).format('lll')
    }
    $('[data-toggle="tooltip"]').tooltip(
        {title: render_time}
    );
    var sidebar = $(".sidebar");
    $("#J_open_cate").on('click',function (e) {
        e.stopPropagation();
        sidebar.toggleClass("show");
    });
    $("body").on('click', function (e) {
        if(sidebar.hasClass('show')){
            sidebar.removeClass("show");
        }
    })
});
