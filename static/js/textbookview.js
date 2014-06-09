var TextbookView = (function(jQuery, d3, markdown, _) {
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
                "title" : data[i].title,
                "uid" : _uid(data[i]),
                "id" : j,
                "y" : j/(data.length-1),
            });
            links.push({
                "source" : j,
                "target" : j+1,
            })
        }
        links.pop();
        return {nodes: nodes, links: links}
    }

    function _uid(d,i) {
        return "section_" + d.title.replace(/[^a-zA-Z]/g, '') + i;
    }

    function _fill_graph(div, data) {
        var graph = _create_graph(_flatten_graph(data));
        
        var width = 200, 
            height=$(window).height();

        var svg = d3.selectAll(div).append("svg")
            .attr("width", "100%")
            .attr("height", "100%");

        var node = svg.selectAll(".node")
            .data(graph.nodes)
          .enter().append("circle")
            .attr("class", "node")//function(d,i) { return "node " + _uid(d,i); })
            .attr("r", 25)
            .attr("cx", width/2)
            .attr("cy", function(d,i) { return height * d.y; });

        jQuery(document).scroll(function(event) { _magnify_graph(div, event) });

        // TODO: figure out a good way of doing links... do i need force directed
        // in order to get the `d.source.x` properties?
        //var link = svg.selectAll(".link")
        //    .data(graph.links)
        //  .enter().append("line")
        //    .attr("class", "link")
        //    .attr("x1", 100)
        //    .attr("y1", function(d) { return d.source*100 + 25; })
        //    .attr("x2", 100)
        //    .attr("y2", function(d) { return d.target*100 - 25; });
        
        node.append("title")
            .text(function(d) { return d.title; });
    }

    function _magnify_graph(div, event) {
        var scrollTop = $(window).scrollTop() + 25,
            windowHeight = $(window).height() - 50,
            docHeight = $(document).height() - 50;
        
        var elements = d3.selectAll(div).selectAll(".node");
        var numElements = elements[0].length;

        elements
            .attr("r", function(d,i) { 
                var uid = _uid(d, i);
                var element = $("." + uid);
                var etop = element.offset().top;
                var ebottom = element.height() + etop;

                var factor;
                if (ebottom < scrollTop + 5*numElements) {
                    factor = Math.pow(ebottom/scrollTop, 2) / 2;
                } else if (etop > scrollTop + windowHeight - 5*numElements) {
                    factor = Math.pow((etop-docHeight)/(windowHeight-docHeight),2) / 2;
                } else {
                    console.log(uid);
                    factor = 1.0;
                }
                return 25 * factor;
            })
            .attr("cy", function(d,i) {
                var uid = _uid(d, i);
                var element = $("." + uid);
                var etop = element.offset().top;

                console.log(elements);
                var y = Math.min(Math.max(etop - scrollTop, 5 + 10*i), windowHeight - 5 - 10*(numElements - i));

                return y;
            });
    }

    function _fill_text(div, data, level, num_children) {
        var level = level || 1;
        var num_children = num_children || 0;
        jQuery("<h" + level + "/>").html(data.title).appendTo(div);

        if (data.type == 'content_node') {
            var content = jQuery("<div/>").addClass("markdown").addClass(_uid(data, num_children)).appendTo(div);
            jQuery.getJSON('/api/v0/getcontentnode?node_id=' + data.id, function(data) { 
                var mdtree = _reformat_markdown_headings(markdown.parse(data.text), level);
                //var html = markdown.renderJsonML(markdown.toHTMLTree(mdtree));
                var html = markdown.toHTML(mdtree);
                content.html(html);
            })
            return num_children + 1;
        }

        for (var i in data.children) {
            num_children = _fill_text(div, data.children[i], level+1, num_children);
        }
        return num_children;
    }

    function _reformat_markdown_headings(mdtree, level) {
        _.each(mdtree, function(d,i) {
            if (i != 0) {
                d[1].level += level;
            }
        })
        return mdtree;
    }

    return module;
})(jQuery, d3, markdown, _)
