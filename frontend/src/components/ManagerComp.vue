<template>
    <div class="tablediv">
        <v-card>
            <v-card-title>
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
                :items="desserts"
                :search="search"
                class="elevation-1"
            >
                <template v-slot:top>
                <v-toolbar
                    flat
                >
                    <v-toolbar-title>Gestiune venituri</v-toolbar-title>
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
                            Adauga
                            </v-btn>
                        </template>

                        <v-card>
                            <v-card-title>
                                <span class="text-h5">Gestionare finante</span>
                            </v-card-title>

                            <v-card-text>
                                <v-container>
                                        <v-text-field
                                        v-model="editedItem.name"
                                        label="Name"
                                        ></v-text-field>

                                        <v-text-field
                                        v-model="editedItem.year"
                                        label="Year"
                                        ></v-text-field>

                                        <v-select
                                        :items="types"
                                        v-model="editedItem.type"
                                        label="Type"
                                        ></v-select>
                                        
                                        <v-select
                                        v-if="(editedItem.type && ['Cheltuiala', 'Venit'].includes(editedItem.type) )"
                                        :items="subtypes[editedItem.type].options"
                                        v-model="editedItem.subtype"
                                        :label="subtypes[editedItem.type].label"
                                        ></v-select>

                                        <div v-if="editedItem.type && editedItem.subtype">
                                            <v-text-field
                                            v-for="field in otherFieldsSchema[editedItem.type][editedItem.subtype]"
                                            v-bind:key="field.label"
                                            :label="field.label"
                                            v-model="editedItem[field.label.toLowerCase().replaceAll(' ', '-')]"
                                            >{{field.label}}</v-text-field>
                                            
                                        </div>
                                        
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

                    <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                            <v-icon
                            v-bind="attrs"
                            v-on="on"
                            small
                            class="mr-2"
                            @click="editItem(item)"
                            >
                            mdi-pencil
                            </v-icon>
                        </template>
                        <span>Editare {{item.type.toLowerCase()}}</span>
                    </v-tooltip>

                    <v-tooltip 
                    v-if="item.type=='Venit' && ['Curs B2C', 'Curs B2B', 'Coaching', 'Consultanta'].includes(item.subtype)"
                    bottom>
                        <template v-slot:activator="{ on, attrs }">
                            <v-icon
                            v-bind="attrs"
                            v-on="on"
                            small
                            class="mr-2"
                            @click="editedItem.name=item.name;dialog=true"
                            >
                            mdi-plus-box
                            </v-icon>
                        </template>
                        <span>Adauga o cheltuiala asociata</span>
                    </v-tooltip>

                    <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                            <v-icon
                            v-bind="attrs"
                            v-on="on"
                            small
                            class="mr-2"
                            @click="deleteItem(item)"
                            >
                            mdi-delete
                            </v-icon>
                        </template>
                        <span>Sterge {{item.type.toLowerCase()}}</span>
                    </v-tooltip>
                </template>
            </v-data-table>
        </v-card>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: "ManagerComp",
    data () {
        return {
            search: '',
            dialog: false,
            dialogDelete: false,
            editedIndex: -1,
            editedItem: {
                name: '',
                type: '',
                year: new Date().getFullYear()  + 1
            },
            defaultItem: {
                name: '',
                type: '',
                year: new Date().getFullYear()  + 1
            },
            types:[
                'Cheltuiala',
                'Venit'
            ],
            typesMapping:{
                Cheltuiala: 'expenses',
                Venit: 'revenue'
            },
            subtypes:{
                'Cheltuiala':{
                    label: 'Expense type',
                    options: [
                        'Curs B2C',
                        'Curs B2B',
                        'Consultanta',
                        'Coaching',
                        'Others'
                    ]
                },
                'Venit':{
                    label: 'Revenue type',
                    options: [
                        'Curs B2C',
                        'Curs B2B',
                        'Coaching',
                        'Consultanta',
                    ]
                }
            },
            otherFieldsSchema:{
                'Venit': {
                    'Curs B2C': [
                        {
                            label: 'Iteratii',
                        },
                        {
                            label: 'Cost'
                        },
                        {
                            label: 'Medie cursanti'
                        }
                    ],
                    'Curs B2B': [
                        {
                            label: "Cost"
                        },
                        {
                            label: "Days"
                        }
                    ],
                    'Coaching': [
                        {
                            label: "Cost"
                        },
                        {
                            label: "Days"
                        }
                    ],
                    'Consultanta': [
                        {
                            label: "Cost"
                        },
                        {
                            label: "Days"
                        }
                    ]
                },
                'Cheltuiala': {
                    'Curs B2C': [
                        {
                            label: 'Cost'
                        }
                    ],
                    'Curs B2B': [
                        {
                            label: 'Cost'
                        }
                    ],
                    'Consultanta':[
                        {
                            label: 'Cost'
                        }
                    ],
                    'Coaching':[
                        {
                            label: 'Cost'
                        }
                    ],
                    'Others': [
                        {
                            label: 'Cost'
                        }
                    ]
                }
            },
            headers: [
                {
                    text: 'Name',
                    align: 'start',
                    value: 'name',
                },
                {
                    text: 'Type',
                    value: 'type'
                },
                {
                    text: 'Subtype',
                    value: 'subtype'
                },
                {
                    text: 'Year',
                    value: 'year'
                },
                {
                    text: 'Actions',
                    value: 'actions',
                    sortable: false
                },
            ],
            desserts: [
            ],
        }
    },
    mounted: function(){
        this.initTable();
    },
    watch: {
        dialog (val) {
            val || this.close()
        },
        dialogDelete (val) {
            val || this.closeDelete()
        },
    },
    methods: {
        editItem (item) {
            this.editedIndex = this.desserts.indexOf(item)
            this.editedItem = Object.assign({}, item)
            this.dialog = true
        },

        deleteItem (item) {
            this.editedIndex = this.desserts.indexOf(item)
            this.editedItem = Object.assign({}, item)
            this.dialogDelete = true
        },

        deleteItemConfirm () {
            var obj = this;
            let type = this.typesMapping[this.desserts[this.editedIndex].type];
            let id = this.desserts[this.editedIndex]._id.$oid;

            axios.delete(
                "http://localhost:8080/" + type + "/" + id
            )
            .then(response => {
                console.log(response.data);
                obj.desserts.splice(this.editedIndex, 1)
                obj.closeDelete()
            })
            .catch(errors => {
                console.log(errors);
            });
            // this.desserts.splice(this.editedIndex, 1)
            // this.closeDelete()
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

        save () {
            var obj = this;
            let request_data = this.editedItem;

            if (this.editedIndex > -1) {
                let id = request_data._id.$oid;
                delete request_data._id;
                request_data.year = parseInt(request_data.year);
                axios.put(
                    "http://localhost:8080/" + this.typesMapping[this.editedItem.type] + "/" + id,
                    request_data
                )
                .then(response => {
                    console.log(response.data);
                })
                .catch(error => {
                    console.log(error);
                })
                Object.assign(this.desserts[this.editedIndex], this.editedItem)
            } else {
                request_data.year = parseInt(request_data.year);
                axios.post(
                    "http://localhost:8080/" + this.typesMapping[this.editedItem.type] + "/",
                    request_data
                )
                .then(response => {
                    request_data._id = JSON.parse(response.data.id);
                    obj.desserts.push(request_data)
                })
                .catch(error => {
                    console.log(error);
                })
            }
            this.close()
        },

        initTable () {
            var obj = this;
            const requestOne = axios.get("http://localhost:8080/expenses/");
            const requestTwo = axios.get("http://localhost:8080/revenue/");
            axios.all([requestOne, requestTwo]).then(axios.spread((...responses) => {
                const responseOne = JSON.parse(responses[0].data);
                const responseTwo = JSON.parse(responses[1].data);
                obj.desserts = responseOne.concat(responseTwo);
            })).catch(errors => {
                console.log(errors)
            })
        }
    }
}
</script>

<style scoped>
.tablediv{
    margin-top: 24px;
    width: 70%;
    margin-left: 15%;
}
@media screen and (max-width: 600px) {
    .tablediv{
        margin-top: 24px;
        width: 98%;
        margin-left: 1%;
    }
}
</style>