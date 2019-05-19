function update_list(base_url) {
    $.getJSON(base_url, function(result){
        cards_in = result['cards_in'];
        cards_out = result['cards_out'];
        cards_in_list = [];
        cards_out_list = [];
        console.log("cards_in");
        for (var t = 0; t < cards_in.length; t++){
            cards_in_list += "<li> +"+cards_in[t].qty+" "+cards_in[t].card+"</li>";
        }
        for (var t = 0; t < cards_out.length; t++){
            cards_out_list += "<li> -"+cards_out[t].qty+"  "+cards_out[t].card+"</li>";
        }
        $(".cards_in").html(cards_in_list);
        $(".cards_out").html(cards_out_list);
    })
}

$( document ).ready(function() {
    base_url = "{% url 'sideboard-edit-json'  object.slug %}",
    update_list(base_url);
});

$(".update_link").click(function (e) {
    var value = $(this).attr("href");
    console.log(value);
    update_list(value);
    e.preventDefault();
});
