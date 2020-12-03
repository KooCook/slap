// set the dimensions and margins of the graph
const margin = {top: 30, right: 30, bottom: 30, left: 30},
  width = 800 - margin.left - margin.right,
  height = 800 - margin.top - margin.bottom;

// append the svg object to the body of the page
const svg = d3.select("#my_dataviz")
.append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
.append("g")
  .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

fetch('csv/song_matrix.csv')
  .then(response => response.text())
  .then(text => { return d3.csvParse(text) })
  .then(data => {
// d3.csv("csv/song_matrix.csv", function(data) {
    const posWord = new Map([...new Set(data.map(d => [d.x, d.word]))]);

    // Build X scales and axis:
    const x = d3.scaleBand()
      .range([ 0, width ])
      .domain(posWord.keys())
      .padding(0.01);
    const xAxis = svg.append("g")
      .attr("transform", "translate(0," + 0 + ")")
      .call(d3.axisTop(x)
        .tickFormat(function(d) {
          return posWord.get(d)
        })
      )

    // Build Y scales and axis:
    const y = d3.scaleBand()
      .range([ 0, height ])
      .domain(posWord.keys())
      .padding(0.01);
    const yAxis = svg.append("g")
      .call(d3.axisLeft(y)
        .tickFormat(function(d) {
          return posWord.get(d)
        })
      );

    const clip = svg.append("defs").append("svg:clipPath")
      .attr("id", "clip")
      .append("svg:rect")
      .attr("width", width )
      .attr("height", height )
      .attr("x", 0)
      .attr("y", 0);

    // Create the scatter variable: where both the circles and the brush take place
    const scatter = svg.append('g')
      .attr("clip-path", "url(#clip)")

    // Draw rects from array of object
    scatter.selectAll()
    .data(data, function(d) { return d.x+':'+d.y; })
    .enter()
    .append("rect")
      .attr("x", function(d) { return x(d.x) })
      .attr("y", function(d) { return y(d.y) })
      .attr("width", x.bandwidth() )
      .attr("height", y.bandwidth() )
      .style("fill", function(d) { return d.color })

    // A function that updates the chart when the user zoom and thus new boundaries are available
    function updateChart() {

      // recover the new scale
      // TODO: FIX HERE
      const newX = d3.event.transform.rescaleX(x);
      const newY = d3.event.transform.rescaleY(y);

      // update axes with these new boundaries
      xAxis.call(d3.axisTop(newX).tickFormat(d => posWord.get(d)))
      yAxis.call(d3.axisLeft(newY).tickFormat(d => posWord.get(d)))

      // update circle position
      scatter
        .selectAll("rect")
        .attr('x', function(d) {return newX(d.x)})
        .attr('y', function(d) {return newY(d.y)});
    }

    // Set the zoom and Pan features: how much you can zoom, on which part, and what to do when there is a zoom
    const zoom = d3.zoom()
        .scaleExtent([.5, 20])  // This control how much you can unzoom (x0.5) and zoom (x20)
        .extent([[0, 0], [width, height]])
        .on("zoom", updateChart);

    // This add an invisible rect on top of the chart area. This rect can recover pointer events: necessary to understand when the user zoom
    svg.append("rect")
        .attr("width", width)
        .attr("height", height)
        .style("fill", "none")
        .style("pointer-events", "all")
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
        .call(zoom);
    // now the user can zoom and it will trigger the function called updateChart

  })
  // .catch(error => {
  //   console.error('Error:', error);
  // });