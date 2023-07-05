import { getUserInfo, login, logout,register,forgotPassword } from "@/api/fadmin/login";
import { getToken, removeToken, setToken } from "@/core/services/JwtService";
import { Module, Action, Mutation, VuexModule } from "vuex-module-decorators";


@Module
export default class AuthModule extends VuexModule{
    token = getToken("access")
    name = ""
    avatar = ""
    roles:Array<any> = []
    permissions:Array<any> = []
    unread_msg_count = 0

    // 登录
    @Action
    Login(credentials:object) {
        console.log(credentials)
        return new Promise((resolve,reject)=>{
            login(credentials).then(res => {
                console.log(res)
                setToken("access",res.data.access);
                setToken("refresh",res.data.refresh);
                this.context.commit("SET_TOKEN", res.data.access);
                resolve(res);
            }).catch(error => {
                reject(error);
            });
        });
    }

    // 注册   TODO 注册功能完善
    @Action
    Register(credentials:object) {
        console.log(credentials)
        return new Promise((resolve,reject)=>{
            register(credentials).then(res => {
                console.log(res)
                setToken("access",res.data.access);
                setToken("refresh",res.data.refresh);
                this.context.commit("SET_TOKEN", res.data.access);
                resolve(res);
            }).catch(error => {
                console.log(error);
                reject(error);
            });
        });
    }
    // 找回密码
    @Action
    ForgotPassword(credentials:object) {
        console.log(credentials)
        return new Promise((resolve,reject)=>{
            forgotPassword(credentials).then(res => {
                console.log(res)
                setToken("access",res.data.access);
                setToken("refresh",res.data.refresh);
                this.context.commit("SET_TOKEN", res.data.access);
                resolve(res);
            }).catch(error => {
                console.log(error);
                reject(error);
            });
        });
    }

    @Action
    GetUserInfo(){
        return getUserInfo().then(res => {  // 所有请求默认都是带token的 所以不用传参
            console.log(res)

        }).catch(error => {
            console.log(error);
        });
    }


    @Mutation
    SET_TOKEN(token: string | null){
        this.token = token;
    }
    @Mutation
    SET_NAME(name: string){
        this.name = name;
    }
    @Mutation
    SET_AVATAR(avatar: string){
        this.avatar = avatar;
    }
    @Mutation
    SET_ROLES(roles: Array<any>){
        this.roles = roles;
    }
    @Mutation
    SET_PERMISSIONS(permissions: Array<any>){
        this.permissions = permissions;
    }
    @Mutation
    SET_UNREAD_MSG_COUNT(unread_msg_count: number){
        this.unread_msg_count = unread_msg_count;
    }

}



