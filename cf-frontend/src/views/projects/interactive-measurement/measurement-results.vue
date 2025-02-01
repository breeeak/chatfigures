<template>
    <div class="container-fluid px-4">
        <div class="row d-flex justify-content-center">
            <!--  左侧关系树-->
            <div class="col-2 d-flex flex-column align-items-stretch  ">
                <div class="border rounded my-2 p-2">
                    <p class="fw-bolder mb-2 text-center">
                        Image Information
                    </p>
                    <p class="mb-2">
                        <span class="fw-bolder">w: </span>
                        <span>{{initOptions.img_width}}</span>
                        <span class="fw-bolder ms-2">h: </span>
                        <span>{{initOptions.img_height}}</span>
                        <span class="fw-bolder ms-2">x: </span>
                        <span>{{mousePoint.x}}</span>
                        <span class="fw-bolder ms-2">y: </span>
                        <span>{{mousePoint.y}}</span>
                    </p>
                </div>
                <div >
                    <div class="border rounded mb-2 p-2">
                        <p class="fw-bolder mb-2 text-center">
                            Label Information
                        </p>
                        <div class="" data-bs-spy="scroll" style="overflow: auto;height: 300px;">
                            <table class="table table-striped ">
                                <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Length</th>
                                    <th>Area</th>
                                </tr>
                                </thead>
                                <tbody>
                                <template v-for="(item, index) in ['line','anything','poly','rect', 'circle']" :key="index">
                                    <tr v-for="(obj, index2) in fabricObjects.get(item)" :key="index+'-'+index2">
                                        <th>{{item}}{{index2+1}}</th>
                                        <td>{{ obj['results']['actLineLength'] }}{{ obj['results']['actLineUnit']}}</td>
                                        <td>{{ obj['results']['actArea']?obj['results']['actArea']+''+obj['results']['actAreaUnit']+'²':"" }}</td>
                                    </tr>
                                </template>
                                </tbody>
                            </table>
                        </div>
                        <div class="d-flex flex-wrap justify-content-between mt-2">
                            <div class="">
                                <button  data-bs-toggle="modal" data-bs-target="#tableModal" class="btn btn-sm btn-primary text-white mb-2" type="button" >
                                    Show Details
                                </button>
                            </div>
                            <div class="">
                                <button  @click="exportDetailLabels" class="btn btn-sm btn-primary text-white mb-2" type="button" >
                                    Export Labels
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="d-flex flex-column justify-content-end w-100 text-center">
                    <div class="border rounded p-2 mb-2">
                        <p class="fw-bolder mb-2">
                            Scale Information
                        </p>
                      <div class="mb-2 row align-items-center">
                          <label for="ActualLength" class="col-sm-5 col-form-label fw-bolder fs-8">Actual Length</label>
                          <div class="col input-group"  v-if="scaleInfo.isLabel">
                              <input type="text" :disabled="isActLengthDisabled" v-model="scaleInfo.actLength" class="form-control form-control-sm" id="ActualLength" placeholder="Actual Length">
                              <button @click="reAddBarLabel('labels')" v-if="reAddActLengthButton" class="btn btn-sm btn-primary text-white" type="button" id="button-addon2">Add</button>
                          </div>
                          <div class="col-sm-7"  v-else>
                              <button @click="addBarLabel('labels')" :class="currentToolType == 'labels' && isActive ? 'btn-danger' : 'btn-primary'"  class="btn btn-sm w-100 text-white">Add Label</button>
                          </div>
                      </div>
                      <div class="mb-2 row align-items-center">
                          <label for="BarLength" class="col-sm-5 col-form-label fw-bolder fs-8">Bar Length</label>
                          <div class="col input-group"  v-if="scaleInfo.isBar">
                              <input type="number" :disabled="isBarLengthDisabled" v-model="scaleInfo.barLength" class="form-control form-control-sm" id="BarLength" placeholder="Bar Length">
                              <button @click="reAddBarLabel('bars')" v-if="reAddBarLengthButton" class="btn btn-sm btn-primary text-white" type="button" id="button-addon2">Add</button>
                          </div>
                          <div class="col-sm-7"  v-else>
                              <button @click="addBarLabel('bars')" :class="currentToolType == 'bars' && isActive ? 'btn-danger' : 'btn-primary'" class="btn btn-sm w-100  text-white">Add Bar</button>
                          </div>
                      </div>
                      <div class="mb-2 row align-items-center">
                          <label for="ppm" class="col-sm-5 col-form-label fw-bolder fs-8">PixelsPerMeter</label>
                          <div class="col-sm-7">
                              <input  type="number" disabled v-model="scaleInfo.ppm" class="form-control form-control-sm" id="ppm" placeholder="Pixel Per Meter">
                          </div>
                      </div>
                      <!---->
                    </div>
                    <div>
                      <button @click="editScaleBar" class="btn btn-sm w-100 text-white mb-2" :class='isEditScaleBar? "btn-success": "btn-primary"' type="button">
                          {{ isEditScaleBar? "Confirm": "Edit"}} Scale Bar
                      </button>
                      <!---->
                      <button  @click="showHideScaleBar" class="btn btn-sm btn-primary w-100 text-white mb-2" :class='isShowScaleBar? "btn-dark": "btn-primary"' type="button" >
                          {{ isShowScaleBar? "Hide": "Show"}} Scale Bar
                      </button>
                    </div>
                    <router-link :to="{ name: 'user-guidelines'}" class="fw-bolder link-primary mb-2">Need Help? User Guidelines</router-link>
                </div>
            </div>
            <div id="panel" class="col-9 rounded border bg-dark">

        <div class="p-5">
            <div class="mb-2">
                <span class="badge badge-primary" v-if="isLoadSAM">
                 SAM model is ready
                </span>
                <span class="badge badge-danger" v-else>
                 SAM model is Loading
                </span>
            </div>
        <div id="toolbar" class=" d-flex align-items-center justify-content-center flex-wrap  bg-dark pb-5 mt-1">
            <!--begin::Symbol-->
            <template v-for="(item, index) in toolBarIcons" :key="index">
                <!--        func TODO 1. 盒子模型有点问题 点击空白处也会 出发事件 2. DrawType改成ENUM -->
                <div
                        class="symbol symbol-50px me-5"
                        @click="changeDrawType(item.drawType)"
                        :title="item.tips"
                        v-if="item.type == 'draw'"
                >
          <span
                  class="symbol-label"
                  :class="
              currentToolType == item.drawType && isActive ? 'bg-light-warning' : ''
            "
          >
            <span
                    :class="
                currentToolType == item.drawType && isActive ? 'svg-icon-danger' : ''
              "
                    class="svg-icon svg-icon-2x btn btn-hover-scale"
            >
              <inline-svg :src="item.icon"/>
            </span>
          </span>
                </div>
                <!--        info-->
                <div
                        v-if="item.type == 'info'"
                        class="symbol symbol-50px me-5 justify-content-center d-flex"
                        :title="item.tips"
                >
                    <span class="symbol-label w-75px fw-bold" :id="item.drawType"></span>
                </div>
                <!--        osd-->
                <div
                        class="symbol symbol-50px me-5"
                        :title="item.tips"
                        v-if="item.type == 'osd'"
                >
          <span class="symbol-label">
            <span
                    class="svg-icon-danger svg-icon svg-icon-2x btn btn-hover-scale"
                    :id="item.drawType"
            >
              <inline-svg :src="item.icon"/>
            </span>
          </span>
                </div>
                <!--        func-->
                <div
                        class="symbol symbol-50px me-5"
                        :title="item.tips"
                        v-if="item.type == 'func'"
                        @click="doDrawFuc(item.drawType)"
                >
          <span class="symbol-label">
            <span
                    class="svg-icon-primary svg-icon svg-icon-2x btn btn-hover-scale"
            >
              <inline-svg :src="item.icon"/>
            </span>
          </span>
                </div>
                <!--        separate-->
                <div class="me-10" v-if="item.type == 'separate'"></div>
            </template>
        </div>
        <!--end::Item-->
      </div>
          <div id="canvasFrame">
              <div id="canvasDiv" class="canvasDiv h-700px border-dashed mx-0 px-0 mb-5"
              ></div>
              <div id="crosshair-h" class="hair"></div>
              <div id="crosshair-v" class="hair"></div>
          </div>
        </div>
        </div>
    </div>
  <!--      弹窗 超出边界的提示信息-->
    <div class="toast-container position-fixed top-0 end-0 p-3">
        <div id="boundaryToast" class="toast align-items-center text-bg-danger" role="alert" aria-live="assertive"
             aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body text-white" v-html="boundaryMsg">
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"
                        aria-label="Close"></button>
            </div>
        </div>
    </div>
  <!--  弹窗 修改绘制内容 TODO-->
    <draw-option-modal id="drawOption" @setDrawOptions="getDrawOptions"/>
  <!-- 表格详细信息的Modal -->
    <div class="modal fade" id="tableModal" tabindex="-1" aria-labelledby="tableModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered mw-650px">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="tableModalLabel">Modal title</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="" data-bs-spy="scroll" style="overflow: auto;height: 300px;">
                        <table id="line-table"  class="table table-striped" v-if="fabricObjects.get('line')!.length>0">
                            <thead>
                            <tr>
                                <th>Line</th>
                                <th>Length</th>
                                <th>Pixel Length</th>
                            </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(obj, index2) in fabricObjects.get('line')" :key="'line-'+index2">
                                    <th>line{{index2+1}}</th>
                                    <td>{{ obj['results']['actLineLength'] }}{{ obj['results']['actLineUnit']}}</td>
                                    <td>{{ obj['results']['lineLength'] }}px</td>
                                </tr>
                            </tbody>
                        </table>
                        <table id="poly-table"  class="table table-striped" v-if="fabricObjects.get('poly')!.length>0">
                            <thead>
                            <tr>
                                <th>Poly</th>
                                <th>Perimeter</th>
                                <th>Area</th>
                                <th>Pixel Perimeter</th>
                                <th>Pixel Area</th>
                            </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(obj, index2) in fabricObjects.get('poly')" :key="'poly-'+index2">
                                    <th>poly{{index2+1}}</th>
                                    <td>{{ obj['results']['actLineLength'] }}{{ obj['results']['actLineUnit']}}</td>
                                    <td>{{ obj['results']['actArea']+''+obj['results']['actAreaUnit']+'²'}}</td>
                                    <td>{{ obj['results']['lineLength']}}px</td>
                                    <td>{{ obj['results']['area'] +'px²'}}</td>
                                </tr>
                            </tbody>
                        </table>
                        <table id="anything-table"  class="table table-striped" v-if="fabricObjects.get('anything')!.length>0">
                            <thead>
                            <tr>
                                <th>Poly</th>
                                <th>Perimeter</th>
                                <th>Area</th>
                                <th>Pixel Perimeter</th>
                                <th>Pixel Area</th>
                            </tr>
                            </thead>
                            <tbody>
                            <tr v-for="(obj, index2) in fabricObjects.get('anything')" :key="'anything-'+index2">
                                <th>anything{{index2+1}}</th>
                                <td>{{ obj['results']['actLineLength'] }}{{ obj['results']['actLineUnit']}}</td>
                                <td>{{ obj['results']['actArea']+''+obj['results']['actAreaUnit']+'²'}}</td>
                                <td>{{ obj['results']['lineLength']}}px</td>
                                <td>{{ obj['results']['area'] +'px²'}}</td>
                            </tr>
                            </tbody>
                        </table>
                        <table id="rect-table"  class="table table-striped" v-if="fabricObjects.get('rect')!.length>0">
                            <thead>
                            <tr>
                                <th>Rectangle</th>
                                <th>Width</th>
                                <th>Height</th>
                                <th>Perimeter</th>
                                <th>Area</th>
                                <th>Pixel Width</th>
                                <th>Pixel Height</th>
                                <th>Pixel Perimeter</th>
                                <th>Pixel Area</th>
                            </tr>
                            </thead>
                            <tbody>
                            <tr v-for="(obj, index2) in fabricObjects.get('rect')" :key="'rect-'+index2">
                                <th>rect{{index2+1}}</th>
                                <td>{{ obj['results']['actWidth'] }}{{ obj['results']['actWidthUnit']}}</td>
                                <td>{{ obj['results']['actHeight'] }}{{ obj['results']['actHeightUnit']}}</td>
                                <td>{{ obj['results']['actLineLength'] }}{{ obj['results']['actLineUnit']}}</td>
                                <td>{{ obj['results']['actArea']+''+obj['results']['actAreaUnit']+'²'}}</td>

                                <td>{{ obj['results']['width'] }}px</td>
                                <td>{{ obj['results']['height'] }}px</td>
                                <td>{{ obj['results']['lineLength'] }}px</td>
                                <td>{{ obj['results']['area'] +'px²'}}</td>
                            </tr>
                            </tbody>
                        </table>
                        <table id="circle-table" class="table table-striped" v-if="fabricObjects.get('circle')!.length>0">
                            <thead>
                            <tr>
                                <th>Circle</th>
                                <th>Radius</th>
                                <th>Perimeter</th>
                                <th>Area</th>
                                <th>Pixel Radius</th>
                                <th>Pixel Perimeter</th>
                                <th>Pixel Area</th>
                            </tr>
                            </thead>
                            <tbody>
                            <tr v-for="(obj, index2) in fabricObjects.get('circle')" :key="'circle-'+index2">
                                <th>circle{{index2+1}}</th>
                                <td>{{ obj['results']['actRadius'] }}{{ obj['results']['actRadiusUnit']}}</td>
                                <td>{{ obj['results']['actLineLength'] }}{{ obj['results']['actLineUnit']}}</td>
                                <td>{{ obj['results']['actArea']+''+obj['results']['actAreaUnit']+'²'}}</td>

                                <td>{{ obj['results']['radius'] }}px</td>
                                <td>{{ obj['results']['lineLength'] }}px</td>
                                <td>{{ obj['results']['area'] +'px²'}}</td>
                            </tr>
                            </tbody>
                        </table>


                    </div>
                </div>
                <div class="modal-footer">
                    <button @click="exportDetailLabels" type="button" class="btn btn-primary text-white">Export to Excel</button>
                </div>
            </div>
        </div>
    </div>

