// 上传并检测
import request from "@/core/services/ApiService";

export function getFigureSeparationUrl() {
    return request.defaults.baseURL + "/figures/detectSubfigures/";
}

// 获取一个新的image和数据
export function getFigureSeparationResults(params:any) {
    return request({
        url: "/figures/getFigureSeparationResults/",
        method: "get",
        params: params  // get传参必须用params
    });
}

// 获取一个新的image和数据
export function getFigureSeparationList(params:any) {
    return request({
        url: "/figures/getFigureSeparationList/",
        method: "post",
        data: params
    });
}

// 导出所有的结果
export function exportAllSeparations(params:any) {
    return request({
        url: "/figures/exportAllSeparations/",
        method: "post",
        data: params,
        responseType: 'blob'    // 二进制流必须写明
    });
}

// 上传文件
export function figureSeparationUpload(params:any) {
    return request({
        url: "/figures/figureSeparationUpload/",
        method: "post",
        data: params
    });
}