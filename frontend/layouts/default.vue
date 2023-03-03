<template>
  <v-app class="background-custom-dark">
    
    <v-main>
      <v-container>
        <Nuxt />
      </v-container>
    </v-main>
    <v-footer
      :absolute="!fixed"
      app
      style="background-color: #363740; color: white;"
    >
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: 'DefaultLayout',
  data () {
    return {
      fixed: false
    }
  }
}
</script>

<style scoped>
img{
  width: 40px;
  height: 40px;
  border-radius: 100%;
}
</style>