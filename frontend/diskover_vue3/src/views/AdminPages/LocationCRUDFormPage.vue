<template>
  <v-container class="grey lighten-4 fill-height d-flex align-center justify-center">
    <v-row justify="center">
      <v-col cols="12" md="10" lg="8"> <!-- Adjusted width -->
        <!-- Form Container with White Background -->
        <div class="form-container">
          <v-row>
            <v-col cols="12">
              <label>Name</label>
              <v-text-field
                placeholder="Name"
                color="black"
                v-model="name"
                :readonly="isReadOnly"
                :error="isReadOnly"
              />
            </v-col>
            <v-col cols="12">
              <label>Category</label>
              <v-select
                :items="categoryItems"
                placeholder="Category"
                color="black"
                :menu-props="{zIndex:'1001'}"
                v-model="categoryId"
                :readonly="isReadOnly"
                :error="isReadOnly"
              />
            </v-col>
            <v-col cols="12">
              <div class="maroon-chips">
                <label>Tags</label>
                <v-select
                  :items="tagItems"
                  placeholder="Tags"
                  color="black"
                  chips
                  deletable-chips
                  :menu-props="{zIndex:'1001'}"
                  multiple
                  v-model="tagIds"
                  :readonly="isReadOnly"
                  :error="isReadOnly"
                />
              </div>
            </v-col>
            <v-col cols="12">
              <label>Description</label>
              <v-textarea
                v-model="description"
                color="black"
                auto-grow
                placeholder="Description"
                :readonly="isReadOnly"
                :error="isReadOnly"
              />
            </v-col>
            <v-col cols="12">
              <FormMapView
                height="300px"
                @click="handleMapClick"
                :defaultFormCoords="defaultCoords"
                :readonly="isReadOnly"
              />
              <v-btn @click="resetMapView" class="mt-2">Reset Map</v-btn>
            </v-col>
            <v-col cols="12">
              <label>LatLng (Click on the map to set):</label>
              <v-text-field
                label="Coordinates"
                v-model="coordsDisplay"
              />
            </v-col>
            <v-col cols="12">
              <div class="maroon-chips">
                <v-autocomplete
                  v-model="subareaIds"
                  :items="subareaItems"
                  :search-input.sync="subareaSearch"
                  @input="subareaSearch=null"
                  multiple
                  cache-items
                  hide-selected
                  auto-select-first
                  chips
                  clearable
                  deletable-chips
                  label="Subareas"
                  placeholder="Search a subarea"
                  color="blue"
                  :menu-props="{zIndex:'1001'}"
                  :readonly="isReadOnly"
                  :error="isReadOnly"
                />
              </div>
            </v-col>
            <v-col cols="12">
              <div class="maroon-chips">
                <v-autocomplete
                  v-model="mainBuildingId"
                  :items="mainBuildingItems"
                  :search-input.sync="mainBuildingSearch"
                  @input="mainBuildingSearch=null"
                  cache-items
                  hide-selected
                  auto-select-first
                  clearable
                  label="Main Building"
                  placeholder="Search a main building"
                  color="blue"
                  :menu-props="{zIndex:'1001'}"
                  :readonly="isReadOnly"
                  :error="isReadOnly"
                />
              </div>
            </v-col>
            <v-col cols="12">
              <v-row justify="end" class="mt-4">
                <v-btn v-if="mode=='create'" color="success" class="mr-2" @click="handleCreateClick()" :disabled="isSubmitting">Create Location</v-btn>
                <v-btn v-else-if="mode=='update'" color="success" class="mr-2" @click="handleUpdateClick()" :disabled="isSubmitting">Update Location</v-btn>
                <v-btn v-else color="error" class="mr-2" @click="handleDeleteClick()" :disabled="isSubmitting">Delete Location</v-btn>
                <v-btn @click="handleCancelClick()">Cancel</v-btn>
              </v-row>
            </v-col>
          </v-row>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import AdminVerifierMixin from "@/mixins/AdminVerifierMixin";
import { useMainStore } from "@/stores/index.js";
import FormMapView from "@/components/map/FormMapView.vue"; // Import the FormMapView component

