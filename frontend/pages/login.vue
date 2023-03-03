<template>
    <v-app>
        <v-main>
            <v-container fluid>
                <LoginComponent />
            </v-container>
        </v-main>

    </v-app>
</template>

<script>
import LoginComponent from '../components/login_form.vue'

export default {
  name: 'login-page',
  components:{
        LoginComponent
    }
}
</script>

<style scoped>

</style>