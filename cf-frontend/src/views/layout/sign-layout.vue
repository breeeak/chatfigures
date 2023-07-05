<template>
  <!--begin::Wrapper-->
  <div class="row d-flex justify-content-center align-items-center w-100 bg-div">
    <div class="col-xxl-6 d-none d-xxl-block text-center">
      <img src="/static/images/design/signin.webp"
           class="h-700px" alt="Chat Figures——Scientific Figure Understanding" >
    </div>
    <router-view></router-view>
  </div>
  <!--end::Wrapper-->
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useStore } from "vuex";
import { useRouter } from "vue-router";
// 字体图标
import { library } from '@fortawesome/fontawesome-svg-core'
import { faEye,faEyeSlash } from '@fortawesome/free-solid-svg-icons'
// 表单验证
import * as Yup from "yup";
import { ErrorMessage, Field, Form } from "vee-validate";
// 弹窗
import Swal from "sweetalert2";


const APP_NAME = import.meta.env.VITE_APP_NAME;
library.add(faEye,faEyeSlash)
const store = useStore();
const router = useRouter();

const submitButton = ref<HTMLButtonElement | null>(null);
const submitLoading = ref(false)
const formData = ref({"username":"","email":"","password":""});

//Create form validation object
const validate_schema = Yup.object().shape({
  email: Yup.string()
      .email("Please enter a valid email")
      .required("Please enter a valid email"),
  password: Yup.string()
      .min(4, "Password characters must be at least" + " ${min}")
      .required("Please enter password"),
});

const onSubmit = (values: any) => {
  // 登录按钮
  submitButton.value!.disabled = true;
  submitLoading.value = true;
  formData.value.username = formData.value.email;
  console.log(formData)
  store.dispatch("Login", formData.value).then((res)=>{
    Swal.fire({
      //title: "Login Error",
      text: "You have successfully logged in!",
      icon: "success",
      buttonsStyling: false,
      showConfirmButton: false,
      timer: 1500, //后面的无效 没有按钮
    }).then(()=> {
      // Go to page after successfully login
      router.push({ name: "dashboard" });
    });
  }).catch(()=>{
    Swal.fire({
      //title: "Login Error",
      text: "Username and password mismatch",
      icon: "error",
      buttonsStyling: false,
      confirmButtonText: "Try again",
      customClass: {
        confirmButton: "btn btn-lg btn-danger text-light",
      },
    }).then(()=>{
      submitButton.value!.disabled = false;
      submitLoading.value = false;
    });
  });
}

// toggleShow password
const showPassword = ref(false);
const toggleShow = () => {
  showPassword.value = !showPassword.value;
};

</script>

<style scoped>
.bg-div {
  background-image: linear-gradient(#d16ba5, #86a8e7);
  background-size: 100% 100%;
  position : absolute;
  width : 100%;
  height : 100%;
}
</style>