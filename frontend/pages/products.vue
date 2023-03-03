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
            :items="products"
            :search="search"
            sort-by="id"
            class="elevation-1"
        >
            <template v-slot:[`item.harga`]="{item}">
                Rp {{ item.harga | formatNumber }}
            </template>
            <template v-slot:[`item.kuantitas`]="{item}">
                {{ item.kuantitas | formatNumber }}
            </template>
            <template v-slot:top>
            <v-toolbar
                flat
            >
                <v-toolbar-title>Products</v-toolbar-title>
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
                    Add Product
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
                            v-model="editedItem.nama"
                            label="Nama Product"
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
                            <v-select
                            v-model="editedItem.id_kategori"
                            :items="categories"
                            label="Kategori"
                            item-text="nama"
                            item-value="id"
                            return-value="id"
                            :rules="rules_required"
                            required
                            ></v-select>
                        </v-col>
                        <v-col
                            cols="12"
                            sm="6"
                            md="4"
                        >
                            <v-text-field
                            v-model="editedItem.harga"
                            label="Harga"
                            :rules="rules_only_number_required"
                            required
                            ></v-text-field>
                        </v-col>
                        <v-col
                            cols="12"
                            sm="6"
                            md="4"
                        >
                            <v-text-field
                            v-model="editedItem.kuantitas"
                            label="Stok"
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
                class="mr-2"
                @click="editItem(item)"
            >
                mdi-pencil
            </v-icon>
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
      dialogDelete: false,
      search: '',
      headers: [
        { text: 'ID', value: 'id' },
        {
          text: 'Name',
          align: 'start',
          sortable: false,
          value: 'nama',
        },
        { text: 'Kategori', value: 'kategori.nama' },
        { text: 'Harga', value: 'harga' },
        { text: 'Stok', value: 'kuantitas' },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      products: [],
      categories: [],
      editedIndex: -1,
      editedId: null,
      editedItem: {
        nama: '',
        id_kategori: '',
        harga: '',
        kuantitas: '',
      },
      defaultItem: {
        nama: '',
        id_kategori: '',
        harga: '',
        kuantitas: '',
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
      this.getCategory()
    },

    methods: {
      async getData(){
        await this.$axios
        .get('v1/stok_produk/')
        .then((res) => {
          this.products = res.data
        })
        .catch((err) => {
          console.log(err)
        })
      },
      async getCategory(){
        await this.$axios
        .get('v1/kategori_produk/')
        .then((res) => {
          this.categories = res.data
        })
        .catch((err) => {
          console.log(err)
        })
      },

      editItem (item) {
        this.editedIndex = this.products.indexOf(item)
        this.editedId = item.id
        this.editedItem.nama = item.nama
        this.editedItem.id_kategori = item.kategori.id
        this.editedItem.harga = item.harga
        this.editedItem.kuantitas = item.kuantitas
        this.dialog = true
      },

      deleteItem (item) {
        this.editedId = item.id
        this.dialogDelete = true
      },

      async deleteItemConfirm () {
        await this.$axios
        .delete(`v1/stok_produk/delete_stok_produk/${this.editedId}`)
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
          .put(`v1/stok_produk/update_stok_produk/${this.editedId}`, this.editedItem)
          .then((res) => {
            this.close()
            this.getData()
          })
          .catch((err) => {
            console.log(err)
          })
        } else {
          await this.$axios
          .post(`v1/stok_produk/create_stok_produk/`, this.editedItem)
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
