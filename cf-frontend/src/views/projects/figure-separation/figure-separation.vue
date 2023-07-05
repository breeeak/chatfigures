<template>
  <!--Nav-->
  <nav-bar/>
  <!--Nav-->
  <div class="container" >
    <!--begin::Hero-->
    <section id="Home">
      <div class="row">
        <div class="col-12 text-center my-5">
          <p class="display-6 my-4">Automatic Compound Figure Separation and Label Extraction！</p>

          <div class="text-gray-400 fw-bold fs-5">
            No download required. Available online for any computer. If you need help, please check our
            <router-link :to="{ name: 'separation-guidelines'}" class="fw-bolder link-primary">User Guidelines</router-link>.
          </div>
        </div>
      </div>


      <!--begin::Dropzone Upload-->.
      <div class="row mt-lg-5">
        <div class="d-flex flex-column mb-5">
          <div class="dropzone dz-message" id="previews">
            <div class="" v-if="showBtn">
              <button
                  class="align-self-center btn btn-lg btn-primary my-5 text-white"
                  type="submit"
                  :disabled="loading"
                  @click="uploadAndDetect"
              >
               <span v-if="!loading" class="indicator-label">
                    Upload and Start Separation
                  </span>
                <span v-else class="indicator-progress">
                    Please wait ...
                   <span
                       class="spinner-border spinner-border-sm align-middle ms-2"
                   ></span>
               </span>
              </button>
            </div>
            <!--begin::Message-->
            <div  v-if="!showBtn">
              <!--begin::Icon-->
              <font-awesome-icon class="text-danger align-self-center fs-3" icon="fa-cloud-arrow-up"/>
              <!--end::Icon-->
              <!--begin::Info-->
              <div class="ms-4">
                <h3 class="fs-5 fw-bolder text-gray-900 mb-1">
                  Drop scientific figure here or click to upload.
                </h3>
                <span class="fs-7 fw-bold text-gray-400"
                >Upload up to 10 M with image format
                        (JPG,PNG,BMP,TIFF...).</span
                >
              </div>
              <!--end::Info-->
            </div>
            <!--end::Message-->
          </div>
          <!--begin::Foot-->
          <div class="d-flex flex-column p-2">
            <div class="fw-bold">
              <div class="text-gray-600 fs-8">
                You are responsible for the image you upload and we will never share your images with anyone else. Learn
                more about our
                <a href="/privacy-policy.html">Privacy Policy</a> & <a href="/terms-conditions.html">User terms</a>
              </div>
            </div>
          </div>
          <!--end::Foot-->
        </div>
      </div>
      <!--end::Dropzone-->

    </section>
    <!--end::Hero-->

    <!--begin::Features-->
    <section id="Features">
      <div class="row">
        <div class="col-12 text-center my-5">
          <h1>Features</h1>
        </div>
      </div>
      <div class="row">
        <!--begin::Col-->
        <div class="col-md-4 px-5 text-center">
          <!--begin::Illustration-->
          <img
              src="/static/images/design/Support-online.webp"
              class="mh-200px mb-9 rounded-3 shadow-lg"
              alt=""
          />
          <!--end::Illustration-->
          <div class="text-center mb-10 mb-md-0">
            <!--begin::Heading-->
            <div class="d-flex flex-center mb-5">
              <!--begin::Badge-->
              <span
                  class="badge badge-circle badge-light-success fw-bolder p-5 me-3 fs-3"
              >1</span>
              <!--end::Badge-->
              <!--begin::Title-->
              <div class="fs-5 fs-lg-3 fw-bolder text-dark">
                Support online & offline figures
              </div>
              <!--end::Title-->
            </div>
            <!--end::Heading-->
            <!--begin::Description-->
            <div class="fw-bold fs-6 fs-lg-4 text-muted">
              You can upload your images from your local computer or from the web with the help of our browser
              extension.
            </div>
            <!--end::Description-->
          </div>
        </div>
        <!--end::Col-->
        <!--begin::Col-->
        <div class="col-md-4 px-5 text-center">
          <!--begin::Illustration-->
          <img
              src="/static/images/design/Figure-separation.webp"
              class="mh-200px mb-9 rounded-3 shadow-lg"
              alt=""
          />
          <!--end::Illustration-->
          <div class="text-center mb-10 mb-md-0">
            <!--begin::Heading-->
            <div class="d-flex flex-center mb-5">
              <!--begin::Badge-->
              <span
                  class="badge badge-circle badge-light-success fw-bolder p-5 me-3 fs-3"
              >2</span
              >
              <!--end::Badge-->
              <!--begin::Title-->
              <div class="fs-5 fs-lg-3 fw-bolder text-dark">
                Figure separation with labels
              </div>
              <!--end::Title-->
            </div>
            <!--end::Heading-->
            <!--begin::Description-->
            <div class="fw-bold fs-6 fs-lg-4 text-muted">
              AI-based automatically separate compound figure panels as well as their corresponding
              labels.
            </div>
            <!--end::Description-->
          </div>
        </div>
        <!--end::Col-->
        <!--begin::Col-->
        <div class="col-md-4 px-5">
          <div class="text-center mb-10 mb-md-0 text-center">
            <!--begin::Illustration-->
            <img
                src="/static/images/design/Free-download.webp"
                class="mh-200px mb-9 rounded-3 shadow-lg"
                alt=""
            />
            <!--end::Illustration-->
            <!--begin::Heading-->
            <div class="d-flex flex-center mb-5">
              <!--begin::Badge-->
              <span
                  class="badge badge-circle badge-light-success fw-bolder p-5 me-3 fs-3"
              >3</span
              >
              <!--end::Badge-->
              <!--begin::Title-->
              <div class="fs-5 fs-lg-3 fw-bolder text-dark">
                Free download & export
              </div>
              <!--end::Title-->
            </div>
            <!--end::Heading-->
            <!--begin::Description-->
            <div class="fw-bold fs-6 fs-lg-4 text-muted">
              You can free download all sub figures or export json format labels.
              The separate results can be customized by yourself.
            </div>
            <!--end::Description-->
          </div>
        </div>
        <!--end::Col-->
      </div>
    </section>
    <!--end::Features-->
    <!--begin::Resources-->
    <section id="Resources" class="my-lg-10">
      <div class="row">
        <div class="col-12 text-center my-5">
          <h1>Resources</h1>
        </div>
      </div>
      <div class="row">
        <div class="col-md-4  mt-2">
          <div class="d-flex justify-content-center align-items-center">
            <a href="https://chrome.google.com/webstore/detail/chat-figures/ekoknoogfnngkknedfbodhnlkhdioiih" target="_blank" class="btn btn-sm btn-dark bg-opacity-75 btn-hover-scale text-white ">
              <img
                  src="/static/brands/chrome-color-svgrepo-com.svg"
                  class="me-5 rounded text-white h-30px"
                  alt=""
              />
              <span class="text-white fs-5 ">Google Chrome Extension</span>
            </a>
          </div>
          <div class="text-gray-400 fw-bold fs-5 text-center mt-2">
            <router-link :to="{name:'separation-instructions'}" class="fw-bolder link-primary">Instructions</router-link
            > on how to use the extension.
          </div>
        </div>

        <div class="col-md-4  mt-2 d-flex justify-content-center flex-column">
          <div class="m-2">
          <!--begin::Title-->
            <h4>Need Support or Report Bugs?</h4>
            <!--end::Title-->
            <!--begin::Text-->
            <div class="text-gray-400 fw-bold fs-4 mt-2"
            >Email to
                <a href="mailto:shuomeng2-c@my.cityu.edu.hk"
                   class="link-primary fw-bold text-hover-dark text-nowrap"
                >shuomeng2-c@my.cityu.edu.hk</a
                ></div>
            <!--end::Text-->
          </div>
        </div>



        <div class="col-md-4 mt-2 d-flex flex-column justify-content-center">
          <!--begin::Link-->
          <div class="mb-2">
            <a href="https://github.com/breeeak/chatfigures" class="d-flex align-items-center"  target="_blank">
              <img
                  src="/static/brands/github-color-svgrepo-com.svg"
                  class="h-20px me-2"
                  alt=""
              />
              <div class="text-hover-primary text-dark fw-bold fs-5 d-inline"
              >Source Code on Github</div>
            </a>
          </div>
          <!--end::Link-->
          <!--begin::Link-->
          <div class="mb-2">
            <a href="https://portland-my.sharepoint.com/:u:/g/personal/shuomeng2-c_my_cityu_edu_hk/EZEbSfiIb-5Kkp0uI2aR7rEBwOX3snh6hz22eapyFlnvkg?e=Y33AFL" class="d-flex align-items-center" target="_blank">
              <img
                  src="/static/brands/ms-onedrive-svgrepo-com.svg"
                  class="h-20px me-2 rounded"
                  alt=""
              />
              <div class="text-hover-primary text-dark fw-bold fs-5 d-inline"
              >Labeled Dataset on Onedrive</div>
            </a>
          </div>
          <!--end::Link-->
        </div>
      </div>
    </section>
    <!--end::Resources-->
  </div>
