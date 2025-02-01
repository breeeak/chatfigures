<template>

    <div class="container-fluid px-4">
        <div class="row d-flex justify-content-center">
            <!--  左侧关系树-->
            <div class="col-2 d-flex flex-column align-items-stretch">
                <div id="treebar" class="" data-bs-spy="scroll" style="overflow: auto;height: 700px;">
                    <DTree v-model="fileTreeData" ref="fileTree" :watermark="false" :maxLevel="2"
                           :eachDraggable="onTreeDrag" :eachDroppable="onTreeDrop" :statHandler="initTreeStat"
                           @change="onTreeChange">
                        <template #default="{ node }">
                            <div class="border rounded p-1 " :style="node.color">
                                <div class="text-nowrap">
                                  <span class="symbol-label">
                                    <span class="svg-icon-light svg-icon btn btn-sm btn-hover-scale p-1">
                                      <inline-svg :src="node.icon"/>
                                    </span>
                                  </span>
                                  <span class="text-white">
                                    {{ node.text }}
                                  </span>
                                </div>
                            </div>
                        </template>
                    </DTree>
                </div>
                <div class="d-flex flex-column justify-content-end w-100" style="height: 25%">
                    <!--重新计算关系-->
                    <button @click="calcAllRelations" class="btn btn-sm btn-primary w-100 text-white mb-2"
                            type="button">
                        Calculate Label Relations
                    </button>
                    <!--名称提示-->
                    <div class="card w-100 ">
                        <div class="card-header bg-secondary">
                            <strong> {{ img_index + 1 }}: </strong> {{ img_name }}
                        </div>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item ">
                                <div class="toast-body">
                                    <div v-if="showToast">
                                        <h6 class="text-danger">{{ currentToolToast }}</h6>
                                        <div v-if="(currentStep>startStep) && isStepLabel" class="">
                                            <button type="button" @click="backToLastStep"
                                                    class="btn btn-sm btn-danger text-white">
                                                Back to last step
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </li>
                        </ul>
                    </div>
                    <!--      打开关闭drawer-->
                    <div id="allImagesBtn" class="w-100 mt-2">
                        <!--  右侧图片浏览器-->
<!--                        <AsideFigureList @changeIndex="indexChanged" :current_index="img_index"/>-->
                    </div>

                </div>

                <!--      弹窗 当前绘制状态的提示 deprecated-->
                <div class="toast-container position-fixed bottom-0 start-0 p-3">
                    <div id="liveToast" class="toast" data-bs-autohide="false" role="alert" aria-live="assertive"
                         aria-atomic="true">
                        <div class="toast-body p-2">
                            <h6 class="my-1">{{ currentToolToast }}</h6>
                            <div v-if="(currentStep>startStep) && isStepLabel" class="pt-1 border-top">
                                <button type="button" @click="backToLastStep"
                                        class="btn btn-sm btn-danger text-white p-2">
                                    Back to last step
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <!--  右侧面板-->
            <div id="panel" class="col-9 rounded border pt-5  bg-dark">
                <div class="p-5">
                    <div id="toolbar" class=" d-flex align-items-center justify-content-center flex-wrap  bg-dark pb-5">
                        <!--begin::Symbol-->
                        <template v-for="(item, index) in labelBarIcons" :key="index">
                            <!--        func TODO 1. 盒子模型有点问题 点击空白处也会 出发事件 2. DrawType改成ENUM -->
                            <div
                                    class="symbol symbol-50px me-5 mt-5"
                                    @click="changeDrawType(item.drawType,index)"
                                    :title="item.tips"
                                    v-if="item.type == 'draw'">
                                <span class="symbol-label" :class=" currentToolType == item.drawType && isActive ? 'bg-light-warning' : ''">
                                  <span :class="currentToolType == item.drawType && isActive ? 'svg-icon-danger' : ''"
                                          class="svg-icon svg-icon-2x btn btn-hover-scale">
                                    <inline-svg :src="item.icon"/>
                                  </span>
                                </span>
                            </div>
                            <!--        info-->
                            <div
                                    v-if="item.type == 'info'"
                                    class="symbol symbol-50px me-5  mt-5 justify-content-center d-flex"
                                    :title="item.tips">
                                <span class="symbol-label w-75px fw-bold" :id="item.drawType"></span>
                            </div>
                            <!--        osd-->
                            <div class="symbol symbol-50px me-5  mt-5"
                                    :title="item.tips"
                                    v-if="item.type == 'osd'">
                              <span class="symbol-label">
                                <span class="svg-icon-danger svg-icon svg-icon-2x btn btn-hover-scale" :id="item.drawType">
                                  <inline-svg :src="item.icon"/>
                                </span>
                              </span>
                            </div>
                            <!--        func-->
                            <div
                                    class="symbol symbol-50px me-5  mt-5"
                                    :title="item.tips"
                                    v-if="item.type == 'func'"
                                    @click="doDrawFuc(item.drawType)">
                                <span class="symbol-label">
                                  <span class="svg-icon-primary svg-icon svg-icon-2x btn btn-hover-scale" >
                                    <inline-svg :src="item.icon"/>
                                  </span>
                                </span>
                            </div>
                            <!--        separate-->
                            <div class="me-5" v-if="item.type == 'separate'"></div>
                        </template>
                    </div>
                    <!--end::Item-->
                </div>
                <div id="canvasFrame">
                    <div
                            id="canvasDiv"
                            class="canvasDiv h-700px border-dashed mx-0 px-0 mb-5"
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
    <draw-option-modal id="drawOption" :isLabelVue="true" @setDrawOptions="getDrawOptions"/>
</template>

<script lang="ts" setup>
import {onMounted, ref, reactive} from "vue";
import {getToken, setToken} from "@/core/services/JwtService";
//import AsideFigureList from "@/views/projects/figure-labeler/aside-figure-list.vue";
//import {blankStdJson} from "@/core/mocks/figure_label";
import {labelBarIcons} from "@/core/plugins/DrawEditor/toolbars";
import {
    isIntersection,
    getRandomColor,
    getIntersectionArea
} from "@/core/tools/MathUtil";
import {
    drawRect,
    drawText,
    getFabricCanvasById,
    getPoint,
    getViewerById,
    initSeaDragon,
} from "@/core/plugins/DrawEditor/overlay";
import {LabelStateEnum as StateEnum} from "@/core/plugins/DrawEditor/overlay";
import DrawOptionModal from "@/views/projects/figure-labeler/draw-option-modal.vue"  //不能删除
import {downloadImgFile} from "@/core/tools/ExportUtil";
import {getNewLabel} from "@/api/projects/figure-labeler";
// 下面是绘图工具
// 弹窗
import Swal from "sweetalert2";
import {Modal, Toast} from "bootstrap";
// 分步提示
import Driver from 'driver.js';
import 'driver.js/dist/driver.min.css';

// 关系图
import type {Draggable} from '@he-tree/vue'
import {Draggable as DTree} from '@he-tree/vue'
import '@he-tree/vue/style/default.css'

// 字体图标
import {library} from '@fortawesome/fontawesome-svg-core'
import {faEye, faEyeSlash} from '@fortawesome/free-solid-svg-icons'
import {useRouter} from "vue-router";

