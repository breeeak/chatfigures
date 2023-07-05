import { default as request } from "@/core/services/ApiService";

// 新增文件
export function addSaveFile(data) {
    // return request.post("/fadmin/system/savefile/", data);
    //return request.post("/figures/upload/", data);
    // 获取baseURL

    return request.defaults.baseURL + "/figures/upload/";
}

export function getUploadUrl() {
    return request.defaults.baseURL + "/fadmin/file/";
}
