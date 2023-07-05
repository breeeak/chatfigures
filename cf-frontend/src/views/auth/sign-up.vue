<template>
  <!--begin::Wrapper-->
    <div class="col-sm-8 col-xxl-5 bg-white rounded shadow-sm py-5 px-15">
      <!--begin::Heading-->
      <div class="text-center mb-10">
        <!--begin::Title-->
        <h1 class="text-dark mb-3">
          Create an Account
        </h1>
        <!--end::Title-->

        <!--begin::Link-->
        <div class="text-gray-400 fw-bold fs-4">
          Already have an account?
          <router-link to="/sign-in" class="link-primary fw-bolder">
            Sign in here
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
              autocomplete="off"
              placeholder="Enter a valid email address"
          />
          <!--end::Input-->
          <ErrorMessage class="text-danger" name="email" />
        </div>

        <!-- Password input -->
        <div class="d-flex justify-content-between">
          <label class="form-label fs-6 fw-bolder text-dark">Password</label>
        </div>
        <div class="input-group" >
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
        <!--begin::Hint-->
        <div class="text-muted mt-1 mb-4 ">
          Use 8 or more characters with a mix of letters, numbers, symbols.
        </div>
        <!--end::Hint-->

        <!-- Password Confirm input -->
        <label class="form-label fs-6 fw-bolder text-dark">Confirm Password</label>
        <div class="input-group" >
          <!--begin::Input-->
          <Field
              class="form-control form-control-solid"
              :type="showPassword?'text':'password'"
              name="password_confirm"
              v-model="formData.confirm_password"
              placeholder="Enter password again"

          />
          <!--end::Input-->
          <span class="input-group-text rounded-end" id="inputGroupPrepend" @click="toggleShow">
            <font-awesome-icon v-if="showPassword" icon="fa-solid fa-eye" />
            <font-awesome-icon v-else icon="fa-solid fa-eye-slash" />
          </span>
        </div>
        <ErrorMessage class="text-danger"  name="password_confirm" />
        <!--begin::Submit button-->
        <button ref="submitButton"   type="submit" class="btn btn-lg btn-primary w-100 mb-5 mt-5 text-light"
        ><span v-if="submitLoading" class="spinner-border spinner-border-sm" role="status"></span>
          Continue</button>
        <!--end::Submit button-->

        <!--begin::Input group-->
        <div class="row mb-10 text-center">
          <div class="text-muted">
            By continuing, you agree with our <a href="/privacy-policy.html">Privacy Policy</a> & <a href="/terms-conditions.html">User terms</a>
          </div>
        </div>
        <!--end::Input group-->

      </Form>
    </div>
  <!--end::Wrapper-->
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useStore } from "vuex";
import { useRouter } from "vue-router";
// 表单验证
import * as Yup from "yup";
import { ErrorMessage, Field, Form } from "vee-validate";
// 弹窗
import Swal from "sweetalert2";
import { library } from '@fortawesome/fontawesome-svg-core'
import { faEye,faEyeSlash } from '@fortawesome/free-solid-svg-icons'
library.add(faEye,faEyeSlash)
const store = useStore();
const router = useRouter();

const submitButton = ref<HTMLButtonElement | null>(null);
const submitLoading = ref(false)
const formData = ref({"email":"","password":"","confirm_password":""});

//Create form validation object
const validate_schema = Yup.object().shape({
  email: Yup.string()
      .email("Please enter a valid email")
      .required("Please enter a valid email"),
  password: Yup.string()
      .min(4, "Password characters must be at least" + " ${min}")
      .required("Please enter password"),
  password_confirm: Yup.string()
      .oneOf([Yup.ref("password"), null], "Passwords must match")
      .required("Please enter password again"),
});

const onSubmit = (values: any) => {
  submitButton.value!.disabled = true;
  submitLoading.value = true;
  console.log(values)
  console.log(formData)
  store.dispatch("Login", formData.value).then((res)=>{
    Swal.fire({
      //title: "Login Error",
      text: "Welcome! You have successfully registered!",
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

  // TODO submit Register
}

// toggleShow password
const showPassword = ref(false);
const toggleShow = () => {
  showPassword.value = !showPassword.value;
};

</script>

<style scoped>

</style>