//页面加载完成前先请求results样式
// const results: any = await getLabel(1); // 这个是前端的加载方式
let img_index = ref(0);    // 储存后台数据的第几个
const router = useRouter();
// 从cookie中拿到img_index
let img_index_cookie = getToken("img_index");
console.log(img_index_cookie)
if (img_index_cookie) {
    // TODO 有可能后天没有这个index导致报错
    img_index.value = parseInt(img_index_cookie);
} else {
    setToken("img_index", img_index.value.toString());
}
const img_name = ref("");  // 储存后台数据的第几个
let labelResults = {};
const fileTreeData: any = ref([]);
let currentTreeId: any = ref(0);
const emit = defineEmits(['show-draw-panel'])
const showLastButton = ref(false);  // 总的 某一个开关是否激活
const showToast = ref(false);  // 总的 是否提示当前状态
const isActive = ref(false);  // 总的 某一个开关是否激活
const currentToolType = ref("");  // 当前是哪一一个工具类型
const currentToolToast = ref("");  // 当前工具类型的提示
const boundaryMsg = ref("") // 超出边界、是否是一个矩形的等的提示Toast
const isStepLabel = ref(false);  // 总的 是否是正在逐步标记 一开始是false,除非设置isStepLabelSetting为true,且点击figure
const isStepLabelSetting = ref(false);  // 总的 设置的是否是逐步标记
let maxId = 0;  // 用于存储每一个对象的id number 自增型
const initOptions = {
    canvasId: "canvasDiv",
    ppm: 0,  // 如果ppm为0表示没有比例尺 使用像素
    img_width: 0,
    img_url: 0,
}
let currentState: string = StateEnum.NO_STATE   // 当前的绘制状态
let startStep = ref(-1); // 当顺序标记时初始的步骤 0=>figure,1=>figureno,2=>scalebar, 3=>bar label，-1不是任何状态
let currentStep = ref(-1);
const fabricObjects = ref(new Map<string, Array<any>>())   // 储存所有完成的对象
let currentTreeDragData: any = false;  // 当前拖拽的树对象
for (let key of Object.values(StateEnum)) {
    if (key != StateEnum.NO_STATE && key != StateEnum.EDIT) {
        fabricObjects.value.set(key, [])
    }
}
let relations: any = []// 储存所有的对象关系

let currentDrawObject = {
    "objects": new Array(),
    "texts": new Array(),
    "points": new Array(),
    "results": {},
}
let is_drawing = false;
const initCurrentObj = () => {
    currentDrawObject = {
        "objects": new Array(),
        "texts": new Array(),
        "points": new Array(),
        "results": {},
    }
}
// 初始化一个目标
const initOneResult = (category, category_index, results) => {
    const points = [{
        "x": results["points"][0][0],
        "y": results["points"][0][1],
    }, {
        "x": results["points"][1][0],
        "y": results["points"][1][1],
    }];
    const icon = labelBarIcons[category_index].icon;
    let showText = labelBarIcons[category_index].shortTitle;
    const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId)
    drawOptions.stroke = getRandomColor(-1)
    console.log(results["points"], 1)
    const rect = drawRect(points, drawOptions, overlayFabricCanvas, results["id"]);
    currentDrawObject.objects.push(rect);
    currentDrawObject.points = points;
    currentDrawObject.results = results;
    if (category == StateEnum.FIGURE_NOS || category == StateEnum.LABELS) {
        if (!("text" in results)) {
            results["text"] = ""
        }

        const text = drawText(results["text"], results["id"], points, drawOptions, overlayFabricCanvas);
        showText = showText + results["text"]
        currentDrawObject.texts.push(text);
    }
    fabricObjects.value.get(category)!.push(currentDrawObject);
    initCurrentObj();
    // 初始化tree;
    const tree = {
        "text": showText + "-" + results["id"],
        "type": category,
        "id": results["id"],
        "icon": icon,
        "color": {"background-color": drawOptions.stroke},  //先随机给一个颜色，后面再把相同的设置成同一颜色
        "children": []
    }
    return tree
}

// 初始化检测的标签结果
const initResults = (results) => {
    const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId)
    const allTrees: any = {}
    let index = 0;
    maxId = 0;// 每次开始前都初始化最大id
    for (let key of fabricObjects.value.keys()) {
        if (!(key in results)) {
            continue
        }
        for (let figure of results[key]) {
            // 初始化最大id;
            if (figure["id"] > maxId) {
                maxId = figure["id"]
            }
            const tree = initOneResult(key, index, figure);
            allTrees[figure["id"]] = tree;
        }
        index = index + 1;
    }
    // 初始化关系
    relations = results["relations"];
    if (!("relations" in Object.keys(results))) {
        relations = []
    }
    // 按照关系来设置相同的颜色
    for (let i = 0; i < relations.length; i++) {
        const strokeColor = getRandomColor(i);
        let startKey = 0;
        for (let j = 0; j < relations[0].length; j++) {
            if (relations[i][j] > 0) {
                const toRemoves = overlayFabricCanvas.getObjects().filter(obj => obj.data === relations[i][j]);
                if (toRemoves.length > 0) {
                    toRemoves[0].set({stroke: strokeColor});
                }
                // 关系的填充
                allTrees[relations[i][j]]["color"]["background-color"] = strokeColor;
                if (startKey != 0) {
                    allTrees[startKey]["children"].push(allTrees[relations[i][j]]);
                    allTrees[relations[i][j]] = false; // 这个id用过了就不能再用了。
                } else {
                    startKey = relations[i][j]
                }
            }
        }
    }
    const tempTree: any = []
    // 初始化关系图
    for (let obj of Object.values(allTrees)) {
        if (obj) {
            tempTree.push(obj)    // 是否要把没有关系的放在最后再说吧
        }
    }
    fileTreeData.value = tempTree; // 这个插件必须用等号赋值才可以更新数据
    overlayFabricCanvas.renderAll();
    // 默认先不初始化完成后将鼠标指针改变
    const currentStateToken = getToken("currentState");
    currentState = StateEnum.NO_STATE;
    let typeIndex = 0;
    if (currentStateToken) {
        currentToolType.value = "";
        for (let key of Object.values(StateEnum)) {
            if (key == currentStateToken) {
                currentState = currentStateToken;
                break;
            }
            typeIndex++;
        }
    }
    changeDrawType(currentState, typeIndex - 1);
}

// 初始化数据
const init = (results) => {
    console.log(results)
    initOptions.ppm = results.ppi;
    initOptions.img_width = results.width;
    initOptions.img_url = results.name;
    img_name.value = results.name.split("\\")[results.name.split("\\").length - 1];
    console.log(img_name.value)
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
    const canvasFrame = document.querySelectorAll("#canvasFrame")[0];
    canvasFrame.addEventListener("mousemove", (event: Event) => {
        const e = event as MouseEvent;
        ch!.style.display = "block";
        cv!.style.display = "block";
        ch!.style.top = e.pageY + "px";
        cv!.style.left = e.pageX + "px";
    });
    canvasFrame.addEventListener("mouseout", (event: Event) => {
        ch!.style.display = "none";
        cv!.style.display = "none";
    });
}

// 一上来先初始化一下
onMounted(() => {
    //加载完成后初始化
    getNewLabel({
        "type": "current",
        "save": false,
        "index": img_index.value,
        "results": {},
    }).then((response) => {
        if (response["code"] == 200) {
            console.log(response)
            labelResults = response.data.results;
            init(labelResults);
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Error when get results! ' + response["msg"]
            }).then(() => {
                //router.push({name: "figure-separation"})
            })
        }
    }).catch((error) => {
        console.log(error)
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: "You don‘t have permission for this file!"
        }).then(() => {
            //router.push({name: "figure-separation"})
        })
    })

    // 绑定下一张图片
    const nextImg: HTMLElement | null = document.getElementById("next_img");
    nextImg?.addEventListener("click", (e) => {
        doNewLabel("next")
    })
    // 绑定上一张图片
    const lastImg: HTMLElement | null = document.getElementById("last_img");
    lastImg?.addEventListener("click", (e) => {
        doNewLabel("last")
    });
    // 提示信息
    const driver = new Driver({
        showButtons: false, // Do not show control buttons in footer
        keyboardControl: true, // Allow controlling through keyboard (escape to close, arrow keys to move)
        overlayClickNext: true,
        opacity: 0.75,
        className: 'bg-light',
    });

