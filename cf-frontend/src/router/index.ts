import {createRouter, createWebHistory} from 'vue-router'
import {toRaw} from "vue";
import store from "@/store";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
          path: "/",
          redirect: {name: "home"},
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
                        import("@/views/projects/figure-separation/figure-separation.vue"),
                },
                {
                    path: "separation-results/:resultId",
                    name: "separation-results",
                    component: () =>
                        import("@/views/projects/figure-separation/separation-results.vue"),
                }
            ],
        },
        {
            path: "/",
            component: () => import("@/views/layout/base-layout.vue"),
            children: [
                {
                    path: "label-editor",
                    name: "label-editor",
                    component: () =>
                        import("@/views/projects/figure-labeler/label-editor.vue"),
                }
            ],
        },
        {
            path: "/docs",
            component: () => import("@/views/layout/base-layout.vue"),
            children: [
                {
                    path: "user-guidelines",
                    name: "user-guidelines",
                    component: () =>
                        import("@/views/projects/docs/user-guidelines.vue"),
                },
                {
                    path: "extension-instructions",
                    name: "extension-instructions",
                    component: () =>
                        import("@/views/projects/docs/extension-instructions.vue"),
                }
            ],
        },
        {
            path: "/",
            component: () => import("@/views/layout/base-layout.vue"),
            children: [
                {
                    path: "interactive-measurement",
                    name: "interactive-measurement",
                    component: () =>
                        import("@/views/projects/interactive-measurement/interactive-measurement.vue"),
                },
                {
                    path: "measurement-results/:resultId",
                    name: "measurement-results",
                    component: () =>
                        import("@/views/projects/interactive-measurement/measurement-results.vue"),
                }
            ],
        },
        {
            path: '/',
            component: () => import("@/views/layout/base-layout.vue"),
            children: [
                {
                    path: "",    // home
                    name: "home",
                    component: () => import("@/views/projects/home/project-home.vue"),
                },
                {
                    path: "404",    // 404
                    name: "404",
                    component: () => import("@/views/projects/error-pages/Error404.vue"),
                },
            ],
        },
        {
            path: '/:pathMatch(.*)*',   // 全局404 跳转到首页 放到最后
            name:"not-found",
            redirect: '/404',
        },
    ]
})


export default router
