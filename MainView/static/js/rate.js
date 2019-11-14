

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}




$(document).ready(function(){

    $url = $("#request_rate_one").val();

    $("#star1").click(function(){
        $productID = $("#productID").val();
        $url = $("#request_rate_one").val();
        $rate_number = 1;
     
        $.ajax({
            type: "GET",
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            url: $url,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            async: true,
            cache: false,
            data: {
                'id': $productID ,
                'n_rate': $rate_number
            },
            success: function (data) {
                console.log(data)
                console.log("success");
            },error: function(error){
                console.log(error);
            }

        });

    });
});

$(document).ready(function(){

    $url = $("#request_rate_one").val();

    $("#star2").click(function(){
        $productID = $("#productID").val();
        $url = $("#request_rate_one").val();
        $rate_number = 2;
     
        $.ajax({
            type: "GET",
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            url: $url,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            async: true,
            cache: false,
            data: {
                'id': $productID ,
                'n_rate': $rate_number
            },
            success: function (data) {
                console.log(data)
                console.log("success");
            },error: function(error){
                console.log(error);
            }

        });

    });
});

$(document).ready(function(){

    $url = $("#request_rate_one").val();

    $("#star3").click(function(){
        $productID = $("#productID").val();
        $url = $("#request_rate_one").val();
        $rate_number = 3;
     
        $.ajax({
            type: "GET",
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            url: $url,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            async: true,
            cache: false,
            data: {
                'id': $productID ,
                'n_rate': $rate_number
            },
            success: function (data) {
                console.log(data)
                console.log("success");
            },error: function(error){
                console.log(error);
            }

        });

    });
});

$(document).ready(function(){

    $url = $("#request_rate_one").val();

    $("#star4").click(function(){
        $productID = $("#productID").val();
        $url = $("#request_rate_one").val();
        $rate_number = 4;
     
        $.ajax({
            type: "GET",
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            url: $url,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            async: true,
            cache: false,
            data: {
                'id': $productID ,
                'n_rate': $rate_number
            },
            success: function (data) {
                console.log(data)
                console.log("success");
            },error: function(error){
                console.log(error);
            }
        });
    });
});


$(document).ready(function(){

    $url = $("#request_rate_one").val();

    $("#star5").click(function(){
        $productID = $("#productID").val();
        $url = $("#request_rate_one").val();
        $rate_number = 5;
     
        $.ajax({
            type: "GET",
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            url: $url,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            async: true,
            cache: false,
            data: {
                'id': $productID ,
                'n_rate': $rate_number
            },
            success: function (data) {
                console.log(data)
                console.log("success");
            },error: function(error){
                console.log(error);
            }

        });

    });
});



