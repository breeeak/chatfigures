<template>
<!--    <nav-bar />-->
    <div class="container">
        <div class="row">
            <div class="col-12 text-center my-5">
                <p class="display-5 my-4">User Guidelines</p>
            </div>
        </div>
        <div class="row">
            <ul>
                <li><a href="#figure-separation">Figure Separation Guidelines</a></li>
                <li><a href="#interactive-measurement">Interactive Measurement Guidelines</a></li>
            </ul>
        </div>
        <div class="row" id="figure-separation">
            <div class="col-12 my-5">
                <p class="display-6 my-4">Figure Separation Guidelines</p>
            </div>
        </div>
        <div class="row d-inline" >
            <p>
                If you want separate compound figures on any website, you can install our chrome extension. Please refer to the <router-link :to="{name:'extension-instructions'}">Chrome Extension Instruction</router-link> for more details.
            </p>
        </div>
        <div class="row d-inline" >
            <h1>Getting Started</h1>
            <p>
                0. Go to our website for <router-link to="figure-separation">Figure Separation</router-link>.
            </p>
            <p>
                1. Click and choose an local image. You can also drag and drop an image to the canvas.
            </p>
            <div class="text-center">
                <img  class="w-50" src="/static/images/docs/figure-seperation/upload.jpg" alt="install-chrome">
            </div>
            <p>
                2. Click "Upload and Start Separation". Then, separation results will be shown on a new tab.
            </p>
            <div class="text-center">
                <img  class="w-50" src="/static/images/docs/figure-seperation/3newtab.jpg" alt="3newtab">
            </div>
            <p>
                3. You can customize the result, download each sub figure, export json format labels.
            </p>
            <div class="text-center">
                <img  class="w-50" src="/static/images/docs/figure-seperation/4download.jpg" alt="download">
            </div>
        </div>
        <div class="row d-inline" >
            <h1>Quick Reference</h1>
            <div class="text-center">
                <img  class="w-75" src="/static/images/docs/figure-seperation/references.jpg" alt="install-chrome">
            </div>
        </div>
        <div class="row d-inline" >
            <h1>Short Cut</h1>
            <p>
                1. select an object and press "ctrl + del" to delete object
            </p>
            <p>
                2. press "middle mouse button" to drag viewport
            </p>
            <p>
                3. press "shift + mouse wheel"to zoom in or zoom out viewport
            </p>
        </div>
        <div class="row d-inline" >
            <h1>Restful API</h1>
            <p>
                You can upload an image in base64 format to do the compound figure separation.
            </p>
            <h4 class="mt-5">Request Url</h4>
            <table class="table table-striped table-hover w-50 border">
                <tr>
                    <th>Method</th>
                    <th>Url</th>
                </tr>
                <tr>
                    <td>Post</td>
                    <td>https://www.chatfigures.com/api/figures/figureSeparationUpload/</td>
                </tr>
            </table>
            <h4  class="mt-5">Request Parameters</h4>
            <table class="table table-striped table-hover w-50 border">
                <tr>
                    <th>Name</th>
                    <th>is_required</th>
                    <th>Type</th>
                    <th>Description</th>
                </tr>
                <tr>
                    <td>filename</td>
                    <td>true</td>
                    <td>string</td>
                    <td>the name of the image</td>
                </tr>
                <tr>
                    <td>base64data</td>
                    <td>true</td>
                    <td>string</td>
                    <td>base64 encoded image</td>
                </tr>
            </table>
            <h4  class="mt-5">Response Format</h4>
            <table class="table table-striped table-hover w-50 border">
                <tr>
                    <th>Name</th>
                    <th>Type</th>
                    <th>Description</th>
                </tr>
                <tr>
                    <td>code</td>
                    <td>int</td>
                    <td>status code 200 for success</td>
                </tr>
                <tr>
                    <td>taskId</td>
                    <td>int</td>
                    <td>the taskId</td>
                </tr>
                <tr>
                    <td>jsonDict</td>
                    <td>json</td>
                    <td>the detection results</td>
                </tr>
                <tr>
                    <td>redirectUrl</td>
                    <td>string</td>
                    <td>you can view the results with this url</td>
                </tr>
                <tr>
                    <td>token</td>
                    <td>string</td>
                    <td>you need to request with this token as head (Authorization) for "redirectUrl"</td>
                </tr>
            </table>
        </div>

        <!--Interactive Measurement-->
        <div class="row" id="interactive-measurement">
            <div class="col-12 my-5">
                <p class="display-6 my-4">Interactive Measurement Guidelines</p>
            </div>
        </div>

        <div class="row d-inline" >
            <h1>Getting Started</h1>
            <p>
                0. Go to our website for <router-link to="interactive-measurement">Interactive Measurement</router-link>.
            </p>
            <p>
                1. Click and choose an local image. You can also drag and drop an image to the canvas.
            </p>
            <div class="text-center">
                <img  class="w-50" src="/static/images/docs/interactive-measurements/upload.jpg" alt="install-chrome">
            </div>
            <p>
                2. Click "Upload and Start Measurement". Then, scale information will be extracted on a new tab.
            </p>
            <div class="text-center">
                <img  class="w-50" src="/static/images/docs/interactive-measurements/results_im.jpg" alt="3newtab">
            </div>
            <p>
                3. You can customize the scale information, measurement and export json format labels.
            </p>
