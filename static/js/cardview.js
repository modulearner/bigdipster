function cardview_init() {
    var cardcontainers = $('.card_user_node_root');
    cardcontainers.each(_get_card_info);
}

function _get_card_info(i, card) {
    var card_jq = $(card);
    var node_id = card_jq.attr('nodeid');
    var api_url = '/api/v0/getusernodegraph?node_id=' + node_id;
    $.getJSON(api_url, function(data) {
        _fill_card(card_jq, data);
    });
}

function _fill_card(htmlnode, root) {
    var root_div = $("<div/>").html("Node: " + root.title);
    if (root.type == 'content_node') {
        root_div.addClass('card_content_node')
        $.getJSON('/api/v0/getcontentnode?node_id=' + root.id, function(data) {
            root_div.html('Content: ' + data.title + ': ' + data.description);
        });
    } else {
        root_div.addClass('card_user_node');
    }
    root_div.appendTo(htmlnode);
    
    for (var i=0; i<root.children.length; i++) {
        _fill_card(root_div, root.children[i]);
    }
}