</template>

<script lang="ts" setup>
import {onMounted, reactive, ref} from "vue";
import {figureSeparationBar, toolBarIcons} from "@/core/plugins/DrawEditor/toolbars";
import {measureCircle,
    measureLine,
    measurePoly,
    measureRect,
    showTextInfo,
    getRandomColor,
    validateLabelText,
    isIntersection,
} from "@/core/tools/MathUtil";
import {
    drawCircle,
    drawLine,
    drawRect,
    drawText,
    drawMark,
    drawPolygon,
    getFabricCanvasById,
    getPoint,
    getViewerById,
    initSeaDragon,
    movingLineEndPoint,
} from "@/core/plugins/DrawEditor/overlay";
import DrawOptionModal from "@/views/projects/figure-separation/draw-option-modal.vue"  //不能删除
import {downloadImgFile} from "@/core/tools/ExportUtil";
import {getResults, measureAnythingPoint, initMeasureImage} from "@/api/projects/interactive-measurement";
// 下面是绘图工具
// 弹窗
import Swal from "sweetalert2";
import {Modal, Toast} from "bootstrap";
import {useRoute, useRouter} from "vue-router";
import { writeFile, utils  } from "xlsx";
import OpenSeadragon from "openseadragon";
const emit = defineEmits(['show-draw-panel'])

const router = useRouter();
const route = useRoute();

const resultId:string = route.params.resultId as string;
let barResults:any = {};
const maxId = ref(0); // 最大id  用于生成唯一id 放在scale 和label上面
const boundaryMsg = ref("") // 超出边界、是否是一个矩形的等的提示Toast
const isActive = ref(false);  // 总的 某一个开关是否激活
const isLoadSAM = ref(false)    // 是否已经加载SAM模型
const currentToolType = ref("");  // 当前是哪一一个工具类型
const isEditScaleBar=ref(false);  // 是否是编辑比例尺状态
const isShowScaleBar=ref(true);  // 是否显示比例尺标签
const isBarLengthDisabled=ref(true);  // 是否可以编辑比例尺长度
const isActLengthDisabled=ref(true);  // 是否可以编辑比例尺长度
const reAddActLengthButton=ref(false);  // 是否可以重新添加比例尺长度
const reAddBarLengthButton=ref(false);  // 是否可以重新添加比例尺长度
const mousePoint = reactive({   // 当前鼠标的位置
    x:0,
    y:0
})

const drawOptions = {
    "originX": "left",
    "originY": "top",
    "opacity": "0.6",
    "textBackgroundColor": "#fefefe",
    "fill": "transparent",

    "selectable": false,
    "color": "#F43F61",
    "drawWidth": 5,

    "fontSize": 15,
    "textColor": "#009EF7",
    "strokeWidth": 2,
    "stroke": "#F43F61",
}
const initOptions = {
    canvasId: "canvasDiv",
    ppm: 0,  // 如果ppm为0表示没有比例尺 使用像素
    img_width: 0, // TODO 检查这么设置能否正常响应。
    img_height: 0,
    img_url:0,
}
let currentState: string = ""   // 当前的绘制状态
const fabricObjects = ref(new Map<string, Array<any>>())   // 储存所有完成绘制的对象
for (let i = 0; i < toolBarIcons.length; i++) {
    if (toolBarIcons[i].type == "draw" && toolBarIcons[i].drawType != "edit") {
        fabricObjects.value.set(toolBarIcons[i].drawType, [])
    }
}
const scale_keys = ["bars", "labels"]   // 储存识别的scale key值
const draw_keys = ["anything","line", "poly", "rect", "circle", "text"]   // 储存识别的draw key值
for (let i = 0; i < scale_keys.length; i++) {
    fabricObjects.value.set(scale_keys[i], [])
}

// TODO 添加图中不存在的scale text
const scaleInfo =reactive( {
    "barLength": 0,
    "actLength": "",
    "ppm": 1,
    "isBar": false,
    "isLabel": false,
    "isppm": false,
})

let currentDrawObject = {
    "objects": new Array(),
    "starts": new Array(),
    "ends": new Array(),
    "texts": new Array(),
    "points": new Array(),
    "results": {},
}
let is_drawing = false;
const initCurrentObj = () => {
    currentDrawObject = {
        "objects": new Array(),
        "starts": new Array(),
        "ends": new Array(),
        "texts": new Array(),
        "points": new Array(),
        "results": {},
    }
}

