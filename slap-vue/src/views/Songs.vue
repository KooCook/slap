<template>
  <div class="container">
    <b-skeleton-wrapper :loading="loading">
      <template #loading>
        <b-skeleton width="85%"></b-skeleton>
        <b-skeleton width="55%"></b-skeleton>
        <b-skeleton width="70%"></b-skeleton>
      </template>
      <div class="row">
          <div class="col-3" v-for="song in songs" :key="song.id">
            <b-card>
              <b-card-title>{{ song.title }}</b-card-title>
              <b-card-text>
                by {{ song.artists.join(", ") }}

              </b-card-text>
              <!--<b-card-text class="small text-muted">Last updated 3 mins ago</b-card-text>-->
              <b-button :to="'/song/' + song.id" variant="primary">See details</b-button>
            </b-card>
          </div>
      </div>
      <b-pagination
              v-model="currentPage"
              :total-rows="totalCount"
              :per-page="perPage"
              aria-controls="my-table"
              @change="onChangePage"
      ></b-pagination>
    </b-skeleton-wrapper>
  </div>
</template>

<script>
const SongLyricsPopularitySlap = require("@/modules/slap-client");

export default {
  data() {
    return {
      songs: [],
      currentPage: 8,
      perPage: 25,
      totalCount: 0,
      loading: true
    };
  },
  watch: {
  },
  methods: {
    onChangePage(page) {
      this.$router.push({path: 'songs', query: { page }})
      this.fetchData()
    },
    fetchData() {
      this.loading = true
      const api = new SongLyricsPopularitySlap.DefaultApi();
      api.slapFlaskPublicControllersSongsGetSongs({ ...this.$route.query }, (error, data) => {
        if (error) {
          console.error(error);
        } else {
          this.songs = data.results
          console.log(data)
          this.perPage = 25
          this.totalCount = data['count']
          setTimeout(() => this.currentPage = this.$route.query.page)
          this.loading = false
        }
      })
    }
  },
  mounted() {
    this.fetchData()
  },
};
</script>

<style>
</style>
