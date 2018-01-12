/* 
 * Code taken from
 * https://github.com/distillpub/post--momentum
 */

function sliderGen(dims) {

  var onChange    = function() {}
  var ticks = [0, 1]
  var margin = {right: 50, left: 50}
  var curr_xval = 0
  var cr = 9
  var tickwidth = 1.5
  var tickheight = 7
  var ticksym = false // |---|-- vs |____|__
  var shifty = -10
  var ticktitles = function(d,i) { return numberWithCommas(d) }
  var showticks = true
  var default_xval = 0

  function renderSlider(divin) {

    var minLambda = Math.min.apply(null, ticks.filter(function(i) {return !isNaN(i)}))
    var maxLambda = Math.max.apply(null, ticks.filter(function(i) {return !isNaN(i)}))
    var width = dims[0] - margin.left - margin.right
    var height = dims[1]

    var svg = divin.append("svg")
	                  .attr("width", dims[0])
	                  .attr("height", dims[1])
	                  .style("position", "relative")
	                  .append("g")
	                  .attr("transform", "translate(0," + shifty + ")")

    var x = d3.scaleLinear()
        .domain([0, maxLambda])
        .range([0, width])
        .clamp(true);

    var slidersvg = svg.append("g")
        .attr("class", "slidersvg")
        .attr("transform", "translate(" + margin.left + "," + height / 2 + ")");

    var dragger = slidersvg.append("line")
        .attr("class", "track")
        .attr("x1", x.range()[0])
        .attr("x2", x.range()[1])
      .select(function() { return this.parentNode.appendChild(this.cloneNode(true)); })
        .attr("class", "track-inset")
      .select(function() { return this.parentNode.appendChild(this.cloneNode(true)); })
        .attr("class", "track-overlay")
        .call(d3.drag()
          .on("start.interrupt", function() { slidersvg.interrupt(); })
          .on("start drag", function() {
            var xval = x.invert(d3.event.x)
            handle.attr("transform", "translate(" + x(xval) + ",0)" );
            curr_xval = xval
            onChange(xval, handle)
          }));

    var ticksvg = slidersvg.append("g")

    if (showticks) {
	    ticksvg.selectAll("rect")
	      .data(ticks, function(d,i) {return i})
	      .enter().append("rect")
	      .attr("x", function(i) { return isNaN(i) ? -100: x(i) - tickwidth/2})
	      .attr("y", 9)
	      .attr("width", tickwidth )
	      .attr("height", function(d, i) { return (isNaN(i)) ? 0: ticksym ? tickheight*2: tickheight;} )
	      .attr("opacity",0.2 )

	    ticksvg.selectAll("text")
	      .data(ticks, function(d,i) {return i})
	      .enter().append("text")
				  .attr("class", "ticktext")
				  .attr("opacity", 0.3)
				  .attr("text-anchor", "middle")
			      .attr("transform", function(i) { return "translate(" + (isNaN(i) ? -100: x(i) - tickwidth/2 + 1) + "," + (tickwidth*2 + 24) + ")" })
			      .html(ticktitles)
	}
    ticksvg.selectAll("circle")
      .data(ticks,function(d,i) {return i})
      .enter()
      .append("circle", ".track-overlay")
      .attr("cx", function(i) { return isNaN(i) ? -100: x(i);})
      .attr("cy", 0)
      .attr("r", 3)
      .attr("opacity", 0.0)
      .on("click", function(lambda){
        var xval = lambda
        curr_xval = xval
        handle.attr("transform", "translate(" + x(xval) + ",0)" );
        onChange(xval, handle)
      })

    /*
      Update the ticks
    */
    var updateTicks = function(newticks) {

      var d1 = ticksvg.selectAll("rect")
        .data(newticks,function(d,i) {return i})

      d1.exit().remove()
      d1.merge(d1).transition().duration(50)
        .attr("x", function(i) { return isNaN(i) ? -100: x(i) - 0.5})

      var d2 = ticksvg.selectAll("circle")
        .data(newticks,function(d,i) {return i})
      d2.exit().remove()
      d2.merge(d2)
        .attr("cx", function(i) { return isNaN(i) ? -100: x(i);})

    }

    var handle = slidersvg.insert("g", ".track-overlay")
        .attr("transform", "translate(" + x(curr_xval) + ",0)" );

    handle.insert("circle")
        .attr("class", "handle")
        .attr("r", cr)
        .style("fill", "#ff6600")
        .style("fill-opacity", 1)
        .style("stroke", "white")
        .call(d3.drag()
          .on("start.interrupt", function() { slidersvg.interrupt(); })
          .on("start drag", function() {
            var xval = x.invert(d3.mouse(dragger.node())[0])
            handle.attr("transform", "translate(" + x(xval) + ",0)" );
            curr_xval = xval
            onChange(xval, handle)
          }));

    handle.insert("text")
          .attr("transform", "translate(0,22)")
          .attr("text-anchor","middle")
          .style("font-size", "10px")

    handle.moveToFront()
    return {xval : function() { return curr_xval },
    		tick : updateTicks,
    		init:function() {
		        handle.attr("transform", "translate(" + x(default_xval) + ",0)" );
		        onChange(default_xval, handle)
    		}
    }

  }

  renderSlider.ticktitles = function(f) {
    ticktitles = f
    return renderSlider
  }

  renderSlider.change = function(f) {
    onChange = f
    return renderSlider
  }

  renderSlider.margin = function(m) {
    margin = m
    return renderSlider
  }

  renderSlider.ticks = function(m) {
    ticks = m
    return renderSlider
  }

  renderSlider.startxval = function(m) {
    curr_xval = m
    default_xval = m
    return renderSlider
  }

  renderSlider.margins = function(l, r) {
    margin = {right: l, left: r}
    return renderSlider
  }

  renderSlider.cRadius = function(m) {
    cr = m
    return renderSlider
  }

  renderSlider.tickConfig = function(_1,_2,_3) {
    tickwidth = _1
    tickheight = _2
    ticksym = _3 // |---|-- vs |____|__
    return renderSlider
  }

  renderSlider.shifty = function(_) {
  	shifty = _
    return renderSlider
  }

  renderSlider.showticks = function(_) {
    showticks = _
    return renderSlider
  }

  renderSlider.shifty = function(_) {
  	shifty = _; return renderSlider
  }
  return renderSlider
}

/* Moves a svg element to the front */
d3.selection.prototype.moveToFront = function() {
  return this.each(function(){
    this.parentNode.appendChild(this);
  });
};

d3.selection.prototype.moveToBack = function() {
    return this.each(function() {
        var firstChild = this.parentNode.firstChild;
        if (firstChild) {
            this.parentNode.insertBefore(this, firstChild);
        }
    });
};

// http://stackoverflow.com/questions/2901102/how-to-print-a-number-with-commas-as-thousands-separators-in-javascript
function numberWithCommas(x) {
    var parts = x.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return parts.join(".");
}
