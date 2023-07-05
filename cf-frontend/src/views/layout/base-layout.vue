<template>
  <div class="page-container">
    <!--begin::Content-->
      <div class="content-wrap">
              <router-view></router-view>
      </div>
    <!--end::Content-->
    <!--begin::Footer-->
    <page-footer class="footer"/>
    <!--end::Footer-->
  </div>
</template>

<script setup lang="ts">
import PageFooter from "@/views/layout/page-footer.vue";
import {onMounted} from "vue";


onMounted(() => {

});



</script>


<style scoped lang="scss">
.page-container{
  position: relative;
  min-height: 100vh;
}
.content-wrap{
  padding-bottom: 2.5rem; /* Footer height */
}
.footer {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 2.5rem;            /* Footer height */
}

</style>