// Define the steps for introduction
    driver.defineSteps([
        {
            element: '#toolbar',
            popover: {
                title: 'Toolbars',
                description: 'You can add, edit new figure labels, zoom in and out, and save the results.',
                position: 'bottom-center'
            }
        },
        {
            element: '#panel',
            popover: {
                title: 'Image Panel',
                description: 'Image is shown here, \n shift + mouse scroll wheel to zoom in/out,\n hold middle mouse button to drag view',
                position: 'left'
            }
        },
        {
            element: '#treebar',
            popover: {
                title: 'Label Relationship Tree',
                description: 'Drag to make relationship between labels',
                position: 'right'
            }
        },
        {
            element: '#allImagesBtn',
            popover: {
                title: 'Click to show all images',
                description: 'Click to show all images in the right offcanvas',
                position: 'right'
            }
        },
    ]);
    // Start the introduction
    // 提示信息只运行一次
    const hasShowHelpToken = getToken("hasShowHelp");
    console.log(hasShowHelpToken)
    if (hasShowHelpToken != "1") {
        setToken("hasShowHelp", "1")
        driver.start();
    }
});
// indexChanged事件
const indexChanged = (index) => {
    console.log(index);
    img_index.value = index;
    doNewLabel("current")
}


// 上一张下一张提交到后台并重新初始化
const doNewLabel = (type, save = true) => {
    const resultJson = combineJsonLabel();
    const formData = {
        "type": type,
        "save": save,
        "index": img_index.value,
        "results": resultJson,
    }
    console.log(formData)
    getNewLabel(formData).then((data: any) => {
        if (data.code == 200) {
            labelResults = data.data.results;
            img_index.value = data.data.index;
            setToken("img_index", img_index.value.toString());
            img_name.value = labelResults["name"].split("\\")[labelResults["name"].split("\\").length - 1]
            clearDraw();
            const viewer = getViewerById(initOptions.canvasId)
            viewer.destroy();   // 清除目前所有的seadragon设置
            init(labelResults);
        }
    })
};


// 监听text修改事件，能够修改text的lablel
const editTextListener = (event) => {
    const {canvasObject, isExists} = findCanvasObjectByNameOrData(event.target.name, false)
    if (isExists) {
        canvasObject.results.text = event.target.text;
    }
    console.log(event)
    console.log(fabricObjects)
}


// 选中移动事件
const editSelectedEventListener = (event) => {
    // 主要是fabricObjects的results更新 Object需要更新吗？  Line Poly 的更新 一动多个都动
    if (event.selected.length > 0 && (event.selected[0].type == "rect")) {
        let selectedObj = event.selected[0]; //默认选择的是list 类型
        const {canvasObject, category} = findCanvasObjectByNameOrData(selectedObj.name, false)
        selectedObj.on("moving", function () {
            if (category == StateEnum.FIGURE_NOS || category == StateEnum.LABELS) {
                // 同时移动text。
                if (canvasObject.texts.length > 0) {
                    canvasObject.texts[0].set({
                        left: selectedObj.left,
                        top: selectedObj.top,
                    });
                }
            }
            const left = canvasObject.objects[0].left;
            const top = canvasObject.objects[0].top;
            const right = left + canvasObject.objects[0].width * canvasObject.objects[0].scaleX;
            const bottom = top + canvasObject.objects[0].height * canvasObject.objects[0].scaleY;
            const objRec = [[left, top], [right, bottom]];
            if (isLabelFormatRight(objRec)) {
                canvasObject.points[0].x = left;
                canvasObject.points[0].y = top;
                canvasObject.points[1].x = right;
                canvasObject.points[1].y = bottom;
                canvasObject.results.points = objRec;
            } else {// 如果不符合规范 设置不超过boundary
                console.log("out boundry")
                canvasObject.objects[0].set({
                    left: canvasObject.results.points[0][0],
                    top: canvasObject.results.points[0][1],
                })
                canvasObject.objects[0].setCoords();
                console.log(canvasObject)
            }
        });
    }
}
const editScaledListener = (event) => {
    // 主要是尺寸的变化 TODO 需要禁用旋转
    let scaledObject = event.target;
    console.log(scaledObject.type)
    if (scaledObject.type == "rect") { // 只处理矩形
        const {canvasObject} = findCanvasObjectByNameOrData(scaledObject.name, false)
        // 重新计算结果 根据left和top 还有scaled来重新计算
        const left = canvasObject.objects[0].left;
        const top = canvasObject.objects[0].top;
        const right = left + canvasObject.objects[0].width * canvasObject.objects[0].scaleX;
        const bottom = top + canvasObject.objects[0].height * canvasObject.objects[0].scaleY;

        // 判断这次变换是否符合基本规则
        const objRec = [[left, top], [right, bottom]];
        if (isLabelFormatRight(objRec)) {
            canvasObject.points[0].x = left;
            canvasObject.points[0].y = top;
            canvasObject.points[1].x = right;
            canvasObject.points[1].y = bottom;
            canvasObject.results.points = objRec;
        } else {// 如果不符合规范 设置不超过boundary
            console.log("out boundry")
            const width = canvasObject.results.points[1][0] - canvasObject.objects[0].left;
            const height = canvasObject.results.points[1][1] - canvasObject.objects[0].top;
            const scaleX = width / canvasObject.objects[0].width;   // 只能通过它来修改
            const scaleY = height / canvasObject.objects[0].height;
            canvasObject.objects[0].set({
                left: canvasObject.results.points[0][0],
                top: canvasObject.results.points[0][1],
                scaleX: scaleX,
                scaleY: scaleY,
            })
            canvasObject.objects[0].setCoords();
            console.log(canvasObject)
        }
    }
}

