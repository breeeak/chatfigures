<template>
  <!--begin::Modal - New Target-->
  <div
      class="modal fade"
      tabindex="-2"
      aria-hidden="true"
      ref="settingModalRef"
  >
    <!--begin::Modal dialog-->
    <div class="modal-dialog modal-dialog-centered mw-650px">
      <!--begin::Modal content-->
      <div class="modal-content rounded">
        <!--begin::Modal header-->
        <div class="modal-header pb-0 border-0 justify-content-end">
          <!--begin::Close-->
          <div
              class="btn btn-sm btn-icon btn-active-color-primary"
              data-bs-dismiss="modal"
          >
            <span class="svg-icon fs-1">
              <font-awesome-icon icon="fa-xmark"/>
            </span>
          </div>
          <!--end::Close-->
        </div>
        <!--begin::Modal body-->
        <div class="modal-body scroll-y px-10 px-lg-15 pt-0 pb-15">
          <!--begin::Heading-->
          <div class="mb-8 text-center">
            <!--begin::Title-->
            <h1 class="mb-3">Draw Settings</h1>
            <!--end::Title-->
            <!--begin::Description-->
            <div class="text-gray-400 fw-bold fs-5">
              If you need help, please check our
              <a href="#" class="fw-bolder link-primary">User Guidelines</a
              >.
            </div>
            <!--end::Description-->
          </div>
          <!--end::Heading-->

          <!--begin::Input group-->
          <div class="d-flex flex-column " >
            <!--begin::Row All show settings-->
            <div class="row  mb-2  g-0" v-if="!isLabelVue">
              <!--begin::Label-->
              <label class="d-flex align-items-center mb-2">
                <div class="fw-bolder fs-6 "
                >Hide/Show Labels, Draws, Text, Summary</div
                >
                <span data-bs-toggle="tooltip" data-bs-placement="top" title="Hide or Show Labels or Draws">
                <font-awesome-icon icon="fa-solid fa-circle-info" class="ms-2 fs-7 text-gray-400"/>
              </span>
              </label>
              <div class="bg-light p-2 rounded">
                <div
                    class="form-check form-switch form-check-custom form-check-solid d-flex row g-0 mb-5"
                >
                  <div class="col-6 d-flex align-items-center" >
                    <input
                        class="form-check-input"
                        type="checkbox"
                        v-model="show_labels"
                        id="showLabel"
                    />
                    <label class="form-check-label" for="showLabel"
                    >{{ show_labels ? "Show" : "Hide" }} Labels</label
                    >
                  </div>
                  <div class="col-6 d-flex align-items-center">
                    <input
                        class="form-check-input"
                        type="checkbox"
                        value=""
                        id="showDraw"
                        v-model="show_draws"
                    />
                    <label class="form-check-label" for="showDraw"
                    >{{ show_draws ? "Show" : "Hide" }} Draws</label
                    >
                  </div>
                </div>
                <div
                    class="form-check form-switch form-check-custom form-check-solid d-flex row g-0"
                >
                  <div class="col-6 d-flex align-items-center">
                    <input
                        class="form-check-input"
                        type="checkbox"
                        value=""
                        id="showText"
                        v-model="show_text"
                    />
                    <label class="form-check-label" for="showText"
                    >{{ show_text ? "Show" : "Hide" }} Text</label
                    >
                  </div>
                  <div class="col-6 d-flex align-items-center">
                    <input
                        class="form-check-input"
                        type="checkbox"
                        value=""
                        id="showSummary"
                        v-model="show_summary"
                    />
                    <label class="form-check-label" for="showSummary"
                    >{{ show_summary ? "Show" : "Hide" }} Summary</label
                    >
                  </div>
                </div>
              </div>
            </div >
            <!--end::Row-->

            <!--begin::Row Text Size-->
            <div class="row mb-2">
              <!--begin::Label-->
              <label class="d-flex align-items-center fw-bolder mb-2 col-3">
                <span >Text Size</span>
                <span data-bs-toggle="tooltip" data-bs-placement="top" title="Specify the drawing text size">
                <font-awesome-icon icon="fa-solid fa-circle-info" class="ms-2 fs-7 text-gray-400"/>
              </span>
              </label>
              <!--end::Label-->
              <div class="col-3">
                <input type="number"  min="1" max="50" step="1"  class="form-control form-control-sm" v-model="text_size" >
              </div>
              <div class="col-6 d-flex align-items-center">
                <input type="range" v-model="text_size" class="form-range" min="1" max="100" step="1">
              </div>
            </div>
          </div>
          <!--end::Row Text Color-->
          <div class="mb-8 row" v-if="!isLabelVue">
            <!--begin::Label-->
            <label class="d-flex align-items-center fs-6 fw-bolder mb-2 col-3">
              <span>Text Color</span>
              <span data-bs-toggle="tooltip" data-bs-placement="top" title="Specify the drawing text color">
                <font-awesome-icon icon="fa-solid fa-circle-info" class="ms-2 fs-7 text-gray-400"/></span>
            </label>
            <div class="dropend col-8">
              <button
                  type="button"
                  id="dropdown-text"
                  class="btn btn-sm dropdown-toggle text-white"
                  data-bs-toggle="dropdown"
                  aria-expanded="true"
                  :style="{ background: text_color }"
              >
                Click to choose text color
              </button>
              <div class="dropdown-menu" aria-labelledby="dropdown-text">
                <ColorPicker
                    style="box-sizing: unset"
                    theme="light"
                    :color="text_color"
                    @changeColor="changeTextColor"
                />
              </div>
            </div>
            <!--end::Label-->
          </div>


          <!--begin::Row Draw width-->
          <div class="row mb-2" >
            <!--begin::Label-->
            <label class="d-flex align-items-center fw-bolder mb-2 col-3">
              <span>Draw Width</span>
              <span data-bs-toggle="tooltip" data-bs-placement="top" title="Specify the drawing pen width">
                <font-awesome-icon icon="fa-solid fa-circle-info" class="ms-2 fs-7 text-gray-400"/>
              </span>
            </label>
            <!--end::Label-->
            <div class="col-3">
              <input type="number"  min="1" max="50" step="1"  class="form-control form-control-sm" v-model="draw_size" >
            </div>
            <div class="col-6 d-flex align-items-center ">
              <input type="range" v-model="draw_size" class="form-range" min="1" max="20" step="1" >
            </div>
          </div>
        <!--end::Row-->

          <!--end::Row Draw Color-->
          <div class="mb-8 row" v-if="!isLabelVue">
            <!--begin::Label-->
            <label class="d-flex align-items-center fw-bolder mb-2 col-3">
              <span>Draw Color</span>
              <span data-bs-toggle="tooltip" data-bs-placement="top" title="Specify the drawing line color">
                <font-awesome-icon icon="fa-solid fa-circle-info" class="ms-2 fs-7 text-gray-400"/></span>
            </label>
            <div class="dropend col-8">
              <button
                  type="button"
                  id="dropdown-text"
                  class="btn btn-sm dropdown-toggle text-white"
                  data-bs-toggle="dropdown"
                  aria-expanded="true"
                  :style="{ background: draw_color }"
              >
                Click to choose draw color
              </button>
              <div class="dropdown-menu" aria-labelledby="dropdown-text">
                <ColorPicker
                    style="box-sizing: unset"
                    theme="light"
                    :color="draw_color"
                    @changeColor="changeDrawColor"
                />
              </div>
            </div>
            <!--end::Label-->
          </div>

          <!--end::Input group-->
        </div>
        <!--end::Modal body-->
      </div>
      <!--end::Modal content-->
    </div>
    <!--end::Modal dialog-->
  </div>
  <!--end::Modal - New Target-->

