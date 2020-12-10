<template>
  <div class="container">
    <Navbar></Navbar>
    <main>
      <slot></slot>
    </main>
  </div>
</template>

<script>
import Navbar from "@/components/Navbar.vue";
export default {
  name: "BaseLayout",
  components: {
    Navbar,
  },
};
</script>

<style>
</style>