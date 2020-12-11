import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import D3Test from "../views/D3Test.vue";
import Overview from "../views/Overview.vue";
import SongDetailView from "../views/SongView.vue";
import SongListView from "../views/Songs.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/d3-test",
    name: "D3",
    component: D3Test,
  },
  {
    path: "/overview",
    name: "Overview",
    component: Overview,
  },
  {
    path: "/song/:id",
    name: "SongDetailView",
    component: SongDetailView,
  },
  {
    path: "/songs",
    name: "Songs",
    component: SongListView,
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue"),
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
