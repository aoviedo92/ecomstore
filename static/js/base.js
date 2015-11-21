$(document).ready(function () {
    //configuracion del tooltip
    $('.tooltip').tooltipster({
        maxWidth: 250,
        contentAsHTML: true,
        theme: 'tooltipster-shadow'
    });
    //cuando se cambie el tipo de moneda enviar form
    $("#id_currency_select").change(function () {
        $("#id_currency_form").submit()
    });
    //configurar megapanel para q salga alineado con el menu y los items del menu
    $('a.group-name').hover(function () {
        var group_name = $(this).text();
        var megapanel = $('.megapanel');
        switch (group_name) {
            case "Uniformes":
//                                megapanel.css({'padding': '15px', 'padding-right': '25px'});#}
                megapanel.css({'margin-left': '300px'});
                break;
            case "Tejidos":
//                                megapanel.css({'padding': '15px', 'padding-right': '150px'});#}
                megapanel.css({'margin-left': '250px'});
                break;
            case "Bodas":
                megapanel.css({'margin-left': '180px'});
                break;
            case "Mujeres":
                megapanel.css({'margin-left': '110px'});
                break;
            case "Hombres":
                megapanel.css({'margin-left': '0px'});
                break;
        }
    })
});