</template>

<script lang="ts" setup>
import {onBeforeUnmount, onMounted, ref} from "vue";
import { useRouter } from 'vue-router'
import {library} from '@fortawesome/fontawesome-svg-core'
import {faXmark, faCloudUpload} from '@fortawesome/free-solid-svg-icons'
import {getFigureSeparationUrl} from "@/api/projects/figure-separation";
import{getToken,setToken} from "@/core/services/JwtService";
import NavBar from "@/components/layout/nav-bar.vue";
// 弹窗
import Swal from "sweetalert2";
// 上传文件插件
import Dropzone from "dropzone";
library.add(faXmark, faCloudUpload)

// 设置token
let authorization:any = "";
if (getToken("access")!=null){
    authorization = "Bearer " + getToken("access");
}

const router = useRouter();
let myDropzone: any = null;
Dropzone.autoDiscover = false; // 新版本要加上这个 文件上传
const uploadBtn = () => {

  myDropzone = new Dropzone(document.body, {
    //url: "https://lsky.mengshuo.xyz/api/upload", // Set the url for your upload script location
    url: getFigureSeparationUrl(), // Set the url for your upload script location
    headers: {
      "Cache-Control": "",
      "X-Requested-With": "",
      Authorization: authorization,
    },
    method: "post",
    paramName: "image", // The name that will be used to transfer the file
    maxFiles: 1,
    maxFilesize: 10, // MB
    addRemoveLinks: true,
    acceptedFiles: "image/*", //允许的类型
    thumbnailWidth: 500, //缩略图宽度
    thumbnailHeight: undefined, //缩略图高度
    previewsContainer: "#previews", //上传图片容器
    autoProcessQueue: false, //是否自动上传
    removedfile: function (file) {
      if (file.previewElement != null && file.previewElement.parentNode != null) {
        file.previewElement.parentNode.removeChild(file.previewElement);
      }
      showBtn.value = false;  // 移除后关闭按钮
    },
  });
  // 为上传添加额外参数  可以使用监听的方式 也可以上面removedfile的方式
  // myDropzone.on("sending", function (file, xhr, formData) {
  //   formData.append("userName", "bob");
  // });
  myDropzone.on("success", function (file, response: any) {
    console.log(response);
    if (response.code !== 200) {
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: response.msg,
      })
      return;
    }else {
      setToken("access", response.data["token"]);
      router.push({ name: "separation-results", params: {resultId:response.data["id"]} });
    }
    myDropzone.destroy();  // 销毁
  });
  myDropzone.on("addedfile", function (file) {
    if (myDropzone.files.length > 1) {   // 如果数目大于1就替换掉之前上传的
      myDropzone.removeFile(myDropzone.files[0]);
    }
    setTimeout(() => {
      if (file.accepted) {
        showBtn.value = true;
      }
    }, 10)   // 必须要setTimeout 才能获得到属性
  });
};
onMounted(() => {
  uploadBtn();
});
onBeforeUnmount(() => {
  if (myDropzone){
    myDropzone.destroy();
  }
});
const uploadAndDetect = () => {
  loading.value = true;
  //需要先获取得到这个上传元素
  let myDropzone = Dropzone.forElement(document.body);
  myDropzone.processQueue();  //手动上传

}
const loading = ref<boolean>(false);
const showBtn = ref<boolean>(false);



</script>

<style scoped>

</style>