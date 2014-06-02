var CardView = (function(jQuery, _) {
    var module = {};

    var user_node_template = _.template("<span class='user_title cf'><%= title %></span>");
    var content_node_template = _.template("<span class='title'><%= title %></span><span class=description><%= description %></span><span class=standards>(<%= standards.join(', ') %>)</span>");

    module.init = function() {
        var cardcontainers = jQuery('.card_user_node_root');
        _.each(cardcontainers, module.init_card);
    }

    module.collapse = function(event) {
        event.stopPropagation();
        var block = jQuery(this);
        block.toggleClass("card_hide");
    }
    
    module.init_card = function(card) {
        var card_jq = jQuery(card);
        var node_id = card_jq.attr('nodeid');
        var api_url = '/api/v0/getusernodegraph?node_id=' + node_id;
        jQuery.getJSON(api_url, function(data) {
            var root = jQuery("<ol/>").addClass('card_user_node');
            root.appendTo(card_jq);
            _fill_card(root, data);
        }).fail(function() {
            card_jq.html("<p class='card_error'>Could not find content</p>");
        });
    }
    
    function _fill_card(htmlnode, root) {
        var content_div = jQuery("<li/>").addClass("card_content");
        content_div.appendTo(htmlnode);
    
        if (root.type == 'content_node') {
            root.description = "";
            root.standards = [];
            htmlnode.addClass("cf");
            content_div.html(content_node_template(root)).addClass("card_content_node");
            jQuery.getJSON('/api/v0/getcontentnode?node_id=' + root.id, function(data) {
                content_div.html(content_node_template(data));
            })
        } else {
            content_div.html(user_node_template(root));
            content_div.click(module.collapse);

            var root_div = jQuery("<ol/>").addClass('card_user_node');
            root_div.appendTo(content_div);

            var fill_child = _.partial(_fill_card, root_div);
            _.each(root.children, fill_child);
        }
    }

    return module;
})(jQuery, _)
