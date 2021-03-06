var CardView = (function(jQuery, _) {
    var module = {};

    var user_node_template = _.template("<span class='user_title'><%= title %></span>");
    var content_node_template = _.template("<span class='title'><%= title %></span><span class=description><%= description %></span>");

    module.init = function() {
        var cardcontainers = jQuery('.card_user_node_root');
        _.each(cardcontainers, module.init_card);
    }

    module.collapse = function() {
        var block = jQuery(this).parent();
        block.toggleClass("card_hide");
    }
    
    module.init_card = function(card) {
        var card_jq = jQuery(card);
        var node_id = card_jq.attr('nodeid');
        var api_url = '/api/v0/usernodegraph?node_id=' + node_id;
        jQuery.getJSON(api_url, function(data) {
            _fill_card(card_jq, data);
        }).fail(function() {
            card_jq.html("<p class='card_error'>Could not find content</p>");
        });
    }
    
    function _fill_card(htmlnode, root) {
        var content_div = jQuery("<p/>").addClass("card_content");
        var root_div = jQuery("<div/>");
        content_div.appendTo(root_div);
    
        if (root.type == 'content_node') {
            root_div.addClass('card_content_node')
            root.description = "";
            content_div.html(content_node_template(root));
            jQuery.getJSON('/api/v0/contentnode?node_id=' + root.id, function(data) {
                content_div.html(content_node_template(data));
            })
        } else {
            content_div.html(user_node_template(root));
            content_div.click(module.collapse);
            root_div.addClass('card_user_node');
            root_div.addClass('cf');
        }
        root_div.appendTo(htmlnode);
        
        var fill_child = _.partial(_fill_card, root_div);
        _.each(root.children, fill_child);
    }

    return module;
})(jQuery, _)