// 根据name或者data寻找是fabric中的哪个物体
const findCanvasObjectByNameOrData = (name, category, kind = "name") => {
    // 结果返回是那个物体，types是什么类型objects或者texts, 具体kclss的索引,category：物体的StateEnum，是否存在
    const defaultResults = {"canvasObject": {}, "types": "", "index": 0, "category": "", "isExists": false}
    const findCanvasObject = (name, category, kind = "name") => {
        const aimedObjects = fabricObjects.value.get(category);
        if (aimedObjects) {// 键存在
            for (let i = 0; i < aimedObjects.length; i++) {
                const canvasObject = aimedObjects[i]
                for (let types of ["objects", "texts"]) {
                    for (let j = 0; j < canvasObject[types].length; j++) {
                        if (canvasObject[types][j][kind] == name) {
                            return {
                                "canvasObject": canvasObject,
                                "types": types,
                                "index": i,
                                "category": category,
                                "isExists": true
                            }
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
        for (let key of Object.values(StateEnum)) {
            let results = findCanvasObject(name, key, kind)
            if (results.isExists) {
                return results
            }
        }
        return defaultResults
    }
}

const mouseMoveListener = (event) => {
    if (!is_drawing) {
        return
    }   //如果不是正在绘制状态直接退出
    const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId);
    const point = getPoint(event, "canvasDiv");
    // 任何状态下都是绘制矩形
    const rect = currentDrawObject.objects[0];
    const lastPoint = currentDrawObject.points[0];
    // Bug 当倒着方向绘制时 负值  到一定程度 bolder边界就会消失 所以必须重新绘制
    const left = Math.min(point.x, lastPoint.x)
    const top = Math.min(point.y, lastPoint.y)
    const right = Math.max(point.x, lastPoint.x)
    const bottom = Math.max(point.y, lastPoint.y)
    const rec_width = Math.round(right - left);
    const rec_height = Math.round(bottom - top); // 就是可以有负值 但负值显示会有bug
    rect.set({width: rec_width, height: rec_height, left: left, top: top}) // 更改宽和高
    rect.setCoords();
    overlayFabricCanvas.renderAll();
}
// 监听鼠标点击交互事件
const mouseDownListener = (event) => {
    const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId);
    const point = getPoint(event, initOptions.canvasId);
    if (currentState == StateEnum.EDIT || currentState == StateEnum.NO_STATE) {
        return;
    }
    if (!is_drawing) {  // 第一次点击
        maxId = maxId + 1;  // 自增型的id
        // 是否是逐步绘制由设置决定吧 TODO 这里改设置了 只有点第一个figure的时候才是逐步绘制
        // 如果起始标记不是figure 就不能逐步绘制 并且只要开始绘制就暂时不能再拖拽目标了
        if (startStep.value != 0) {
            isStepLabel.value = false;
        } else {
            isStepLabel.value = isStepLabelSetting.value; // 可以控制开启
        }
        // 每次绘制都给一个随机颜色，除非是关系的逐步标记
        if (!(isStepLabel.value && currentStep.value != startStep.value)) {
            drawOptions.stroke = getRandomColor(-1);
        }
        const rect = drawRect([point], drawOptions, overlayFabricCanvas, maxId+"");
        currentDrawObject.objects.push(rect);
        currentDrawObject.points.push(point);
        is_drawing = true;
    } else { // 第二次点击绘制 将当前的绘制对象添加到这个物体中 同时清空当前的

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
        //  2.其他目标是否在最大的figure里。
        if (currentState != StateEnum.FIGURES && startStep.value == 0) { //当前不是figure 并且开始是figure
            // 获取这个figure
            const figureObjId = relations[relations.length - 1][0];
            if (figureObjId > 0) {
                const figureObj = findCanvasObjectByNameOrData(figureObjId, false, "data");
                console.log(figureObj)

                if (figureObj.isExists) {
                    const figureRec = figureObj.canvasObject.results.points;
                    console.log(figureRec)
                    console.log(objRec)
                    if (!isIntersection(figureRec, objRec)) {
                        // 提示请在目标内绘制
                        boundaryMsg.value = `<div>
                Please label within your Labeled Subfigure boundary!
              </div>
              <div>
                (Press <strong>ESC</strong> to cancel the current draw)
              </div>`;
                        const toast = new Toast("#boundaryToast")
                        toast.show()
                        return;
                    }
                }
            }
        }
        // 检查通过了 才能添加这个点
        currentDrawObject.points.push(point);
        // 是否是一步步的标记
        const nextStep = () => {
            // 弹窗到右上角 是否继续标记
            let showTitle: any = ""
            if (currentStep.value < 3) { // 前三步 可以跳到下一步
                showTitle = labelBarIcons[currentStep.value + 1].title;
            } else { // 第四步 直接跳到第一步
                relations[relations.length - 1][relations[0].length - 1] = maxId; //
                console.log(relations)
                // 根据状态返回到初始状态 初始状态是LABELS没有下一步的弹窗
                if (currentStep.value != startStep.value) {
                    currentStep.value = startStep.value
                    currentState = labelBarIcons[startStep.value].drawType
                    changeDrawType(currentState)
                }
                showToast.value = true;
                return;
            }
            // 前三步的提示信息 是否要一步步的标记
            Swal.fire({
                position: 'top-end',
                title: "",
                html: `<h4>Is there a corresponding</h4> <h2>${showTitle} </h2> <h4>for this subfigure?</h4>`,
                icon: "info",
                buttonsStyling: false,
                showCancelButton: true,
                confirmButtonText: `Yes, label relevant ${showTitle}`,
                cancelButtonText: "No, return start step",
                customClass: {
                    confirmButton: "btn btn-sm fw-bold btn-success text-white me-2",
                    cancelButton: "btn btn-sm fw-bold btn-primary text-white",
                },
            }).then((result) => {
                // 无论是否跳转先保留关系
                relations[relations.length - 1][currentStep.value] = maxId; //
                if (result.isConfirmed) {
                    // 跳转之前保留关系 TODO 关系的撤销，检验，修改
                    // 确定的话 就转到下一个
                    currentStep.value = currentStep.value + 1;
                    currentState = labelBarIcons[currentStep.value].drawType;
                    changeDrawType(currentState)
                } else {
                    // 如果选择返回的话
                    // 当前状态之后的都是0，表示没有状态
                    for (let i = 1; i < 4 - currentStep.value; i++) {
                        relations[relations.length - 1][currentStep.value + i] = 0;
                    }
                    // 回到最开始的状态 需要判断当前不是最开始状态才回到
                    if (currentStep.value != startStep.value) {
                        currentStep.value = startStep.value
                        currentState = labelBarIcons[currentStep.value].drawType
                        changeDrawType(currentState)
                    } else {// 如果当前就是最开始状态的话 重新啊显示toast
                        showToast.value = true;
                    }
                    // 关闭正在绘制逐步绘制
                    isStepLabel.value = false;
                }
            });
        }

        // 先关闭toast
        // showToast.value= false;
        // 对于figure no 与 bar label需要弹窗一个输入数值
        if (currentState == StateEnum.FIGURE_NOS || currentState == StateEnum.LABELS) {
            // 校验输入的字符串
            const inputValidators: any = (value) => {
                // TODO 判断输入的字符串是否是在支持的标签单位上 输入的是否包含数字
                console.log(currentState)
                console.log(value)
                if (!value) {
                    return 'You need to input text!'
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
                    const textObj = drawText(showText, maxId, [point], drawOptions, overlayFabricCanvas);
                    currentDrawObject.texts.push(textObj);
                } else {
                    showText = "NAN";
                    const textObj = drawText(showText, maxId, [point], drawOptions, overlayFabricCanvas);
                    currentDrawObject.texts.push(textObj);
                }
                currentDrawObject.results = {id: maxId, points: [[left, top], [right, bottom]], text: showText};
                fabricObjects.value.get(currentState)!.push(currentDrawObject);
                initCurrentObj(); // 不能放在后面 这里有一个then 后执行。
                // 数据的更新
                // 初始化tree;
                const tree = {
                    "text": labelBarIcons[currentStep.value].shortTitle + showText + "-" + maxId,
                    "type": currentState,
                    "id": maxId,
                    "icon": labelBarIcons[currentStep.value].icon,
                    "color": {"background-color": drawOptions.stroke},
                    "children": []
                }
                if (isStepLabel.value) {
                    if (currentStep.value == startStep.value) {//第一步的跳转先初始化
                        relations.push([-1, -1, -1, -1])//-1表示不确定，0表示没有，其他对应关联id
                        currentTreeId.value = maxId; // 最外层tree的id
                        const tempTree = Object.assign([], fileTreeData.value);
                        tempTree.push(tree); // 初始状态直接放下这个物体
                        fileTreeData.value = tempTree;
                    } else {// 只要不是初始化就使用上一次的tree,再上一次的tree children里面放入。
                        //  最外层tree的放入这个子对象
                        if (currentTreeId.value != 0) {
                            for (let treeObj of fileTreeData.value) {
                                if (treeObj.id == currentTreeId.value) {
                                    treeObj["children"].push(tree);
                                }
                            }
                        }
                        const tempTree = Object.assign([], fileTreeData.value);
                        fileTreeData.value = tempTree;
                    }
                    nextStep();//可能会改变当前状态并跳转到下一步
                } else {
                    const tempTree = Object.assign([], fileTreeData.value);
                    tempTree.push(tree); // 初始状态放下这个物体
                    fileTreeData.value = tempTree;
                    changeTreeRelation(tree.id); // 判断是否有关系存在并作出改变
                }
            });

            overlayFabricCanvas.renderAll(); //不能放在弹窗里面更新 否则绘制的位置不对 原因未知
            is_drawing = false;
        } else {
            // 计算这个的results。
            currentDrawObject.results = {id: maxId, points: [[left, top], [right, bottom]]};
            fabricObjects.value.get(currentState)!.push(currentDrawObject);

            // 数据的更新
            // 初始化tree;
            const tree = {
                "text": labelBarIcons[currentStep.value].shortTitle + "-" + maxId,
                "type": currentState,
                "id": maxId,
                "icon": labelBarIcons[currentStep.value].icon,
                "color": {"background-color": drawOptions.stroke},
                "children": []
            }
            if (isStepLabel.value) {
                if (currentStep.value == startStep.value) {//第一步的跳转先初始化
                    relations.push([-1, -1, -1, -1])//-1表示不确定，0表示没有，其他对应关联id
                    currentTreeId.value = maxId;
                    fileTreeData.value.push(tree);
                    const tempTree = Object.assign([], fileTreeData.value);
                    fileTreeData.value = tempTree;
                } else {// 只要不是初始化就使用上一次的tree,再上一次的tree children里面放入。
                    // 应该是按照id查找
                    if (currentTreeId.value != 0) {
                        for (let treeObj of fileTreeData.value) {
                            if (treeObj.id == currentTreeId.value) {
                                treeObj["children"].push(tree);
                            }
                        }
                    }
                    const tempTree = Object.assign([], fileTreeData.value);
                    fileTreeData.value = tempTree;
                }
                nextStep();//可能会改变当前状态并跳转到下一步
            } else {
                fileTreeData.value.push(tree);
                const tempTree = Object.assign([], fileTreeData.value);
                fileTreeData.value = tempTree;
                changeTreeRelation(tree.id); // 判断是否有关系存在并作出改变
            }
            overlayFabricCanvas.renderAll();
            is_drawing = false;
            initCurrentObj();
        }
    }
    console.log(fileTreeData)
    console.log(fabricObjects.value)
    console.log(currentDrawObject)
    console.log(relations)
}
// 对所有的子对象进行遍历 关系生成
const calcAllRelations = () => {
    for (let category of [StateEnum.FIGURE_NOS, StateEnum.BARS, StateEnum.LABELS]) {
        fabricObjects.value.get(category)!.forEach((obj) => {
            changeTreeRelation(obj.results.id);
        })
    }
}


// 判断绘制物体的所属关系并修改tree和objects,relations
const changeTreeRelation = (aimedId) => {
    // 获得所有的外层Figures然后比较最大的重合面积。
    const {canvasObject, category, isExists} = findCanvasObjectByNameOrData(aimedId, false, "data")
    if (!isExists || category == StateEnum.FIGURES) {
        return;
    }
    // 根据是否相交以及相交的面积，得到所有可以加入到的figure id
    const figures = fabricObjects.value.get(StateEnum.FIGURES)!;
    if (figures.length == 0) {
        return;
    }
    let maxArea = 0;
    let possibleFigureIds: any = [];
    let tempPossibleFigureId = -1;
    let figureAreas: any = [];
    let tempFigureArea = 0;
    // 先找到相交面积最大的那些figure
    for (let figure of figures) {
        const area = getIntersectionArea(figure.results.points, canvasObject.results["points"]);
        if (area > maxArea) {
            maxArea = area;
            tempPossibleFigureId = figure.results.id;
            tempFigureArea = Math.abs((figure.results.points[1][0] - figure.results.points[0][0]) * (figure.results.points[1][1] - figure.results.points[0][1]));
        } else if (area == maxArea && area != 0) {
            possibleFigureIds.push(tempPossibleFigureId);
            figureAreas.push(tempFigureArea);
            tempPossibleFigureId = figure.results.id;
            tempFigureArea = Math.abs((figure.results.points[1][0] - figure.results.points[0][0]) * (figure.results.points[1][1] - figure.results.points[0][1]));
        }
    }
    if (tempPossibleFigureId != -1) {
        possibleFigureIds.push(tempPossibleFigureId);
        figureAreas.push(tempFigureArea);
    }
    if (aimedId == 18) {
        console.log(possibleFigureIds)
        console.log(figureAreas)
    }
    const used_Ids: any = [];
    // 从这些相交面积最大的figure里面筛选出没有这个类型的figure
    for (let i = 0; i < possibleFigureIds.length; i++) {
        for (let treeObj of fileTreeData.value) {
            if (treeObj.id == possibleFigureIds[i]) {
                // 一个figure里每种类型只能有一个
                let canPush = true;
                for (let child of treeObj.children) {
                    if (child.type == category) { // 如果有这种类型就不可以放入
                        canPush = false;
                        break;
                    }
                }
                if (canPush) {
                    used_Ids.push(possibleFigureIds[i]);
                }
            }
        }
    }
    // 如果有两个以上，就取面积最小的figure
    let final_Id = -1;
    if (used_Ids.length > 1) {
        let minArea = figureAreas[0];
        let minIndex = 0;
        for (let i = 1; i < figureAreas.length; i++) {
            if (figureAreas[i] < minArea) {
                minArea = figureAreas[i];
                minIndex = i;
            }
        }
        final_Id = used_Ids[minIndex];
    } else {
        // 如果有一个，就取这个
        if (used_Ids.length == 1) {
            final_Id = used_Ids[0];
        }
    }
    // 有符合条件的figure就放入，没有就算了。
    if (final_Id != -1) {
        // 修改这个figure的children，将目标物体加入
        const figure_indexes = findTreeObjectsIndexById(final_Id);
        const aim_indexes = findTreeObjectsIndexById(aimedId);
        let aimedColor = "";
        // 保证类型正确才能放
        if (figure_indexes[0] != -1 && aim_indexes[0] != -1 && figure_indexes[0] != aim_indexes[0] &&
            fileTreeData.value[aim_indexes[0]].type != StateEnum.FIGURES && fileTreeData.value[figure_indexes[0]].type == StateEnum.FIGURES) {
            aimedColor = fileTreeData.value[figure_indexes[0]].color["background-color"];
            fileTreeData.value[aim_indexes[0]].color = fileTreeData.value[figure_indexes[0]].color; // 将目标物体的颜色改为figure的颜色
            fileTreeData.value[figure_indexes[0]].children.push(fileTreeData.value[aim_indexes[0]]); // 将目标物体加入
            fileTreeData.value.splice(aim_indexes[0], 1);  // 删除原来的目标物体
            const tempTree = Object.assign([], fileTreeData.value);
            fileTreeData.value = tempTree;
        }
        // 改变最后的目标物体的颜色
        const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId);
        const fabricObjs = overlayFabricCanvas.getObjects().filter(obj => obj.data === aimedId);
        if (fabricObjs.length > 0) {
            for (let fabricObj of fabricObjs) {
                // 修改颜色。
                console.log(aimedColor)
                fabricObj.set({stroke: aimedColor})
            }
            overlayFabricCanvas.renderAll();
        }
        // 修改关系relations
        calcRelations();
    }
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


// 判断当前的工具状态
const judgeCurrentState = () => {
    // currentToolType -> line, polygon, circle, rectangle, edit
    if (isActive.value) {
        if (currentToolType.value == "figures") {
            currentState = StateEnum.FIGURES
        } else if (currentToolType.value == "figure_nos") {
            currentState = StateEnum.FIGURE_NOS
        } else if (currentToolType.value == "bars") {
            currentState = StateEnum.BARS
        } else if (currentToolType.value == "labels") {
            currentState = StateEnum.LABELS
        } else if (currentToolType.value == "edit") {
            currentState = StateEnum.EDIT
        }
    } else {
        currentState = StateEnum.NO_STATE
    }
    //  设置token 用于刷新页面时恢复状态
    setToken("currentState", currentState)
    console.log(currentState)
}
// 逐步标记时跳转到上一步
const backToLastStep = () => {
    // 关闭返回到上一步
    if (currentStep.value > startStep.value) {
        currentStep.value = currentStep.value - 1
        currentState = labelBarIcons[currentStep.value].drawType
        changeDrawType(currentState)
        //  删除当前的对象
        undoCurrentDraw();
        // 删除上一步绘制的对象,对象关系。
        const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId)
        const lastDrawObject = fabricObjects.value.get(currentState)!.pop();
        for (let key of Object.keys(lastDrawObject)) {
            if (key != "results" && key != "points") {
                if (lastDrawObject[key].length > 0) {
                    for (let kclss of lastDrawObject[key]) {
                        const toRemoves = overlayFabricCanvas.getObjects().filter(obj => obj.name === kclss.name);
                        if (toRemoves.length > 0) {
                            overlayFabricCanvas.remove(toRemoves[0])
                        }
                    }
                }
            }
        }
        // 二维的relations currentStep当前状态设为-1即可  如果全为-1，这个relations是无效的
        relations[relations.length - 1][currentStep.value] = -1;
        // 关系树的删除
        const indexs = findTreeObjectsIndexById(lastDrawObject.results.id)
        if (indexs[0] != -1 && indexs[1] == -1) {
            fileTreeData.value.splice(indexs[0], 1) // 最顶级找到的直接删除即可
        } else if (indexs[0] != -1 && indexs[1] != -1) { // 子级中直接删除即可
            fileTreeData.value[indexs[0]].children.splice(indexs[1], 1)
        }
        const tempTree = Object.assign([], fileTreeData.value);
        fileTreeData.value = tempTree;
        console.log(fileTreeData)
        console.log(fabricObjects)
        console.log(relations)
        overlayFabricCanvas.renderAll();
    } else { // 如果是第一步就不能再返回 这里应该不会进入。
        showLastButton.value = false;
    }
}

// 每次点击ToolBar 都会进行下面的操作
function changeDrawType(newType: string, index = -1) {
    if (index != -1) { // 如果传过来值不等于-1说明是一个点击事件 记录初始状态
        startStep.value = index;
        currentStep.value = index;  //当前就是这个状态
    }
    const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId)// 获取已经建立的fabricOverlay对象
    if (currentToolType.value == newType) {
        isActive.value = !isActive.value;// 两次点击的一致 是开关
    } else {
        //两次点击的不一致 改变ToolBar 同时设为激活状态
        currentToolType.value = newType;
        isActive.value = true;
    }
    if (isActive.value && currentToolType.value != StateEnum.NO_STATE) { // 激活任意工具改变鼠标类型
        overlayFabricCanvas.defaultCursor = "crosshair";
        overlayFabricCanvas.hoverCursor = "crosshair";
        // 展示右下角的toast提示  index!=-1 点击事件再提示？
        currentToolToast.value = labelBarIcons[currentStep.value].tips;
        //toast.show();
        showToast.value = true;

    } else {
        overlayFabricCanvas.defaultCursor = "default";
        overlayFabricCanvas.hoverCursor = "default";
        // 关闭toast
        // toast.hide()
        showToast.value = false;
    }
    if (currentToolType.value == "edit" && isActive.value) { //如果是修改编辑
        overlayFabricCanvas.defaultCursor = "crosshair";
        overlayFabricCanvas.hoverCursor = "move";
        // 设置所有的都可以选中
        let allObjects = overlayFabricCanvas.getObjects();
        for (const obj of allObjects) {
            obj.set("selectable", true);
            obj.setCoords(); // 必须加上它才能移动。 重新计算坐标
        }
    } else {  // 只要不是编辑 继承上面的默认Cursor方式
        let allObjects = overlayFabricCanvas.getObjects();
        for (const obj of allObjects) {
            // obj.hoverCursor = "default";
            obj.set("selectable", false);
            obj.setCoords(); // 必须加上它才能移动。
        }
    }
    console.log(currentToolType.value, isActive.value, `startStep=${startStep.value}`);
    judgeCurrentState()
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
                Swal.fire({
                    title: "Success!",
                    icon: "success",
                    showConfirmButton: false,
                    timer: 1550
                });
            }
        });
    } else if (func_type == "save") {//保存图像画板
        exportDraw()
    } else if (func_type == "export") {
        console.log("export");
        exportJsonLabel()
        // let canvasJson = JSON.stringify(overlay.fabricCanvas().toObject());
        // console.log(canvasJson);
        //TODO 导出到Excel
    } else if (func_type == "setting") {
        const settingModal = new Modal("#drawOption");
        settingModal.show();
    } else if (func_type == "back") {
        // 跳转到另一个面板
        emit("show-draw-panel", true)
        console.log("back")
    }
}

