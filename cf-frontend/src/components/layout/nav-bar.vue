<template>
    <nav class="navbar navbar-expand-lg sticky-top bg-light">
        <div class="container" >
            <router-link class="navbar-brand " :to="{name:router_name}">
                <div class="d-flex ">
                    <img src="@/assets/images/logos/chat-figures-logo-no-background.svg" alt="" width="180" height="60"
                         class="d-inline align-text-top">
                    <div class="align-self-center ms-5 d-none d-sm-none d-md-block">
                        <h4 class="d-inline"> {{title}} </h4>
                    </div>
                </div>
            </router-link>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
                    aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            Functions
                        </a>
                        <ul class="dropdown-menu">
                            <li><router-link class="dropdown-item" :class="router_name=='figure-separation'?'link-primary':''" :to="{name:'figure-separation'}">Figure Separation</router-link></li>
                            <li><router-link class="dropdown-item" :class="router_name=='interactive-measurement'?'link-primary':''" :to="{name:'interactive-measurement'}">Interactive Measurement</router-link></li>
                        </ul>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" aria-current="page" href="#Features">
                            Features
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#Resources">Resources</a>
                    </li>
                    <li class="nav-item">
                        <router-link target="_blank" class="nav-link" :to="{ name: 'user-guidelines'}">Documentation</router-link>
                    </li>
                </ul>
                <router-link class="btn btn-sm btn-danger btn-hover-scale text-white d-none" :to="{ name: 'sign-in'}">
                    Sign In / Sign Up
                </router-link>
            </div>
        </div>
    </nav>
</template>

<script setup lang="ts">
const props = defineProps({
    title: {
        type: String,
        default: "Figure Separation",
    },
    router_name: {
        type: String,
        default: "figure-separation",
    },
})
</script>

<style scoped>

</style>