<template>
  <div class="centered-container">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  created() {
    if (this.$route.name == 'admin_blank') {  
      this.$router.replace({name: '404'})
    }
  }
};
</script>

<style scoped>
.centered-container {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
