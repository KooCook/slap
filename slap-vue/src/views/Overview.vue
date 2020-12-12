<template>
  <div class="container">
    {{ selected }}
    <b-form-group>
    <b-form-select v-model="repetition.selected" :options="options"></b-form-select>
    vs.
    <b-form-select v-model="popularity.selected" :options="popularity.options" @change="onPopChanged"></b-form-select>
    </b-form-group>
    <Plotly :data="data" :layout="layout" :display-mode-bar="false"></Plotly>
  </div>
</template>

<style>
</style>

<script>
  import { Plotly } from 'vue-plotly'
  const SongLyricsPopularitySlap = require("@/modules/slap-client");

  let trace1 = {
    x: [1, 2, 3, 4, 5],
    y: [1, 6, 3, 6, 1],
    mode: 'markers',
    type: 'scatter',
    name: 'Sample songs',
    text: ['A-1', 'A-2', 'A-3', 'A-4', 'A-5'],
    marker: { size: 12 }
  };

  let trace2 = {
    x: [2, 3, 4, 5],
    y: [16, 5, 11, 9],
    mode: 'lines',
    name: 'Fitted line'
  }

  // const trace2 = {
  //   x: [1.5, 2.5, 3.5, 4.5, 5.5],
  //   y: [4, 1, 7, 1, 4],
  //   mode: 'markers',
  //   type: 'scatter',
  //   name: 'Team B',
  //   text: ['B-a', 'B-b', 'B-c', 'B-d', 'B-e'],
  //   marker: { size: 12 }
  // };

  export default {
    components: {
      Plotly
    },
    data() {
      return {
        options: [
          // { value: null, text: 'Please select an option' },
          { value: 'compressibility', text: 'Compressibility' },
          // { value: 'b', text: 'Selected Option' },
          // { value: { C: '3PO' }, text: 'This is an option with object value' },
          // { value: 'd', text: 'This one is disabled', disabled: true }
        ],
        repetition: {
          selected: "compressibility",
        },
        popularity: {
          selected: "youtube_view",
          options: [
            { value: 'youtube_view', text: 'YouTube view count' },
            { value: 'spotify_popularity', text: 'Spotify Popularity Index' },
          ]
        },
        data: [ trace1, trace2 ],//, trace2 ],
        layout: {
          xaxis: {
            title: 'Compressibility'
          },
          yaxis: {
            title: 'YouTube View'
          },
          title:'Data Labels Hover'
        }
      }
    },
    methods: {
      onPopChanged() {
        this.fetchData()
      },
      fetchData() {
        const api = new SongLyricsPopularitySlap.DefaultApi();
        api.slapListRepetitionPopularityPlots({popFacet: this.popularity.selected},(error, data) => {
          if (error) {
            console.error(error);
          } else {
            const { x, y, text } = data.data
            trace2.x = data.line_data.x
            trace2.y = data.line_data.y
            trace1.x = x
            trace1.y = y
            trace1.text = text
          }
        })
      }
    },
    mounted() {
      this.fetchData()
    },
    }
</script>