// 一上来先初始化一下
onMounted(() => {
    // 获取识别的bar和label
    getResults({resultId}).then((response) => {
        if (response["code"] == 200) {
            barResults = response.data;
            init(barResults);
        }else {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Error when get results! ' + response["msg"]
            }).then(() => {
                router.push({name: "figure-separation"})
            })
        }
    }).catch((error) => {
        console.log(error)
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: "You don‘t have permission for this file!"
        }).then(() => {
            router.push({name: "interactive-measurement"})
        })
    })
    // 准备测量对象 加载SAM模型
    initMeasureImage({resultId}).then((response) => {
        console.log(response)
        if (response["code"]==200){
            isLoadSAM.value = true
            // Swal.fire({
            //     icon: 'success',
            //     title: 'Success',
            //     text: 'Load SAM success! you can start measure anything now!'
            // })
        }
    }).catch((error) => {
        isLoadSAM.value = false
        console.log(error)
        // Swal.fire({
        //     icon: 'error',
        //     title: 'Oops...',
        //     text: "Load SAM error! You can use other tools to measure."
        // })
    });
});

const init = (results) => {
    console.log(results)
    initOptions.ppm = Math.round(results.ppi);
    initOptions.img_width = results.width;
    initOptions.img_height = results.height;
    initOptions.img_url = results.name;
    initSeaDragon(initOptions);
    initResults(results);
    // 初始化放大倍率
    const viewer = getViewerById(initOptions.canvasId);
    const imgCanvas = viewer.drawer.canvas;
    const zoomInfo = imgCanvas["width"] / initOptions.img_width;
    const zoomEl = document.querySelectorAll("#zoom-num")[0];
    zoomEl.textContent = "" + zoomInfo.toFixed(2);
    // 绑定绘制事件
    const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId);
    overlayFabricCanvas.on("mouse:down", mouseDownListener);
    overlayFabricCanvas.on("mouse:move", mouseMoveListener);
    // 绑定修改事件 监听选中物体事件 只有线条这种形式需要一下子都选中。
    overlayFabricCanvas.on({
        "selection:updated": editSelectedEventListener,   // 更新的时候触发
        "selection:created": editSelectedEventListener,   // 选中的时候触发
    });
    overlayFabricCanvas.on({
        "object:scaling": editScaledListener,   // 更新的时候触发
    });
    overlayFabricCanvas.on({
        "text:changed": editTextListener,   // 更新的时候触发
    });
    // 鼠标的箭头十字
    const ch = document.getElementById("crosshair-h");
    const cv = document.getElementById("crosshair-v");
    const canvasFrame = document.getElementById("canvasFrame");
    canvasFrame?.addEventListener("mousemove", (event: Event) => {
        const e = event as MouseEvent;
        ch!.style.display = "block";
        cv!.style.display = "block";
        ch!.style.top = e.pageY + "px";
        cv!.style.left = e.pageX + "px";
    });
    canvasFrame?.addEventListener("mouseout", (event: Event) => {
        ch!.style.display = "none";
        cv!.style.display = "none";
    });
    // 初始化状态
    changeDrawType(currentState);
}

// 初始化检测的标签结果
const initResults = (results) => {
    // 初始化每一个对象
    maxId.value = 0;// 每次开始前都初始化最大id
    for (let key of ["bars", "labels"]) {
        for (let obj of results[key]) {
            // 初始化最大id;
            if (obj["id"] > maxId.value) {
                maxId.value = obj["id"]
            }
            initOneObject(key, obj);
        }
    }
    // 更新比例尺信息
    if (results.ppi==0){
        scaleInfo.isppm = false;
        scaleInfo.ppm = 0;
    }else {
        scaleInfo.isppm = true;
        scaleInfo.ppm = Math.round(results.ppi);
    }
    console.log(scaleInfo)

    // 最后再随机一个颜色
    drawOptions.stroke = getRandomColor(-1);
}

// 初始化一个目标
const initOneObject = (category, obj) => {
    const points = [{
        "x": obj["points"][0][0],
        "y": obj["points"][0][1],
    }, {
        "x": obj["points"][1][0],
        "y": obj["points"][1][1],
    }];
    const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId)
    drawOptions.stroke = getRandomColor(-1)
    const rect = drawRect(points, drawOptions, overlayFabricCanvas, obj["id"]);
    currentDrawObject.objects.push(rect);
    currentDrawObject.points = points;
    currentDrawObject.results = obj;
    if (category == "labels") {
        if (!("text" in obj)) {
            obj["text"] = ""
        }
        const text = drawText(obj["text"], obj["id"], points, drawOptions, overlayFabricCanvas);
        currentDrawObject.texts.push(text);
        // 更新比例尺信息
        if(obj["text"]!=""){
            scaleInfo.isLabel = true;
        }else {
            scaleInfo.isLabel = false;
        }
        scaleInfo.actLength = obj["text"];
    }else{
        // 更新比例尺信息
        scaleInfo.isBar = true;
        scaleInfo.barLength = Math.abs(obj["points"][1][0] - obj["points"][0][0]);
    }
    fabricObjects.value.get(category)!.push(currentDrawObject);
    initCurrentObj();
}

// 导出结果
const exportDetailLabels = () => {
    console.log("exportDetailLabels")
    const workbook = utils.book_new();
    for (let key of ["anything","line", "poly","rect", "circle"]) {
        const data = document.getElementById(key+"-table");
        if (data){
            const worksheet = utils.table_to_sheet(data)
            utils.book_append_sheet(workbook, worksheet, key);
        }
    }
    if (workbook.SheetNames.length==0){
        Swal.fire({
            title: "No data to export!",
            buttonsStyling: false,
            confirmButtonText: "OK",
            customClass: {
                confirmButton: "btn fw-bold btn-primary text-white",
            },
        });
        return;
    }
    writeFile(workbook, "export.xlsx");
}


// 是否显示scalebar
const showHideScaleBar = () => {
    if (isEditScaleBar.value){
        return;
    }
    isShowScaleBar.value = !isShowScaleBar.value;
    const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId);
    for(let key of scale_keys){ // labels和bars
        for (let obj of fabricObjects.value.get(key)!) {
            for (let o of obj.objects) {
                o.visible = isShowScaleBar.value;
            }
            for (let o of obj.texts) {
                o.visible = isShowScaleBar.value;
            }
        }
    }
    overlayFabricCanvas.renderAll();
}
const reAddBarLabel = (types)=>{
    if(types=="bars") {
        scaleInfo.isBar = false;
        changeDrawType(types);
        reAddBarLengthButton.value = false;
    }else {
        scaleInfo.isLabel = false;
        changeDrawType(types);
        reAddActLengthButton.value = false;
    }

}

// 新增bar 或 label
const addBarLabel = (types) =>{
    Swal.fire({
        position: 'top-end',
        title: "Do the image have "+types+"?",
        buttonsStyling: false,
        showCancelButton: true,
        confirmButtonText: `Yes, label it in the image`,
        cancelButtonText: "No, input it directly",
        customClass: {
            confirmButton: "btn btn-sm fw-bold btn-success text-white me-2",
            cancelButton: "btn btn-sm fw-bold btn-primary text-white",
        },
    }).then((result) => {
        // 结果上添加result.value，标签的text
        console.log(result)
        if(result.isConfirmed){
            changeDrawType(types);
        }else if(String(result.dismiss) == "cancel"){
            isEditScaleBar.value = true;  // 进入编辑状态
            if(types=="bars") {
                scaleInfo.isBar = true;
                isBarLengthDisabled.value = false;
                reAddBarLengthButton.value = false;
            }else {
                scaleInfo.isLabel = true;
                isActLengthDisabled.value = false;
                reAddActLengthButton.value = false;
            }
        }else{
            return
        }
    });
}
const updateAllScaleInfo = (newPPM)=>{
    console.log(fabricObjects.value)
    for (let key of draw_keys){
        if(key!="text"){
            const drawObjects = fabricObjects.value.get(key)
            for (let obj of drawObjects!){
                const results = obj.results;
                results["ppm"] = newPPM;
                let newResults = results;
                let newTextInfo = "";
                if (key=="rect"){
                    newResults = measureRect(results["width"],results["height"],results["ppm"]);
                    newTextInfo = showTextInfo(newResults,"rect",false)
                }else if (key=="circle"){
                    newResults = measureCircle(results["radius"],results["ppm"]);
                    newTextInfo = showTextInfo(newResults,"circle",false)
                }else if (key=="poly"){     // TODO 每一条线的单独修改 不是texts[0]
                    newResults = measurePoly(obj.points,results["ppm"]);
                    newTextInfo = showTextInfo(newResults,"poly",false)
                    for(let i=0;i<obj.points.length;i++){
                        if(i+1<obj.points.length){
                            const lineResults = measureLine(obj.points[i],obj.points[i+1],results["ppm"]);
                            const lineTextInfo = showTextInfo(lineResults,"line",false);
                            obj.texts[i].set("text",lineTextInfo);
                        }else {
                            const lineResults = measureLine(obj.points[i],obj.points[0],results["ppm"]);
                            const lineTextInfo = showTextInfo(lineResults,"line",false);
                            obj.texts[i].set("text",lineTextInfo);
                        }

                    }
                }else if (key=="line"){
                    newResults = measureLine(obj.points[0],obj.points[1],results["ppm"]);
                    newTextInfo = showTextInfo(newResults,"line",false)
                }else if (key=="anything"){
                    newResults = measurePoly(obj.points,results["ppm"]);
                    newTextInfo = showTextInfo(newResults,"poly",false)
                }
                if (obj.texts.length>0){
                    obj.texts[obj.texts.length-1].set("text",newTextInfo);
                }
                obj.results = newResults;
            }
        }
    }

}


