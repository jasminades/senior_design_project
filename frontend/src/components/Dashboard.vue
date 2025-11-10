<template>
  <v-app>
    <v-app-bar flat color="#f5f6fa">
      <v-toolbar-title class="font-weight-bold text-h5" style="color:#1d1d6c">
        NeuroScan Dashboard
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text color="#1d1d6c" @click="logout">Logout</v-btn>
    </v-app-bar>

    <v-container fluid class="dashboard-bg fill-height pa-0">
      <v-row class="fill-height d-flex justify-center align-center">
        <v-col cols="12" md="6">
          <v-card class="pa-6 elevation-12 mx-auto upload-card">
            <v-card-title class="text-h5 font-weight-bold mb-4 text-center">
              Upload MRI for Analysis
            </v-card-title>

           <div
            class="dropzone py-6 px-4"
            @dragover.prevent
            @dragenter.prevent
            @drop.prevent="handleDrop"
            style="border: 2px dashed #1d1d6c; border-radius: 16px; background-color: #f5f7ff; min-height: 220px;"
          >
            <div class="d-flex justify-center mb-2" v-if="filePreview">
              <v-img
                :src="filePreview"
                max-width="200"
                max-height="200"
                contain
                class="rounded-lg"
              />
            </div>

            <v-icon v-else size="40" color="#1d1d6c">mdi-upload</v-icon>

            <p class="mt-1 text-body-2" v-if="!filePreview">
              Drag & Drop your MRI file here
            </p>
            <p class="text-body-2" v-else>
              File Selected: <strong>{{ fileName }}</strong>
            </p>

            <v-btn
              color="#1d1d6c"
              @click="browseFile"
              class="mt-2 text-body-2"
              size="small"
            >
              Browse Files
            </v-btn>

            <input ref="fileInput" type="file" hidden accept="image/*" @change="handleFile" />
          </div>

          <div v-if="loading" class="text-center mt-3">
            <v-progress-circular
              :size="50"
              :width="5"
              indeterminate
              color="#1d1d6c"
            ></v-progress-circular>
            <p class="mt-1 text-body-2">Analyzing MRI image...</p>
          </div>

          <v-btn
            v-if="filePreview && !loading"
            color="#1d1d6c"
            block
            class="mt-3"
            size="small"
            @click="analyzeFile"
          >
            Analyze
          </v-btn>

          <v-fade-transition>
          <div v-if="result" class="mt-5 text-center">
            <v-card
              class="pa-4 elevation-4 result-card mx-auto"
              color="#f9f9ff"
              width="85%"
            >
              <v-icon size="36" color="#1d1d6c" class="mb-2">mdi-brain</v-icon>
              <h3 class="text-subtitle-1 font-weight-bold mb-1">Analysis Result</h3>

              <p class="text-body-2 mb-0">
                <strong>Prediction:</strong> {{ result.prediction }}
              </p>

              <p class="text-body-2">
                <strong>Confidence:</strong> {{ result.confidence }}
              </p>
            </v-card>
          </div>
        </v-fade-transition>


          <div v-if="error" class="mt-4 text-center">
            <v-alert type="error" class="text-body-2 pa-2">{{ error }}</v-alert>
          </div>
          </v-card>
        </v-col>

        <v-col cols="12" md="4">
          <v-card class="mt-4 pa-4 rounded-xl" color="blue-grey-lighten-5">
            <v-card-title class="text-h6 font-weight-bold mb-2">Quick Tips</v-card-title>
            <v-card-text>
              <ul class="text-body-2">
                <li>Ensure your MRI image is clear, well-lit, and properly cropped before uploading (PNG or JPG format supported).</li>
                <li>BrainScan AI uses deep learning to analyze brain regions and detect early indicators of Alzheimer’s disease.</li>
                <li>For best results, upload images with a resolution above 512×512 pixels and a size under 10MB.</li>
                <li>Depending on image size and server load, analysis usually completes in 3–8 seconds.</li>
                <li>Your uploaded image is processed securely and never stored after prediction.</li>
              </ul>
            </v-card-text>

            
          </v-card>

          <v-card class="mt-4 pa-4 rounded-xl" color="blue-grey-lighten-5">
            <v-card-title class="text-h6 font-weight-bold mb-2">Important Notice</v-card-title>
            <v-card-text>
              <ul class="text-body-2">
                  NeuroScan is an experimental tool and should <u>not</u> be used for medical diagnosis.
                  Always consult a qualified healthcare professional for accurate evaluation and interpretation of MRI results.
              </ul>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
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
        await new Promise(resolve => setTimeout(resolve, 2000));
        this.result = response.data;
      } catch (err) {
        console.error(err);
        this.error = err.response?.data?.error || "An error occurred during analysis.";
      } finally {
        this.loading = false;
      }
    },
    logout() {
      this.$router.push({ name: "Login" });
    },
  },
};
</script>

