import OpenSeadragon from "openseadragon";
import { fabric } from "fabric";
import "./openseadragon-scalebar";
import "./openseadragon-fabricjs-overlay";
import {getUUID, measureLine, showTextInfo} from "@/core/tools/MathUtil";


export interface InitOptions {
    canvasId:string;
    zoomScale:number;
    pixelPerMeter:number;
    drawColor:string;
    drawWidth:number;
}

// export enum StateEnum {
//     NO_STATE="no_state",
//     LINE="line",
//     POLY="poly",
//     RECT="rect",
//     CIRCLE="circle",
//     TEXT="text",
//     EDIT="edit",
// }
export enum LabelStateEnum {
    NO_STATE="no_state",
    FIGURES="figures",
    FIGURE_NOS="figure_nos",
    BARS="bars",
    LABELS="labels",
    EDIT="edit",
}


export function getViewerById(canvasId:string){
    const viewer = OpenSeadragon.getViewer(OpenSeadragon.getElement(canvasId));  // 获取已经建立的viewer对象
    return viewer
}
export function getFabricCanvasById(canvasId:string){
    const viewer = getViewerById(canvasId);  // 获取已经建立的viewer对象
    const overlayFabricCanvas = viewer["_fabricjsOverlayInfo"].fabricCanvas(); // 获取已经建立的fabricOverlay对象
    return overlayFabricCanvas
}
// 移动线组的端点事件
export const movingLineEndPoint = (lineGroups,moveType,newPoint,ppm) => {    // lineGroups
    // moveType对应的是objects starts ends中的一种
    const startLine = lineGroups[0];
    const middleLine = lineGroups[1];
    const endLine = lineGroups[2];
    if (moveType == "starts") {  // 移动的是starts 固定的就是ends
        startLine.set("originX", "center");
        startLine.set("originY", "center");
        middleLine.set({
            x1: newPoint.x,
            y1: newPoint.y, //这个不够准确，应该是获取这个物体的中心 暂时没有找到函数
            x2: endLine.getCenterPoint().x, //必须这样才能获得真实位置
            y2: endLine.getCenterPoint().y,
        });
    } else {
        endLine.set("originX", "center");
        endLine.set("originY", "center");
        middleLine.set({
            x1: startLine.getCenterPoint().x,
            y1: startLine.getCenterPoint().y,
            x2: newPoint.x,
            y2: newPoint.y, //这个不够准确，应该是获取这个物体的中心 暂时没有找到函数
        });
    }
    const angle =(Math.atan2(middleLine.get("y1") - middleLine.get("y2"),
                middleLine.get("x1") - middleLine.get("x2")) *180) /Math.PI;
    if (startLine.type != "circle") {
        startLine.rotate(angle);
    }
    if (endLine.type != "circle") {
        endLine.rotate(angle);
    }
    const newResults = measureLine({ x: middleLine.get("x1"), y: middleLine.get("y1") },{ x: middleLine.get("x2"), y: middleLine.get("y2") },ppm)
    if (lineGroups.length==3){
        return newResults; // 没有text显示 就直接返回结果即可
    }
    const textObj = lineGroups[3];
    // 移动中间的text信息
    const middlePoint = {
        x: (middleLine.get("x1") + middleLine.get("x2")) / 2,
        y: (middleLine.get("y1") + middleLine.get("y2")) / 2,
    };
    const newTextInfo = showTextInfo(newResults,"line",false);
    textObj.set({ left: middlePoint.x, top: middlePoint.y,text:newTextInfo})
    if (angle > 90) {
        textObj.rotate(angle - 180);
    } else if (angle < -90) {
        textObj.rotate(angle + 180);
    } else {
        textObj.rotate(angle);
    }
    return newResults;
}


