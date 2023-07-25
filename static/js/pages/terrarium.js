$(document).on("click",".show_animal",function(){
    var animal_id = $(this).data('id');
    window.location.assign("/animal/"+animal_id); 
});

$('#animals').dataTable({
"responsive": true,
"paging": false,
"order": [[0, 'asc']],
"stateSave": true
});

$(document).ready(function(){
    $('.show_terrarium_image').click(function(){
        $('.modal-content').html('<div class="modal-body"><img src="{{ image }}" class="rounded img-fluid mx-auto"></div>')
        $('#modal_details').modal('show'); 
    });
    $('.show_all_history').click(function(){
        if ($(this).html().includes("less")) {
            url = `/terrarium/history/get_all/${terrarium_id}?less=1`
            $('.show_all_history').html('<div style="text-transform: uppercase;">Show all <i class="bi bi-chevron-right"></i></div>');                
        } else {
            url = `/terrarium/history/get_all/${terrarium_id}`
            $('.show_all_history').html('<div style="text-transform: uppercase;"> <i class="bi bi-chevron-left"></i> Show less</div>');
        }
        $.ajax({
            url: url,
            type: 'get',
            success: function(data){
                $('.history_card').html(data);
            }
        })
    });
});
$('.terrarium_edit_button').on('click',function(){
$('.modal-content').load(`/terrarium/edit/${terrarium_id}`,function(){
    $('#modal_details').modal('show'); 
    $('.terrarium_delete_button').click(function(){
                        if (confirm("Are You Sure ?")) {
                            $.ajax({
                                    url: '/terrarium/delete/'+terrarium_id,
                                    type: 'post',
                                    data: {terrarium_id: terrarium.id},
                                    success: function(data) {
                                        window.location.replace("/"); 
                                    }
                                });
                        }
                    });
});
});

$('.terrarium_feeding_button').on('click',function(){
    window.location.assign(`/feeding/multi?terrarium=${terrarium_id}`);
});

$('.terrarium_history_button').on('click',function(){
    window.location.assign(`/history/multi?terrarium=${terrarium_id}`);
});

$(document).on("click",".equipment_edit",function(){
var feed_id = $(this).data('id');
$.ajax({
    url: '/terrarium/equipment/edit/'+feed_id,
    type: 'get',
    success: function(data){ 
        $('.modal-content').html(data); 
        $('.modal-content').append(data.htmlresponse);
        $('#modal_details').modal('show');
        $('.equipment_delete_button').click(function(){
            var feed_id = $(this).data('id');
            if (confirm("Are You Sure ?")) {
                $.ajax({
                        url: '/terrarium/equipment/delete/'+feed_id,
                        type: 'post',
                        data: {terrarium_id: terrarium_id},
                        success: function(data) {
                            location.reload(true); 
                        }
                    });
            }
        });
    }
});
});

$(document).on("click",".lamp_edit",function(){
var feed_id = $(this).data('id');
$.ajax({
    url: '/terrarium/lamp/edit/'+feed_id,
    type: 'get',
    success: function(data){ 
        $('.modal-content').html(data); 
        $('.modal-content').append(data.htmlresponse);
        $('#modal_details').modal('show');
        $('.lamp_delete_button').click(function(){
            var feed_id = $(this).data('id');
            if (confirm("Are You Sure ?")) {
                $.ajax({
                        url: '/terrarium/lamp/delete/'+feed_id,
                        type: 'post',
                        data: {terrarium_id: terrarium.id},
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
    url: '/terrarium/history/edit/'+feed_id,
    type: 'get',
    success: function(data){ 
        $('.modal-content').html(data); 
        $('.modal-content').append(data.htmlresponse);
        $('#modal_details').modal('show');
        $('.history_delete_button').click(function(){
            var feed_id = $(this).data('id');
            if (confirm("Are You Sure ?")) {
                $.ajax({
                        url: '/terrarium/history/delete/'+feed_id,
                        type: 'post',
                        data: {animal_id: terrarium.id},
                        success: function(data) {
                            location.reload(true); 
                        }
                    });
            }
        });
    }
});
});

$('.equipment_add_button').on('click',function(){
$('.modal-content').load(`/terrarium/equipment/add/${terrarium_id}`,function(){
    $('#modal_details').modal('show'); 
});
});

$('.lamp_add_button').on('click',function(){
$('.modal-content').load(`/terrarium/lamp/add/${terrarium_id}`,function(){
    $('#modal_details').modal('show'); 
});
});

$('.history_add_button').on('click',function(){
$('.modal-content').load(`/terrarium/history/add/${terrarium_id}`,function(){
    $('#modal_details').modal('show');
});
});