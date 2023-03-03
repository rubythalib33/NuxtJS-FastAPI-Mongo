<template>
    <v-app class = "background-custom">
        <v-navigation-drawer
        v-model="drawer"
        :mini-variant="miniVariant"
        :clipped="clipped"
        fixed
        app
        dark
        >
        <v-img
                src="/POS_ADMIN_dark.png"
                height="100"
                contain
        ></v-img>
        <hr style="width: 50%; margin: auto">
        <v-list >
            <v-list-item
            v-for="(item, i) in items"
            :key="i"
            :to="item.to"
            router
            exact
            >
            <v-list-item-action>
                <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-action>
            <v-list-item-content>
                <v-list-item-title v-text="item.title" />
            </v-list-item-content>
            </v-list-item>
        </v-list>
        </v-navigation-drawer>
        <v-app-bar :clipped-left="clipped" fixed app>
      <v-app-bar-nav-icon @click.stop="miniVariant = !miniVariant" />
      <v-toolbar-title v-text="title" />
      <v-spacer />
      <v-menu offset-y>
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          icon
          v-bind="attrs"
          v-on="on"
        >
              <v-icon>mdi-cog-outline</v-icon>
        </v-btn>
      </template>
      <v-list>
        <v-btn
        class="ma-2"
        outlined
        color="indigo"
        @click="keluar()"
        >
            Logout
        </v-btn>
      </v-list>
    </v-menu>
    </v-app-bar>
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
    name: 'NavSideBarComponent',
    data () {
        return {
            username: 'Johny',
            avatar: 'https://images.pexels.com/photos/4556737/pexels-photo-4556737.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
            clipped: false,
            drawer: true,
            fixed: false,
            items: [
                {
                    icon: 'mdi-chart-donut',
                    title: 'Overview',
                    to: '/'
                },
                {
                    icon: 'mdi-account-settings',
                    title: 'Users',
                    to: '/users'
                },
                {
                    icon: 'mdi-city',
                    title: 'Branches Management',
                    to: '/branches'
                },
                {
                    icon: 'mdi-chart-bubble',
                    title: 'Products',
                    to: '/products'
                },
                {
                    icon: 'mdi-widgets',
                    title: 'Kategori Produk',
                    to: '/category'
                },
                {
                    icon: 'mdi-file-chart',
                    title: 'Pembelian',
                    to: '/pembelian'
                },
                {
                    icon: 'mdi-chart-line',
                    title: 'Penjualan',
                    to: '/penjualan'
                },
                {
                    icon: 'mdi-cash-100',
                    title: 'Pengeluaran Lain',
                    to: '/pengeluaran_lain'
                },
                {
                    icon: 'mdi-account-check',
                    title: 'Member',
                    to: '/member'
                },
                {
                    icon: 'mdi-percent',
                    title: 'Diskon Member',
                    to: '/diskon'
                },
            ],
            miniVariant: false,
            right: true,
        }
    },
    computed: {
        title () {
            return this.$route.meta.title || ''
        }
    },
    methods: {
        keluar () {
            this.$auth.logout()
            this.$router.push('/login')
        }
    }
}
</script>

<style scoped>
.background-custom{
    background-color: #F7F8FC;
}
.v-navigation-drawer {
    background-color: #363740;
}
img{
  width: 40px;
  height: 40px;
  border-radius: 100%;
}
</style>