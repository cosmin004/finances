<template>
  <div class="tablediv">
      <v-card>
          <v-img
            class="white--text align-end"
            height="200px"
            :src="require('../assets/stats.jpeg')"
        >
            <!-- <v-card-title>
                Analytics dashboard
            </v-card-title> -->
        </v-img>
            <v-card-title>
                Analytics dashboard
            </v-card-title>
            <v-card-subtitle>
                Currently selected year
                <v-dialog
                    ref="dialog"
                    v-if="isMobile()"
                    v-model="menu"
                    :return-value.sync="date"
                    persistent
                    width="290px"
                >
                    <template v-slot:activator="{ on, attrs }">
                        <v-chip
                            class="mr-2"
                            v-bind="attrs"
                            v-on="on"
                        >
                            <v-icon left>
                                mdi-timer-sand
                            </v-icon>
                            {{year}}
                        </v-chip>
                    </template>
                    <v-date-picker
                        v-model="date"
                        type="month"
                        no-title
                        scrollable
                        ref="picker"
                        @input="save"
                        reactive
                    >
                    <v-spacer></v-spacer>
                    <v-btn
                        text
                        color="primary"
                        @click="menu = false"
                    >
                        Cancel
                    </v-btn>
                    <v-btn
                        text
                        color="primary"
                        @click="$refs.menu.save(date)"
                    >
                        OK
                    </v-btn>
                    </v-date-picker>
                </v-dialog>
                <v-menu
                    ref="menu"
                    v-model="menu"
                    v-else
                    :close-on-content-click="false"
                    :return-value.sync="date"
                    transition="scale-transition"
                    offset-y
                    max-width="290px"
                    min-width="auto"
                >
                    <template v-slot:activator="{ on, attrs }">
                        <v-chip
                            class="mr-2"
                            v-bind="attrs"
                            v-on="on"
                        >
                            <v-icon left>
                                mdi-timer-sand
                            </v-icon>
                            {{year}}
                        </v-chip>
                    </template>
                    <v-date-picker
                        v-model="date"
                        type="month"
                        no-title
                        scrollable
                        ref="picker"
                        @input="save"
                        reactive
                    >
                    <v-spacer></v-spacer>
                    <v-btn
                        text
                        color="primary"
                        @click="menu = false"
                    >
                        Cancel
                    </v-btn>
                    <v-btn
                        text
                        color="primary"
                        @click="$refs.menu.save(date)"
                    >
                        OK
                    </v-btn>
                    </v-date-picker>
                </v-menu>
            </v-card-subtitle>

            <v-divider class="mx-4"></v-divider>
            <v-card-title>
                Raport venituri si cheltuieli
            </v-card-title>

            <v-card-text>
                <v-container fluid>
                    <v-row dense>
                        <v-col
                        v-for="card in cards"
                        :key="card.title"
                        :cols="card.flex"
                        >
                            <v-card>
                                <v-img
                                :src="card.src"
                                class="white--text align-end"
                                gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                                height="200px"
                                >
                                <v-card-title v-text="card.title"></v-card-title>
                                </v-img>
                                
                                <v-card-text style="text-align: center">
                                    <h1>
                                        {{card.amount}}
                                    </h1>
                                </v-card-text>
                            </v-card>
                        </v-col>
                    </v-row>
                </v-container>
            </v-card-text>

            <v-divider class="mx-4"></v-divider>
            <v-card-title v-if="cards[2].amount != '0 Lei'">
                Distributie venituri si cheltuieli
            </v-card-title>
            <v-card-title v-else>
                Adauga venituri si cheltuieli pentru a vizualiza mai multe
            </v-card-title>

            <v-card-text v-if="cards[2].amount != '0 Lei'">
                <v-container fluid>
                    <v-row dense>
                        <v-col
                        :cols="(isMobile() ? 12 : 6)"
                        >
                            <Plotly :data="expensesChart.data" :layout="expensesChart.layout" :display-mode-bar="false"></Plotly>
                        </v-col>
                        <v-col
                        :cols="(isMobile() ? 12 : 6)"
                        >
                            <Plotly :data="revenueChart.data" :layout="revenueChart.layout" :display-mode-bar="false"></Plotly>
                        </v-col>
                    </v-row>
                </v-container>
            </v-card-text>

      </v-card>
  </div>
</template>

