$(function() {
    // Submit post on submit
    $('#post-form').on('submit', function(event){
        event.preventDefault();
        create_post();
    });

    // AJAX for posting
    function create_post() {
        $.ajax({
            url : "/summary/create_post/", // the endpoint
            type : "POST", // http method
            data : { 
                text_title : $('#text-title').val(),
                text : $('#text-to-submit').val() 
            }, // data sent with the post request
            // handle a successful response
            success : function(json) 
            {
                // remove the value from the inputs
                $('#text-to-submit').val('');
                $('#text-title').val('');

                // update the results div
                var paragraphs = json.summary.split('/r/n');
                var summary_elements = '<b>Text Summary</b><br />';
                for (var i = 0; i < paragraphs.length; i++)
                {
                    summary_elements += '<p>' + paragraphs[i] + '</p><br />';
                }
                $('#results').html(summary_elements);
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) 
            {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };


    // This function gets cookie with a given name
    function getCookie(name) 
    {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) 
    {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) 
    {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});