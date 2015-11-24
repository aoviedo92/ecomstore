$(document).ready(function () {
    function tooltip(elem, content) {
        $(elem).tooltipster({
            maxWidth: 300,
            contentAsHTML: true,
            theme: 'tooltipster-discount',
            arrow: false,
            content: content
        });
    }

    tooltip('.tooltip-discount', null);
    tooltip('.tooltip-tax', null);
    //todo cuando se recibe la respuesta, esta viene en este formato: $xx.xx, llevarlo a xx.xxcuc, tratar de agregarle + o - delante denotando promocion o impuesto
    $("#discount_code").keypress(function (event) {
        var code = $(this).val();
        if (event.keyCode == 13) {
            var url = "/cart/process-discount-code/";
            var data = {code: code};
            var func = function (response) {
                var css_class;
                var cart_discount = $('#cart-discount');
                var cart_tax = $('#cart-tax');
                if (response.success == "True") {
                    css_class = 'code-success'
                } else {
                    css_class = 'code-error'
                }
                $('#cart-subtotal').text(response.cart_subtotal);
                cart_discount.text(response.discount);
                cart_tax.text(response.shipping_tax);

                $('#cart-total').text(response.total);
                $("#discount_code").removeClass().addClass(css_class);
                if (response.shipping_tax == "0") {
                    cart_tax.removeClass().addClass('tax-no');
                    tooltip('.tooltip-tax', null)
                }
                else {
                    cart_tax.removeClass().addClass('tax-yes');
                    $('.tooltip-tax').tooltipster('hide');
                }

                if (response.promotions) {
                    cart_discount.removeClass().addClass('tooltip-discount discount-yes');
                    tooltip('.tooltip-discount', response.promotions)
                }
                else {
                    cart_discount.removeClass().addClass('cart');
                    $('.tooltip-discount').tooltipster('hide');
                }
            };
            ajax(url, data, func);
            event.preventDefault();
        }
    });

});