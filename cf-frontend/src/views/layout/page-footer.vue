<template>
  <!--begin::Footer-->
  <section id="footer">
    <div class="container-fluid">
      <!--begin::Copyright-->
      <div class="text-dark text-center fw-bold fst-italic ">
        <div class="fw-bold d-inline text-danger"> {{ theYear }} &copy; </div>
        <a href="/" class="text-danger text-hover-primary">
          Chat Figures
        </a>
      </div>
      <!--end::Copyright-->
    </div>
  </section>
  <!--end::Footer-->
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "page-footer",
  setup() {
    let now = new Date();
    let theYear = now.getFullYear();
    if (theYear < 1900) theYear = theYear + 1900;
    return {
      theYear,
    };
  },
});
</script>

<style scoped lang="scss">
</style>
