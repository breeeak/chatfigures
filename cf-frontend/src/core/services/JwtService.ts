
// @ts-ignore
import Cookies from "js-cookie";
const ID_TOKEN_KEY = "fAdmin-Token";

// TODO js-cookie考虑是否增加expires 参考：https://github.com/js-cookie/js-cookie


/**
 * @description get token form Cookies
 * @param name: access or refresh
 */
export const getToken = (name:string): string | null => {
    return Cookies.get(`${ID_TOKEN_KEY}-${name}`);
};

/**
 * @description save token into Cookies
 * @param token: string
 * @param name: access or refresh
 * @param expires
 */
export const setToken = (name:string, token: string, expires:number=7): void => {
    if (expires){   // 如果设置了过期时间 chrome 对于localhost设置过期时间无效 使用127.0.0.1即可
        return Cookies.set(`${ID_TOKEN_KEY}-${name}`, token, { expires:expires });
    }
    return Cookies.set(`${ID_TOKEN_KEY}-${name}`, token);
};

/**
 * @description remove token form Cookies
 * @param name: access or refresh
 */
export const removeToken = (name:string): void => {
    return Cookies.remove(`${ID_TOKEN_KEY}-${name}`);
};

/**
 * @description 拿到 cookie 全部的值
 */
export const getAll = function () {
    return Cookies.get()
}

export default { getToken, setToken, removeToken,getAll};