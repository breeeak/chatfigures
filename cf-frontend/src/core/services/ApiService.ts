import axios from "axios";
import { getToken } from "@/core/services/JwtService";
import ErrorCode from "@/core/services/ErrorCode";

axios.defaults.headers["Content-Type"] = "application/json;charset=utf-8";

// 创建axios实例
const service = axios.create({
    // axios中请求配置有baseURL选项，表示请求URL公共部分
    baseURL: import.meta.env.VITE_APP_BASE_API,
    // 超时
    timeout: import.meta.env.VITE_APP_TIMEOUT,
});

// request拦截器
service.interceptors.request.use((config) => {
    // 是否需要设置 token
    const isToken = (config.headers || {}).isToken === false; //默认是false 除非设置了headers isToken=false, 才关闭关闭校验
    if (getToken("access") && !isToken) {   // 先从客户端找是否有token, 如果得到了token 并且没有关闭token
        config.headers!["Authorization"] = "Bearer " + getToken("access"); // 让每个请求携带自定义token 请根据实际情况自行修改
    }
    return config;
});

// 响应拦截器
service.interceptors.response.use((res) => {
    // 未设置状态码则默认成功状态
    const code = res.data.code || 200;
    //如果在错误码里 Reject
    if (ErrorCode.indexOf(code) != -1) {
        console.log("error", code);
        return Promise.reject(res);
    } else {
        console.log(res)
        return Promise.resolve(res.data);    //只需要返回里面的data即可 因为data有个双重嵌套
    }
});


export default service;