// 清除画板
function clearDraw() {
    const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId)// 获取已经建立的fabricOverlay对象
    overlayFabricCanvas.clear();
    initCurrentObj();
    // 清空fabricObjects
    fabricObjects.value.forEach((value, key) => {
        fabricObjects.value.set(key, []);
    })
    relations = [];   // 清空关系
    fileTreeData.value = [];// 清空标记数据
    console.log(fabricObjects.value)
    console.log(relations)
    console.log(fileTreeData.value)
}

// 综合当前的信息
const combineJsonLabel = () => {
    const blankJson = {
        "name": "",
        "meta": {},
        "width": 0,
        "height": 0,
        "ppi": 0,
        "figures": [],
        "figure_nos": [],
        "bars": [],
        "labels": [],
        "relations": []
    }
    fabricObjects.value.forEach((arr, key: any) => {
        for (let obj of arr) {
            blankJson[key].push(obj.results)
        }
    })
    // TODO 是否要加一个后端识别接口或者计算label相关信息的函数？
    // 注意经过前端用户操作后，部分计算信息丢失，例如bar的实际长度，figure的ppi等。
    if (Object.keys(labelResults).length != 0) {
        const name = labelResults["name"].split("\\")[labelResults["name"].split("\\").length - 1];
        console.log(name);
        blankJson.name = name;  // 这个name需要再处理
        blankJson.meta = labelResults["meta"];
        blankJson.width = labelResults["width"];
        blankJson.height = labelResults["height"];
        blankJson.ppi = labelResults["ppi"];
    }
    blankJson["relations"] = relations;// relations已经同步过了 可以直接相等后导出
    return blankJson
}