// 修改scale bar  做的只是切换状态
const editScaleBar = ()=>{
    if(is_drawing){ // 如果是正在绘制 删掉当前绘制的东西
        const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId)
        console.log(currentDrawObject);
        // 直接删除当前对象即可 同时初始化currentDrawObject
        for(let key of Object.keys(currentDrawObject)){
            if (key!="results" && key!="points"){
                if (currentDrawObject[key].length>0){
                    for (let kclss of currentDrawObject[key]){
                        overlayFabricCanvas.remove(kclss)
                    }
                }
            }
        }
        is_drawing=false;
        initCurrentObj()
    }
    if (currentState!=""){
        changeDrawType(""); // 切换到默认状态
    }
    if (!isShowScaleBar.value){ // 如果没有显示，那么就显示
        showHideScaleBar();
    }
    if (isEditScaleBar.value){  // 如果当前是编辑状态  判断能否确定结果 关闭编辑状态
        // 先判断当前的label格式是否正确
        let newLabel = scaleInfo.actLength;  // 默认处理的是额外添加的
        let oldLabel = "";
        if (fabricObjects.value.get("labels")!.length>0){ // 这里的是绘图绘制的
            newLabel = fabricObjects.value.get("labels")![0].texts[0].text;
            oldLabel = fabricObjects.value.get("labels")![0].results.text;
        }
        // TODO 如果new label变成空了的话就找不到这个字符串了
        let {isValidate, actm, acttext, msg}= validateLabelText(newLabel);
        // 如果bar==0 并且actLength="" 那么就是没有scalebar
        if (scaleInfo.barLength<=0 && acttext==""){
            isValidate = true;
            scaleInfo.barLength = 0;
            actm = 1;
        }else if(scaleInfo.barLength<=0){
            isValidate = false;
            msg = "The length of scale bar must be greater than 0";
        }
        if (!isValidate){
            Swal.fire({
                title: 'Error!',
                text: msg,
                icon: 'error',
                confirmButtonText: 'Noted'
            }).then((result) => {
                if (result.isConfirmed) {
                    return;
                }
            })
            return;
        }
        scaleInfo.actLength = acttext;
        scaleInfo.ppm = Math.round(scaleInfo.barLength/actm);
        if(fabricObjects.value.get("labels")!.length>0){
            fabricObjects.value.get("labels")![0].results.text = acttext;
        }
        // TODO 修改一系列信息， 考虑保存到数据库
        initOptions.ppm = scaleInfo.ppm;
        const viewer = getViewerById(initOptions.canvasId);
        if (initOptions.ppm==0){
            // @ts-ignore
            viewer.scalebar({
                pixelsPerMeter: 1,
                sizeAndTextRenderer: OpenSeadragon["ScalebarSizeAndTextRenderer"].PIXEL_LENGTH,
            });
        }else {
            // @ts-ignore
            viewer.scalebar({
                pixelsPerMeter: initOptions.ppm,
                sizeAndTextRenderer: OpenSeadragon["ScalebarSizeAndTextRenderer"].METRIC_LENGTH,
            });
        }

        updateAllScaleInfo(initOptions.ppm);
    }
    // 改变能否编辑的状态
    isEditScaleBar.value=!isEditScaleBar.value;
    const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId);
    for(let key of scale_keys){ // labels和bars
        if(fabricObjects.value.get(key)!.length==0){  // 如果没有绘制过，就设计可以修改那两个信息
            if(key=="bars"){
                isBarLengthDisabled.value = !isEditScaleBar.value;
                reAddBarLengthButton.value = isEditScaleBar.value;
            }else {
                isActLengthDisabled.value = !isEditScaleBar.value;
                reAddActLengthButton.value = isEditScaleBar.value;
            }
        }
        for (let obj of fabricObjects.value.get(key)!) {
            for (let o of obj.objects) {
                o.set("selectable", isEditScaleBar.value);
                o.setCoords(); // 必须加上它才能移动。 重新计算坐标
                if (isEditScaleBar.value) {
                    o.hoverCursor = "move";
                } else {
                    o.hoverCursor = "default";
                }
            }
            for (let o of obj.texts) {
                o.set("selectable", isEditScaleBar.value);
                o.set("editable", isEditScaleBar.value);
                o.setCoords(); // 必须加上它才能移动。 重新计算坐标
                o.hoverCursor = "move";
                if (isEditScaleBar.value) {
                    o.hoverCursor = "move";
                } else {
                    o.hoverCursor = "default";
                }
            }
        }
    }
    overlayFabricCanvas.discardActiveObject();
    overlayFabricCanvas.renderAll();
}


// 根据name或者data寻找是fabric中的哪个物体
const findCanvasObjectByNameOrData = (name, category, kind = "name") => {
    // 结果返回是那个物体，types是什么类型objects或者texts, 具体kclss的索引,category：物体的类别，是否存在
    const defaultResults = {"canvasObject": {}, "types": "", "index": 0, "category": "", "isExists": false}
    const findCanvasObject = (name, category, kind = "name") => {
        const aimedObjects = fabricObjects.value.get(category);
        if (aimedObjects) {// 键存在
            for (let i = 0; i < aimedObjects.length; i++) {
                const canvasObject = aimedObjects[i]
                for (let types of ["objects", "texts","starts", "ends"]) {
                    for (let j = 0; j < canvasObject[types].length; j++) {
                        if (canvasObject[types][j][kind] == name) {
                            console.log("ss",i)
                            return {"canvasObject": canvasObject, "types": types, "index": j, "category": category, "isExists": true}
                        }
                    }
                }
            }
        }
        return defaultResults   //找不到返回空值 types是在哪里找到的这个名字  不包括texts
    }
    if (category) {
        return findCanvasObject(name, category, kind)
    } else {
        for (let key of fabricObjects.value.keys()) {
            let results = findCanvasObject(name, key, kind)
            if (results.isExists) {
                return results
            }
        }
        return defaultResults
    }
}


// 监听text修改事件，能够修改text的label
const editTextListener = (event) => {
    const {canvasObject,isExists,category}=findCanvasObjectByNameOrData(event.target.name,false)
    if (isExists){
        if (category!="labels"){  // 如果是labels，那么就不能直接更新 需要confirm后才能更新 判断是否符合格式 不符合弹窗提示 返回原来的格式
            canvasObject.results.text = event.target.text;
        }
    }
}

