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
            :items="users"
            :search="search"
            sort-by="nama"
            class="elevation-1"
        >
            <template v-slot:top>
            <v-toolbar
                flat
            >
                <v-toolbar-title>User Managements</v-toolbar-title>
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
                    Create User
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
                            label="User Name"
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
                        <!-- edit password -->
                        <v-col
                            cols="12"
                            sm="6"
                            md="4"
                        >
                            <v-text-field
                            v-model="editedPassword"
                            label="Password"
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
                        <v-col
                            cols="12"
                            sm="6"
                            md="4"
                        >
                            <v-text-field
                            v-model="editedItem.nik"
                            label="NIK"
                            :rules="rules_required"
                            required
                            ></v-text-field>
                        </v-col>
                        <!-- dropdown branches -->
                        <v-col
                            cols="12"
                            sm="6"
                            md="4"
                        >
                            <v-select
                            v-model="editedItem.id_branch"
                            :items="branches"
                            label="Branch"
                            item-text="nama"
                            item-value="id"
                            return-value="id"
                            ></v-select>
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
                <v-dialog
                v-model="dialogChangePassword"
                max-width="500px"
                >
                <v-card>
                  <v-form
                    ref="form"
                    v-model="valid"
                    lazy-validation
                  >
                    <v-card-title>
                    <span class="text-h5">Change Password</span>
                    </v-card-title>

                    <v-card-text>
                    <v-container>
                        <v-row>
                        <!-- edit password -->
                        <v-col
                            cols="12"
                            sm="6"
                            md="4"
                        >
                            <v-text-field
                            v-model="editedPassword"
                            label="Password"
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
                        @click="closePassword"
                    >
                        Cancel
                    </v-btn>
                    <v-btn
                        :disabled="!valid"
                        color="blue darken-1"
                        text
                        @click="savePassword"
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
                <v-dialog v-model="dialogAdmin" max-width="500px">
                <v-card>
                    <v-card-title class="text-h5">Are you sure you want to change this user to admin?</v-card-title>
                    <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="closeAdmin">Cancel</v-btn>
                    <v-btn color="blue darken-1" text @click="changeAdmin">OK</v-btn>
                    <v-spacer></v-spacer>
                    </v-card-actions>
                </v-card>
                </v-dialog>
                <v-dialog v-model="dialogNotAdmin" max-width="500px">
                <v-card>
                    <v-card-title class="text-h5">Are you sure you want to change this user to not admin?</v-card-title>
                    <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="closeNotAdmin">Cancel</v-btn>
                    <v-btn color="blue darken-1" text @click="changeNotAdmin">OK</v-btn>
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
            <v-icon
                small
                @click="setAdmin(item)"
            >
                mdi-account-star
            </v-icon>
            <v-icon
                small
                @click="setNotAdmin(item)"
            >
                mdi-account-star-outline
            </v-icon>
            <v-icon
                small
                @click="setPassword(item)"
            >
              mdi-key
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
      search: '',
      dialogDelete: false,
      dialogAdmin: false,
      dialogNotAdmin: false,
      dialogChangePassword: false,
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
        { text: 'NIK', value: 'nik' },
        { text: 'Branch', value: 'branch.nama' },
        { text: 'Admin', value: 'is_superuser'},
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      users: [],
      branches: [],
      editedIndex: -1,
      editedPassword: '',
      editedItem: {
        nama: '',
        email: '',
        no_telp: '',
        alamat: '',
        nik: '',
        id_branch: '',
      },
      defaultItem: {
        nama: '',
        email: '',
        no_telp: '',
        alamat: '',
        nik: '',
        id_branch: '',
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
      this.getBranch()
    },

    methods: {
      async getData(){
        await this.$axios
        .get('v1/user/')
        .then((res) => {
          this.users = res.data
        })
        .catch((err) => {
          console.log(err)
        })
      },

      async getBranch(){
        await this.$axios
        .get('v1/branch/')
        .then((res) => {
          this.branches = res.data
        })
        .catch((err) => {
          console.log(err)
        })
      },

      editItem (item) {
        this.editedIndex = this.users.indexOf(item)
        this.editedId = item.id
        this.editedItem.nama = item.nama
        this.editedItem.email = item.email
        this.editedItem.no_telp = item.no_telp
        this.editedItem.alamat = item.alamat
        this.editedItem.nik = item.nik
        if(item.branch){
          this.editedItem.id_branch = item.branch.id
        }
        this.dialog = true
      },

      setPassword(item){
        this.editedId = item.id;
        this.dialogChangePassword = true;
      },

      setAdmin(item){
        if (item.is_superuser != true){
          this.dialogAdmin = true
          this.editedId = item.id
        }
        else{
          alert('This user is already admin')
        }
      },

      setNotAdmin(item){
        if (item.is_superuser != false){
          this.dialogNotAdmin = true
          this.editedId = item.id
        }
        else{
          alert('This user is already not admin')
        }
      },

      async savePassword(){
        await this.$axios.patch('v1/user/change_password/'+this.editedId, {
          new_password: this.editedPassword
        }).then((res)=>{
          this.getData()
          this.closePassword()
        }).catch((err)=>{
          console.log(err)
        })
      },

      async changeAdmin(){
        await this.$axios
        .put('v1/user/change_level_user/' + this.editedId, {
          is_superuser: true,
          is_admin: true,
        })
        .then((res) => {
          this.dialogAdmin = false
          this.getData()
        })
        .catch((err) => {
          console.log(err)
        })
      },

      async changeNotAdmin(){
        await this.$axios
        .put('v1/user/change_level_user/' + this.editedId, {
          is_superuser: false,
          is_admin: false,
        })
        .then((res) => {
          this.closeNotAdmin()
          this.getData()
        })
        .catch((err) => {
          console.log(err)
        })
      },

      deleteItem (item) {
        this.editedId = item.id
        this.dialogDelete = true
      },

      async deleteItemConfirm () {
        await this.$axios
        .delete(`v1/user/delete_user/${this.editedId}`)
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
          this.editedPassword = ''
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

      closeAdmin () {
        this.dialogAdmin = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
          this.editedId = null
        })
      },

      closeNotAdmin () {
        this.dialogNotAdmin = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
          this.editedId = null
        })
      },

      closePassword() {
        this.dialogChangePassword = false;
        this.$nextTick(() => {
          this.editedPassword = ''
          this.editedIndex = -1
          this.editedId = null
        })
      },

      async save () {
        if (this.editedIndex > -1) {
          if (this.editedPassword != '') {
            console.log('diabaikan dulu wkwk')
          }
          await this.$axios
          .patch(`v1/user/update_user/${this.editedId}`, this.editedItem)
          .then((res) => {
            this.getData()
            this.close()
          })
          .catch((err) => {
            console.log(err)
            console.log(this.editedItem)
          })
        } else {
          this.editedItem.password = this.editedPassword
          await this.$axios
          .post(`v1/user/create_user/`, this.editedItem)
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
