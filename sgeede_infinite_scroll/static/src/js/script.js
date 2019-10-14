$(document).ready(function(){
    var grid = $('.sgeede-infinite-scroll');
    var isTable = false;
    if($('tbody', grid).length) {
        grid = $('tbody', grid);
        isTable = true;
    }

    grid.masonry({
        itemSelector: '.sgeede-infinite-scroll .sgeede-infinite-get'
    });

    grid.infinitescroll({
        // Loading Text
        loading: {
            finishedMsg: "<em>All products has been showed.</em>",
            msgText: '<em>Load next products...</em>',
            isTable: isTable
        },

        // Pagination element that will be hidden
        navSelector: '.sgeede-infinite-pagination',

        // Next page link
        nextSelector: '.sgeede-infinite-pagination a',

        // Selector of items to retrieve
        itemSelector: '.sgeede-infinite-scroll .sgeede-infinite-get',
        
        // Max Pagination
        maxPage: parseInt($(".sgeede-infinite-pagination span.max-page").text()),
    },

    // Function called once the elements are retrieved
    function(new_elts) {
        var elts = $(new_elts).css('opacity', 0);
        elts.animate({opacity: 1});
        grid.masonry('appended', elts);
    });
})