// 导出当前的标准json格式
const exportJsonLabel = () => {
    const jsonLabel = combineJsonLabel()
    let link = document.createElement('a')
    link.download = 'label.json'
    link.href = 'data:text/plain,' + JSON.stringify(jsonLabel)
    link.click()
}


// 导出当前画板
function exportDraw() {
// TODO 这么导出的清晰度有点低   toSVG试试
    const viewer = getViewerById(initOptions.canvasId)
    const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId)// 获取已经建立的fabricOverlay对象
    // 添加原始图片信息
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

let drawOptions = {
    "originX": "left",
    "originY": "top",
    "opacity": "0.6",
    "textBackgroundColor": "#fefefe",
    "fill": "transparent",

    "selectable": false,
    "color": "#F43F61",
    "drawWidth": 5,

    "fontSize": 30,   // TODO 字体大小是否需要自适应？
    "textColor": "#009EF7",
    "strokeWidth": 3,
    "stroke": "#F43F61",
}
// 得到设置的绘制值 设置按钮的modal
const getDrawOptions = (editOptions) => {
    drawOptions.fontSize = parseInt(editOptions.text_size);
    drawOptions.strokeWidth = parseInt(editOptions.draw_size);
}

const initDrawOption = () => {
    drawOptions = {
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
        "strokeWidth": 3,
        "stroke": "#F43F61",
    }
}
// delete object by id;
const deleteByID = (id) => {
    const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId);
    const {isExists, canvasObject, category, index} = findCanvasObjectByNameOrData(id, false, "data")
    if (!isExists) {
        return
    }
    for (let key of Object.keys(canvasObject)) {
        if (key != "points" && key != "results") {
            for (let kclss of canvasObject[key]) {
                // 不是同一个对象了 所以要从这里面找再删除
                const toRemoves = overlayFabricCanvas.getObjects().filter(obj => obj.name === kclss.name);
                if (toRemoves.length > 0) {
                    overlayFabricCanvas.remove(toRemoves[0])
                }
            }
        }

    }
    // 如果有关系 把这个的关系给关掉
    if (canvasObject.results.id > 0) {
        for (let i = 0; i < relations.length; i++) {
            for (let j = 0; j < relations[0].length; j++) {
                if (relations[i][j] == canvasObject.results.id) {
                    relations[i][j] = -1;
                }
            }
        }
    }
    // 删除关系树。
    if (canvasObject.results.id > 0) {
        const treeObjIndexs = findTreeObjectsIndexById(canvasObject.results.id);
        if (treeObjIndexs[0] != -1 && treeObjIndexs[1] == -1) {// 找到对象了,且是在顶级找到的
            if (fileTreeData.value[treeObjIndexs[0]].children.length > 0) {// 这个对象还有子对象,把子对象提上来，同时删掉这个对象
                for (let treeObj of fileTreeData.value[treeObjIndexs[0]].children) {
                    fileTreeData.value.push(treeObj);// 放最后的
                }
                fileTreeData.value.splice(treeObjIndexs[0], 1)
            } else {//没有子对象 直接把他删除即可
                fileTreeData.value.splice(treeObjIndexs[0], 1)
            }
        } else if (treeObjIndexs[0] != -1 && treeObjIndexs[1] != -1) {
            // 如果是在子级里面找到的。可以直接把这个对象删掉
            fileTreeData.value[treeObjIndexs[0]].children.splice(treeObjIndexs[1], 1)
        }
    }
    // 找到这个tree,
    // 如果没有关系，直接删除即可。
    // 有关系，看看是否是figure，如果是把底层的都提上来。再把它删掉
    // 如果不是figure,直接删除即可。把figure的children去掉。
    const tempTree = Object.assign([], fileTreeData.value);
    fileTreeData.value = tempTree;
    //先把这个对象整个的从fabricObjects移除吧 TODO  后期考虑加个状态 暂时删除
    fabricObjects.value.get(category)!.splice(index, 1);
    overlayFabricCanvas.discardActiveObject().requestRenderAll();
}


