<template>
    <v-app class = "background-custom">
      <v-card-title>
              <v-spacer></v-spacer>
              <v-text-field
                v-model="search"
                append-icon="mdi-magnify"
                label="Search"
                single-line
                hide-details
              ></v-text-field>
        </v-card-title>
        <v-data-table
            :headers="headers"
            :items="pengeluaran_lainnya"
            :search="search"
            :custom-filter="filterByIDColumn"
            sort-by="name"
            class="elevation-1"
        >
            <template v-slot:[`item.total_pengeluaran`]="{item}">
                Rp {{ item.total_pengeluaran | formatNumber }}
            </template>
            <template v-slot:top>
            <v-toolbar
                flat
            >
                <v-toolbar-title>Pengeluaran Lain</v-toolbar-title>
                <v-divider
                class="mx-4"
                inset
                vertical
                ></v-divider>
                <v-spacer></v-spacer>
                <v-dialog
                v-model="dialog"
                max-width="500px"
                >
                <template v-slot:activator="{ on, attrs }">
                    <v-btn
                    color="primary"
                    dark
                    class="mb-2"
                    v-bind="attrs"
                    v-on="on"
                    >
                    Add Pengeluaran
                    </v-btn>
                </template>
                <v-card>
                  <v-form
                    ref="form"
                    v-model="valid"
                    lazy-validation
                  >
                    <v-card-title>
                    <span class="text-h5">{{ formTitle }}</span>
                    </v-card-title>

                    <v-card-text>
                    <v-container>
                        <v-row>
                        <v-col
                            cols="12"
                            sm="6"
                            md="4"
                        >
                            <v-text-field
                            v-model="editedItem.keterangan"
                            label="Keterangan"
                            :rules="rules_required"
                            required
                            ></v-text-field>
                        </v-col>
                        <!-- dropdown category -->
                        <v-col
                            cols="12"
                            sm="6"
                            md="4"
                        >
                        </v-col>
                        <v-col
                            cols="12"
                            sm="6"
                            md="4"
                        >
                            <v-text-field
                            v-model="editedItem.total_pengeluaran"
                            label="Total Pengeluaran"
                            :rules="rules_only_number_required"
                            required
                            ></v-text-field>
                        </v-col>
                        </v-row>
                    </v-container>
                    </v-card-text>

                    <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                        color="blue darken-1"
                        text
                        @click="close"
                    >
                        Cancel
                    </v-btn>
                    <v-btn
                        :disabled="!valid"
                        color="blue darken-1"
                        text
                        @click="save"
                    >
                        Save
                    </v-btn>
                    </v-card-actions>
                  </v-form>
                </v-card>
                
                </v-dialog>
                <v-dialog v-model="dialogDelete" max-width="500px">
                <v-card>
                    <v-card-title class="text-h5">Are you sure you want to delete this item?</v-card-title>
                    <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="closeDelete">Cancel</v-btn>
                    <v-btn color="blue darken-1" text @click="deleteItemConfirm">OK</v-btn>
                    <v-spacer></v-spacer>
                    </v-card-actions>
                </v-card>
                </v-dialog>
            </v-toolbar>
            </template>
            <template v-slot:[`item.actions`]="{ item }">
            <v-icon
                small
                @click="deleteItem(item)"
            >
                mdi-delete
            </v-icon>
            </template>
        </v-data-table>
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
    data: () => ({
      rules_required: [
        (v) => !!v || 'Required',
      ],
      rules_only_number_required: [
        (v) => !!v || 'Required',
        (v) => /^\d+$/.test(v) || 'Only number allowed',
        (v) => v > 0 || 'Only number greater than 0 allowed',
      ],
      dialog: false,
      search: '',
      dialogDelete: false,
      headers: [
        { text: 'ID', value: 'id' },
        {
          text: 'Name',
          align: 'start',
          sortable: false,
          value: 'keterangan',
        },
        { text: 'Pengeluaran', value: 'total_pengeluaran' },
        { text: 'Datetime', value: 'created_at' },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      pengeluaran_lainnya: [],
      editedIndex: -1,
      editedId: null,
      editedItem: {
        keterangan: '',
        total_pengeluaran: '',
      },
      defaultItem: {
        keterangan: '',
        total_pengeluaran: '',
      },
    }),

    computed: {
      formTitle () {
        return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
      },
    },

    watch: {
      dialog (val) {
        val || this.close()
      },
      dialogDelete (val) {
        val || this.closeDelete()
      },
    },

    mounted(){
      this.getData()
    },

    methods: {
      filterByIDColumn (value, search, item) {
        return item.id.toString().toLowerCase().indexOf(search.toLowerCase()) > -1
      },

      async getData(){
        await this.$axios
        .get('v1/pengeluaran_lain/')
        .then((res) => {
          this.pengeluaran_lainnya = res.data
          for (let i = 0; i < this.pengeluaran_lainnya.length; i++) {
                this.pengeluaran_lainnya[i].created_at = this.pengeluaran_lainnya[i].created_at.substring(0, 10);
            }
        })
        .catch((err) => {
          console.log(err)
        })
      },

      editItem (item) {
        this.editedIndex = this.pengeluaran_lainnya.indexOf(item)
        this.editedId = item.id
        this.editedItem.keterangan = item.keterangan
        this.editedItem.total_pengeluaran = item.total_pengeluaran
        this.dialog = true
      },

      deleteItem (item) {
        this.editedId = item.id
        this.dialogDelete = true
      },

      async deleteItemConfirm () {
        await this.$axios
        .delete(`v1/pengeluaran_lain/delete_pengeluaran_lain/${this.editedId}`)
        .then((res) => {
          this.closeDelete()
          this.getData()
        })
        .catch((err) => {
          console.log(err)
        })
      },

      close () {
        this.dialog = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
          this.editedId = null
        })
      },

      closeDelete () {
        this.dialogDelete = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
          this.editedId = null
        })
      },

      async save () {
        if (this.editedIndex > -1) {
          await this.$axios
          .put(`v1/pengeluaran_lain/update_pengeluaran_lain/${this.editedId}`, this.editedItem)
          .then((res) => {
            this.close()
            this.getData()
          })
          .catch((err) => {
            console.log(err)
          })
        } else {
          await this.$axios
          .post(`v1/pengeluaran_lain/create_pengeluaran_lain/`, this.editedItem)
          .then((res) => {
            this.close()
            this.getData()
          })
          .catch((err) => {
            console.log(err)
          })
        } 
      },
    }
}
</script>

<style scoped>
.image-avatar{
  width: 40px;
  height: 40px;
  border-radius: 100%;
}
</style>
