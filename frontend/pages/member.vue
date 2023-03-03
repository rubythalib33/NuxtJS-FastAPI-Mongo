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
            :items="member"
            :search="search"
            sort-by="nama"
            class="elevation-1"
        >
            <template v-slot:top>
            <v-toolbar
                flat
            >
                <v-toolbar-title>Member Managements</v-toolbar-title>
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
                    Create Member
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
                            label="User name"
                            :rules="rules_required"
                            required
                            ></v-text-field>
                        </v-col>
                        <v-col
                            cols="12"
                            sm="6"
                            md="4"
                        >
                            <v-text-field
                            v-model="editedItem.email"
                            label="Email"
                            :rules="rules_required"
                            required
                            ></v-text-field>
                        </v-col>
                        <v-col
                            cols="12"
                            sm="6"
                            md="4"
                        >
                            <v-text-field
                            v-model="editedItem.no_telp"
                            label="Phone Number"
                            :rules="rules_required"
                            required
                            ></v-text-field>
                        </v-col>
                        <v-col
                            cols="12"
                            sm="6"
                            md="4"
                        >
                            <v-text-field
                            v-model="editedItem.alamat"
                            label="Address"
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

export default {
    layout: 'menu',
    data: () => ({
      rules_required: [
        (v) => !!v || 'Required',
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
        { text: 'Email', value: 'email' },
        { text: 'Nomor Hp', value: 'no_telp' },
        { text: 'Address', value: 'alamat' },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      member: [],
      editedIndex: -1,
      editedId: null,
      editedItem: {
        nama: '',
        email: '',
        no_telp: '',
        alamat: '',
      },
      defaultItem: {
        nama: '',
        email: '',
        no_telp: '',
        alamat: '',
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
        .get('v1/member/')
        .then((res) => {
          this.member = res.data
        })
        .catch((err) => {
          console.log(err)
        })
      },

      editItem (item) {
        this.editedIndex = this.member.indexOf(item)
        this.editedId = item.id
        this.editedItem.nama = item.nama
        this.editedItem.email = item.email
        this.editedItem.no_telp = item.no_telp
        this.editedItem.alamat = item.alamat
        this.dialog = true
      },

      deleteItem (item) {
        this.editedId = item.id
        this.dialogDelete = true
      },

      async deleteItemConfirm () {
        await this.$axios
        .delete(`v1/member/delete_member/${this.editedId}`)
        .then((res) => {
          this.getData()
          this.closeDelete()
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
          .put(`v1/member/update_member/${this.editedId}`, this.editedItem)
          .then((res) => {
            this.getData()
            this.close()
          })
          .catch((err) => {
            console.log(err)
          })
        } else {
          await this.$axios
          .post(`v1/member/create_member/`, this.editedItem)
          .then((res) => {
            this.getData()
            this.close()
          })
          .catch((err) => {
            console.log(err)
            console.log(this.editedItem)
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