// 监听删除事件
document.addEventListener("keyup", (e) => {
    if (e.ctrlKey && e.keyCode === 46) {
        console.log(" ctrl + delete");
        //delete快速删除
        const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId);
        let selection = overlayFabricCanvas.getActiveObjects();
        console.log(selection)
        if (selection.length > 0) {
            deleteByID(selection[0].data)
        }
    } else if (e.keyCode === 27) {
        //esc键关闭撤销正在绘制
        console.log("esc");
        undoCurrentDraw();
    } else if (e.shiftKey && e.keyCode === 53 || (e.shiftKey && e.altKey && e.keyCode === 69)) {
        console.log("shift alt e 或5快速进入编辑界面 待增加 ");
        changeDrawType("edit", 4)
    } else if (e.shiftKey && e.keyCode === 49) {
        changeDrawType(StateEnum.FIGURES, 0)
    } else if (e.shiftKey && e.keyCode === 50) {
        changeDrawType(StateEnum.FIGURE_NOS, 1)
    } else if (e.shiftKey && e.keyCode === 51) {
        changeDrawType(StateEnum.BARS, 2)
    } else if (e.shiftKey && e.keyCode === 52) {
        changeDrawType(StateEnum.LABELS, 3)
    } else if (e.ctrlKey && e.keyCode === 90) {
        //快速删除最后绘制的对象
        deleteByID(maxId);
        maxId--;
        console.log("TODO ctrl+z快速撤销上一步 待增加 ");
    } else if (e.shiftKey && e.keyCode === 39) {
        console.log("shift+right 下一步 保存当前标注");
        doNewLabel("next")
    } else if (e.shiftKey && e.keyCode === 37) {
        doNewLabel("last")
        console.log("shift+left 上一步 保存当前标注");
    } else if (e.ctrlKey && e.keyCode === 39) {
        console.log("ctrl+right 下一步 不保存当前标注");
        doNewLabel("next", false)
    } else if (e.ctrlKey && e.keyCode === 37) {
        console.log("ctrl+left 上一步 不保存当前标注");
        doNewLabel("last", false)
    } else if (e.ctrlKey && e.shiftKey && e.keyCode === 83) {
        calcAllRelations();
    } else if (e.altKey && e.shiftKey && e.keyCode === 83) {
        // alt+shift+s 保存当前标注
        console.log("alt+shift+s 保存当前标注");
        doNewLabel("current", true);
        // 提示请在目标内绘制
        boundaryMsg.value = `<div>
                Labels has been saved!
              </div>
              `;
        const toast = new Toast("#boundaryToast")
        toast.show()
    } else if (e.altKey && e.shiftKey && e.keyCode === 68) {
        //    alt+shift+d 保存当前标注
        console.log("alt+shift+d 重复当前标注");
        if (currentState != StateEnum.EDIT) {
            return;
        }
        const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId);
        let selections = overlayFabricCanvas.getActiveObjects();
        for (let select of selections) {
            const {canvasObject, category} = findCanvasObjectByNameOrData(select.data, false, "data");
            let category_index = 0;
            for (let key of fabricObjects.value.keys()) {
                if (key == category) {
                    break;
                }
                category_index++;
            }
            maxId = maxId + 1;
            const offsetLength = drawOptions.drawWidth * 3;
            const newResult = {
                id: maxId,
                points: [[canvasObject["results"].points[0][0] + offsetLength, canvasObject["results"].points[0][1] + offsetLength],
                    [canvasObject["results"].points[1][0] + offsetLength, canvasObject["results"].points[1][1] + offsetLength]],
            }
            // 判断对象是否有某个key
            if ("text" in canvasObject["results"]) {
                newResult["text"] = canvasObject["results"]["text"];
            }
            console.log(canvasObject["results"])
            const tree = initOneResult(category, category_index, newResult)
            fileTreeData.value.push(tree);
            const tempTree = Object.assign([], fileTreeData.value);
            fileTreeData.value = tempTree;   // 必须加上这一句要不然不会同步更新；
            console.log(fabricObjects)
            console.log(fileTreeData)
            // 设置所有的都可以选中
            let allObjects = overlayFabricCanvas.getObjects();
            for (const obj of allObjects) {
                obj.set("selectable", true);
                obj.setCoords(); // 必须加上它才能移动。 重新计算坐标
            }
        }
    }
});
// 得到目标tree的具体Index;
const findTreeObjectsIndexById = (id) => {
    for (let i = 0; i < fileTreeData.value.length; i++) {
        if (fileTreeData.value[i].id == id) {
            return [i, -1];
        }
        for (let j = 0; j < fileTreeData.value[i]["children"].length; j++) {
            if (fileTreeData.value[i]["children"][j].id == id) {
                return [i, j];
            }
        }
    }
    return [-1, -1];
}


