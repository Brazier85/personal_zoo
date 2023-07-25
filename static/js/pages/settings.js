$(document).on("click",".ft_edit",function(){
    var feed_id = $(this).data('id');
    $.ajax({
        url: '/settings/ft_edit/'+feed_id,
        type: 'get',
        success: function(data){ 
            $('.modal-content').html(data); 
            $('.modal-content').append(data.htmlresponse);
            $('#modal_details').modal('show');
            $('.ft_delete_button').click(function(){
                var feed_id = $(this).data('id');
                if (confirm("Are You Sure ?")) {
                    $.ajax({
                            url: '/settings/ft_delete/'+feed_id,
                            type: 'post',
                            data: {},
                            success: function(data) {
                                location.reload(true); 
                            }
                        });
                }
            });
        }
    });
});
$(document).on("click",".ht_edit",function(){
    var feed_id = $(this).data('id');
    $.ajax({
        url: '/settings/ht_edit/'+feed_id,
        type: 'get',
        success: function(data){ 
            $('.modal-content').html(data); 
            $('.modal-content').append(data.htmlresponse);
            $('#modal_details').modal('show');
            $('.ht_delete_button').click(function(){
                var feed_id = $(this).data('id');
                if (confirm("Are You Sure ?")) {
                    $.ajax({
                            url: '/settings/ht_delete/'+feed_id,
                            type: 'post',
                            data: {},
                            success: function(data) {
                                location.reload(true); 
                            }
                        });
                }
            });
        }
    });
});
$(document).on("click",".htt_edit",function(){
    var feed_id = $(this).data('id');
    $.ajax({
        url: '/settings/htt_edit/'+feed_id,
        type: 'get',
        success: function(data){ 
            $('.modal-content').html(data); 
            $('.modal-content').append(data.htmlresponse);
            $('#modal_details').modal('show');
            $('.htt_delete_button').click(function(){
                var feed_id = $(this).data('id');
                if (confirm("Are You Sure ?")) {
                    $.ajax({
                            url: '/settings/htt_delete/'+feed_id,
                            type: 'post',
                            data: {},
                            success: function(data) {
                                location.reload(true); 
                            }
                        });
                }
            });
        }
    });
});
$(document).on("click",".at_edit",function(){
    var feed_id = $(this).data('id');
    $.ajax({
        url: '/settings/at_edit/'+feed_id,
        type: 'get',
        success: function(data){ 
            $('.modal-content').html(data); 
            $('.modal-content').append(data.htmlresponse);
            $('#modal_details').modal('show');
            $('.at_delete_button').click(function(){
                var feed_id = $(this).data('id');
                if (confirm("Are You Sure ?")) {
                    $.ajax({
                            url: '/settings/at_delete/'+feed_id,
                            type: 'post',
                            data: {},
                            success: function(data) {
                                location.reload(true); 
                            }
                        });
                }
            });
        }
    });
});
$(document).on("click",".tt_edit",function(){
    var feed_id = $(this).data('id');
    $.ajax({
        url: '/settings/tt_edit/'+feed_id,
        type: 'get',
        success: function(data){ 
            $('.modal-content').html(data); 
            $('.modal-content').append(data.htmlresponse);
            $('#modal_details').modal('show');
            $('.tr_delete_button').click(function(){
                var feed_id = $(this).data('id');
                if (confirm("Are You Sure ?")) {
                    $.ajax({
                            url: '/settings/tt_delete/'+feed_id,
                            type: 'post',
                            data: {},
                            success: function(data) {
                                location.reload(true); 
                            }
                        });
                }
            });
        }
    });
});
$('.ft_add_button').on('click',function(){
    $('.modal-content').load('/settings/ft_add',function(){
        $('#modal_details').modal('show'); 
    });
});
$('.ht_add_button').on('click',function(){
    $('.modal-content').load('/settings/ht_add',function(){
        $('#modal_details').modal('show'); 
    });
});
$('.htt_add_button').on('click',function(){
    $('.modal-content').load('/settings/htt_add',function(){
        $('#modal_details').modal('show'); 
    });
});
$('.at_add_button').on('click',function(){
    $('.modal-content').load('/settings/at_add',function(){
        $('#modal_details').modal('show'); 
    });
});
$('.tt_add_button').on('click',function(){
    $('.modal-content').load('/settings/tt_add',function(){
        $('#modal_details').modal('show'); 
    });
});