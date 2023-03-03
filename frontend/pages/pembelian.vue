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
            :items="pembelian"
            :search="search"
            :custom-filter="filterByIDColumn"
            sort-by="name"
            class="elevation-1"
        >   
            <template v-slot:[`item.total_pembelian`]="{item}">
                Rp {{ item.total_pembelian | formatNumber }}
            </template>
            <template v-slot:top>
            <v-toolbar
                flat
            >
                <v-toolbar-title>Pembelian</v-toolbar-title>
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
                    New Item
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
                            <!-- DATA TABLE -->
                            <v-data-table
                                :headers="headers_product"
                                :items="editedItem.list_produk"
                                sort-by="name"
                                class="elevation-1"
                            >   
                                <template v-slot:[`item.harga_satuan`]="{item}">
                                    Rp {{ item.harga_satuan | formatNumber }}
                                </template>
                                <template v-slot:[`item.kuantitas_beli`]="{item}">
                                    {{ item.kuantitas_beli | formatNumber }}
                                </template>
                                <template v-slot:top>
                                <v-toolbar
                                    flat
                                >
                                    <v-toolbar-title>Product</v-toolbar-title>
                                    <v-divider
                                    class="mx-4"
                                    inset
                                    vertical
                                    ></v-divider>
                                    <v-spacer></v-spacer>
                                    <v-dialog
                                    v-model="dialog_product"
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
                                        New Item
                                        </v-btn>
                                    </template>
                                    <v-card>
                                        <v-form
                                            ref="form"
                                            v-model="validproduct"
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
                                                <!-- v-select product -->
                                                <v-select
                                                v-model="editedItem_product.id_stok_produk"
                                                :items="products"
                                                item-text="nama"
                                                item-value="id"
                                                label="Product"
                                                required
                                                ></v-select>
                                            </v-col>
                                            <v-col
                                                cols="12"
                                                sm="6"
                                                md="4"
                                            >
                                                <v-text-field
                                                v-model="editedItem_product.kuantitas_beli"
                                                label="Kuantitas"
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
                                                v-model="editedItem_product.harga_satuan"
                                                label="Harga Beli"
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
                                            @click="close_product"
                                        >
                                            Cancel
                                        </v-btn>
                                        <v-btn
                                            :disabled="!validproduct"
                                            color="blue darken-1"
                                            text
                                            @click="save_product"
                                        >
                                            Save
                                        </v-btn>
                                        </v-card-actions>
                                        </v-form>
                                    </v-card>
                                    
                                    </v-dialog>
                                    <v-dialog v-model="dialogDelete_product" max-width="500px">
                                    <v-card>
                                        <v-card-title class="text-h5">Are you sure you want to delete this item?</v-card-title>
                                        <v-card-actions>
                                        <v-spacer></v-spacer>
                                        <v-btn color="blue darken-1" text @click="closeDelete_product">Cancel</v-btn>
                                        <v-btn color="blue darken-1" text @click="deleteItemConfirm_product">OK</v-btn>
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
                                    @click="editItem_product(item)"
                                >
                                    mdi-pencil
                                </v-icon>
                                <v-icon
                                    small
                                    @click="deleteItem_product(item)"
                                >
                                    mdi-delete
                                </v-icon>
                                </template>
                            </v-data-table>
                            <!-- DATA TABLE -->
                        </v-row>
                        <v-row>
                        <v-col
                            cols="12"
                            sm="6"
                            md="4"
                        >
                            <v-text-field
                            v-model="editedItem.supplier"
                            label="Supplier"
                            :rules="rules_required"
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
      dialogDelete: false,
        headers: [
        { text: 'ID', value: 'id' },
        { text: 'Total Pembelian', value: 'total_pembelian' },
        { text: 'Supplier', value: 'supplier' },
        { text: 'Created Date', value: 'created_at' },
        { text: 'Actions', value: 'actions', sortable: false },
        ],
      headers_product: [
        { text: 'ID', value: 'stok_produk.id' },
        { text: 'Produk', value: 'stok_produk.nama' },
        { text: 'Harga Beli', value: 'harga_satuan' },
        { text: 'Kuantitas', value: 'kuantitas_beli' },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      search: '',
      pembelian: [],
      products: [],
      products_to_buy: [],
      editedIndex: -1,
      editedId: null,
      editedItem: {
        list_produk: [],
        daftar_produk: [],
        total_pembelian: '',
        supplier: '',
      },
      defaultItem: {
        list_produk: [],
        daftar_produk: [],
        total_pembelian: '',
        supplier: '',
      },

      dialog_product: false,
      dialogDelete_product: false,
      editedIndex_product: -1,
      editedItem_product: {
        id_stok_produk: '',
        harga_satuan: '',
        kuantitas_beli: '',
      },
      defaultItem_product: {
        id_stok_produk: '',
        harga_satuan: '',
        kuantitas_beli: '',
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
        dialog_product (val) {
            val || this.close_product()
        },
        dialogDelete_product (val) {
            val || this.closeDelete_product()
        },
    },

    mounted () {
        this.getPembelian();
        this.getProducts();
    },

    methods: {
      filterByIDColumn (value, search, item) {
        return item.id.toString().toLowerCase().indexOf(search.toLowerCase()) > -1
      },

      async getPembelian () {
        try {
          const response = await this.$axios.get('v1/pembelian/');
          this.pembelian = response.data;
        //   change created date format in this.pembelian
        for (let i = 0; i < this.pembelian.length; i++) {
            this.pembelian[i].created_at = this.pembelian[i].created_at.substring(0, 10);
        }

        } catch (error) {
          console.error(error);
        }
      },
        async getProducts () {
            try {
            const response = await this.$axios.get('v1/stok_produk/');
            this.products = response.data;
            } catch (error) {
            console.error(error);
            }
        },

      editItem (item) {
        this.editedIndex = this.pembelian.indexOf(item)
        this.editedId = item.id
        this.editedItem.list_produk = item.list_produk;
        this.editedItem.daftar_produk = this.convert_list_produk_to_daftar_produk(item.list_produk);
        this.editedItem.supplier = item.supplier;
        this.editedItem.total_pembelian = item.total_pembelian;
        this.dialog = true
      },

      convert_list_produk_to_daftar_produk (list_produk) {
        let daftar_produk = [];
        for (let i = 0; i < list_produk.length; i++) {
            daftar_produk.push({
                id_stok_produk: list_produk[i].stok_produk.id,
                harga_satuan: list_produk[i].harga_satuan,
                kuantitas_beli: list_produk[i].kuantitas_beli,
            });
        }
        return daftar_produk;
      },

      deleteItem (item) {
        this.editedId = item.id
        this.dialogDelete = true
      },

      async deleteItemConfirm () {
        try {
          const response = await this.$axios.delete(`v1/pembelian/delete_pembelian/${this.editedId}`);
          this.closeDelete();
          this.getPembelian();
        } catch (error) {
          console.error(error);
        }
      },

      close () {
        this.dialog = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
        this.getPembelian();
      },

      closeDelete () {
        this.dialogDelete = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
          this.editedId = null
        })
        this.getPembelian();
      },

      async save () {
        this.editedItem.daftar_produk = this.convert_list_produk_to_daftar_produk(this.editedItem.list_produk);
        this.editedItem.total_pembelian = this.editedItem.daftar_produk.reduce((acc, cur) => {
            return acc + cur.harga_satuan * cur.kuantitas_beli
        }, 0)
        if (this.editedIndex > -1) {
          await this.$axios.put('v1/pembelian/update_pembelian/'+this.editedId, {
            daftar_produk: this.editedItem.daftar_produk,
            total_pembelian: this.editedItem.total_pembelian,
            supplier: this.editedItem.supplier,
          })
          .then((res)=>{
            this.getPembelian();
            this.close();
          })
          .catch((err)=>{
            console.error(err);
          })
        } else {
          await this.$axios.post('v1/pembelian/create_pembelian/', {
            daftar_produk: this.editedItem.daftar_produk,
            total_pembelian: this.editedItem.total_pembelian,
            supplier: this.editedItem.supplier,
          })
          .then((res)=>{
            this.getPembelian();
            this.close();
          })
          .catch((err)=>{
            console.error(err);
          })
        }
      },

      get_item_product(){
          return this.pembelian[this.editedIndex].produk
      },

      editItem_product (item) {
        this.editedIndex_product = this.editedItem.list_produk.indexOf(item)
        this.editedItem_product.id_stok_produk = item.stok_produk.id
        this.editedItem_product.harga_satuan = item.harga_satuan
        this.editedItem_product.kuantitas_beli = item.kuantitas_beli
        this.dialog_product = true
      },

      deleteItem_product (item) {
        this.editedIndex_product = this.editedItem.list_produk.indexOf(item)
        this.dialogDelete_product = true
      },

      deleteItemConfirm_product () {
        this.editedItem.list_produk.splice(this.editedIndex_product, 1)
        this.closeDelete_product()
      },

      close_product () {
        this.dialog_product = false
        this.$nextTick(() => {
          this.editedIndex_product = -1
        })
      },

      closeDelete_product () {
        this.dialogDelete_product = false
        this.$nextTick(() => {
          this.editedItem_product = Object.assign({}, this.defaultItem_product)
          this.editedIndex_product = -1
        })
      },

      get_produk_by_id(id){
        for (let i = 0; i < this.products.length; i++) {
            if (this.products[i].id == id) {
                return this.products[i]
            }
        }
      },

      save_product () {
        this.editedItem_product.stok_produk = Object.assign({}, this.get_produk_by_id(this.editedItem_product.id_stok_produk));
        if (this.editedIndex_product > -1) {
          Object.assign(this.editedItem.list_produk[this.editedIndex_product], this.editedItem_product)
        } else {
          this.editedItem.list_produk.push(this.editedItem_product)
        }
        this.close_product()
      },
    },
    
}
</script>

<style scoped>
.image-avatar{
  width: 40px;
  height: 40px;
  border-radius: 100%;
}
</style>
