<template>
  <!--begin::Wrapper-->
    <div class="col-sm-8 col-xxl-4  bg-white rounded shadow-sm p-10 p-lg-15">
      <!--begin::Heading-->
      <div class="text-center mb-10">
        <!--begin::Title-->
        <h1 class="text-dark mb-3">
          Sign In to<br>
          <span class="text-danger">{{ APP_NAME }}</span>
        </h1>
        <!--end::Title-->

        <!--begin::Link-->
        <div class="text-gray-400 fw-bold fs-4">
          New Here?
          <router-link to="/sign-up" class="link-primary fw-bolder">
            Create an Account
          </router-link>
        </div>
        <!--end::Link-->
      </div>
      <!--begin::Heading-->

      <Form @submit="onSubmit" :validation-schema="validate_schema">
        <!-- Email input -->
        <div class="mb-4" >
          <label class="form-label fs-6 fw-bolder text-dark">Email</label>
          <!--begin::Input-->
          <Field
              class="form-control"
              type="text"
              name="email"
              v-model="formData.email"
              placeholder="Enter a valid email address"
          />
          <!--end::Input-->
          <ErrorMessage class="text-danger" name="email" />
        </div>

        <!-- Password input -->
        <div class="d-flex justify-content-between">
          <label class="form-label fs-6 fw-bolder text-dark">Password</label>
          <router-link to="/password-reset" class="link-primary fs-6 fw-bolder">
            Forget Password ?
          </router-link>
        </div>
        <div class="mb-4 input-group" >
          <!--begin::Input-->
          <Field
              class="form-control form-control-solid"
              :type="showPassword?'text':'password'"
              name="password"
              v-model="formData.password"
              placeholder="Enter password"
          />
          <!--end::Input-->
          <span class="input-group-text rounded-end" id="inputGroupPrepend" @click="toggleShow">
            <font-awesome-icon v-if="showPassword" icon="fa-solid fa-eye" />
            <font-awesome-icon v-else icon="fa-solid fa-eye-slash" />
          </span>
        </div>
        <ErrorMessage class="text-danger"  name="password" />
        <!--begin::Submit button-->
        <button ref="submitButton"  type="submit" class="btn btn-lg btn-primary w-100 mb-5 mt-5 text-light"
        ><span v-if="submitLoading" class="spinner-border spinner-border-sm" role="status"></span>
          Continue</button>
        <!--end::Submit button-->
      </Form>
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
      router.push({ name: "figure-separation" });
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

</style>