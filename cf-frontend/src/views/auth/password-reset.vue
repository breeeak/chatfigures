<template>
  <!--begin::Wrapper-->
    <div class="col-sm-8 col-xxl-4 bg-white rounded shadow-sm p-10 p-lg-15">
      <!--begin::Heading-->
      <div class="text-center mb-10">
        <!--begin::Title-->
        <h1 class="text-dark mb-3">
          Forget Password ?
        </h1>
        <!--end::Title-->
        <!--begin::Link-->
        <div class="text-gray-400 fw-bold fs-4">
          Enter your email to reset your password.
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

        <div class="d-flex flex-wrap justify-content-center pb-lg-0">
          <button ref="submitButton"  type="submit" class="btn btn-lg btn-primary text-light me-2"
          >
            <span v-if="submitLoading" class="spinner-border spinner-border-sm" role="status"></span>
            Submit</button>
          <router-link
              to="/sign-in"
              class="btn btn-outline-primary text-hover-white ms-2"
          >Cancel</router-link>
        </div>
      </Form>
    </div>
  <!--end::Wrapper-->
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
// 表单验证
import * as Yup from "yup";
import { ErrorMessage, Field, Form } from "vee-validate";
const submitButton = ref<HTMLButtonElement | null>(null);
const submitLoading = ref(false)
const formData = ref({"email":""});

//Create form validation object
const validate_schema = Yup.object().shape({
  email: Yup.string()
      .email("Please enter a valid email")
      .required("Please enter a valid email"),
});

const onSubmit = (values: any) => {
  submitButton.value!.disabled = true;
  submitLoading.value = true;
  console.log(values)
  console.log(formData)
  // TODO reset password

}

</script>

<style scoped>

</style>