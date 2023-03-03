<template>
    <v-app class = "background-custom">
        <v-data-table
            :headers="headers"
            :items="discount"
            sort-by="name"
            class="elevation-1"
        >   <template v-slot:[`item.diskon`]="{item}">
                {{ item.diskon }} %
            </template>
            <template v-slot:top>
            <v-toolbar
                flat
            >
                <v-toolbar-title>Diskon Managements</v-toolbar-title>
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
                            v-model="editedItem.diskon_member"
                            label="Diskon Member"
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
            </template>
        </v-data-table>
    </v-app>    
</template>

<script>

export default {
    layout: 'menu',
    data: () => ({
      // only number rule non negatif
      rules_required: [
        (v) => !!v || 'Required',
        (v) => /^\d+$/.test(v) || 'Only number allowed',
        (v) => v > 0 || 'Only number greater than 0 allowed',
        (v) => v<= 30 || 'Forbited upper 30 %'
      ],
      dialog: false,
      dialogDelete: false,
      headers: [
        {
          text: 'Diskon',
          align: 'start',
          sortable: false,
          value: 'diskon_member',
        },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      discount: [],
      branches: ['Kebon Jeruk', 'Palagan', 'Padang', 'Pondok Gede'],
      editedIndex: 0,
      editedItem: {
        diskon_member: '',
      },
      defaultItem: {
        diskon_member: '',
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
      async getData(){
        await this.$axios
        .get('v1/diskon/')
        .then((res) => {
          this.discount = [res.data]
        })
        .catch((err) => {
          console.log(err)
        })
      },

      editItem (item) {
        this.editedIndex = this.discount.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },

      close () {
        this.dialog = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },

      closeDelete () {
        this.dialogDelete = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },

      async save () {
        if (this.editedIndex > -1) {
          await this.$axios
          .put(`v1/diskon/update_diskon/`, this.editedItem)
          .then((res) => {
            this.getData()
            this.close()
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
