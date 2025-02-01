<template>
  <div class="d-flex flex-column flex-center flex-column-fluid p-10">
          <!--begin::Illustration-->
          <img
                  src="/static/images/projects/404.png"
                  alt=""
                  class="mb-10 h-lg-450px"
          />
          <!--end::Illustration-->

          <!--begin::Message-->
          <h1 class="fw-bold mb-10 align-self-center " style="color: #a3a3c7">
              Seems there is nothing here
          </h1>
          <!--end::Message-->

          <!--begin::Link-->
          <router-link :to="{ name: 'home'}" class="align-self-center btn btn-lg btn-primary my-5 text-white"
          >Return Home</router-link>

          <!--end::Link-->
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, onUnmounted } from "vue";
import { useStore } from "vuex";

export default defineComponent({
  name: "error-404",
  components: {},
  setup() {
    const store = useStore();

    onMounted(() => {
    });

    onUnmounted(() => {
    });

    return {
    };
  },
});
</script>
