import request from "@/core/services/ApiService"

// 获取一个新的image和数据
export function getNewLabel(params:any) {
    return request({
        url: "/figures/getNewLabel/",
        method: "post",
        data: params
    });
}

// 获取多个Image和其状态
export function getLabelList(params:any) {
    return request({
        url: "/figures/getLabelList/",
        method: "post",
        data: params
    });
}

// 导出数据
export function exportLabels(params:any) {
    return request({
        url: "/figures/compressLabel/",
        method: "post",
        data: params,
        responseType: 'blob'    // 二进制流必须写明
    });
}