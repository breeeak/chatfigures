import request from "@/core/services/ApiService"

// 登录方法
export function login(params:any) {
    return request({
        url: "/fadmin/login/",
        method: "post",
        data: params
    });
}
// 注册方法
export function register(params:any) {
    return request({
        url: "/fadmin/register/",
        method: "post",
        data: params
    });
}
// 找回密码方法
export function forgotPassword(params:any) {
    return request({
        url: "/fadmin/forgotPassword/",
        method: "post",
        data: params
    });
}

// 获取用户详细信息
export function getUserInfo() {
    return request({
        url: "/fadmin/getInfo/",
        method: "get"
    });
}

// 退出方法
export function logout() {
    return request({
        url: "/fadmin/logout/",
        method: "post"
    });
}