const undoCurrentDraw = () => {
    if (is_drawing) {
        const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId)
        console.log(currentDrawObject);
        // 直接删除当前对象即可 同时初始化currentDrawObject
        for (let key of Object.keys(currentDrawObject)) {
            if (key != "results" && key != "points" && key != "texts") {
                if (currentDrawObject[key].length > 0) {
                    for (let kclss of currentDrawObject[key]) {
                        overlayFabricCanvas.remove(kclss)
                    }
                }
            }
        }
        is_drawing = false;
        initCurrentObj()
    }
}


// // 2.获取子组件ref实例
// const fileTree = ref<typeof Draggable>();
//
// onMounted(()=>{
//   console.log(fileTree.value!.getData());
//
// });


// tree节点拖拽时的函数。
const onTreeDrag = (stat) => {
    if (isStepLabel.value) { //如果是逐步绘制则不允许拖拽
        return false;
    }
    console.log(stat)
    const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId);
    const fabricObjs = overlayFabricCanvas.getObjects().filter(obj => obj.data === stat.data.id);
    let timeOut;
    if (fabricObjs.length > 0) {
        for (let fabricObj of fabricObjs) {
            // 修改颜色。
            fabricObj.set({
                fill: stat.data.color["background-color"],
                opacity: 0.5,
                stroke: stat.data.color["background-color"]
            })
            timeOut = setTimeout(() => {
                fabricObj.set({fill: "transparent"});
                overlayFabricCanvas.renderAll();
            }, 1000)
        }
        overlayFabricCanvas.renderAll();
    }
    if (stat.data.type == StateEnum.FIGURES) {
        return false;
    } else if (stat.data.type == StateEnum.FIGURE_NOS || stat.data.type == StateEnum.BARS || stat.data.type == StateEnum.LABELS) {
        currentTreeDragData = stat; // 储存一下当前拖拽的对象
        return true;
    }else {
        return true;
    }
}
// 当有Tree对象进入时函数
const onTreeDrop = (stat) => {
    // 将当前拖拽对象的颜色高亮显示
    const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId);
    const fabricObjs = overlayFabricCanvas.getObjects().filter(obj => obj.data === currentTreeDragData.data.id);
    if (fabricObjs.length > 0) {
        for (let fabricObj of fabricObjs) {
            // 修改颜色。
            fabricObj.set({
                fill: stat.data.color["background-color"],
                opacity: 0.5,
                stroke: stat.data.color["background-color"]
            })
        }
        overlayFabricCanvas.renderAll();
    }

    console.log(stat) // stat是目标对象 不是拖拽对象
    for (let treeObj of stat.children) {
        if (treeObj.data.type == currentTreeDragData.data.type) { // 如果已经有了这个类别就不能拖入
            if (treeObj.data.id != currentTreeDragData.data.id) {  // 原来就有的可以
                return false;
            }
        }
    }
    if (stat.data.type == StateEnum.FIGURES) {
        return true;
    } else if (stat.data.type == StateEnum.FIGURE_NOS || stat.data.type == StateEnum.BARS || stat.data.type == StateEnum.LABELS) {
        return false;  //这些物体是不能有子对象的。
    }else {
        return true;
    }
    // 首先判断能不能放下去
}
// Stat的初始化函数 控制是否可以拖拽
const initTreeStat = (stat) => {
    return stat
}
// 拖拽完成且造成改变时触发 改变relations 应该会造成整个的改变了
const onTreeChange = () => {
    const treeRelations: any = [];
    const usedColorList: any = []
    for (let treeObj of fileTreeData.value) {
        // 每一个数都应该有不同的颜色。
        if (usedColorList.indexOf(treeObj.color["background-color"]) != -1) { // 用过这个颜色 重新生成
            treeObj.color = {"background-color": getRandomColor(-1)};
        }
        usedColorList.push(treeObj.color["background-color"])
        if (treeObj.children.length > 0) {
            const relation = [treeObj.id, 0, 0, 0]; //只要在树里的 都可以看成是没有未确定的了
            for (let i = 0; i < treeObj.children.length; i++) {
                // children设置成parent的颜色
                treeObj.children[i].color = treeObj.color;
                if (treeObj.children[i].type == StateEnum.FIGURE_NOS) {
                    relation[1] = treeObj.children[i].id;
                } else if (treeObj.children[i].type == StateEnum.BARS) {
                    relation[2] = treeObj.children[i].id;
                } else if (treeObj.children[i].type == StateEnum.LABELS) {
                    relation[3] = treeObj.children[i].id;
                }
            }
            treeRelations.push(relation)
        }
    }
    const tempTree = Object.assign([], fileTreeData.value);
    fileTreeData.value = tempTree;   // 必须加上这一句要不然不会同步更新；
    relations = treeRelations;
    console.log(relations)
    // 将所有对象的颜色改成透明色
    const overlayFabricCanvas = getFabricCanvasById(initOptions.canvasId);
    const fabricObjs = overlayFabricCanvas.getObjects();
    if (fabricObjs.length > 0) {
        for (let fabricObj of fabricObjs) {
            // 修改颜色。
            fabricObj.set({fill: "transparent"})
        }
        overlayFabricCanvas.renderAll();
    }
}

// 拖拽完成且造成改变时触发 改变relations 应该会造成整个的改变了
const calcRelations = () => {
    const treeRelations: any = [];
    for (let treeObj of fileTreeData.value) {
        if (treeObj.children.length > 0) {
            const relation = [treeObj.id, 0, 0, 0]; //只要在树里的 都可以看成是没有未确定的了
            for (let i = 0; i < treeObj.children.length; i++) {
                // children设置成parent的颜色
                if (treeObj.children[i].type == StateEnum.FIGURE_NOS) {
                    relation[1] = treeObj.children[i].id;
                } else if (treeObj.children[i].type == StateEnum.BARS) {
                    relation[2] = treeObj.children[i].id;
                } else if (treeObj.children[i].type == StateEnum.LABELS) {
                    relation[3] = treeObj.children[i].id;
                }
            }
            treeRelations.push(relation)
        }
    }
    relations = treeRelations;
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