// 得到当前点击的位置点
export const getPoint = function (options, canvasId) {
    const viewer = getViewerById(canvasId);  // 获取已经建立的viewer对象
    const overlayFabricCanvas = viewer["_fabricjsOverlayInfo"].fabricCanvas(); // 获取已经建立的fabricOverlay对象
    const offset_x = overlayFabricCanvas.calcOffset().viewportTransform[4];
    const offset_y = overlayFabricCanvas.calcOffset().viewportTransform[5];
    const zoom = viewer.viewport.getZoom(true);
    const imageZoom = viewer.viewport.viewportToImageZoom(zoom);
    //openSeadragon.setMouseNavEnabled(!drawType);
    const px = (options.e.offsetX - offset_x) / imageZoom;
    const py = (options.e.offsetY - offset_y) / imageZoom;
    return { x: px, y: py, imageZoom: imageZoom };
};
// 绘制矩形
export const drawRect = (points,options, canvas, labelId="rect") => {
    if (points.length==1){
        points.push(points[0]); //如果只有一个点就增加一个
    }
    if(points.length==2){
        const left = Math.min(points[0].x,points[1].x)
        const top = Math.min(points[0].y,points[1].y)
        const right = Math.max(points[0].x,points[1].x)
        const bottom = Math.max(points[0].y,points[1].y)
        const rec_width = Math.round(right-left);
        const rec_height = Math.round(bottom-top); // 就是可以有负值

        const obj = new fabric.Rect({
        name:"rect_"+getUUID(),
        data:labelId,   // 对于识别类型可以根据id来找到对象  对于绘制类型是根据name来寻找的
        "left": left,
        "top": top,
        width: rec_width,
        height: rec_height,
        fill: options.fill,
        stroke: options.stroke,
        strokeWidth: options.strokeWidth,
        selectable: options.selectable, //是否可被选中
        });
        obj.lockRotation = true;    // 禁止旋转
        canvas.add(obj);
        return obj;
    }



};

// 绘制圆形
export const drawCircle = (points,options, canvas, labelId="circle") => {
    let cir_radius = 10;
    if(points.length==2){
        cir_radius = Math.sqrt(
            (points[1].x - points[0].x) * (points[1].x - points[0].x) +
            (points[1].y - points[0].y) * (points[1].y - points[0].y)
        );
    }
    const obj = new fabric.Circle({
        name: "circle_"+getUUID(),
        data: labelId,
        left: points[0].x,
        top: points[0].y,
        radius: cir_radius,
        originX: "center",
        originY: "center",
        fill: options.fill,
        stroke: options.stroke,
        strokeWidth: options.strokeWidth,
        selectable: options.selectable, //是否可被选中
    });
    // 只能等比例变化
    obj.setControlsVisibility({
        mt: false, // middle top disable
        mb: false, // midle bottom
        ml: false, // middle left
        mr: false, // I think you get it
    });
    canvas.add(obj);
    return obj;
};
// 绘制标志
export const drawMark = (points,options, canvas, labelId="mark") => {
    let cir_radius = 5;
    if(points.length==2){
        cir_radius = Math.sqrt(
            (points[1].x - points[0].x) * (points[1].x - points[0].x) +
            (points[1].y - points[0].y) * (points[1].y - points[0].y)
        );
    }
    const obj = new fabric.Circle({
        name: "mark_"+getUUID(),
        data: labelId,
        left: points[0].x,
        top: points[0].y,
        radius: cir_radius,
        originX: "center",
        originY: "center",
        fill: options.stroke,   // 实心
        stroke: options.stroke,
        strokeWidth: options.strokeWidth,
        selectable:false, //是否可被选中
    });
    // 只能等比例变化
    obj.setControlsVisibility({
        mt: false, // middle top disable
        mb: false, // midle bottom
        ml: false, // middle left
        mr: false, // I think you get it
        tl: false, // top left
        tr: false, // top right
        bl: false, // bottom left
        br: false, // bottom right
    });
    canvas.add(obj);
    return obj;
};
// 绘制polygon
export const drawPolygon = (points,options, canvas, labelId="polygon") => {
    // list 形式 转为 points
    if (points.length==1){
        return null;
    }

    const obj = new fabric.Polygon(points, {
        name: "polygon_"+getUUID(),
        data: labelId,
        fill: options.stroke,
        stroke: options.stroke,
        originX: "center",
        originY: "center",
        strokeWidth: options.strokeWidth,
        opacity: 0.5,
        selectable: false, //是否可被选中
    });
    canvas.add(obj);
    return obj;
}


