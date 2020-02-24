import Vue from 'vue';
import Vuex from 'vuex';
import gear from './gear';
import inventory from './inventory';
import monster from './monster';
import application from './application'

Vue.use(Vuex);

const config = {
    modules: {
        gear: gear,
        inventory: inventory,
        monster: monster,
        application: application
    },
    state: {

    },
    mutations: {

    },
    actions: {
        
    }
}

export default new Vuex.Store(config)