// 监听canvas的物体选中事件
const editSelectedEventListener = (event) => {
    // 主要是fabricObjects的results更新 Object需要更新吗？  Line Poly 的更新 一动多个都动
    console.log(event)
    if (event.selected.length > 0 && (event.selected[0].type == "line" || event.selected[0].type == "poly")) {
        let selectedObj = event.selected[0]; //默认选择的是list 类型
        const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId)
        let {canvasObject, types: movingType, index} = findCanvasObjectByNameOrData(selectedObj.name, false)
        // 监听每个物体的移动事件
        if (movingType != "objects") { // 移动的是端点
            const allLineComponents = [canvasObject.starts[index], canvasObject.objects[index], canvasObject.ends[index], canvasObject.texts[index]]
            let allLineComponents2:any = [];
            let index2=index;
            // 同时控制另一个端点移动
            const originalDX = selectedObj.getCenterPoint().x;
            const originalDY = selectedObj.getCenterPoint().y;
            const originLocations = {x:0,y:0}
            let movingType2:any = movingType;
            if (selectedObj.type== "poly"){
                if (movingType == "starts") {
                    movingType2 = "ends"
                    index2 = index - 1 < 0 ? canvasObject.starts.length - 1 : index - 1;
                    originLocations.x = canvasObject.ends[index2].getCenterPoint().x;
                    originLocations.y = canvasObject.ends[index2].getCenterPoint().y;
                } else {
                    console.log(index)
                    movingType2 = "starts"
                    index2 = index + 1 < canvasObject.starts.length ? index + 1 : 0;
                    originLocations.x = canvasObject.starts[index2].getCenterPoint().x;
                    originLocations.y = canvasObject.starts[index2].getCenterPoint().y;
                }
                allLineComponents2 = [canvasObject.starts[index2], canvasObject.objects[index2], canvasObject.ends[index2], canvasObject.texts[index2]]
            }
            selectedObj.on("moving", function (options) {
                const point = {
                    x: options.transform.target.getCenterPoint().x,
                    y: options.transform.target.getCenterPoint().y,
                };

                let results = movingLineEndPoint(allLineComponents, movingType, point, initOptions.ppm)
                if (selectedObj.type=="poly"){
                    // 两个端点同时移动
                    const deltaX = selectedObj.left - originalDX;
                    const deltaY = selectedObj.top - originalDY;
                    movingLineEndPoint(allLineComponents2, movingType2, point, initOptions.ppm);
                    overlayFabricCanvas.renderAll();
                    canvasObject[movingType2][index2].set({left: originLocations.x + deltaX, top: originLocations.y + deltaY})
                    // 重新计算结果
                    canvasObject.points[index].x = point.x;
                    canvasObject.points[index].y = point.y;
                    results = measurePoly(canvasObject.points,initOptions.ppm);
                    const textInfo = showTextInfo(results,"poly",false)
                    canvasObject.texts[canvasObject.texts.length-1].set({"text":textInfo})
                }
                canvasObject.results = results;
                overlayFabricCanvas.renderAll();
            });
        } else { //移动的是中间那条线 TODO 移动成组的方式不行 所以采用如下方法 可以尝试改进  如果移动了endpointline 再移动它的话可能会出现endpointline偏移
            const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId)
            const {canvasObject} = findCanvasObjectByNameOrData(selectedObj.name, selectedObj.type)
            const originLocations: any = []
            for (let key of ["ends", "objects", "starts", "texts"]) {
                if (canvasObject[key].length > 0) {
                    for (let object of canvasObject[key]) {
                        if (object.name != selectedObj.name) {
                            originLocations.push({x: object.left, y: object.top})
                        }
                    }
                }
            }
            const originalDX = selectedObj.left;
            const originalDY = selectedObj.top;
            selectedObj.on("moving", function (options) {
                const deltaX = selectedObj.left - originalDX;
                const deltaY = selectedObj.top - originalDY;
                let i = 0;
                for (let key of ["ends", "objects", "starts", "texts"]) {
                    if (canvasObject[key].length > 0) {
                        for (let object of canvasObject[key]) {
                            if (object.name != selectedObj.name) {
                                object.set({left: originLocations[i].x + deltaX, top: originLocations[i].y + deltaY})
                                i = i + 1;
                            }
                        }
                    }
                }
                overlayFabricCanvas.renderAll();
            });
        }
    }
}
const editScaledListener = (event) => {
    // 主要是尺寸的变化 如果旋转假定是不改变大小的  默认横纵一样的比例尺 没有禁用旋转  只有Rect和circle
    let scaledObject = event.target;
    if (scaledObject.type == "rect" || scaledObject.type == "circle"){
        const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId)
        const {canvasObject, types, category, index} = findCanvasObjectByNameOrData(scaledObject.name, false)
        // 重新计算结果
        let newResults = {}
        if (scaledObject.type == "rect") {
            if (category == "bars"){  // 说明是编辑的scale bar 或者scale label
                const barLength = Math.abs(Math.round(scaledObject.width * scaledObject.scaleX));
                if (barLength == 0) {
                    return;
                }
                scaleInfo.ppm = Math.round((barLength / scaleInfo.barLength) * scaleInfo.ppm);  // 重新计算ppm 按比例变化
                scaleInfo.barLength = barLength;
                initOptions.ppm = scaleInfo.ppm;
                // 修改scalebar
                const viewer = getViewerById(initOptions.canvasId);
                //@ts-ignore
                viewer.scalebar({
                    pixelsPerMeter: initOptions.ppm,
                    sizeAndTextRenderer: OpenSeadragon["ScalebarSizeAndTextRenderer"].METRIC_LENGTH,
                })

            }
            newResults = measureRect(scaledObject.width * scaledObject.scaleX, scaledObject.height * scaledObject.scaleY, initOptions.ppm)
        } else {
            newResults = measureCircle(scaledObject.radius * scaledObject.scaleX, initOptions.ppm)
        }
        canvasObject.results = newResults;
        if (scaledObject.data == "rect" || scaledObject.data == "circle"){  // 是绘制的形状，修改文字
            if (canvasObject.texts.length > 0) {
                const textInfo = canvasObject.texts[0];
                const newTextInfo = showTextInfo(newResults, scaledObject.data, false)
                textInfo.set({"text": newTextInfo})
            }
        }
        overlayFabricCanvas.renderAll();
    }
}