// 绘制文本
export const drawText = (showtext, type, points,options, canvas) => {
    let text_selectable = options.selectable
    if (type=="edit"){
        text_selectable = true
        showtext = "Double Click to Edit!"
    }
    const text = new fabric.IText(showtext, {
        //绘制文本
        name: type+"_"+getUUID(),
        data:type,  // edit 或者传过来的info
        left: points[0].x,
        top: points[0].y,
        selectable:text_selectable,
        fontSize: options.fontSize,
        fill: options.textColor,

        opacity: options.opacity,
        originX: options.originX,
        originY: options.originY,
        textBackgroundColor: options.textBackgroundColor,
    });
    if (options.scaleToWidth) {
        text.setCoords();
        text.scaleToWidth(options.scaleToWidth);
    }
    if (options.scaleToHeight) {
        text.setCoords();
        text.scaleToHeight(options.scaleToHeight);
    }
    canvas.add(text);
    return text;
};
// 画线
export const drawLine = (type, points, options, canvas) => {
    let TYPE = "line"
    let DATA = "line"
    if (type){
        TYPE = type.split(".")[0]
        DATA = type.split(".")[1]
    }
    let line_points = [points[0].x,points[0].y,points[0].x,points[0].y];
    if(points.length==2){
        line_points = [points[1].x,points[1].y,points[0].x,points[0].y];
    }
    if(DATA=="starts"||DATA=="ends"){
        const show_y1 = points[0].y - options.strokeWidth*options.drawWidth;
        const show_y2 = points[0].y + options.strokeWidth*options.drawWidth;
        line_points = [points[0].x, show_y1, points[0].x, show_y2];
    }

    const line = new fabric.Line(line_points, {
        name: type+"_"+getUUID(),
        data:DATA,
        "type":TYPE,        //TODO 检查设置这个type是否会影响导出
        stroke: options.stroke,
        strokeWidth: options.strokeWidth,
        selectable: options.selectable, //是否可被选中
    });
    canvas.add(line);
    // 只能平移 所以要关闭所有的控制
    line.setControlsVisibility({
        mt: false, // middle top disable
        mb: false, // midle bottom
        ml: false, // middle left
        mr: false, // I think you get it
        bl: false, // I think you get it
        br: false, // I think you get it
        tl: false, // I think you get it
        tr: false, // I think you get it
        mtr: false, // I think you get it
    });
    return line;
};

// 修改鼠标中键拖动的操作方式
const changeZoomScrollOperation = (openSeadragon) => {
    // Need to prevent the context menu or it'll interfere with dragging.
    // 修改默认的鼠标按键 按住中键拖动 放大缩小
    const trackerElement = openSeadragon.container;
    const mouse_tracker  = OpenSeadragon.MouseTracker as any;
    let drag;
    function capturePointer(event) {
        if (mouse_tracker.havePointerCapture) {
            if (mouse_tracker.havePointerEvents) {
                // Can throw InvalidPointerId
                trackerElement.setPointerCapture(event.originalEvent.pointerId);
            } else {
                trackerElement.setCapture(true);
            }
        }
    }
    function releasePointer(event) {
        if (mouse_tracker.havePointerCapture) {
            if (mouse_tracker.havePointerEvents) {
                // Can throw InvalidPointerId
                trackerElement.releasePointerCapture(event.originalEvent.pointerId);
            } else {
                trackerElement.releaseCapture();
            }
        }
    }
    openSeadragon.setMouseNavEnabled(false);
    new OpenSeadragon.MouseTracker({
        element: trackerElement,
        nonPrimaryPressHandler: function (event) {
            if (event["button"] === 1) {
                // Middle
                capturePointer(event);
                drag = {
                    lastPos: event["position"].clone(),
                };
            }
        },
        scrollHandler: function (event) {
            if (event["shift"]) {   // 如果想要按住shift才放大缩小的话
                openSeadragon.viewport.applyConstraints();
                const vp = openSeadragon.viewport.viewerElementToViewportCoordinates(
                    event["position"]
                );
                openSeadragon.viewport.panTo(vp);
                openSeadragon.viewport.zoomBy(event["scroll"] === 1 ? 1.1 : 0.9);
            }
            // 只使用鼠标中键放大缩小
            // const vp = openSeadragon.viewport.windowToViewportCoordinates(
            //     event["position"]
            // );
            // openSeadragon.viewport.panTo(vp);
            // openSeadragon.viewport.zoomBy(event["scroll"] === 1 ? 1.1 : 0.9);
        },
        moveHandler: function (event) {
            if (drag) {
                const deltaPixels = drag.lastPos.minus(event["position"]);
                const deltaPoints =
                    openSeadragon.viewport.deltaPointsFromPixels(deltaPixels);
                openSeadragon.viewport.panBy(deltaPoints);
                drag.lastPos = event["position"].clone();
            }
        },
        nonPrimaryReleaseHandler: function (event) {
            if (event["button"] === 1) {
                releasePointer(event);
                drag = null;
            }
        },
    });
};

