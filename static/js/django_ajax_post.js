/**
 * Este script de javascript permite trabajar transparentemente solicitudes que requieren
 * protecci�n del token CSRF por medio de AJAX JQUERY.
 * Esto te permitir� hacer solcitudes a web Services de Django por medio de AJAX Jquery.
 * Para utilizarlo basta con integrar el archivo DjangoAjax.js en tu directorio de JS  y hacer referencia a �l en tus templates
 * que requieren del uso de AJAX por POST o alg�n otro que requiera el token CSRF.
 * Este script est� basado en la documentaci�n oficial de Django https://docs.djangoproject.com
 */

$(function () {
    //Obtenemos la informaci�n de csfrtoken que se almacena por cookies en el cliente
    var csrftoken = getCookie('csrftoken');

    //Agregamos en la configuraci�n de la funcion $.ajax de Jquery lo siguiente:
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    function sameOrigin(url) {
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

// usando jQuery
    function getCookie(name) {
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


    function csrfSafeMethod(method) {
        // estos m�todos no requieren CSRF
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));

    }
});



function ajax(url, data, func) {
    jQuery.post(
        url,
        data,
        func,
        "json"
    );
}