export default {
  mixins: [AdminVerifierMixin],
  components: {
    FormMapView, // Register the FormMapView component
  },
  mounted() {
    this.handleRouteChange();
    this.coords = this.defaultCoords;
  },
  data() {
    return {
      name: "",
      categoryId: "",
      tagIds: [],
      description: "",
      coords: [],
      defaultCoords: this.$defaultStartCoords,
      subareaIds: [],
      subareaSearch: "",
      subareaItems: [],
      mainBuildingId: 0,
      mainBuildingSearch: "",
      mainBuildingItems: [],
      isSubmitting: false,
    };
  },
  computed: {
    categoryItems() {
      const mainStore = useMainStore();
      return mainStore.categories.map((cat) => ({
        text: cat.name,
        value: cat.id,
      }));
    },
    tagItems() {
      const mainStore = useMainStore();
      return mainStore.tags.map((tag) => ({
        text: tag.name,
        value: tag.id,
      }));
    },
    isReadOnly() {
      return this.mode == "delete" ? true : false;
    },
    id() {
      return this.$route.params.id;
    },
    mode() {
      return this.$route.params.mode;
    },
    coordsDisplay: {
      get() {
        return Array.isArray(this.coords) ? this.coords.join(', ') : '';
      },
      set(value) {
        const [lat, lng] = value.split(',').map((coord) => parseFloat(coord.trim()));
        if (!isNaN(lat) && !isNaN(lng)) {
          this.coords = [lat, lng];
        }
      },
    },
  },
  watch: {
    $route(newRoute, oldRoute) {
      this.handleRouteChange();
    },
    subareaSearch(newSearch) {
      this.apiGetSubareaItems(newSearch);
    },
    mainBuildingSearch(newSearch) {
      this.apiGetMainBuildingItems(newSearch);
    },
  },
  methods: {
    resetMapView() {
      this.$eventBus.emit("reset-map-view", 15);
    },
    handleMapClick(newCoords) {
      console.log("Received coordinates:", newCoords); // Debugging
      if (Array.isArray(newCoords)) {
        this.coords = newCoords;
      } else {
        console.error("Invalid coordinates received:", newCoords); // Debugging
      }
    },
    handleRouteChange() {
      this.apiGetSubareaItems("");
      this.apiGetMainBuildingItems("");
      if (this.mode == "update" || this.mode == "delete") {
        this.getUpdateData(this.id);
      }
    },
    getUpdateData(id) {
      this.$http
        .get(`/admin/locations/${id}`)
        .then((response) => {
          console.log(
            "successful retrieved location update/delete data from API: ",
            response.data
          );
          let {
            name,
            category,
            tags,
            description,
            lat,
            lng,
            subareas,
            main_building,
          } = response.data;
          this.name = name;
          this.categoryId = category;
          this.tagIds = tags;
          this.description = description;
          this.defaultCoords = [lat, lng];
          this.coords = [lat, lng];
          this.subareaIds = subareas;
          this.mainBuildingId = main_building;
          console.log(main_building);
        })
        .catch((error) => {
          console.log(
            "error retrieving location update/delete data from API: ",
            error
          );
        });
    },
    apiGetSubareaItems(searchValue) {
      this.$http
        .get(`/admin/locations`, {
          params: {
            search: searchValue
          },
          paramsSerializer: params => {
            return this.$qs.stringify(params, { indices: false });
          }
        })
        .then(response => {
          this.subareaItems = response.data.map(sub => {
            return {
              text: sub.name,
              value: sub.id
            };
          });
        })
        // alert an error if unsuccessful GET
        .catch(error => {
          alert("error receiving queried results from API: ");
          console.log(error);
        })
        .finally(() => (this.isLoading = false));
    },
    apiGetMainBuildingItems(searchValue) {
      this.$http
        .get(`/admin/locations`, {
          params: {
            search: searchValue
          },
          paramsSerializer: params => {
            return this.$qs.stringify(params, { indices: false });
          }
        })
        .then(response => {
          this.mainBuildingItems = response.data.map(building => {
            return {
              text: building.name,
              value: building.id
            };
          });
        })
        // alert an error if unsuccessful GET
        .catch(error => {
          alert("error receiving queried results from API: ");
          console.log(error);
        })
        .finally(() => (this.isLoading = false));
    },

    handleCancelClick() {
      this.$router.go(-1);
    },
    handleDeleteClick() {
      this.isSubmitting = true
      this.$http
        .delete(`/admin/locations/${this.id}/`)
        .then(response => {
          console.log("successfully deleted location from API", response);
          this.$router.push(`/map/search`);
        })
        .catch(function(error) {
          alert("error deleting location to API", error);
        })
        .finally(() => {
          this.isSubmitting = false
        });;
    },
    handleCreateClick() {
      this.isSubmitting = true
      this.$http
        .post(`/admin/locations/`, {
          name: this.name,
          category: this.categoryId,
          tags: this.tagIds,
          description: this.description,
          lat: this.coords[0],
          lng: this.coords[1],
          subareas: this.subareaIds,
          main_building: this.mainBuildingId
        })
        .then(response => {
          console.log("successfully posted new location to API", response);
          this.$router.push(`/map/details/${response.data.id}`);
        })
        .catch(function(error) {
          alert("error posting new location to API", error);
        })
        .finally(() => {
          this.isSubmitting = false
        });
    },
    handleUpdateClick() {
      this.$http
        .patch(`/admin/locations/${this.id}/`, {
          name: this.name,
          category: this.categoryId,
          tags: this.tagIds,
          description: this.description,
          lat: this.coords[0],
          lng: this.coords[1],
          subareas: this.subareaIds,
          main_building: this.mainBuildingId
        })
        .then(response => {
          console.log("successfully patched updated location to API", response);
          this.$router.push(`/map/details/${this.id}`);
        })
        .catch(function(error) {
          alert("error patching updated location to API", error);
        })
        .finally(() => {
          this.isSubmitting = false
        });;
    }
  }
};
</script>

<style scoped>
.form-container {
  background-color: white; /* White background for the form */
  padding: 20px; /* Add padding inside the form */
  border-radius: 8px; /* Rounded corners */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Optional shadow for better visibility */
  width: 100%; /* Ensure it takes the full width of the column */
}

label {
  font-weight: bold !important;
  font-size: 16px !important;
}

.maroon-chips .v-chip {
  background-color: var(--v-primary-base) !important;
  color: white;
}
</style>