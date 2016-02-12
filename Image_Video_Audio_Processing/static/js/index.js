    ////////////////////////////////////////////////////////////////////////////////////////
    /**
     *Image_Video_Audio_Processing
     * index.js module
     **/
    ////////////////////////////////////////////////////////////////////////////////////////

    /* 
        Add all jquery module dependencies here.
    */

    function getCookie(name) {
        //Get Cookie name and values 
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    // Uploading Image files

    $( "#fileupload" ).click(function() {
        $('#loader').append('&nbsp;<span class="glyphicon glyphicon-refresh glyphicon-refresh-animate" id="globalloadericon"></span>');
        $('#imgupload').append("<h4>Loading Image ....</h4>");
        $('.carousel').css('display','none');
    });

    $( "#a_upload" ).click(function() {
        $('#loader_audio').append('&nbsp;<span class="glyphicon glyphicon-refresh glyphicon-refresh-animate" id="globalloadericon"></span>');
        $('#imgupload').append("<h4>Loading Audio ...</h4>");
    });
    
    $( "#v_upload" ).click(function() {
        $('#loader_video').append('&nbsp;<span class="glyphicon glyphicon-refresh glyphicon-refresh-animate" id="globalloadericon"></span>');
        $('#imgupload').append("<h4>Loading Video ...</h4>");
    });
    var csrftoken = getCookie('csrftoken');
    var url = '/core/image/basic/';
    $('#fileupload').fileupload({
        url: url,
        crossDomain: false,
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        dataType: 'json',
        done: function (e, data) {
            $('.carousel').css('display','block');
            color_table = ""
            face_count =""
            duplicate_image =""
            count_duplicate_image = ""
            count = ""
            $('#image_files').empty();
            $('#loader').empty();
            $("#imgupload").empty();
            $("#imgColors").empty();
            $("#imgtext").empty();
            $("#imgfaces").empty();
            $("#imgcor").empty();
            $.each(data.result.files, function (index, file) {
                $('<p/>').text(file.name).appendTo('#image_files');
                $("#imgupload").append("<img src="+file.url+" class='img-responsive'>");
            });

            face_count = "Face Count:" + data.result.face_count;
            $('#imgfaces').append(face_count);
            if (data.result.face_detected){
                $("#imgupload").append("<img src="+data.result.face_detected+" class='img-responsive'>");
            }

            $('<p/>').text(data.result.extract_text).appendTo('#imgtext');


            $.each(data.result.checkDuplicateImage, function (index, duplicateimage) {
                if(index==0){
                    duplicate_image += '<div class="item active">';
                }
                else{
                    duplicate_image += '<div class="item">';
                }
                duplicate_image += '<div class="col-md-12 cor-col"><a href="#"><img src="'+duplicateimage+'" class="img-responsive"></a></div>'
                duplicate_image += '</div>';
            });
            $("#imgcor").append(count_duplicate_image);
            $("#imgcor").append(duplicate_image);
            var totalItems = $('.carousel-inner .item').length;
            var currentIndex = $('.carousel-inner .active').index() + 1;
            $('#myCarousel').on('slid.bs.carousel', function() {
                $("#count").empty();
                interval: 4000
                currentIndex = $('.carousel-inner .active').index() + 1;
                $('<p/>').text(currentIndex+' of '+totalItems).appendTo('#count');
            });

            color_table = '<table id="color" class="table table-striped">';
            color_table += '<thead><tr><th>Color</th><th>Percentage analysed</th></thead>'
            color_table += '<tbody>'
            $.each(data.result.getImageColor, function (index, imagecolor) {
                color_table += '<tr><td><span class="box" style="background-color:'+ index+'"></span>'+index+'</td>'+'<td>'+imagecolor+' % </td></tr>'
            });
            color_table += '<tbody></table>'
            $('#imgColors').append(color_table);
        },
        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('#progress .progress-bar').css(
                'width',
                progress + '%'
            );
        },
        error: function (e, errors) {
            $('#image_files').empty();
            $('<b style="color: red;">').text("Invalid File Type").appendTo('#image_files');
        }
    }).prop('disabled', !$.support.fileInput)
        .parent().addClass($.support.fileInput ? undefined : 'disabled');

// Uploading Audio files
    var csrftoken = getCookie('csrftoken');
    var audio_url = 'core/audio/basic/';
    $('#a_upload').fileupload({
        url: audio_url,
        crossDomain: false,
        acceptFileTypes: /(\.|\/)(mp3)$/i,
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        dataType: 'json',
        done: function (e, data) {
            $('#audio_files').empty();
            $('#loader_audio').empty();
            $("#audioup").empty();
            $("#audtext").empty();
            $.each(data.result.files, function (index, file) {
                $('<p/>').text(file.name).appendTo('#audio_files');
                $('#audioup').append("<audio controls><source src="+file.url+" type='audio/mpeg'/></audio>");
            });
        },
        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('#audio_progress .progress-bar').css(
                'width',
                progress + '%'
            );
        },
        error: function (e, data) {
            $.each(data.result.files, function (index, file) {
                $('<p/>').text("Invalid File type").appendTo('#audio_files');
            });
        }
    }).prop('disabled', !$.support.fileInput)
        .parent().addClass($.support.fileInput ? undefined : 'disabled');

// Uploading Video files
    var csrftoken = getCookie('csrftoken');
    var video_url = 'core/video/basic/';
    $('#v_upload').fileupload({
        url: video_url,
        crossDomain: false,
        acceptFileTypes: /(\.|\/)(mp4)$/i,
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        dataType: 'json',
        done: function (e, data) {
            $("#video_files").empty();
            $('#loader_video').empty();
            $("#videoup").empty();
            $("#vidtext").empty();
            $("#vidaudio").empty();
            $("#vidlengt").empty();
            $.each(data.result.files, function (index, file) {
                $('<p/>').text(file.name).appendTo('#video_files');
                $('#videoup').append("<video width='680' height='380' controls><source src="+file.url+" type='video/mp4'/></video>");
            });
        },
        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('#video_progress .progress-bar').css(
                'width',
                progress + '%'
            );
        },
        error: function (e, data) {
            $('<p/>').text(data).appendTo('data');
        }
    }).prop('disabled', !$.support.fileInput)
        .parent().addClass($.support.fileInput ? undefined : 'disabled');