export function initSeaDragon(initOptions) {
    //初始化视图
    const openSeadragon = new OpenSeadragon.Viewer({
        crossOriginPolicy: "Anonymous",
        id: initOptions.canvasId, //指定显示的div
        //prefixUrl: "//src/assets/openseadragon/prefix/", //库中按钮等图片所在文件夹
        prefixUrl: "/static/images/openseadragon/prefix/", //库中按钮等图片所在文件夹 必须要复制到对应路径下  动态加载src 不能放在assets下 放在public下
        tileSources:{
                type: "image",
                url: initOptions.img_url,
        },
        sequenceMode: true,
        //showReferenceStrip: true,
        //referenceStripScroll: "vertical", // 显示多个图片
        //说明所要显示源图片的信息
        gestureSettingsMouse: { clickToZoom: false }, //设置鼠标单击不可放大
        showNavigator: true, //导航视图
        // // mouseNavEnabled:false,
        navigatorAutoFade: false, //导航栏永久存在
        // // navigatorBackgroundColor:'white',
        // // navigatorPosition: "TOP_LEFT",
        navigatorPosition: "ABSOLUTE",
        navigatorTop: "4px",
        navigatorLeft: "5px",
        navigatorHeight: "90px",
        navigatorWidth: "200px", //导航窗口的位置
        navigatorBackground: "#fefefe",
        navigatorBorderColor: "#191970",
        navigatorDisplayRegionColor: "#FF0000",
        zoomInButton: "zoom-in", //放大
        zoomOutButton: "zoom-out", //缩小
        homeButton: "home", //恢复默认
        fullPageButton: "full-page", //全屏
        //previousButton: "previous-figure", //上一幅图片
        //nextButton: "next-figure", //上一幅图片
        // // debugMode: true, //开启调试模式
        // // debugGridColor:'#1B9E77', //调试模式下网格的颜色
        panHorizontal: true, //false:不能水平移动，只能竖直移动
        // defaultZoomLevel: 0.8, //初始化默认放大倍数，按home键也返回该层
        minZoomLevel: 0.1, //最小允许放大倍数
        maxZoomLevel: 10, //最大允许放大倍数
        // visibilityRatio: 0.3, //图片在框内的最小比例
        constrainDuringPan: true, //(default: false)是否限制拖拽出允许显示范围
    });
    // 初始化scalebar
    if (initOptions.ppm==0){
        // @ts-ignore
        openSeadragon.scalebar({
            pixelsPerMeter: 1, //设置像素与实际的比值 如果是像素对像素 或者未知即设为1
            minWidth: "100px",
            xOffset: 5,
            yOffset: 10,
            stayInsideImage: false,
            color: "rgb(0, 0, 0)",
            fontColor: "rgb(0, 0, 0)",
            backgroundColor: "rgba(255, 255, 255, 0.5)",
            fontSize: "middle",
            barThickness: 4,
            sizeAndTextRenderer: OpenSeadragon["ScalebarSizeAndTextRenderer"].PIXEL_LENGTH,     //单位 是像素
        });
    }else{
        // @ts-ignore
        openSeadragon.scalebar({
            pixelsPerMeter: initOptions.ppm, //设置像素与实际的比值 如果是像素对像素 或者未知即设为1
            minWidth: "100px",
            xOffset: 5,
            yOffset: 10,
            stayInsideImage: false,
            color: "rgb(0, 0, 0)",
            fontColor: "rgb(0, 0, 0)",
            backgroundColor: "rgba(255, 255, 255, 0.5)",
            fontSize: "middle",
            barThickness: 4,
            sizeAndTextRenderer: OpenSeadragon["ScalebarSizeAndTextRenderer"].METRIC_LENGTH,     //单位 是像素
        });
    }

    //初始化画板 引入fabricJs
    // initialize overlay初始化
    //@ts-ignore
    const overlay = openSeadragon.fabricjsOverlay({ scale: initOptions.img_width}); // 传入图片的宽度
    overlay.fabricCanvas().freeDrawingBrush.color = "red"; //设置自由绘颜色
    overlay.fabricCanvas().freeDrawingBrush.width = 2;
    // 关闭鼠标点击拖动 改为鼠标中键拖动
    changeZoomScrollOperation(openSeadragon);
    // 放大倍数的实时显示 TODO 第一次显示有问题  应该是图片像素的放大倍数  不是实际PPI
    function updateZoomLabel() {
        const zoom = openSeadragon.viewport.getZoom(true);
        const imageZoom = openSeadragon.viewport.viewportToImageZoom(zoom);
        const zoomEl = document.querySelectorAll("#zoom-num")[0];
        zoomEl.textContent = "" + imageZoom.toFixed(2);
    }
    // 绑定放大倍数的实时显示的事件
    openSeadragon.addHandler("animation", updateZoomLabel);
}