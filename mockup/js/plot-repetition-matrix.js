// set the dimensions and margins of the graph
const margin = {top: 30, right: 30, bottom: 30, left: 30},
  width = 450 - margin.left - margin.right,
  height = 450 - margin.top - margin.bottom;

// append the svg object to the body of the page
const svg = d3.select("#my_dataviz")
.append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
.append("g")
  .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

// Labels of row and columns
const myGroups = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
const myVars = ["v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v10"]

// Build X scales and axis:
const x = d3.scaleBand()
  .range([ 0, width ])
  .domain(myGroups.map((val, idx) => idx))
  .padding(0.01);

svg.append("g")
  .attr("transform", "translate(0," + height + ")")
  .call(d3.axisBottom(x)
    .tickFormat(function(d, i) {
      // tickFormat accepts a function that returns the label to use in the axis/scale/sth
      // function param == Array.prototype.map() param
      return myGroups[d]
    })
  )

// Build Y scales and axis:
const y = d3.scaleBand()
  .range([ height, 0 ])
  .domain(myVars.map((val, idx) => idx))
  .padding(0.01);

svg.append("g")
  .call(d3.axisLeft(y)
    .tickFormat(function(d) { return myVars[d] }));

// Build color scale
const myColor = d3.scaleLinear()
  .range(["#ffffff", "#69b3a2"])
  .domain([1,100])

// Draw rects from array of object
function drawRects(data) {
  svg.selectAll()
      .data(data, function(d) { return d.group+':'+d.variable; })
      .enter()
      .append("rect")
        .attr("x", function(d) { return x(myGroups.indexOf(d.group)) })
        .attr("y", function(d) { return y(myVars.indexOf(d.variable)) })
        .attr("width", x.bandwidth() )
        .attr("height", y.bandwidth() )
        .style("fill", function(d) { return myColor(d.value) })

}

fetch('https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/heatmap_data.csv')
  .then(response => response.text())
  .then(text => { return d3.csvParse(text) })
  .then(data => { drawRects(data) })
  .catch(error => {
    console.error('Error:', error);
  });
