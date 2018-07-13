$(document).ready(function(){
    var grid = $('.sgeede-infinite-scroll tbody');

    grid.masonry({
        itemSelector: '.sgeede-infinite-scroll tbody tr.sgeede-infinite-get'
    });

    grid.infinitescroll({
        // Loading Text
        loading: {
            finishedMsg: "<em>All products has been showed.</em>",
            msgText: '<em>Load next products...</em>',
        },

        // Pagination element that will be hidden
        navSelector: '.sgeede-infinite-pagination',

        // Next page link
        nextSelector: '.sgeede-infinite-pagination td a',

        // Selector of items to retrieve
        itemSelector: '.sgeede-infinite-scroll tbody tr.sgeede-infinite-get',
        
        // Max Pagination
        maxPage: parseInt($(".sgeede-infinite-pagination span.max-page").text()),
    },

    // Function called once the elements are retrieved
    function(new_elts) {
        var elts = $(new_elts).css('opacity', 0);
        elts.animate({opacity: 1});
        $(grid).masonry('appended', elts);
    });
})