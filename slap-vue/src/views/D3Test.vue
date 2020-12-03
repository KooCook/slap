<template>
  <v-app>
    <v-container>
      <v-row>
        <v-col cols="4" class="d-flex justify-center align-center">
          <div class="pa-2">
            <h3 class="pb-2">Countries in 2018 with the highest GDP</h3>
            <p>
              Gross domestic product by country allows you to compare the
              economies of the nations. It measures everything produced by
              everyone in the country whether they are citizens or foreigners.
              The data has been taken from
              <a
                href="https://www.thebalance.com/gdp-by-country-3-ways-to-compare-3306012"
                >The Balance</a
              >.
            </p>
          </div>
          <div id="my_dataviz"></div>
        </v-col>
        <v-col id="arc" />
      </v-row>
    </v-container>
  </v-app>
</template>

<script>
import * as d3 from "d3";

export default {
  name: "App",
  data() {
    return {
      gdp: [
        { country: "USA", value: 20.5 },
        { country: "China", value: 13.4 },
        { country: "Germany", value: 4.0 },
        { country: "Japan", value: 4.9 },
        { country: "France", value: 2.8 },
      ],
    };
  },
  mounted() {
    this.generateArc();
    this.generateSongRepMatrix();
  },
  methods: {
    generateArc() {
      const w = 500;
      const h = 500;

      const svg = d3
        .select("#arc")
        .append("svg")
        .attr("width", w)
        .attr("height", h);

      const sortedGDP = this.gdp.sort((a, b) => (a.value > b.value ? 1 : -1));
      const color = d3.scaleOrdinal(d3.schemeDark2);

      const max_gdp = d3.max(sortedGDP, (o) => o.value);

      const angleScale = d3
        .scaleLinear()
        .domain([0, max_gdp])
        .range([0, 1.5 * Math.PI]);

      const arc = d3
        .arc()
        .innerRadius((d, i) => (i + 1) * 25)
        .outerRadius((d, i) => (i + 2) * 25)
        .startAngle(angleScale(0))
        .endAngle((d) => angleScale(d.value));

      const g = svg.append("g");

      g.selectAll("path")
        .data(sortedGDP)
        .enter()
        .append("path")
        .attr("d", arc)
        .attr("fill", (d, i) => color(i))
        .attr("stroke", "#FFF")
        .attr("stroke-width", "1px")
        .on("mouseenter", function () {
          d3.select(this).transition().duration(200).attr("opacity", 0.5);
        })
        .on("mouseout", function () {
          d3.select(this).transition().duration(200).attr("opacity", 1);
        });

      g.selectAll("text")
        .data(this.gdp)
        .enter()
        .append("text")
        .text((d) => `${d.country} -  ${d.value} Trillion`)
        .attr("x", -150)
        .attr("dy", -8)
        .attr("y", (d, i) => -(i + 1) * 25);

      g.attr("transform", "translate(200,300)");
    },
    generateSongRepMatrix() {
      // set the dimensions and margins of the graph
      const margin = { top: 30, right: 30, bottom: 30, left: 30 },
        width = 800 - margin.left - margin.right,
        height = 800 - margin.top - margin.bottom;

      // append the svg object to the body of the page
      const svg = d3
        .select("#my_dataviz")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      fetch("csv/song_matrix.csv")
        .then((response) => response.text())
        .then((text) => {
          return d3.csvParse(text);
        })
        .then((data) => {
          // d3.csv("csv/song_matrix.csv", function(data) {
          const posWord = new Map([...new Set(data.map((d) => [d.x, d.word]))]);

          // Build X scales and axis:
          const x = d3
            .scaleBand()
            .range([0, width])
            .domain(posWord.keys())
            .padding(0.01);
          const xAxis = svg
            .append("g")
            .attr("transform", "translate(0," + 0 + ")")
            .call(
              d3.axisTop(x).tickFormat(function (d) {
                return posWord.get(d);
              })
            );

          // Build Y scales and axis:
          const y = d3
            .scaleBand()
            .range([0, height])
            .domain(posWord.keys())
            .padding(0.01);
          const yAxis = svg.append("g").call(
            d3.axisLeft(y).tickFormat(function (d) {
              return posWord.get(d);
            })
          );

          // const clip = svg
          //   .append("defs")
          //   .append("clipPath")
          //   .attr("id", "clip")
          //   .append("rect")
          //   .attr("width", width)
          //   .attr("height", height)
          //   .attr("x", 0)
          //   .attr("y", 0);

          // Create the scatter variable: where both the circles and the brush take place
          const scatter = svg.append("g").attr("clip-path", "url(#clip)");

          // Draw rects from array of object
          scatter
            .selectAll()
            .data(data, function (d) {
              return d.x + ":" + d.y;
            })
            .enter()
            .append("rect")
            .attr("x", function (d) {
              return x(d.x);
            })
            .attr("y", function (d) {
              return y(d.y);
            })
            .attr("width", x.bandwidth())
            .attr("height", y.bandwidth())
            .style("fill", function (d) {
              return d.color;
            });

          // A function that updates the chart when the user zoom and thus new boundaries are available
          function updateChart(event) {
            x.range(
              [margin.left, width - margin.right].map((d) =>
                event.transform.applyX(d)
              )
            );
            y.range(
              [margin.top, height - margin.bottom].map((d) =>
                event.transform.applyY(d)
              )
            );

            // svg
            //   .selectAll(".bars rect")
            //   .attr("x", d => x(d.name))
            //   .attr("width", x.bandwidth());

            // // recover the new scale
            // const newX = event.transform.rescaleX(x);
            // const newY = event.transform.rescaleY(y);

            // update axes with these new boundaries
            xAxis.call(d3.axisTop(x).tickFormat((d) => posWord.get(d)));
            yAxis.call(d3.axisLeft(y).tickFormat((d) => posWord.get(d)));

            // update circle position
            scatter
              .selectAll("rect")
              .attr("x", function (d) {
                return x(d.x);
              })
              .attr("y", function (d) {
                return y(d.y);
              })
              .attr("width", x.bandwidth())
              .attr("height", y.bandwidth());
          }

          // const extent = [[margin.left, margin.top], [width - margin.right, height - margin.top]];

          // Set the zoom and Pan features: how much you can zoom, on which part, and what to do when there is a zoom
          const zoom = d3
            .zoom()
            .scaleExtent([0.5, 20]) // This control how much you can unzoom (x0.5) and zoom (x20)
            // .translateExtent(extent)
            .extent([
              [0, 0],
              [width, height],
            ])
            .on("zoom", updateChart);

          // This add an invisible rect on top of the chart area. This rect can recover pointer events: necessary to understand when the user zoom
          svg
            .append("rect")
            .attr("width", width)
            .attr("height", height)
            .style("fill", "none")
            .style("pointer-events", "all")
            .attr(
              "transform",
              "translate(" + margin.left + "," + margin.top + ")"
            )
            .call(zoom);
          // now the user can zoom and it will trigger the function called updateChart
        });
      // .catch(error => {
      //   console.error('Error:', error);
      // });
    },
  },
};
</script>
