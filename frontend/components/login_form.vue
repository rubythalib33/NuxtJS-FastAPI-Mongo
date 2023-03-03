<template>
    <v-app>
        <v-container>
            <!-- Create Login Form that can see the password -->
            <v-form v-model="valid" ref="form" lazy-validation>
                <v-img
                    src="/POS_ADMIN.png"
                    height="400"
                    contain
                ></v-img>
                <v-text-field
                    v-model="form.email"
                    :rules="emailRules"
                    label="Email"
                    type="email"
                    prepend-icon="mdi-email"
                    @keyup.enter="login"
                ></v-text-field>
                <v-text-field
                    v-model="form.password"
                    :rules="passwordRules"
                    label="Password"
                    type="password"
                    prepend-icon="mdi-lock"
                    @keyup.enter="login"
                ></v-text-field>
                <v-checkbox
                    v-model="form.remember"
                    label="Remember me"
                ></v-checkbox>
                <v-btn
                    light
                    color="primary"
                    @click="userLogin"
                    :disabled="!valid"
                >
                    Login
                </v-btn>
            </v-form>
        </v-container>
    </v-app>
</template>

<script>
export default{
    name: 'LoginComponent',
    data(){
        return{
            form: {
                email: '',
                password: ''
            },
            emailRules: [
                v => !!v || 'Email is required',
                v => /.+@.+/.test(v) || 'Email must be valid'
            ],
            passwordRules: [
                v => !!v || 'Password is required',
                v => v.length >= 6 || 'Password must be at least 6 characters'
            ]
        }
    },
    methods: {
    async userLogin() {
      try {
        const form = new FormData();
        form.append('email', this.form.email);
        form.append('password', this.form.password);

        let response = await this.$auth.loginWith('local', { data: form })
        .then((response) => {
            this.$auth.strategy.token.set('Bearer '+response.data.access);
            this.$router.push('/');
        })
      } catch (err) {
        console.log(err)
      }
    }
  }
}
</script>

<style scoped>
.v-container{
    background-color: white;
}
.v-form{
    width: 500px;
    margin: auto;
}
</style>