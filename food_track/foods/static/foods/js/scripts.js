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
        url: '/favorite_food/',
        data: {
            'data': button
        },
        success: function(response) {
            var heart = document.getElementById(button);
            if (response == 'False') {
                 $(heart).toggleClass('fa-heart fa-heart-o');
            } else {
                //pass
            }
        }
     });
   });
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