const mouseMoveListener = (event) => {
    const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId);
    const point = getPoint(event, "canvasDiv");
    if(point.x<=0 || point.x>=initOptions.img_width || point.y<=0 || point.y>=initOptions.img_height){
        mousePoint.x = 0
        mousePoint.y = 0
    }else {
        mousePoint.x = Math.round(Math.min(Math.max(point.x,0), initOptions.img_width))
        mousePoint.y = Math.round(Math.min(Math.max(point.y,0), initOptions.img_height))
    }
    if (!is_drawing) {
        return
    }   //如果不是正在绘制状态直接退出

    if (currentState == "rect" || currentState == "bars" || currentState == "labels") {
        const rect = currentDrawObject.objects[0];
        const lastPoint = currentDrawObject.points[0];
        // Bug 当倒着方向绘制时 负值  到一定程度 bolder边界就会消失 所以必须重新绘制
        const left = Math.min(point.x,lastPoint.x)
        const top = Math.min(point.y,lastPoint.y)
        const right = Math.max(point.x,lastPoint.x)
        const bottom = Math.max(point.y,lastPoint.y)
        const rec_width = Math.round(right-left);
        const rec_height = Math.round(bottom-top); // 就是可以有负值 但负值显示会有bug
        rect.set({width: rec_width, height: rec_height,left:left,top:top}) // 更改宽和高
        rect.setCoords();
        if(currentState=="rect"){
            const textInfo = currentDrawObject.texts[0];
            const results = measureRect(rect.width, rect.height, initOptions.ppm);
            const showText = showTextInfo(results, currentState, false)
            textInfo.set({left: point.x, top: point.y, text: showText});
        }
        overlayFabricCanvas.renderAll();
    } else if (currentState == "circle"){
        const circle = currentDrawObject.objects[0];
        const lastPoint = currentDrawObject.points[0];
        const radius = Math.sqrt((point.x - lastPoint.x) * (point.x - lastPoint.x) + (point.y - lastPoint.y) * (point.y - lastPoint.y));
        circle.set({radius: radius});
        const textInfo = currentDrawObject.texts[0];
        const results = measureCircle(radius, initOptions.ppm);
        const showText = showTextInfo(results, currentState, false)
        textInfo.set({left: point.x, top: point.y, text: showText});
        overlayFabricCanvas.renderAll();
    } else if (currentState == "line" || currentState == "poly") {
        const startLine = currentDrawObject.starts[currentDrawObject.objects.length - 1];// 最后一个对象前一个对象是端点
        const middleLine = currentDrawObject.objects[currentDrawObject.objects.length - 1];// 最后一个对象是中间线
        const lastPoint = currentDrawObject.points[currentDrawObject.points.length - 1];// 最后一个对象是起点
        const angle = (Math.atan2(lastPoint.y - point.y, lastPoint.x - point.x) * 180) / Math.PI;
        startLine.rotate(angle);
        middleLine.set({x1: lastPoint.x, y1: lastPoint.y, x2: point.x, y2: point.y});
        const textInfo = currentDrawObject.texts[currentDrawObject.texts.length - 1];
        const results = measureLine(point, lastPoint, initOptions.ppm);
        const showText = showTextInfo(results, "line", false)
        //在中间线的中心绘制距离信息等 这里不用返回
        const middlePoint = {x: (lastPoint.x + point.x) / 2, y: (lastPoint.y + point.y) / 2};
        textInfo.set({left: middlePoint.x, top: middlePoint.y, text: showText, originX: "center", originY: "center"});
        if (angle > 90) {
            textInfo.rotate(angle - 180);
        } else if (angle < -90) {
            textInfo.rotate(angle + 180);
        } else {
            textInfo.rotate(angle);
        }
        overlayFabricCanvas.renderAll();
    }
}
// 监听鼠标点击交互事件
const mouseDownListener = (event) => {
    const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId);
    const point = getPoint(event, initOptions.canvasId);
    if (currentState == "edit") {
        return;
    }
    if (currentState == "rect") {
        if (!is_drawing) {  // 第一次点击
            const rect = drawRect([point], drawOptions, overlayFabricCanvas);
            const textInfo = drawText("", "info", [point], drawOptions, overlayFabricCanvas)
            currentDrawObject.objects.push(rect);
            currentDrawObject.texts.push(textInfo);
            currentDrawObject.points.push(point);
            is_drawing = true;
        } else { // 第二次点击绘制 将当前的绘制对象添加到这个物体中 同时清空当前的
            const rect = currentDrawObject.objects[0];
            currentDrawObject.points.push(point);
            currentDrawObject.results = measureRect(rect.width, rect.height, initOptions.ppm);
            console.log(fabricObjects.value)
            fabricObjects.value.get("rect")!.push(currentDrawObject);
            is_drawing = false
            initCurrentObj();
        }
    } else if (currentState == "circle") {
        if (!is_drawing) {  // 第一次点击
            const circle = drawCircle([point], drawOptions, overlayFabricCanvas)
            const textInfo = drawText("", "info", [point], drawOptions, overlayFabricCanvas)
            currentDrawObject.objects.push(circle);
            currentDrawObject.texts.push(textInfo);
            currentDrawObject.points.push(point);
            is_drawing = true;
        } else {
            const circle = currentDrawObject.objects[0];
            currentDrawObject.results = measureCircle(circle.radius, initOptions.ppm)
            currentDrawObject.points.push(point);
            fabricObjects.value.get("circle")!.push(currentDrawObject);
            is_drawing = false
            initCurrentObj();
        }
    } else if (currentState == "text") {
        if (event.target && event.target.selectable) { //如果点击的有对象 并且对象是可以编辑的状态就不做任何操作  TODO 当编辑的时候 再次点击空白处会多绘制
            return
        }
        const text = drawText("Double Click to Edit!", "text", [point], drawOptions, overlayFabricCanvas)
        currentDrawObject.texts.push(text)
        fabricObjects.value.get("text")!.push(currentDrawObject)
        initCurrentObj();
        changeDrawType("edit"); //切换到编辑状态
    } else if (currentState == "line") {
        if (!is_drawing) {  // 第一次点击
            const startLine = drawLine(currentState + ".starts", [point], drawOptions, overlayFabricCanvas)
            const middleLine = drawLine(currentState + ".line", [point], drawOptions, overlayFabricCanvas)
            const textInfo = drawText("", "info", [point], drawOptions, overlayFabricCanvas)
            currentDrawObject.starts.push(startLine);
            currentDrawObject.objects.push(middleLine);
            currentDrawObject.texts.push(textInfo);
            currentDrawObject.points.push(point); //记录点的位置 便于绘制
            is_drawing = true;
        } else { // 第二次点击绘制 先绘制一个端点 将当前的绘制对象添加到这个物体中 同时清空当前的    TODO 端点可以设置成不同的状态
            const endLine = drawLine(currentState + ".ends", [point], drawOptions, overlayFabricCanvas)
            // 如果是线性的最后的一个端点线应该也要旋转
            const startPoint = currentDrawObject.points[currentDrawObject.points.length - 1]
            const angle = (Math.atan2(startPoint.y - point.y, startPoint.x - point.x) * 180) / Math.PI;
            endLine.rotate(angle); // 最后端点需要旋转一下
            overlayFabricCanvas.renderAll();
            currentDrawObject.ends.push(endLine);
            currentDrawObject.results = measureLine(point, startPoint, initOptions.ppm);
            currentDrawObject.points.push(point);
            fabricObjects.value.get("line")!.push(currentDrawObject);
            is_drawing = false
            initCurrentObj();
        }
    } else if (currentState == "poly") {   //TODO 这里代码可以优化一下 跟LINE
        if (!is_drawing) {  // 第一次点击
            const startLine = drawLine(currentState + ".starts", [point], drawOptions, overlayFabricCanvas)
            const middleLine = drawLine(currentState + ".line", [point], drawOptions, overlayFabricCanvas)
            const textInfo = drawText("", "info", [point], drawOptions, overlayFabricCanvas)
            currentDrawObject.starts.push(startLine);
            currentDrawObject.objects.push(middleLine);
            currentDrawObject.texts.push(textInfo);
            currentDrawObject.points.push(point); //记录点的位置 便于绘制
            is_drawing = true;
            startLine.hoverCursor = "pointer";
        } else { // 只要不是第一次点击 就做如下判断
            // 判断是否继续绘制  是否是落在起点对象上  TODO 把起始点绘制的大一点好些 要不然识别不到了
            if (event.target &&
                event.target.name &&
                event.target.name == currentDrawObject.starts[0].name &&
                currentDrawObject.points.length > 2 // 大于两条线才能闭合 三个点
            ) {
                console.log("end")
                // 关闭鼠标样式
                event.target.hoverCursor = "crosshair";
                // 闭合poly  这个最后一个不需要添加点
                closePolyLine(overlayFabricCanvas)
            } else {
                // 不是结束就是一样的步骤
                const endLine = drawLine(currentState + ".ends", [point], drawOptions, overlayFabricCanvas)
                // 如果是线性的最后的一个端点线应该也要旋转  上一端点已经在移动过程中旋转了
                const startPoint = currentDrawObject.points[currentDrawObject.points.length - 1]
                const angle = (Math.atan2(startPoint.y - point.y, startPoint.x - point.x) * 180) / Math.PI;
                endLine.rotate(angle); // 最后端点需要旋转一下
                currentDrawObject.ends.push(endLine);
                currentDrawObject.points.push(point); //记录点的位置 便于绘制
                // 不是结束位置就多画一条起点端点线
                const startLine = drawLine(currentState + ".starts", [point], drawOptions, overlayFabricCanvas)
                const middleLine = drawLine(currentState + ".line", [point], drawOptions, overlayFabricCanvas)
                const textInfo = drawText("", "info", [point], drawOptions, overlayFabricCanvas)
                currentDrawObject.starts.push(startLine);
                currentDrawObject.objects.push(middleLine);
                currentDrawObject.texts.push(textInfo);
            }
        }
        overlayFabricCanvas.renderAll();
    }else if (currentState=="bars" || currentState=="labels"){
        if(!is_drawing){
            maxId.value = maxId.value + 1;  // 自增型的id
            // 每次绘制都给一个随机颜色
            drawOptions.stroke = getRandomColor(-1);
            const rect = drawRect([point], drawOptions, overlayFabricCanvas, maxId.value+"");
            currentDrawObject.objects.push(rect);
            currentDrawObject.points.push(point);
            is_drawing = true;
        }else{
            // 得到新画的矩形的4个点
            const left = Math.min(currentDrawObject.points[0].x, point.x)
            const top = Math.min(currentDrawObject.points[0].y, point.y)
            const right = Math.max(currentDrawObject.points[0].x, point.x)
            const bottom = Math.max(currentDrawObject.points[0].y, point.y)
            // 每次检查绘制是否符合规范
            // 判断基础的是否符合规范
            const objRec = [[left, top], [right, bottom]];
            if (!isLabelFormatRight(objRec)) {
                const toast = new Toast("#boundaryToast")
                toast.show()
                return;
            }
            // 检查通过了 才能添加这个点
            currentDrawObject.points.push(point);
            if (currentState == "labels") {
                // 校验输入的文字是否符合规范
                const inputValidators: any = (value) => {
                    if (!value) {
                        return 'You need to input text!'
                    }
                    const {isValidate,msg} = validateLabelText(value);
                    if(!isValidate){
                        return msg;
                    }
                }
                Swal.fire({
                    position: 'top-end',
                    title: "Input the text content",
                    input: 'text',
                    inputLabel: 'No need to input bracket',
                    buttonsStyling: false,
                    showCancelButton: false,
                    confirmButtonText: `Yes, confirm text content`,
                    cancelButtonText: "No, input later",
                    inputValue: "",
                    inputValidator: inputValidators,
                    customClass: {
                        confirmButton: "btn btn-sm fw-bold btn-success text-white me-2",
                        cancelButton: "btn btn-sm fw-bold btn-primary text-white",
                    },
                }).then((result) => {
                    // 结果上添加result.value，标签的text
                    let showText = result.value;
                    if (result.isConfirmed) { //确定了才绘制
                        const textObj = drawText(showText, maxId.value, [point], drawOptions, overlayFabricCanvas);
                        currentDrawObject.texts.push(textObj);
                    } else {
                        showText = "1m";
                        const textObj = drawText(showText, maxId.value, [point], drawOptions, overlayFabricCanvas);
                        currentDrawObject.texts.push(textObj);
                    }
                    // 更新scale label信息
                    const {actm, acttext}= validateLabelText(showText);
                    scaleInfo.actLength = acttext;
                    scaleInfo.isLabel = true;
                    if (scaleInfo.isBar){
                        scaleInfo.ppm = Math.round(scaleInfo.barLength/actm);
                        scaleInfo.isppm = true;
                        initOptions.ppm = scaleInfo.ppm;
                        // 修改scalebar
                        const viewer = getViewerById(initOptions.canvasId);
                        //@ts-ignore
                        viewer.scalebar({
                            pixelsPerMeter: initOptions.ppm,
                            sizeAndTextRenderer: OpenSeadragon["ScalebarSizeAndTextRenderer"].METRIC_LENGTH,
                        })
                        updateAllScaleInfo(initOptions.ppm);
                    }
                    if(isEditScaleBar.value){
                        isActLengthDisabled.value = true;
                        reAddActLengthButton.value = false;
                    }
                    currentDrawObject.results = {id: maxId.value, points: [[left, top], [right, bottom]], text: showText};
                    fabricObjects.value.get(currentState)!.push(currentDrawObject);
                    initCurrentObj(); // 不能放在后面 这里有一个then 后执行。
                    changeDrawType("")
                });
                overlayFabricCanvas.renderAll(); //不能放在弹窗里面更新 否则绘制的位置不对 原因未知
                is_drawing = false;
            }else{
                // 更新scale label信息
                scaleInfo.barLength = Math.round(right - left);
                scaleInfo.isBar = true;
                if (scaleInfo.isLabel){
                    const {actm}= validateLabelText(scaleInfo.actLength);
                    scaleInfo.ppm = Math.round(scaleInfo.barLength/actm);
                    scaleInfo.isppm = true;
                    initOptions.ppm = scaleInfo.ppm;
                    // 修改scalebar
                    const viewer = getViewerById(initOptions.canvasId);
                    //@ts-ignore
                    viewer.scalebar({
                        pixelsPerMeter: initOptions.ppm,
                        sizeAndTextRenderer: OpenSeadragon["ScalebarSizeAndTextRenderer"].METRIC_LENGTH,
                    })
                    updateAllScaleInfo(initOptions.ppm);
                }
                if(isEditScaleBar.value){
                    isBarLengthDisabled.value = true;
                    reAddBarLengthButton.value = false;
                }
                // 计算这个的results。
                currentDrawObject.results = {id: maxId.value, points: [[left, top], [right, bottom]]};
                fabricObjects.value.get(currentState)!.push(currentDrawObject);
                // 画完一个矩形后 重置状态
                initCurrentObj();
                overlayFabricCanvas.renderAll(); //不能放在弹窗里面更新 否则绘制的位置不对 原因未知
                is_drawing = false;
                changeDrawType("")
            }

        }
    } else if (currentState=="anything"){
        // 发送请求到后台
        measureAnythingPoint({points:[point]}).then((response) => {
            if (response["code"] == 200) {
                // 画标志点
                const mark = drawMark([point], drawOptions, overlayFabricCanvas);
                // 绘制polygon
                const points = response["data"]["mask"];
                for (let i=0;i<points.length;i++){
                    points[i] = {x:points[i][0],y:points[i][1]}
                }
                const polygon = drawPolygon(points, drawOptions, overlayFabricCanvas);
                // 绘制结果信息
                const textInfo = drawText("", "info", [point], drawOptions, overlayFabricCanvas)
                currentDrawObject.texts.push(textInfo);
                currentDrawObject.results = measurePoly(points,initOptions.ppm)
                const showText = showTextInfo(currentDrawObject.results, "poly", false)
                textInfo.set({text: showText});
                currentDrawObject.objects.push(polygon);
                currentDrawObject.starts.push(mark);
                currentDrawObject.points.push(...points);
                fabricObjects.value.get("anything")!.push(currentDrawObject)
                initCurrentObj();
                is_drawing = false;
                console.log(fabricObjects)
            }else {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Error when get results, please try again! ' + response["msg"]
                }).then(() => {
                    router.push({name: "interactive-measurement"})
                })
            }
        }).catch((error) => {
            console.log(error)
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: "Segment Anything Model is Loading, please wait!"
            })
            initCurrentObj();
            is_drawing = false;
        })

    }
    console.log(fabricObjects)
    console.log(currentDrawObject)
}


