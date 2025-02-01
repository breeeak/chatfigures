<template>

  <!-- offcanvas Show All Images-->
    <div class="offcanvas offcanvas-end" data-bs-scroll="true" :data-bs-backdrop="true" tabindex="-1"
         id="offcanvasWithBothOptions" aria-labelledby="offcanvasWithBothOptionsLabel">
        <div class="offcanvas-header">
            <h5 class="offcanvas-title" id="offcanvasWithBothOptionsLabel">Separated Figures</h5>
            <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>

        <div class="offcanvas-body">
            <!--begin::Wrapper-->
            <div class="text-center" v-if="separationList.length>=1">
                <button @click="exportAll" class="btn btn-sm text-white btn-primary w-100 my-5 ">
                    Export All Labels
                </button>
            </div>
            <!--begin::Demos-->
            <div class="mb-0 ">
                <!--begin::Row-->
                <template v-for="(item, i) in separationList" :key="i">
                    <div class="align-self-center bg-opacity-75 row py-2 rounded border bg-light my-5">
                        <div class="col-12 cursor-pointer" @click="showIndex(item, i)">
                            <!--begin::Demo-->
                            <!--                    颜色框-->
                            <div
                                    :class="`overlay overflow-hidden position-relative ${
                          currentIndex === i
                            ? 'border border-4 border-primary'
                            : 'border border-4 border-gray-200'
                        } rounded`"

                            >
                                <!--                      图片-->
                                <div class="overlay-wrapper bg-danger">
                                    <img crossorigin="anonymous" :id="'img-'+i" :src="item['name']" class="image w-100"
                                         :alt="item['figure_no']"/>
                                </div>
                                <!--                      遮罩-->
                                <div class="overlay-layer bg-dark bg-opacity-10"></div>
                            </div>
                            <div class="text-center">
                                <h4>{{ item['figure_no'] }}</h4>
                            </div>
                            <div class="text-center">
                                <button @click="interactiveMeasurement(i)"
                                        class="btn btn-sm text-white btn-danger w-75">
                                    Interactive Measurement
                                </button>
                            </div>
                            <!--end::Demo-->
                        </div>
                    </div>
                </template>
                <!--end::Row-->
            </div>
            <!--end::Demos-->
        </div>
    </div>
</template>

<script lang="ts">
import {defineComponent, ref} from "vue";
import {exportAllSeparations} from "@/api/projects/figure-separation";
import {interactiveMeasurementUpload} from "@/api/projects/interactive-measurement";
import Swal from "sweetalert2";

export default defineComponent({
    name: "aside-offcanvas",
    props: {
        separationList: {
            type: Array<any>(),
            default: () => [],
        },
        resultId: {
            type: String,
            default: ""
        },
    },
    emits: ["changeIndex"],
    setup(props) {
        const currentIndex = ref(0);
        // 切换显示图片
        const showIndex = (item, index) => {
            currentIndex.value = index;
            // showViewer
            console.log(item, index);
        };
        // // 监听索引的改变
        // 导出所有的结果
        const exportAll = () => {
            exportAllSeparations({"resultId": props.resultId}).then((data: any) => {
                const blob = new Blob([data], {
                    type: 'application/zip'
                })
                const link = document.createElement('a')
                link.href = window.URL.createObjectURL(blob)
                link.download = props.resultId + ".zip"
                link.click()
                //释放内存
                URL.revokeObjectURL(link.href)
            });
        };
        // 交互测量
        const interactiveMeasurement = (index) => {
            // "http://127.0.0.1:8000/media/guest/a8dfe384-6b53-46ec-abbe-f820760b9ffb/Fig--2.jpg?1696990082.6581411"
            // img的内容直接上传到后端
            // 1.获取img的内容
            const img: any = document.getElementById("img-" + index);
            // img 使用canvas转换成blob
            const canvas = document.createElement('canvas')
            const ctx = canvas.getContext('2d')
            canvas.width = img.width
            canvas.height = img.height
            ctx!.drawImage(img, 0, 0, img.width, img.height)
            const imgBlob = canvas.toDataURL('image/png')
            // 上传到后端
            console.log(imgBlob)
            // 生成随机名字
            const imgName = props.resultId + "_"  +  new Date().getTime() + index + ".png"
            const formData = new FormData()
            formData.append('filename', imgName)
            formData.append('base64data', imgBlob)
            // 2.上传到后端
            interactiveMeasurementUpload(formData).then((response: any) => {
                console.log(response)
                const redirectUrl = response.data["redirectUrl"];
                const fullUrl = window.location.protocol + "//" + window.location.host + "/" + redirectUrl;
                console.log(fullUrl)
                // 3.跳转到交互测量页面
                window.open(fullUrl, "_blank");
            }).catch((error: any) => {
                Swal.fire({
                    title: 'Error!',
                    text: "Failed to interactive measurement" + error,
                    icon: 'error',
                    confirmButtonText: 'OK'
                })
            })
        };

        return {
            showIndex,
            currentIndex,
            exportAll,
            interactiveMeasurement,
        };
    },
});


</script>

<style scoped>

</style>