<script>
import { isMobile } from 'mobile-device-detect';
import axios from 'axios';
import { Plotly } from 'vue-plotly'
export default {
    name: 'App',
    components: {
        Plotly
    },
    data: () => ({
        menu: false,
        date: (new Date().getFullYear()  + 1) + '-01',
        cards: [
            {
                title: 'Venituri totale', src: require('../assets/revenue.jpeg'),
                flex: (isMobile ? 12 : 6) ,
                amount: "8000 Lei"
            },
            {
                title: 'Cheltuieli totale',
                src: require('../assets/expenses.jpeg'),
                flex: (isMobile ? 12 : 6),
                amount: "3000 Lei"
            },
            {
                title: 'Profit(venituri - cheltuieli) si net profit margin',
                src: (isMobile ? require('../assets/profitMobile.jpeg') : require('../assets/profitNonMobile.png')),
                flex: 12,
                amount: "5000 Lei(62.5%)"
            },
        ],
        revenue: 0,
        expenses: 0,
        expensesChart: {
            data:[
                {
                    values: [
                        3000,
                        4000,
                        1000
                    ],
                    labels: [
                        'Consultanta',
                        'Cursuri B2B',
                        'Cursuri B2C',
                    ],
                    type: 'pie'
                }
            ],
            layout:{
                title: "Venituri"
            }
        },
        revenueChart: {
            data:[
                {
                    values: [
                        1000,
                        500,
                        1000,
                        500
                    ],
                    labels: [
                        'Consultanta',
                        'Cursuri B2C',
                        'Cursuri B2B',
                        'Other'
                    ],
                    type: 'pie'
                }
            ],
            layout:{
                title: "Cheltuieli"
            }
        }
    }),
    computed: {
        year (){
            return parseInt(this.date.split('-')[0])
        },
    },
    mounted: function() {
        this.getExpensesByCategory();
        this.getRevenueByCategory();
    },
    watch: {
        menu (val) {
            val && this.$nextTick(() => (this.$refs.picker.activePicker = 'YEAR'))
        },
        year () {
            this.getExpensesByCategory();
            this.getRevenueByCategory();
        }
    },
    methods: {
        save (date) {
            this.$refs.menu.save(date);
            this.$refs.picker.activePicker = 'YEAR'
            this.menu = false;
        },
        resetDate () {
            this.date=(new Date().getFullYear()  + 1) + '-01';
            this.$refs.menu.save(this.date)
            this.$refs.picker.activePicker = 'YEAR'
            this.menu = false;
        },
        // TODO: Add picker in dialog for mobile devices
        isMobile: function() {
            return isMobile
        },
        getExpensesByCategory (){
            var obj = this;
            axios.get("http://localhost:8080/expenses/expenses-category/" + this.year)
            .then(
                response => {
                    var values = [];
                    var labels = [];
                    var totalExpenses = 0;

                    for (const key in response.data.subtypes_expenses) {
                        labels.push(key)
                        values.push(response.data.subtypes_expenses[key])
                        totalExpenses += response.data.subtypes_expenses[key]
                    }

                    obj.expensesChart = {
                        data:[
                            {
                                values: values,
                                labels: labels,
                                type: 'pie'
                            }
                        ],
                        layout:{
                            title: "Cheltuieli"
                        }
                    }
                    obj.expenses = totalExpenses;
                    obj.cards[1].amount = totalExpenses + " Lei";
                }
            )
            .catch(error => {
                console.log(error);
            })
        },
        getRevenueByCategory (){
            var obj = this;
            axios.get("http://localhost:8080/revenue/revenue-category/" + this.year)
            .then(
                response => {
                    var values = [];
                    var labels = [];
                    var totalRevenue = 0;

                    for (const key in response.data.subtypes_revenues) {
                        labels.push(key)
                        values.push(response.data.subtypes_revenues[key])
                        totalRevenue += response.data.subtypes_revenues[key]
                    }

                    obj.revenueChart = {
                        data:[
                            {
                                values: values,
                                labels: labels,
                                type: 'pie'
                            }
                        ],
                        layout:{
                            title: "Venituri"
                        }
                    }
                    obj.revenue = totalRevenue;
                    obj.cards[0].amount = totalRevenue + " Lei";
                    var profit = totalRevenue - this.expenses;
                    var profitMargin = Math.round((profit / totalRevenue) * 100)
                    if(totalRevenue == 0){
                        this.cards[2].amount = "0 Lei"
                    } else {
                        this.cards[2].amount = profit + " Lei(" + profitMargin + "%)";
                    }
                }
            )
            .catch(error => {
                console.log(error);
            })
        },
    }
}
</script>

<style scoped>
.tablediv{
    margin-top: 24px;
    width: 70%;
    margin-left: 15%;
    margin-bottom: 24px;
}
@media screen and (max-width: 600px) {
    .tablediv{
        margin-top: 24px;
        width: 98%;
        margin-left: 1%;
        margin-bottom: 24px;
    }
}
</style>