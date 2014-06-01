function cardview_init() {
    var cardcontainers = $('.card_user_node_root');
    _.each(cardcontainers, _get_card_info);
}

function _get_card_info(card) {
    var card_jq = $(card);
    var node_id = card_jq.attr('nodeid');
    var api_url = '/api/v0/getusernodegraph?node_id=' + node_id;
    $.getJSON(api_url, function(data) {
        _fill_card(card_jq, data);
    });
}

var user_node_template = _.template("<%= title %>");
var content_node_template = _.template("<span class='title'><%= title %></span><span class=description><%= description %></span>");

function _fill_card(htmlnode, root) {
    var content_div = $("<p/>").addClass("card_content");
    var root_div = $("<div/>");
    content_div.appendTo(root_div);

    if (root.type == 'content_node') {
        root_div.addClass('card_content_node')
        $.getJSON('/api/v0/getcontentnode?node_id=' + root.id, function(data) {
            content_div.html(content_node_template(data));
        });
    } else {
        content_div.html(user_node_template(root));
        root_div.addClass('card_user_node');
        root_div.addClass('cf');
    }
    root_div.appendTo(htmlnode);
    
    var fill_child = _.partial(_fill_card, root_div);
    _.each(root.children, fill_child);
}
