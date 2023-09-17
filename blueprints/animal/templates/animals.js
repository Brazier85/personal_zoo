// Basic functions
$(document).ready(function(){
    $('.show_animal_image').click(function(){
        $('.modal-content').html('<div class="modal-body"><img src="{{ image }}" class="rounded img-fluid mx-auto"></div>')
        $('#modal_details').modal('show'); 
    });
    $('.show_all_history').click(function(){
        if ($(this).html().includes("less")) {
            url = '/history/get_all/{{ animal.id }}?less=1'
            $('.show_all_history').html('<div style="text-transform: uppercase;">Show all <i class="fa-solid fa-chevron-right"></i></div>');                
        } else {
            url = '/history/get_all/{{ animal.id }}'
            $('.show_all_history').html('<div style="text-transform: uppercase;"> <i class="fa-solid fa-chevron-left"></i> Show less</div>');
        }
        $.ajax({
            url: url,
            type: 'get',
            success: function(data){
                $('.history_card').html(data);
            }
        })
    });
    $('.show_all_feedings').click(function(){
        if ($(this).html().includes("less")) {
            url = '/feeding/get_all/{{ animal.id }}?less=1'
            $('.show_all_feedings').html('<div style="text-transform: uppercase;">Show all <i class="fa-solid fa-chevron-right"></i></div>');                
        } else {
            url = '/feeding/get_all/{{ animal.id }}'
            $('.show_all_feedings').html('<div style="text-transform: uppercase;"> <i class="fa-solid fa-chevron-left"></i> Show less</div>');
        }
        $.ajax({
            url: url,
            type: 'get',
            success: function(data){
                $('.feeding_card_table').html(data);
            }
        })
    });
});
$('.animal_show_weight').on('click',function(){
    $('.modal-content').load('/animal/get_weight/{{ animal.id }}',function(){
        $('#modal_details').modal('show'); 
    });
});

// If user is authenticated
{% if current_user.is_authenticated %}
$(document).on("click",".feeding_edit",function(){
    var feed_id = $(this).data('id');
    $.ajax({
        url: '/feeding/edit/'+feed_id,
        type: 'get',
        success: function(data){ 
            $('.modal-content').html(data); 
            $('.modal-content').append(data.htmlresponse);
            $('#modal_details').modal('show');
            $('#submit').click(function (event) {
                event.preventDefault();
                $.post(url, data = $('#feeding_form').serialize(), function (data) {
                    if (data.status == 'ok') {
                        $('#Modal').modal('hide');
                        location.reload();
                    } else {
                        var obj = JSON.parse(data);
                        for (var key in obj) {
                            if (obj.hasOwnProperty(key)) {
                                var value = obj[key];
                            }
                        }
                        $('.alert').remove()
                        $('<div class="alert alert-danger" role="alert">' + value +'</div>').insertAfter('#' + key);
                        $('.form-group').addClass('has-error')
                    }
                })
            });
            $('.feeding_delete_button').click(function(){
                var feed_id = $(this).data('id');
                if (confirm("Are You Sure ?")) {
                    $.ajax({
                            url: '/feeding/delete/'+feed_id,
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
$(document).on("click",".history_edit",function(){
    var feed_id = $(this).data('id');
    $.ajax({
        url: '/history/edit/'+feed_id,
        type: 'get',
        success: function(data){ 
            $('.modal-content').html(data); 
            $('.modal-content').append(data.htmlresponse);
            $('#modal_details').modal('show');
            $('.history_delete_button').click(function(){
                var feed_id = $(this).data('id');
                if (confirm("Are You Sure ?")) {
                    $.ajax({
                            url: '/history/delete/'+feed_id,
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
$(document).on("click",".document_edit",function(){
    var feed_id = $(this).data('id');
    $.ajax({
        url: '/document/edit/'+feed_id,
        type: 'get',
        success: function(data){ 
            $('.modal-content').html(data); 
            $('.modal-content').append(data.htmlresponse);
            $('#modal_details').modal('show');
            $('.document_delete_button').click(function(){
                var feed_id = $(this).data('id');
                if (confirm("Are You Sure ?")) {
                    $.ajax({
                            url: '/document/delete/'+feed_id,
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
$('.feeding_add_button').on('click',function(){
    $('.modal-content').load('/feeding/add/{{ animal.id }}',function(){
        $('#modal_details').modal('show'); 
    });
});
$('.history_add_button').on('click',function(){
    $('.modal-content').load('/history/add/{{ animal.id }}',function(){
        $('#modal_details').modal('show');
    });
});
$('.animal_qr_button').on('click',function(){
    $('.modal-content').load('/feeding/get_qr/{{ animal.id }}',function(){
        $('#modal_details').modal('show'); 
    });
})
$('.document_add_button').on('click',function(){
    $('.modal-content').load('/document/add/animal/{{ animal.id }}',function(){
        $('#modal_details').modal('show'); 
    });
});
$('.animal_print_button').on('click',function(){
    window.open('/animal/{{ animal.id }}?print=1', '_blank'); 
});
$('.animal_edit_button').on('click',function(){
    $('.modal-content').load('/animal/edit/{{ animal.id }}',function(){
        $('#modal_details').modal('show'); 
        $('.animal_delete_button').click(function(){
                            var animal_id = $(this).data('id');
                            if (confirm("Are You Sure ?")) {
                                $.ajax({
                                        url: '/animal/delete/'+animal_id,
                                        type: 'post',
                                        data: {animal_id: {{ animal.id }}},
                                        success: function(data) {
                                            window.location.replace("/"); 
                                        }
                                    });
                            }
                        });
    });
});
{% endif %}