
function addProductVote(score) {
    var slug = jQuery("#id_slug").val();
    $("#id_rating").val(score);
    var data = {
        rating: score,
        slug: slug
    };
    var url = "/review/product/vote/";
    var func = function (response) {
        var avg_rating = response.avg_rating;
        raty('div#raty_avg', avg_rating);
        $('.comment-about-user-voted').hide({
            duration: 500,
            complete: function () {
                $(this).text(response.comment_about_user_voted).show('slow')
            }
        });
        $('.comment-about-user-voted-avg').text('El promedio se ha actualizado')
    };
    ajax(url, data, func);

}
function addProductReview() {
    var url = "/review/product/add/";
    var slug = jQuery("#id_slug").val();
    var errors = jQuery("#review_errors");
    var data = {
        content: jQuery("#id_content").val(),
        slug: slug
    };
    var func = function (response) {
        var new_review;
        var reviews = jQuery("#reviews");
        if (response.success == "True") {
            // disable the submit button to prevent duplicates
            //jQuery("#submit_review").attr('disabled', 'disabled');
            // if this is first review, get rid of "no reviews" text
            jQuery("#no_reviews").empty();
            reviews.prepend(response.html).slideDown();
            new_review = reviews.children(":first");
            new_review.addClass('new_review');
            jQuery("#review_form").slideToggle();
        }
        else {
            //errors.append(response.html);
            return false
        }
    };
    ajax(url, data, func);
}
function addWishList() {
    var errors = jQuery("#review_errors");
    var slug = jQuery("#id_slug").val();
    var url = "/wishlist/add/";
    var data = {slug: slug};
    var new_html = '<a href="/accounts/my_account/wishlist/">El producto se ha agregado a tu lista de deseos</a>';
    var func = function (response) {
        errors.empty();
        if (response.success == "True") {
            jQuery("#add_wishlist").hide('fade');
            $("#wishlist").append(new_html).slideDown();
        }
        else {
            errors.append("Ya tienes este producto en tu lista de deseos");
        }
    };
    ajax(url, data, func);
}
function removeWishList() {
    var errors = jQuery("#review_errors");
    var slug = jQuery("#id_slug").val();
    var url = "/wishlist/remove/";
    var data = {slug: slug};
    var new_html = '<a href="/accounts/my_account/wishlist/">El producto ha sido eliminado de tu lista de deseos</a>';
    var func = function (response) {
        errors.empty();
        if (response.success == "True") {
            jQuery("#remove_wishlist").hide('fade');
            $("#wishlist").append(new_html).slideDown();
        }
        else {
            errors.append("No existe este producto");
        }
    };
    ajax(url, data, func);
}
function slideToggleReviewForm() {
    jQuery("#review_form").slideToggle();
    jQuery("#add_review").slideToggle();
}
function addTag() {
    var data = {
        tag: jQuery("#id_tag").val(),
        slug: jQuery("#id_slug").val()
    };
    var url = "/tag/product/add/";
    var tags_div = jQuery("#tags");
    var func = function (response) {
        if (response.success == "True") {
            tags_div.empty();
            tags_div.append(response.html);
            jQuery("#id_tag").val("");
        }
    };
    ajax(url, data, func);
}
function prepareDocument() {
    jQuery("#submit_review").click(addProductReview);
    jQuery("#add_wishlist").click(addWishList);
    jQuery("#remove_wishlist").click(removeWishList);
    jQuery("#review_form").addClass('hidden');
    jQuery("#add_review").click(slideToggleReviewForm).addClass('visible');
    //jQuery("#add_review").addClass('visible');
    jQuery("#cancel_review").click(slideToggleReviewForm);
    jQuery("#add_tag").click(addTag);
    jQuery("#id_tag").keypress(function (event) {
        if (event.keyCode == 13 && jQuery("#id_tag").val().length > 2) {
            addTag();
            event.preventDefault();
        }
    });
}

function statusBox() {
    jQuery('<div id="loading">Loading...</div>')
        .prependTo("#add_review")
        .ajaxStart(function () {
            jQuery(this).show();
        })
        .ajaxStop(function () {
            jQuery(this).hide();
        })
}
jQuery(document).ready(prepareDocument);