<template>
  <v-container fluid class="fill-height pa-0">
    <v-row class="fill-height">
      <v-col
        cols="12"
        md="6"
        class="left-side d-flex flex-column justify-center align-center text-center"
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
      >
        <v-card class="pa-6 elevation-12" width="70%">
          <v-card-title class="text-h5 font-weight-bold mb-2">Create an Account</v-card-title>
          <v-card-subtitle class="mb-6">Sign up to get started</v-card-subtitle>

          <v-form ref="registerForm" v-model="valid">
            <v-text-field
              v-model="full_name"
              placeholder="Full Name"
              outlined
              dense
              hide-details="auto"
              prepend-inner-icon="mdi-account"
              class="mb-4"
            />

            <v-text-field
              v-model="email"
              placeholder="Email"
              :rules="[rules.required, rules.email]"
              outlined
              dense
              hide-details="auto"
              prepend-inner-icon="mdi-email"
              class="mb-4"
            />

            <v-text-field
              v-model="password"
              placeholder="Password"
              type="password"
              :rules="[rules.required, rules.min]"
              outlined
              dense
              hide-details="auto"
              prepend-inner-icon="mdi-lock"
              class="mb-4"
            />

            <v-text-field
              v-model="confirmPassword"
              placeholder="Confirm Password"
              type="password"
              :rules="[rules.required, rules.matchPassword]"
              outlined
              dense
              hide-details="auto"
              prepend-inner-icon="mdi-lock-check"
              class="mb-6"
            />

            <v-btn
              color="#1d1d6c"
              block
              class="mb-4"
              :disabled="!valid"
              @click="register"
            >
              Register
            </v-btn>

            <div class="text-center mb-2">or</div>

            <v-btn block color="#1d1d6c" class="mb-0" @click="goLogin">
              Sign In
            </v-btn>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import mriImage from "../assets/mri-illustration.jpg"; 
import "../assets/register.css"; 

export default {
  data() {
    return {
      mriImage,
      full_name: "",
      email: "",
      password: "",
      confirmPassword: "",
      valid: false,
      rules: {
        required: (v) => !!v || "This field is required",
        email: (v) => /.+@.+\..+/.test(v) || "E-mail must be valid",
        min: (v) => v.length >= 6 || "Password must be at least 6 characters",
        matchPassword: (v) => v === this.password || "Passwords must match",
      },
    };
  },
  methods: {
    async register() {
      if (this.$refs.registerForm.validate()) {
        try {
          const response = await fetch("http://localhost:5002/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              full_name: this.full_name,
              email: this.email,
              password: this.password,
            }),
          });

          const data = await response.json();
          if (response.ok) {
            alert("Account created! Please log in.");
            this.$router.push({ name: "Login" });
          } else {
            alert(data.error);
          }
        } catch (err) {
          alert("Server error. Try again later.");
        }
      }
    },
    goLogin() {
      this.$router.push({ name: "Login" });
    },
  },
};
</script>
