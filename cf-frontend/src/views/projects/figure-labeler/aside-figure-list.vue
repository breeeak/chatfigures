<template>

  <!-- offcanvas Show All Images-->
  <div class="offcanvas offcanvas-end" data-bs-scroll="true" :data-bs-backdrop="true" tabindex="-1" id="offcanvasWithBothOptions" aria-labelledby="offcanvasWithBothOptionsLabel">
    <div class="offcanvas-header">
      <h5 class="offcanvas-title" id="offcanvasWithBothOptionsLabel">All Images</h5>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body" >
      <!--begin::Wrapper-->
      <div class="mb-0">
        <!--begin::Demos-->
        <div class="mb-0 ">
          <!--begin::Row-->

          <!--end::Row-->
        </div>
        <!--end::Demos-->
      </div>
      <!--end::Wrapper-->
    </div>
    <div class="text-center">
      <button @click="exportAll" class="btn btn-sm text-white btn-primary w-100 my-5">
        Export All Labels
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import {defineComponent, onMounted, ref, watch} from "vue";
import Offcanvas from "bootstrap/js/dist/offcanvas";
import {getFigureSeparationList} from "@/api/projects/figure-separation";

export default defineComponent({
  name: "aside-figure-list",
  props: {
    separationList: Array,
    currentIndex: Number,
  },
  emits: ["changeIndex"],
  setup(props, { emit }) {
    const currentIndex = ref(0);
    const data = ref([]);
    // getFigureSeparationList({index:currentIndex.value,resultId:props.resultIndex}).then((res:any) => {
    //   console.log(res);
    //   data.value = res.data;
    // });
    // 切换显示图片
    const showFigure = (item, index) => {
      currentIndex.value = index;
      //current_index.value = index;
      emit("changeIndex", index); // 发出改变index的消息 由父组件接收
      // TODO 有bug 不会自动关闭backdrop
      //获得offcanvas实例并调用hide方法
      const offcanvas = Offcanvas.getInstance("#offcanvasWithBothOptions")
      offcanvas?.hide();
      // remove div offcanvas-backdrop class
      const backdrop = document.querySelector(".offcanvas-backdrop.fade.show");
      backdrop?.remove();
    };
    // // 监听索引的改变
    watch(
        () => props.currentIndex,
        (newProps, oldProps) => {
          //TODO 展示图片   这里的图片没有进行处理 是results
          currentIndex.value = newProps || 0;
        }
    );
    // TODO 导出所有的结果
    const exportAll = () => {
      console.log("导出所有的结果");
      // exportLabels({}).then((data:any) => {
      //   const blob = new Blob([data], {
      //     type: 'application/zip'
      //   })
      //   const link = document.createElement('a')
      //   link.href = window.URL.createObjectURL(blob)
      //   link.download = "labels.zip"
      //   link.click()
      //   //释放内存
      //   URL.revokeObjectURL(link.href)
      // });
    };

    //必须在这里才可以获得
    // onUpdated(() => {
    //   console.log(data_info);
    // });
    return {
      showFigure,
      exportAll,
      data
    };
  },
});






</script>

<style scoped>

</style>