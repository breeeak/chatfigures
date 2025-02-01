
import request from "@/core/services/ApiService";

// 上传并检测
export function getDetectUrl() {
    return request.defaults.baseURL + "/measurement/detect/";
}

// 获取一个新的image和数据
export function getResults(params:any) {
    return request({
        url: "/measurement/getResults/",
        method: "get",
        params: params  // get传参必须用params
    });
}
// 初始化图像对象
export function initMeasureImage(params:any) {
    return request({
        url: "/measurement/initMeasureImage/",
        method: "get",
        params: params  // get传参必须用params
    });
}

// 根据点获取一个mask
export function measureAnythingPoint(params:any) {
    return request({
        url: "/measurement/measureAnythingPoint/",
        method: "post",
        data: params  // post传参必须用data
    });
}
// 上传文件并检测
export function interactiveMeasurementUpload(params:any) {
    return request({
        url: "/measurement/interactiveMeasurementUpload/",
        method: "post",
        data: params  // post传参必须用data
    });
}