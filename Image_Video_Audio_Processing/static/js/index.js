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
    $(document).ready(function() {
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
            $('#image_files').empty();
            $("#imgupload").empty();
            console.log(data.result.files);
            $.each(data.result.files, function (index, file) {
                $('<p/>').text(file.name).appendTo('#image_files');
                $("#imgupload").append("<img src="+file.url+" width='680' height='380'>");
            });
        },
        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('#progress .progress-bar').css(
                'width',
                progress + '%'
            );
        }
    }).prop('disabled', !$.support.fileInput)
        .parent().addClass($.support.fileInput ? undefined : 'disabled');

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
        }
    }).prop('disabled', !$.support.fileInput)
        .parent().addClass($.support.fileInput ? undefined : 'disabled');

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
        }
    }).prop('disabled', !$.support.fileInput)
        .parent().addClass($.support.fileInput ? undefined : 'disabled');