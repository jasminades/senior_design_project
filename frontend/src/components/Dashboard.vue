<template>
  <v-container fluid class="fill-height pa-0">
    <v-row class="fill-height d-flex justify-center align-center">
      <v-col cols="12" md="6">
        <v-card class="pa-6 elevation-12 mx-auto" width="80%">
          <v-card-title class="text-h5 font-weight-bold mb-4 text-center">
            Upload MRI for Analysis
          </v-card-title>

          <div
            class="dropzone"
            @dragover.prevent
            @dragenter.prevent
            @drop.prevent="handleDrop"
          >
            <div class="d-flex justify-center mb-2" v-if="filePreview">
              <v-img
                :src="filePreview"
                max-width="250"
                max-height="250"
                contain
              />
            </div>

            <v-icon v-else size="48">mdi-upload</v-icon>

            <p class="mt-2" v-if="!filePreview">Drag & Drop your MRI file here</p>
            <p v-else>File Selected: {{ fileName }}</p>
            <v-btn color="#1d1d6c" @click="browseFile" class="mt-2">Browse Files</v-btn>
            <input ref="fileInput" type="file" hidden accept="image/*" @change="handleFile" />
          </div>

          <v-btn
            v-if="filePreview"
            color="#1d1d6c"
            block
            class="mt-4"
            @click="analyzeFile"
            :loading="loading"
          >
            Analyze
          </v-btn>

          <div v-if="result" class="mt-6 text-center">
            <v-card class="pa-4 elevation-6">
              <h3>Analysis Result</h3>
              <p>Prediction: {{ result.prediction }}</p>
              <p>Confidence: {{ result.confidence }}</p>
            </v-card>
          </div>

          <div v-if="error" class="mt-6 text-center">
            <v-alert type="error">{{ error }}</v-alert>
          </div>

        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";
import "../assets/dashboard.css";

export default {
  data() {
    return {
      fileName: null,
      filePreview: null,
      file: null,
      result: null,
      error: null,
      loading: false,
    };
  },
  methods: {
    handleDrop(e) {
      const file = e.dataTransfer.files[0];
      if (file) this.previewFile(file);
    },
    browseFile() {
      this.$refs.fileInput.click();
    },
    handleFile(e) {
      const file = e.target.files[0];
      if (file) this.previewFile(file);
    },
    previewFile(file) {
      this.fileName = file.name;
      this.file = file;
      const reader = new FileReader();
      reader.onload = (e) => {
        this.filePreview = e.target.result;
      };
      reader.readAsDataURL(file);
      this.result = null;
      this.error = null;
    },
    async analyzeFile() {
      if (!this.file) return;
      this.loading = true;
      this.result = null;
      this.error = null;

      const formData = new FormData();
      formData.append("file", this.file);

      try {
        const response = await axios.post("http://localhost:5001/predict", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        this.result = response.data;
      } catch (err) {
        console.error(err);
        this.error = err.response?.data?.error || "An error occurred during analysis.";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

