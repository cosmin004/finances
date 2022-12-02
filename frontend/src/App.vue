<template>
  <v-app>
    <v-navigation-drawer
    v-model="drawer"
    temporary
    app>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="text-h6">
            <v-avatar>
              <img
                :src="require('./assets/favicon.png')"
                alt="John"
              >
            </v-avatar>
            Academia testarii
          </v-list-item-title>
          <v-list-item-subtitle>
            Finances Analytics
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>

      <v-list
        dense
        nav
      >
        <v-list-item
        v-on:click="page='stats'; drawer=false;"
        link
        >
          <v-list-item-icon>
            <v-icon>
              mdi-chart-bar
            </v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>Statistics</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item
        v-on:click="page='manage'; drawer=false;"
        link
        >
          <v-list-item-icon>
            <v-icon>
              mdi-tab
            </v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>Manage items</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <v-app-bar-nav-icon
      @click="drawer = true"
      v-if="isMobile()"
      ></v-app-bar-nav-icon>
      
      <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          :src="require('./assets/logo-academia-testarii.png')"
          transition="scale-transition"
          max-height=56
          width=170
        />
      </div>

      <v-spacer></v-spacer>
      <div
      v-if="!isMobile()"
      >
        <v-btn
          color="white"
          text
          tile
          class="my-2"
          v-on:click="page='stats'"
        >
          <v-icon
          size="24px"
          left>
            mdi-chart-bar
          </v-icon>
          Statistics
        </v-btn>

        <v-btn
          color="white"
          text
          tile
          class="my-2"
          v-on:click="page='manage'"
        >
          <v-icon
          size="24px"
          left>
            mdi-tab
          </v-icon>
          Manage items
        </v-btn>
      </div>


    </v-app-bar>

    <v-main>
      <component :is="possiblePages[page]"/>
      <!-- <manager-comp/> -->
    </v-main>
  </v-app>
</template>

<script>
import ManagerComp from './components/ManagerComp.vue';
import Dashboard from './components/Dashboard.vue';
import { isMobile } from 'mobile-device-detect';
export default {
  name: 'App',

  components: {
    ManagerComp,
    Dashboard
  },

  data: () => ({
    drawer: false,
    page: 'stats',
    possiblePages: {
      'stats': Dashboard,
      'manage': ManagerComp
    }
  }),
  methods: {
    isMobile: function() {
      return isMobile
    },
  }
};
</script>
