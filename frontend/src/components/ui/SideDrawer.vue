<template>
  <!-- Side Drawer for showing results and details alongside map anchored left -->
  <div
    class="side-drawer-container"
    v-show="isSideDrawerVisible" 
  >
    <FloatingButton
      v-if="isVisible"
      attachedTo="drawer"
      @click="handleToggleSideDrawer"
      class="floating-button"
    />
    <div class="search-drawer" v-show="isVisible">
      <div class="px-2 pt-3 scrollable-content">
        <div class="search-bar-container">
          <SearchBar/>
        </div>
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted, onBeforeUnmount, inject } from 'vue';
import { useDisplay } from 'vuetify';
import { useMapStore } from '@/stores/map';
import FloatingButton from '@/components/ui/FloatingButton.vue';
import SearchBar from '@/components/search/SearchBar.vue';

export default {
  components: {
    FloatingButton,
    SearchBar
  },
  setup() {
    const { mdAndUp } = useDisplay();
    const mapStore = useMapStore();
    const eventBus = inject('eventBus');

    const isVisible = computed({
      get() {
        return mapStore.isSideDrawerVisible;
      },
      set(value) {
        mapStore.setSideDrawer(value);
      }
    });

    const isSideDrawerVisible = computed(() => mapStore.isSideDrawerVisible);

    const toggleVisibility = () => {
      mapStore.setSideDrawer(!isVisible.value);
    };

    const handleToggleSideDrawer = () => {
      toggleVisibility();
      eventBus.emit('toggle-side-drawer');
    };

    const handleEventBusToggle = () => {
      mapStore.setSideDrawer(!mapStore.isSideDrawerVisible);
    };

    onMounted(() => {
      eventBus.on("toggle-side-drawer", handleEventBusToggle);
    });

    onBeforeUnmount(() => {
      eventBus.off("toggle-side-drawer", handleEventBusToggle);
    });

    return {
      mdAndUp,
      isVisible,
      handleToggleSideDrawer,
      isSideDrawerVisible
    };
  }
};
</script>

<style scoped>
.side-drawer-container {
  position: relative;
  height: 100%;
  width: 100%;
  padding: 0;
}

.search-drawer {
  height: 100%;
  width: 100%;
  background-color: #ed9a9c;
  overflow-x: visible !important;
  padding: 0;
}

.scrollable-content {
  max-height: calc(100vh - 50px); /* Adjust the height as needed */
  overflow-y: auto; /* Enable vertical scrolling */
}

.search-bar-container {
  background-color: white; /* Set the background color of the search bar container to white */
  padding: 0px;
  margin: 0px;
}

.floating-button {
  position: absolute;
  right: 0%; /* Adjust this value to position the button slightly outside the drawer */
  top: 50%; /* Center the button vertically */
}
</style>
