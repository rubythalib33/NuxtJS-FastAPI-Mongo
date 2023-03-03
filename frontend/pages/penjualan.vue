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
            :items="penjualan"
            :search="search"
            :custom-filter="filterByIDColumn"
            sort-by="created_at"
            class="elevation-1"
        >   
            <template v-slot:[`item.total_penjualan`]="{item}">
                Rp {{ item.total_penjualan | formatNumber }}
            </template>
            <template v-slot:top>
            <v-toolbar
                flat
            >
                <v-toolbar-title>Penjualan</v-toolbar-title>
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
                                sort-by="nama"
                                class="elevation-1"
                            >   
                                <template v-slot:[`item.harga_satuan`]="{item}">
                                    Rp {{ item.harga_satuan | formatNumber }}
                                </template>
                                <template v-slot:[`item.kuantitas_jual`]="{item}">
                                    {{ item.kuantitas_jual | formatNumber }}
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
                                                <v-select
                                                v-model="editedItem_product.id"
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
                                                v-model="editedItem_product.kuantitas_jual"
                                                label="Kuantitas"
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
                            <v-select
                            v-model="editedItem.id_user_penjual"
                            :items="users"
                            item-text="nama"
                            item-value="id"
                            label="User"
                            required>
                            </v-select>
                        </v-col>
                        <v-col
                            cols="12"
                            sm="6"
                            md="4"
                        >
                            <v-select
                            v-model="editedItem.id_member"
                            :items="members"
                            item-text="nama"
                            item-value="id"
                            label="Member"
                            required>
                            </v-select>
                        </v-col>
                        <v-col
                            cols="12"
                            sm="6"
                            md="4"
                        >
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
        { text: 'Total penjualan', value: 'total_penjualan' },
        { text: 'User', value: 'user_penjual.nama' },
        { text: 'Branch', value: 'user_penjual.branch.nama'},
        { text: 'Member', value: 'member.nama'},
        { text: 'Created Date', value: 'created_at' },
        { text: 'Actions', value: 'actions', sortable: false },
        ],
      headers_product: [
        { text: 'ID', value: 'id' },
        { text: 'Produk', value: 'nama' },
        { text: 'Harga Jual', value: 'harga_satuan' },
        { text: 'Kuantitas', value: 'kuantitas_jual' },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      search: '',
      penjualan: [],
      products: [],
      members: [],
      users: [],
      discount: 0,
      products_to_buy: [],
      editedIndex: -1,
      editedId: null,
      editedItem: {
        daftar_produk: [],
        list_produk: [],
        total_penjualan: '',
        id_member: '',
        total_penjualan: '',
        id_user_penjual: ''
      },
      defaultItem: {
        daftar_produk: [],
        list_produk: [],
        total_penjualan: '',
        id_member: '',
        total_penjualan: '',
        id_user_penjual: ''
      },

      dialog_product: false,
      dialogDelete_product: false,
      editedIndex_product: -1,
      editedItem_product: {
        id: '',
        harga_satuan: '',
        kuantitas_jual: '',
      },
      defaultItem_product: {
        id: '',
        harga_satuan: '',
        kuantitas_jual: '',
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
        this.getPenjualan();
        this.getProducts();
        this.getMembers();
        this.getUsers();
        this.getDiscount();
    },

    methods: {
      filterByIDColumn (value, search, item) {
        return item.id.toString().toLowerCase().indexOf(search.toLowerCase()) > -1
      },

      async getPenjualan () {
        try {
            const response = await this.$axios.get('v1/penjualan/');
            this.penjualan = response.data;
            // change created format in this.penjualan
            for (let i = 0; i < this.penjualan.length; i++) {
                this.penjualan[i].created_at = this.penjualan[i].created_at.substring(0, 10);
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

        async getMembers () {
            try {
                const response = await this.$axios.get('v1/member/');
                this.members = response.data;
            } catch (error) {
                console.error(error);
            }
        },

        async getUsers () {
            try {
                const response = await this.$axios.get('v1/user/');
                this.users = response.data;
            } catch (error) {
                console.error(error);
            }
        },

        async getDiscount () {
            try {
                const response = await this.$axios.get('v1/diskon/');
                this.discount = response.data.diskon_member;
            } catch (error) {
                console.error(error);
            }
        },

      editItem (item) {
        this.editedIndex = this.penjualan.indexOf(item)
        this.editedId = item.id
        this.editedItem.list_produk = item.list_produk
        this.editedItem.id_user_penjual = item.user_penjual.id
        this.editedItem.id_member = item.member.id
        this.dialog = true
        // add nama nama produk to this.penjualan[i].list_produk
        for (let j = 0; j < this.penjualan[this.editedIndex].list_produk.length; j++) {
            for (let k = 0; k < this.products.length; k++) {
                if (this.penjualan[this.editedIndex].list_produk[j].id == this.products[k].id) {
                    this.penjualan[this.editedIndex].list_produk[j].nama = this.products[k].nama;
                }
            }
        }
      },

      deleteItem (item) {
        this.editedId = item.id
        this.dialogDelete = true
      },

      async deleteItemConfirm () {
        try {
            const response = await this.$axios.delete(`v1/penjualan/delete_penjualan/${this.editedId}`);
            this.getPenjualan();
            this.closeDelete();
        } catch (error) {
            console.error(error);
        }
      },

      close () {
        this.dialog = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
          this.editedId = null
        })
        this.getPenjualan();
      },

      closeDelete () {
        this.dialogDelete = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
          this.editedId = null
        })
      },

      convert_list_produk_to_daftar_produk (list_produk) {
        let daftar_produk = [];
        for (let i = 0; i < list_produk.length; i++) {
            daftar_produk.push({
                id_stok_produk: list_produk[i].id,
                harga_satuan: list_produk[i].harga_satuan,
                kuantitas_jual: list_produk[i].kuantitas_jual,
            });
        }
        return daftar_produk;
      },

      async save () {
        this.editedItem.daftar_produk = this.convert_list_produk_to_daftar_produk(this.editedItem.list_produk);
        this.editedItem.total_penjualan = this.editedItem.daftar_produk.reduce((acc, cur)=> {
          console.log(acc)
          return acc + cur.harga_satuan * cur.kuantitas_jual
        }, 0)
        let data = {}
        if (this.editedItem.id_member === ''){
          this.editedItem.total_penjualan = this.editedItem.total_penjualan
          data = {
            daftar_produk: this.editedItem.daftar_produk,
            id_user_penjual: this.editedItem.id_user_penjual,
            total_penjualan: this.editedItem.total_penjualan
          }
        } else {
          this.editedItem.total_penjualan =this.editedItem.total_penjualan - this.editedItem.total_penjualan*this.discount/100;
          data = {
            daftar_produk: this.editedItem.daftar_produk,
            id_member: this.editedItem.id_member,
            id_user_penjual: this.editedItem.id_user_penjual,
            total_penjualan: this.editedItem.total_penjualan
          }
        }
        if (this.editedIndex > -1) {
          await this.$axios.post('v1/penjualan/update_penjualan/'+this.editedId, data).then((res) => {
            this.getPenjualan();
            this.close();
          }).catch((err)=>{
            console.error(err)
          })
        } else {
          await this.$axios.post('v1/penjualan/create_penjualan/', data).then((res) => {
            this.getPenjualan();
            this.close();
          }).catch((err)=>{
            console.error(err)
          })
        }
      },

      get_item_product(){
          return this.penjualan[this.editedIndex].produk
      },

      editItem_product (item) {
        this.editedIndex_product = this.editedItem.list_produk.indexOf(item)
        this.editedItem_product.id = item.id
        this.editedItem_product.kuantitas_jual = item.kuantitas_jual
        // get this.editedItem_product.harga_satuan from this.products
        for(let i=0;i<this.products.length;i++){
          if(this.products[i].id === item.id){
            this.editedItem_product.harga_satuan = this.products[i].harga
          }
        }
        this.dialog_product = true
      },

      deleteItem_product (item) {
        this.editedIndex_product = this.editedItem.list_produk.indexOf(item)
        this.editedItem_product = Object.assign({}, item)
        this.dialogDelete_product = true
      },

      deleteItemConfirm_product () {
        this.editedItem.list_produk.splice(this.editedIndex_product, 1)
        this.closeDelete_product()
      },

      close_product () {
        this.dialog_product = false
        this.$nextTick(() => {
          this.editedItem_product = Object.assign({}, this.defaultItem_product)
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

      save_product () {
        if (this.editedIndex_product > -1) {
          Object.assign(this.editedItem.list_produk[this.editedIndex_product], this.editedItem_product)
        } else {
          for(let i=0;i<this.products.length;i++){
            if(this.products[i].id === this.editedItem_product.id){
              this.editedItem_product.harga_satuan = this.products[i].harga
              this.editedItem_product.nama = this.products[i].nama
            }
          }
          this.editedItem.list_produk.push(this.editedItem_product)
        }
        this.close_product()
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
