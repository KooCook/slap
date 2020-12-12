<template>
    <div class="container">
        <div class="container">
            <h1 class="display-4">{{ song.title }}</h1>
            <p class="lead">by {{ song.artists.join(", ") }}</p>
            <small>{{ song.genres.join(", ") }}</small>
        </div>
        <div class="container">
            <h4>Metrics</h4>
            <Plotly :data="frequency.data" :layout="frequency.layout" :display-mode-bar="false"></Plotly>
            <div class="row">
                <div class="col-6">
                    <h5>Lyrics</h5>
                    <pre>{{ song.lyrics }}</pre>
                </div>
                <div class="col-6">
                    <h5>Repetition Matrix</h5>
                    <div class="container-fluid">
                        <!-- Content here -->
                        <div id="my_dataviz" style="width:100% ;height:100% ;">

                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import * as d3 from "d3";
    import { Plotly } from 'vue-plotly'

    let trace1 = {
        x: ['giraffes', 'orangutans', 'monkeys'],
        y: [20, 14, 23],
        type: 'bar'
    };

    const SongLyricsPopularitySlap = require("@/modules/slap-client");
    export default {
        name: "SongView",
        components: {
            Plotly
        },
        data() {
            return {
                song: {
                    title: "",
                    artists: []
                },
                frequency: {
                    data: [ trace1 ],
                    layout: {
                        xaxis: {
                            title: 'Words'
                        },
                        yaxis: {
                            title: 'Word count'
                        },
                        title:'Word Frequency in lyrics'
                    }
                }
            }
        },
        mounted() {
            this.fetchData()
        },
        methods: {
            fetchData() {
                const api = new SongLyricsPopularitySlap.DefaultApi();
                const songId = this.$route.params.id
                api.retrieveSong(songId, (error, data) => {
                    if (error) {
                        console.error(error);
                    } else {
                        this.song = data
                        console.log(data)
                    }
                })
                function d3Gen(csv_data) {
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
                    const data = d3.csvParse(csv_data);
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
                }
                // let csv_data;
                api.retrieveRepetitionMatrixPlot(songId, (error, data) => {
                    if (error) {
                        console.error(error);
                    } else {
                        const csv_data = data
                        d3Gen(csv_data)
                    }})
                api.listSongWordFrequencyPlots(songId, (error, data) => {
                    if (error) {
                        console.error(error);
                    } else {
                        const { x, y } = data
                        trace1.x = x
                        trace1.y = y
                    }
                })
            }
        }
    }
</script>

<style scoped>

</style>
