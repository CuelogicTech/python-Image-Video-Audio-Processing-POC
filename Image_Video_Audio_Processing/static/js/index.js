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

    $('#img_up').click(function() {
        //SAVE AS Operation
        data = {
        }
        $.ajax({
            url: 'get/image/results',
            data: JSON.stringify(data),
            type: 'POST',
            success: function(response) {
                console.log(response)
            },
            error: function(data) {
                console.log(data);
            }
        });
    });

    $('#video_up').click(function() {
        //SAVE AS Operation
        data = {
        }
        $.ajax({
            url: 'get/video/results',
            data: JSON.stringify(data),
            type: 'POST',
            success: function(response) {
                console.log(response)
            },
            error: function(data) {
                console.log(data);
            }
        });
    });

    $('#audio_up').click(function() {
        //SAVE AS Operation
        data = {
        }
        $.ajax({
            url: 'get/audio/results',
            data: JSON.stringify(data),
            type: 'POST',
            success: function(response) {
                console.log(response)
            },
            error: function(data) {
                console.log(data);
            }
        });
    });