</template>


<script setup lang="ts">
import {Tooltip} from "bootstrap";
import {ref,onMounted} from "vue"
import {library} from '@fortawesome/fontawesome-svg-core'
import {faXmark,faCircleInfo} from '@fortawesome/free-solid-svg-icons'
import { ColorPicker } from "vue-color-kit";
import "vue-color-kit/dist/vue-color-kit.css";
library.add(faXmark,faCircleInfo)



const show_labels = ref(true);
const show_draws = ref(true);
const show_text = ref(true);
const show_summary = ref(true);
const text_size = ref(30);
const draw_size = ref(3);
const text_color = ref("#009EF7");
const draw_color = ref("#F43F61");

const settingModalRef = ref<null | HTMLElement>(null);
const emit = defineEmits(['set-draw-options'])
const props = defineProps({
  isLabelVue: {
    type: Boolean,
    default: false,
  },
})
onMounted(()=>{
  // 加载提示框 TODO 考虑加到全局加载上
  let tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new Tooltip(tooltipTriggerEl)
  })
  // 添加关闭监听Modal监听 返回设置值
  settingModalRef.value!.addEventListener(
      "hidden.bs.modal",
      function (event) {
        emit("set-draw-options", {
          draw_size: draw_size.value,
          text_size: text_size.value,
          draw_color: draw_color.value,
          text_color: text_color.value,
          show_labels: show_labels.value,
          show_draws: show_draws.value,
          show_text: show_text.value,
          show_summary: show_summary.value,
        });
      }
  );
});
const changeTextColor = (color) => {
    text_color.value = color.hex;
};
const changeDrawColor = (color) => {
  draw_color.value = color.hex;
};
</script>

<style scoped lang="scss">

</style>