// 判断绘制的label是否符合基本规范
const isLabelFormatRight = (objRec) => {
    // objRec [[l,t],[r,b]]
    //  0. 判断是否是一个矩形 就是 是否是一条线 至少大于1像素
    if (Math.abs(Math.round(objRec[0][0]) - Math.round(objRec[1][0])) <= 1 || Math.abs(Math.round(objRec[0][1]) - Math.round(objRec[1][1])) <= 1) {
        boundaryMsg.value = `<div>
                Please label with a Rectangle not a Line!
              </div>
              <div>
                (Press <strong>ESC</strong> to cancel the current draw)
              </div>`;
        return false;
    }
    //  1. 当前目标是否超出了整个的画框。
    const viewer = getViewerById(initOptions.canvasId);
    const imgSize = viewer.world.getItemAt(0).getContentSize();
    const frameRec = [[0, 0], [imgSize.x, imgSize.y]];
    let isInBoundary = isIntersection(frameRec, objRec);
    if (!isInBoundary) {
        boundaryMsg.value = `<div>
                Please label within Figure boundary!
              </div>
              <div>
                (Press <strong>ESC</strong> to cancel the current draw)
              </div>`;
        // 提示请在目标内绘制
        return false;
    }
    return true;
}


// 每次点击ToolBar 都会进行下面的操作
function changeDrawType(newType: string) {
    const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId)// 获取已经建立的fabricOverlay对象
    if (newType == "anything" && currentState!="anything"){
        if(!isLoadSAM.value){   //检查SAM模型是否已经加载完成
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: "SAM model is not ready, please wait."
            })
            return
        }
    }
    if (currentToolType.value == newType) {
        isActive.value = !isActive.value;// 两次点击的一致 是开关
    } else {
        //两次点击的不一致 改变ToolBar 同时设为激活状态
        currentToolType.value = newType;
        isActive.value = true;
    }
    // 修改状态
    if (isActive.value) {
        currentState = currentToolType.value
    } else {
        currentState = ""
    }
    console.log(currentState)
    // 不同状态 设置能否编辑 和修改指针样式
    if (currentState == "edit") { //如果是修改编辑
        // 设置所有的都可以选中
        let allObjects = overlayFabricCanvas.getObjects();
        for (const obj of allObjects) {
            console.log(obj.type)
            if (obj.data && (obj.data == "starts"||obj.data == "ends")) {
                obj.hoverCursor = "pointer";  // 手指样式
            }else {
                obj.hoverCursor = "move";
            }
            if (obj.data && (obj.type == "rect" && obj.data != "rect")){
                // 如果type样式是矩形 但是data给的不是rect 就认为是scalebar框
                obj.set("selectable", false);
            }else if (obj.data && (obj.type == "polygon")){ // 如果是polygon 也不可以选中
                obj.set("selectable", false);
            }else{
                obj.set("selectable", true);
            }
            if (obj.type == "i-text") {
                if (obj.data == "text"){
                    obj.set("selectable", true);  // 只有是手动添加的文字才可以编辑
                    obj.set("editable", true);
                }else {
                    if(obj.data=="info"){
                        obj.set("selectable", true);    // info类型可以选中但是不能编辑
                    }else {
                        obj.set("selectable", false);
                    }
                    obj.set("editable", false);
                }
            }
            obj.setCoords(); // 必须加上它才能移动。 重新计算坐标
        }
        overlayFabricCanvas.defaultCursor = "default";
        overlayFabricCanvas.hoverCursor = "default";
    } else if (currentState == ""){  // 如果是空的状态
        let allObjects = overlayFabricCanvas.getObjects();
        for (const obj of allObjects) {
            obj.hoverCursor = "default";
            obj.set("selectable", false);
            obj.set("editable", false);
            obj.setCoords(); // 必须加上它才能移动。
        }
        overlayFabricCanvas.defaultCursor = "default";
        overlayFabricCanvas.hoverCursor = "default";
    }else { // 如果是绘制状态
        let allObjects = overlayFabricCanvas.getObjects();
        for (const obj of allObjects) {
            obj.hoverCursor = "crosshair";
            obj.set("selectable", false);
            obj.set("editable", false);
            obj.setCoords(); // 必须加上它才能移动。
        }
        overlayFabricCanvas.defaultCursor = "crosshair";
        overlayFabricCanvas.hoverCursor = "crosshair";
    }
    overlayFabricCanvas.discardActiveObject();
    overlayFabricCanvas.renderAll();
}

// 进行不同的函数
function doDrawFuc(func_type) {
    if (func_type == "clear") {
        Swal.fire({
            title: "Warning!",
            text: "This operation will remove all labels and draws! It cannot be undone!",
            icon: "warning",
            buttonsStyling: false,
            showCancelButton: true,
            confirmButtonText: "Ok, got it!",
            cancelButtonText: "No, return",
            customClass: {
                confirmButton: "btn fw-bold btn-warning text-white me-2",
                cancelButton: "btn fw-bold btn-primary text-white",
            },
        }).then((result) => {
            if (result.isConfirmed) {
                clearDraw();
            }
        });
    } else if (func_type == "save") {//保存图像画板
        exportDraw()
    } else if (func_type == "export") {
        console.log("export");
        // let canvasJson = JSON.stringify(overlay.fabricCanvas().toObject());
        // console.log(canvasJson);
        //TODO 导出到Excel
        exportJsonLabel()
    } else if (func_type == "setting") {
        const settingModal = new Modal("#drawOption");
        settingModal.show();
    }else if (func_type=="back"){
        emit("show-draw-panel",false)
        console.log("back")
    }
}
// 导出当前的标准json格式
const exportJsonLabel = () => {
    const jsonLabel = combineJsonLabel()
    let link = document.createElement('a')
    link.download = 'label.json'
    link.href = 'data:text/plain,' + JSON.stringify(jsonLabel)
    link.click()
}

// 综合当前的label信息
const combineJsonLabel = () => {
    // TODO 是否需要后端生成json? 暂时不需要
    const blankJson = {
        "name": "",
        "meta": {},
        "width": 0,
        "height": 0,
        "ppi":0,
        "bars": [],
        "labels":[],

        "anything":[],
        "line":[],
        "poly":[],
        "rect":[],
        "circle":[],
        "relations":[]
    }
    fabricObjects.value.forEach((arr,key:any)=>{
        for(let obj of arr){
            if (blankJson[key] && obj.results){
                blankJson[key].push(obj.results)
            }
        }
    })
    // 注意经过前端用户操作后，部分计算信息丢失，例如bar的实际长度，figure的ppi等。
    if (Object.keys(barResults).length != 0){
        const name = barResults["name"].split("\\")[barResults["name"].split("\\").length-1];
        console.log(name);
        blankJson.name = name;  // 这个name需要再处理
        blankJson.meta = barResults["meta"];
        blankJson.width = barResults["width"];
        blankJson.height = barResults["height"];
        blankJson.ppi = scaleInfo.ppm;
    }
    return blankJson
}


// 清除画板
function clearDraw() {
    const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId)// 获取已经建立的fabricOverlay对象
    overlayFabricCanvas.clear();
    // 清除fabricobjects
    for (let i = 0; i < toolBarIcons.length; i++) {
        if (toolBarIcons[i].type == "draw" && toolBarIcons[i].drawType != "edit") {
            fabricObjects.value.set(toolBarIcons[i].drawType, [])
        }
    }
    Swal.fire({
        title: "Success!",
        icon: "success",
        showConfirmButton: false,
        timer: 1550
    });
}

