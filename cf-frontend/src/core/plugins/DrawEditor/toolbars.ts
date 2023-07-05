
export const toolBarIcons = [
    {
        drawType: "line",
        icon: "/static/icons/arr040.svg",
        type: "draw",
        tips: "Measure Distance",
    },
    {
        drawType: "area",
        icon: "/static/icons/art008.svg",
        type: "draw",
        tips: "Measure Area",
    },
    {
        drawType: "rectangle",
        icon: "/static/icons/abs010.svg",
        type: "draw",
        tips: "Draw rectangle",
    },
    {
        drawType: "circle",
        icon: "/static/icons/abs009.svg",
        type: "draw",
        tips: "Draw circle",
    },
    {
        drawType: "text",
        icon: "/static/icons/art001.svg",
        type: "draw",
        tips: "Draw text",
    },
    {
        drawType: "edit",
        icon: "/static/icons/gen055.svg",
        type: "draw",
        tips: "Edit",
    },
    { drawType: "", icon: "", type: "separate", tips: "" },     //占位用
    {
        drawType: "home",
        icon: "/static/icons/gen001.svg",
        type: "osd",
        tips: "Original size",
    },
    // {
    //   drawType: "full-page",
    //   icon: "/static/icons/art008.svg",
    //   type: "osd",
    //   tips: "全屏显示",
    // },
    {
        drawType: "zoom-in",
        icon: "/static/icons/arr009.svg",
        type: "osd",
        tips: "Zoom in",
    },
    { drawType: "zoom-num", icon: "", type: "info", tips: "倍率" },
    {
        drawType: "zoom-out",
        icon: "/static/icons/arr010.svg",
        type: "osd",
        tips: "Zoom out",
    },

    { drawType: "", icon: "", type: "separate", tips: "" },
    {
        drawType: "clear",
        icon: "/static/icons/gen027.svg",
        type: "func",
        tips: "Clear all draws",
    },
    {
        drawType: "setting",
        icon: "/static/icons/cod009.svg",
        type: "func",
        tips: "Settings",
    },
    {
        drawType: "save",
        icon: "/static/icons/gen006.svg",
        type: "func",
        tips: "Output image",
    },
    {
        drawType: "export",
        icon: "/static/icons/fil017.svg",
        type: "func",
        tips: "Output meta info",
    },
    {
        drawType: "back",
        icon: "/static/icons/arr059.svg",
        type: "func",
        tips: "Back to results page",
    },
];


export const labelBarIcons = [
    {
        drawType: "figures",
        title:"Subfigures",
        shortTitle:"Fig#",
        icon: "/static/icons/gen008.svg",
        type: "draw",
        tips: "Add Subfigures",
    },
   {
        drawType: "figure_nos",
        title:"Subfigure Labels",
        shortTitle:"FigNo#",
        icon: "/static/icons/txt010.svg",
        type: "draw",
        tips: "Add Subfigure Label",
    },
    {
        drawType: "bars",
        title:"Scalebar",
        shortTitle:"Bar#",
        icon: "/static/icons/ecm010.svg",
        type: "draw",
        tips: "Add Scalebar",
    },
    {
        drawType: "labels",
        title:"Scalebar Labels",
        shortTitle:"BarT#",
        icon: "/static/icons/txt007.svg",
        type: "draw",
        tips: "Add Scalebar Labels",
    },
    {
        drawType: "edit",
        title:"",
        icon: "/static/icons/gen055.svg",
        type: "draw",
        tips: "Edit label",
    },
    { drawType: "", icon: "", type: "separate", tips: "" },     //占位用
    {
        drawType: "home",
        icon: "/static/icons/gen001.svg",
        type: "osd",
        tips: "Original size",
    },
    {
        drawType: "last_img",
        icon: "/static/icons/arr002.svg",
        type: "osd",
        tips: "Last Image",
    },
    {
        drawType: "zoom-in",
        icon: "/static/icons/arr009.svg",
        type: "osd",
        tips: "Zoom in",
    },
    { drawType: "zoom-num", icon: "", type: "info", tips: "倍率" },
    {
        drawType: "zoom-out",
        icon: "/static/icons/arr010.svg",
        type: "osd",
        tips: "Zoom out",
    },
    {
        drawType: "next_img",
        icon: "/static/icons/arr001.svg",
        type: "osd",
        tips: "Next Image",
    },
    { drawType: "", icon: "", type: "separate", tips: "" },
    {
        drawType: "clear",
        icon: "/static/icons/gen027.svg",
        type: "func",
        tips: "Clear all draws",
    },
    {
        drawType: "setting",
        icon: "/static/icons/cod009.svg",
        type: "func",
        tips: "Settings",
    },
    {
        drawType: "save",
        icon: "/static/icons/gen006.svg",
        type: "func",
        tips: "Output image",
    },
    {
        drawType: "export",
        icon: "/static/icons/fil017.svg",
        type: "func",
        tips: "Output meta info",
    },
    {
        drawType: "back",
        icon: "/static/icons/art002.svg",
        type: "func",
        tips: "Go to measure page",
    },
];


export const figureSeparationBar = [
    {
        drawType: "figures",
        title:"Subfigures",
        shortTitle:"Fig#",
        icon: "/static/icons/gen008.svg",
        type: "draw",
        tips: "Add Subfigures",
        addText: false,
        isTop: true,
        relationIndex: 0,
    },
    {
        drawType: "figure_nos",
        title:"Subfigure Labels",
        shortTitle:"FigNo#",
        icon: "/static/icons/txt010.svg",
        type: "draw",
        tips: "Add Subfigure Label",
        addText: true,
        isTop: false,
        relationIndex: 1,
    },
    {
        drawType: "edit",
        title:"",
        icon: "/static/icons/gen055.svg",
        type: "draw",
        tips: "Edit label",
        shortTitle:"FigNo#",
        addText: false,
        isTop: false,
        relationIndex: 5,
    },
    { drawType: "", icon: "", type: "separate", tips: "" },     //占位用
    {
        drawType: "home",
        icon: "/static/icons/gen001.svg",
        type: "osd",
        tips: "Original size",
    },
    {
        drawType: "zoom-in",
        icon: "/static/icons/arr009.svg",
        type: "osd",
        tips: "Zoom in",
    },
    { drawType: "zoom-num", icon: "", type: "info", tips: "倍率" },
    {
        drawType: "zoom-out",
        icon: "/static/icons/arr010.svg",
        type: "osd",
        tips: "Zoom out",
    },
    { drawType: "", icon: "", type: "separate", tips: "" },
    {
        drawType: "clear",
        icon: "/static/icons/gen027.svg",
        type: "func",
        tips: "Clear all draws",
    },
    {
        drawType: "setting",
        icon: "/static/icons/cod009.svg",
        type: "func",
        tips: "Settings",
    },
    // TODO 报错被污染的图像
    // {
    //     drawType: "save",
    //     icon: "/static/icons/gen006.svg",
    //     type: "func",
    //     tips: "Output image",
    // },
    {
        drawType: "export",
        icon: "/static/icons/fil017.svg",
        type: "func",
        tips: "Output meta info",
    },
    // TODO 反馈模块
    // {
    //     drawType: "feedback",
    //     icon: "/static/icons/art002.svg",
    //     type: "func",
    //     tips: "Feedback errors or corrections to us",
    // },
];