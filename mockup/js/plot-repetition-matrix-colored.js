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
    const posWord = new Map([...new Set(data.map(d => [d.x, d.word]))]);

    // Build X scales and axis:
    const x = d3.scaleBand()
      .range([ 0, width ])
      .domain(posWord.keys())
      .padding(0.01);

    svg.append("g")
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

    svg.append("g")
      .call(d3.axisLeft(y)
        .tickFormat(function(d) {
          return posWord.get(d)
        })
      );

    // Draw rects from array of object
    svg.selectAll()
    .data(data, function(d) { return d.x+':'+d.y; })
    .enter()
    .append("rect")
      .attr("x", function(d) { return x(d.x) })
      .attr("y", function(d) { return y(d.y) })
      .attr("width", x.bandwidth() )
      .attr("height", y.bandwidth() )
      .style("fill", function(d) { return d.color })
  })
  .catch(error => {
    console.error('Error:', error);
  });