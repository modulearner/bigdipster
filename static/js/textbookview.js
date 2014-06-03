var TextbookView = (function(jQuery, d3, _) {
    var module = {};

    module.init = function() {
        var bookcontainers = jQuery('.textbook_root');
        _.each(bookcontainers, module.init_book);
    }

    module.init_book = function(book) {
        var book_jq = jQuery(book);
        var node_id = book_jq.attr('nodeid');
        var api_url = '/api/v0/getusernodegraph?node_id=' + node_id;
        jQuery.getJSON(api_url, function(data) {
            var graph = jQuery("<div/>").addClass("text_graph").appendTo(book);
            var text = jQuery("<div/>").addClass("text_text").appendTo(book);
            _fill_text(text, data);
            _fill_graph(graph, data);
        });
    }

    function _flatten_graph(data, result) {
        var result = result || [];
        if (data.type == 'content_node') {
            result.push(data);
        }
        for (var i in data.children) {
            result = _flatten_graph(data.children[i], result);
        }
        return result;
    }

    function _create_graph(data) {
        var nodes = [];
        var links = [];
        for (var i in data) {
            var j = parseInt(i);
            nodes.push({
                "name" : data[i].title,
                "id" : j,
            });
            links.push({
                "source" : j,
                "target" : j+1,
            })
        }
        links.pop();
        console.log(links);
        return {nodes: nodes, links: links}
    }

    function _fill_graph(div, data) {
        var graph = _create_graph(_flatten_graph(data));
        
        var svg = d3.selectAll(div).append("svg")
            .attr("width", "100%")
            .attr("height", "100%");

        
          var node = svg.selectAll(".node")
              .data(graph.nodes)
            .enter().append("circle")
              .attr("class", "node")
              .attr("r", 25)
              .attr("cx", 100)
              .attr("cy", function(d,i) { return i*100; });

          var link = svg.selectAll(".link")
              .data(graph.links)
            .enter().append("line")
              .attr("class", "link")
              .attr("x1", 100)
              .attr("y1", function(d) { return d.source*100 + 25; })
              .attr("x2", 100)
              .attr("y2", function(d) { return d.target*100 - 25; });
        
          node.append("title")
              .text(function(d) { return d.name; });
    }

    function _fill_text(div, data, level) {
        var level = level || 1;
        jQuery("<h" + level + "/>").html(data.title).appendTo(div);

        if (data.type == 'content_node') {
            var content = jQuery("<div/>").appendTo(div);
            jQuery.getJSON('/api/v0/getcontentnode?node_id=' + data.id, function(data) {
                content.html(data.text);
            })
        }

        for (var i in data.children) {
            _fill_text(div, data.children[i], level+1);
        }
    }

    return module;
})(jQuery, d3, _)
