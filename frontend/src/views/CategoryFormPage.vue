<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-card class="pa-5 form-bg" max-width="600">
      <v-card-title class="primary text-h5 font-weight-light">
        {{ mode === 'create' ? 'Create Category' : 'Edit Category' }}
      </v-card-title>
      
      <v-card-text>
        <v-row>
          <v-col cols="12">
            <v-text-field
              v-model="name"
              label="Category Name"
              placeholder="Enter category name"
              :readonly="isReadOnly"
              :error="isReadOnly"
            />
          </v-col>
          <v-col cols="12">
            <v-text-field
              v-model="url"
              label="URL"
              placeholder="Enter category URL"
              :readonly="isReadOnly"
              :error="isReadOnly"
            />
          </v-col>
          <v-col cols="12">
            <label class="font-weight-bold">Route Color</label>
            <v-text-field
              v-model="color"
              type="color"
              hide-details
              @change="onColorSelected"
            />
          </v-col>
        </v-row>
      </v-card-text>

      <v-card-actions class="justify-center">
        <v-btn color="primary" dark @click="onSubmitClick" :disabled="isSubmitting">
          Submit
        </v-btn>
        <v-btn v-if="mode !== 'create'" color="red" dark @click="onDeleteClick" :disabled="isSubmitting">
          Delete
        </v-btn>
        <v-btn color="grey" dark @click="onCancelClick">
          Cancel
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios'; // Import the Axios instance

const route = useRoute();
const router = useRouter();

const name = ref('');
const url = ref('');
const color = ref('#000000');
const isSubmitting = ref(false);

const id = computed(() => route.params.id);
const mode = computed(() => route.params.mode);
const isReadOnly = computed(() => mode.value === 'delete');

onMounted(() => {
  if (mode.value === 'update' || mode.value === 'delete') {
    getUpdateData(id.value);
  }
});

const getUpdateData = async (id) => {
  try {
    const response = await axios.get(`/admin/categories/${id}/`);
    const data = response.data;
    name.value = data.name;
    url.value = data.url;
    color.value = data.route_color; // Use the correct field name from the backend
  } catch (error) {
    console.error(`Failed to get category ${id}:`, error);
  }
};

const onSubmitClick = async () => {
  isSubmitting.value = true;
  const endpoint = mode.value === 'create' ? '/admin/categories/' : `/admin/categories/${id.value}/`;
  const method = mode.value === 'create' ? 'post' : 'patch';

  try {
    await axios({
      method,
      url: endpoint,
      data: { name: name.value, url: url.value, route_color: color.value },
    });
    router.push('/admin/browse/categories'); // Redirect after success
  } catch (error) {
    console.error('Failed to submit category:', error);
  } finally {
    isSubmitting.value = false;
  }
};

const onDeleteClick = async () => {
  isSubmitting.value = true;
  try {
    await axios.delete(`/admin/categories/${id.value}/`);
    router.push('/admin/browse/categories'); // Redirect after deletion
  } catch (error) {
    console.error('Failed to delete category:', error);
  } finally {
    isSubmitting.value = false;
  }
};

const onCancelClick = () => router.push('/admin/browse/categories');

const onColorSelected = (event) => {
  color.value = event.target.value;
};
</script>

<style scoped>
@import "@/assets/stylesheets/style.css";

.form-bg {
  background-color: white !important;
}

.fill-height {
  height: calc(100vh - 64px);
}

.v-btn {
  display: flex !important;
  visibility: visible !important;
}

.v-btn[color="primary"] {
  background-color: #1976d2 !important; /* Vuetify's primary color */
}

.v-btn[color="red"] {
  background-color: #d32f2f !important;
}

.v-btn[color="grey"] {
  background-color: #757575 !important;
}

.v-btn:hover {
  filter: brightness(1.2);
}
</style>
