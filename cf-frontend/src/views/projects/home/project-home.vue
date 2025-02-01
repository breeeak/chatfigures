<template>
  <div class="container" >
          <div class="row">
              <div class="col-12 text-center my-5">
                  <p class="display-6 my-4">Chatfigures: Vision Language Model Based <br> Biomedical Image Understanding</p>

              </div>
          </div>
        <div class="row">
            <div class="col-12 text-center my-5">
            <div class="text-gray-400 my-4 fw-bold fs-5">
                Try our simple demos
            </div>
            <div class="d-flex justify-content-center">
                <router-link class="btn btn-primary text-white me-5" :to="{name:'figure-separation'}">Figure Separation</router-link>
                <router-link class="btn btn-primary text-white" :to="{name:'interactive-measurement'}">Interactive Measurement</router-link>
            </div>
                <div class="display-6 my-4 text-gray-400">
                    More Functions are Coming Soon!
                </div>
            </div>
        </div>
  </div>
</template>

<script lang="ts" setup>


</script>

<style scoped>

</style>