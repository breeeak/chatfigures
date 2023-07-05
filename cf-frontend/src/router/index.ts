import {createRouter, createWebHistory} from 'vue-router'
import {toRaw} from "vue";
import store from "@/store";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: { name: 'figure-separation' }
        },

        {
            path: "/",
            component: () => import("@/views/layout/base-layout.vue"),
            children: [
                {
                    path: "/",
                    component: () =>
                        import("@/views/layout/sign-layout.vue"),
                    children: [
                        {
                            path: "/sign-in",
                            name: "sign-in",
                            component: () =>
                                import("@/views/auth/sign-in.vue"),
                        },
                        {
                            path: "/sign-up",
                            name: "sign-up",
                            component: () =>
                                import("@/views/auth/sign-up.vue"),
                        },
                        {
                            path: "/password-reset",
                            name: "password-reset",
                            component: () =>
                                import("@/views/auth/password-reset.vue"),
                        },
                    ]
                },
            ],
        },
        {
            path: "/",
            component: () => import("@/views/layout/base-layout.vue"),
            children: [
                {
                    path: "figure-separation",
                    name: "figure-separation",
                    component: () =>
                        import("@/views/projects//figure-separation/figure-separation.vue"),

                },
                {
                    path: "separation-results/:resultId",
                    name: "separation-results",
                    component: () =>
                        import("@/views/projects//figure-separation/separation-results.vue"),
                }
            ],
        },
        {
            path: '/:pathMatch(.*)*',    // 全局404 跳转到首页 放到最后
            name:"not-found",
            redirect: { name: 'figure-separation' },
        },
    ]
})


export default router
