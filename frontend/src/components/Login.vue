<template>
  <v-container fluid class="fill-height pa-0">
  <v-row class="fill-height">
    <v-col
      cols="12"
      md="6"
      class="left-side d-flex flex-column justify-center align-center text-center"
      style="height: 100vh;"
    >
      <v-img
        :src="mriImage"
        alt="MRI Illustration"
        width="300"
        height="300"
        contain
        class="mb-4"
      />
      <h1 class="white--text font-weight-bold mb-2">Welcome to NeuroScan</h1>
      <p class="white--text text-subtitle-1 px-6">
        AI-Driven analysis for early detection of Alzheimer’s disease and cognitive decline.
      </p>
    </v-col>

    <v-col
      cols="12"
      md="6"
      class="right-side d-flex justify-center align-center"
      style="height: 100vh;"
    >
      <v-card class="pa-6 elevation-12" width="70%">
        <v-card-title class="text-h5 font-weight-bold mb-2">Welcome Back!</v-card-title>
        <v-card-subtitle class="mb-6">Sign in to your account</v-card-subtitle>

        <v-form ref="loginForm" v-model="valid">
          <v-text-field
            v-model="email"
            placeholder="Email"
            :rules="[rules.required, rules.email]"
            outlined
            dense
            prepend-inner-icon="mdi-email"
            class="mb-4"
          />
          <v-text-field
            v-model="password"
            placeholder="Password"
            type="password"
            :rules="[rules.required]"
            outlined
            dense
            prepend-inner-icon="mdi-lock"
            class="mb-2"
          />
          <v-btn text small class="mt-1 mb-4" @click="forgotPassword">Forgot Password?</v-btn>

          <v-btn
            color="#1d1d6c"
            block
            class="mb-4"
            :disabled="!valid"
            @click="login"
          >
            Login
          </v-btn>

          <div class="text-center mb-2">or</div>
          <v-btn block color="#1d1d6c" class="mb-0" @click="goRegister">
            Create an account
          </v-btn>
        </v-form>
      </v-card>
    </v-col>
  </v-row>
</v-container>
</template>

<script>
import mriImage from "../assets/mri-illustration.jpg";
import "../assets/login.css"; 

export default {
  data() {
    return {
      mriImage,
      email: "",
      password: "",
      remember: false,
      valid: false,
      rules: {
        required: (v) => !!v || "This field is required",
        email: (v) => /.+@.+\..+/.test(v) || "E-mail must be valid",
      },
    };
  },
  methods: {
    async login() {
      if (this.$refs.loginForm.validate()) {
        try {
          const response = await fetch("http://localhost:5002/login", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              email: this.email,
              password: this.password,
            }),
          });

          const data = await response.json();

          if (response.ok) {
            this.$router.push({ path: "/dashboard" });
          } else {
            alert(data.error);
          }
        } catch (error) {
          alert("Server error. Try again later.");
        }
      }
    },

    forgotPassword() {
      console.log("Redirect to forgot password page");
    },

    goRegister() {
      this.$router.push({ name: "Register" });
    },
  },
};
</script>