// 导出当前画板
function exportDraw() {
    const viewer = getViewerById(initOptions.canvasId)
    const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId)// 获取已经建立的fabricOverlay对象
    // 添加原始图片信息 记得添加：crossOriginPolicy: "Anonymous",
    let imgCanvas = viewer.drawer.canvas;
    let newCanvas = document.createElement("canvas");
    newCanvas.width = imgCanvas["width"];
    newCanvas.height = imgCanvas["height"];
    let newCtx = newCanvas.getContext("2d");
    newCtx!.drawImage(imgCanvas as HTMLCanvasElement, 0, 0);
    // 添加绘制的scaleBar
    let scalebarCanvas = viewer["scalebarInstance"].getAsCanvas();
    let location = viewer["scalebarInstance"].getScalebarLocation();
    newCtx!.drawImage(scalebarCanvas, location.x, location.y);
    let fabricImg = new Image();
    // 添加绘制的信息
    fabricImg.src = overlayFabricCanvas.toDataURL({format: "png"});
    fabricImg.onload = () => {
        newCtx!.drawImage(fabricImg, 0, 0);
        downloadImgFile(newCanvas.toDataURL(), "out.png");
    };
}

// 得到设置的绘制值 设置按钮的modal

const getDrawOptions = (editOptions) => {
    console.log(editOptions)
    drawOptions.fontSize = parseInt(editOptions.text_size);
    drawOptions.textColor = editOptions.text_color;
    drawOptions.strokeWidth = parseInt(editOptions.draw_size);
    drawOptions.stroke = editOptions.draw_color;
    if (isEditScaleBar.value){
        return;
    }
    const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId);
    for (let obj of fabricObjects.value.get("labels")!) {
        for (let o of obj.objects) {
            o.visible = editOptions.show_labels;
        }
        for (let o of obj.texts) {
            o.visible = editOptions.show_labels;
        }
    }
    for (let obj of fabricObjects.value.get("bars")!) {
        for (let o of obj.objects) {
            o.visible = editOptions.show_bars;
        }
    }
    let allObjects = overlayFabricCanvas.getObjects();
    for(let obj of allObjects){
        obj.visible = editOptions.show_draws;
        if (obj.data=="info"){
            obj.visible = editOptions.show_summary && editOptions.show_draws;
        }
    }
    updateTextInfo()

    overlayFabricCanvas.renderAll();

    console.log(drawOptions)
}
// 更新绘制信息
const updateTextInfo = () => {
    for (let key of draw_keys){
        const drawObjects = fabricObjects.value.get(key)
        for (let obj of drawObjects!){
            if (obj.texts.length>0){
                obj.texts[obj.texts.length-1].set("fontSize",drawOptions.fontSize);
                obj.texts[obj.texts.length-1].set("fill",drawOptions.textColor);
            }

        }
    }
}

// 监听删除事件
document.addEventListener("keyup", (e) => {
    if (e.ctrlKey && e.keyCode === 46) {
        console.log("delete");
        //delete快速删除
        const fabricCanvas = getFabricCanvasById(initOptions.canvasId);
        let selection = fabricCanvas.getActiveObjects();
        console.log(selection)
        if (selection.length>0) {
            if (selection[0].data == "edit" || selection[0].data == "info") {  //text类型只删除text
                fabricCanvas.remove(selection[0]);
                console.log(fabricObjects.value)
                return;
            }
            const {canvasObject,category,index} = findCanvasObjectByNameOrData(selection[0].name, false)
            console.log(canvasObject)
            for (let key of Object.keys(canvasObject)) {
                if (key != "points" && key != "results") {
                    for (let kclss of canvasObject[key]) {
                        // 不是同一个对象了 所以要从这里面找再删除
                        const toRemoves = fabricCanvas.getObjects().filter(obj => obj.name === kclss.name);
                        if (toRemoves.length>0){
                            fabricCanvas.remove(toRemoves[0])
                        }
                    }
                }
            }
            // 如果是scale类型还要再做处理
            if (category == "bars") {
                scaleInfo.isBar = false;
                scaleInfo.barLength = 0;
                scaleInfo.isppm = false;
                scaleInfo.ppm = 0;
                initOptions.ppm = scaleInfo.ppm;
                // 修改scalebar 设为pixel类型
                const viewer = getViewerById(initOptions.canvasId);
                //@ts-ignore
                viewer.scalebar({
                    pixelsPerMeter: 1,
                    sizeAndTextRenderer: OpenSeadragon["ScalebarSizeAndTextRenderer"].PIXEL_LENGTH,
                })
                updateAllScaleInfo(initOptions.ppm);
            }else if(category=="labels"){
                scaleInfo.actLength = "";
                scaleInfo.isLabel = false;
                scaleInfo.isppm = false;
                scaleInfo.ppm = 0;
                initOptions.ppm = scaleInfo.ppm;
                // 修改scalebar
                const viewer = getViewerById(initOptions.canvasId);
                //@ts-ignore
                viewer.scalebar({
                    pixelsPerMeter: 1,
                    sizeAndTextRenderer: OpenSeadragon["ScalebarSizeAndTextRenderer"].PIXEL_LENGTH,
                })
                updateAllScaleInfo(initOptions.ppm);
            }

            //先把这个对象整个的从fabricObjects移除吧 TODO  后期考虑加个状态 暂时删除
            fabricObjects.value.get(category)!.splice(index,1);
            fabricCanvas.discardActiveObject().requestRenderAll();

        }
    } else if (e.keyCode === 79) {
        // o键快速闭合 Poly
        console.log("o");
        if (is_drawing && currentState=="poly" && currentDrawObject.points.length > 2){
            currentDrawObject.starts[0].hoverCursor = "crosshair"
            // 强制闭合到原点    修改最后的绘制线
            const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId);
            closePolyLine(overlayFabricCanvas)
        }

    } else if (e.keyCode === 27) {
        //esc键关闭撤销正在绘制
        console.log("esc");
        if (is_drawing){
            const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId)
            console.log(currentDrawObject);
            // 直接删除当前对象即可 同时初始化currentDrawObject
            for(let key of Object.keys(currentDrawObject)){
                if (key!="results" && key!="points"){
                    if (currentDrawObject[key].length>0){
                        for (let kclss of currentDrawObject[key]){
                            overlayFabricCanvas.remove(kclss)
                        }
                    }
                }
            }
            is_drawing=false;
            initCurrentObj()
        }
    } else if (e.keyCode === 69) {
        //TODO 快速进入编辑界面 待增加
        console.log("TODO e快速进入编辑界面 待增加 ");
    } else if (e.ctrlKey && e.keyCode === 90) {
        //TODO 快速撤销上一步 待增加
        console.log("TODO ctrl+z快速撤销上一步 待增加 ");
    }
});

const closePolyLine = (overlayFabricCanvas) => {

    // 强制闭合到原点    修改最后的绘制线
    const startPoint = currentDrawObject.points[0]  // 第一个点
    const lastPoint = currentDrawObject.points[currentDrawObject.points.length - 1]  // 最后一个点
    const lastMiddleLine = currentDrawObject.objects[currentDrawObject.objects.length - 1]  //
    const lastStartLine = currentDrawObject.starts[currentDrawObject.starts.length - 1]  //
    const lastEndTextInfo = currentDrawObject.texts[currentDrawObject.texts.length - 1]   //  最后一个Text
    const angle = (Math.atan2(lastPoint.y - startPoint.y, lastPoint.x - startPoint.x) * 180) / Math.PI;
    lastStartLine.rotate(angle);
    lastMiddleLine.set({x1: lastPoint.x, y1: lastPoint.y, x2: startPoint.x, y2: startPoint.y});
    // 最后一个线的位置也应该回到原点
    const endLine = drawLine(currentState + ".ends", [startPoint], drawOptions, overlayFabricCanvas)
    endLine.rotate(angle);
    currentDrawObject.ends.push(endLine);
    //重新计算最后一条线的距离信息等 这里不用返回
    const lineResults = measureLine(startPoint, lastPoint, initOptions.ppm);
    const showlineText = showTextInfo(lineResults, "line", false)
    const middlePoint = {x: (lastPoint.x + startPoint.x) / 2, y: (lastPoint.y + startPoint.y) / 2};
    lastEndTextInfo.set({
        left: middlePoint.x,
        top: middlePoint.y,
        text: showlineText,
        originX: "center",
        originY: "center"
    });
    if (angle > 90) {
        lastEndTextInfo.rotate(angle - 180);
    } else if (angle < -90) {
        lastEndTextInfo.rotate(angle + 180);
    } else {
        lastEndTextInfo.rotate(angle);
    }
    // 绘制一个汇总计算信息
    const results = measurePoly(currentDrawObject.points, initOptions.ppm);
    const showText = showTextInfo(results, "poly", false)
    const textInfo = drawText(showText, "info", [startPoint], drawOptions, overlayFabricCanvas)
    currentDrawObject.texts.push(textInfo)
    currentDrawObject.results = results;
    fabricObjects.value.get("poly")!.push(currentDrawObject);
    is_drawing = false;
    initCurrentObj()
}


</script>

<style scoped lang="scss">
#crosshair-h {
  width: 100%;
}

#crosshair-v {
  height: 100%;
}

.hair {
  position: fixed;
  top: 0;
  left: 0;

  background: transparent;
  border-top: 1px dotted #000;
  border-left: 1px dotted #000;
  pointer-events: none;
  z-index: 2;
}
</style>