<!--            <div class="text-center">-->
<!--                <img  class="w-50" src="/static/images/docs/interactive-measurements/quick references.jpg" alt="download">-->
<!--            </div>-->
        </div>
        <div class="row d-inline" >
            <h1>Quick Reference</h1>
            <div class="text-center">
                <img class="w-75" src="/static/images/docs/interactive-measurements/quick_references.jpg" alt="install-chrome">
            </div>
        </div>
        <div class="row d-inline" >
            <h1>Short Cut</h1>
            <p>
                1. select an object and press "ctrl + del" to delete object
            </p>
            <p>
                2. press "middle mouse button" to drag viewport
            </p>
            <p>
                3. press "shift + mouse wheel"to zoom in or zoom out viewport
            </p>
            <p>
                4. press "esc" to cancel current draws.
            </p>
            <p>
                5. press "o" to quickly close a polygon.
            </p>
        </div>


        <div class="row d-inline" >
            <h1>Contact</h1>
            <p>
            At present, this project is almost maintained by myself and Copilot 😆 . I know the project has a lot of problems, and there are many places that need to be improved.
            </p>
            <p>
            If you have any questions, please contact me by email: shuomeng2-c@my.cityu.edu.hk
            </p>
            <p>
            This project will be continuously updated at least until my graduation. If you are interested in this project, you can also join me.
            </p>
            <p class="text-danger">
                If you find the response time is too long, the reason may be that the server is not powerful enough. It is just 1 core (2.1GHz) 2G memory 2M bandwidth without GPU.
            </p>
            <p>
                If you like this project, you can buy me a cup of coffee to cover the cost of the server. ☕
                Thank you!
            </p>
        </div>




        <div class="row text-center">
            <div class="col-4">
                <img class="w-50" src="/static/images/docs/bmc_qr.png" alt="">
            </div>
            <div class="col-4">
                <img class="w-50" src="/static/images/docs/wechatpay.jpg" alt="">
            </div>
            <div class="col-4">
                <img class="w-50" src="/static/images/docs/alipay.jpg" alt="">
            </div>
        </div>


        <div class="row text-center mb-5">
            <div class="col-4 ">
                buymeacoffee
            </div>
            <div class="col-4">
                wechatpay
            </div>
            <div class="col-4">
               alipay
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import NavBar from "@/components/layout/nav-bar.vue";
import InteractiveMeasurement from "@/views/projects/interactive-measurement/interactive-measurement.vue";
</script>

<style scoped>

</style>