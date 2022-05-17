$(function() {
   $('.btn').click(function(event) {
     event.preventDefault();
     var csrf_token = $('#favorite_food_form').find('input[name=csrfmiddlewaretoken]').val();
     var button = $(this).val();
     $.ajax({
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        type: 'POST',
        url: '/favorite_food/' + button,
        data: {
            'data': button
        },
        success: function(response) {
            var heart = document.getElementById(button);
            console.log(heart);
            if (response == 'true') {
                 $(heart).toggleClass('fa-heart fa-heart-o');
            } else if (response == 'false') {
                 $(heart).toggleClass('fa-heart fa-heart-o');
            }
        }
     });
   });
});

$(document).ready(function () {

});

function getCookie(cname) {
     var name = cname + "=";
     var ca = document.cookie.split(';');
     for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if(c.indexOf(name) == 0)
           return c.substring(name.length,c.length);
     }
     return "";
}