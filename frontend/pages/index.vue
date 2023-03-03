<template>
    <v-app class="background-custom">
    <!-- lets create title for this page -->
    <!-- Create 4 rounded square with text, inside text is this.data.n_branches, this.data.m_tasks, this.data.monthly_revenue, this.data.monthly_spend -->
    <v-row>
        <v-col cols="12" sm="6" md="3">
            <v-card class="elevation-1">
                <v-card-text>
                    <div class="d-flex justify-center">
                        <v-card-title>
                            <span class="text-h5">Branches</span>
                        </v-card-title>
                    </div>
                    <div class="d-flex justify-center">
                        <div class="font-weight-bold text-uppercase text-h4">{{ data.n_branches }}</div>
                    </div>
                </v-card-text>
            </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="3">
            <v-card class="elevation-1">
                <v-card-text>
                    <div class="d-flex justify-center">
                        <v-card-title>
                            <span class="text-h5">Monthly Sale</span>
                        </v-card-title>
                    </div>
                    <div class="d-flex justify-center">
                        <div class="font-weight-bold text-uppercase text-h4 ">{{ data.monthly_sale | formatNumber }}</div>
                    </div>
                </v-card-text>
            </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="3">
            <v-card class="elevation-1">
                <v-card-text>
                    <div class="d-flex justify-center">
                        <v-card-title>
                            <span class="text-h5">Monthly Revenue</span>
                        </v-card-title>
                    </div>
                    <div class="d-flex justify-center">
                        <div class="font-weight-bold text-uppercase text-h4">Rp. {{ data.monthly_revenue | formatNumber}}</div>
                    </div>
                </v-card-text>
            </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="3">
            <v-card class="elevation-1">
                <v-card-text>
                    <div class="d-flex justify-center">
                        <v-card-title>
                            <span class="text-h5">Monthly Spend</span>
                        </v-card-title>
                    </div>
                    <div class="d-flex justify-center">
                        <div class="font-weight-bold text-uppercase text-h4">Rp {{ data.monthly_spend | formatNumber }}</div>
                    </div>
                </v-card-text>
            </v-card>
        </v-col>
    </v-row>
    
    </v-app>
</template>

<script>
import Vue from 'vue';
var numeral = require("numeral");

Vue.filter("formatNumber", function (value) {
return numeral(value).format("0,0"); // displaying other groupings/separators is possible, look at the docs
});

export default {
    layout: 'menu',
    data () {
        return {
            data: {
                n_branches: 5,
                monthly_sale: 30,
                monthly_revenue: 30000000,
                monthly_spend: 20000000,
            }
        }
    },
    mounted(){
      this.getData()
    },

    methods: {
      async getData(){
        await this.$axios
        .get('v1/overview/')
        .then((res) => {
          this.data.n_branches = res.data.count_branch
          this.data.monthly_sale = res.data.count_penjualan
          this.data.monthly_revenue = res.data.count_pemasukan
            this.data.monthly_spend = res.data.count_pengeluaran

        })
        .catch((err) => {
          console.log(err)
        })
      }
    }
}
</script>

<style scoped>
.rounded-card{
    border-radius:50px;
}
.background-custom{
    background-color: #F7F8FC;
}
</style>
