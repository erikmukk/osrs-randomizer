<template>
    <div class="ui stackable menu">
        <router-link class="item" to="/">OSRS Randomizer</router-link>
        <router-link class="item" to="/about">About</router-link> 
        <a class="item">
            <button class="ui secondary button" @click="changeLayout">
                Change app layout to {{isScrollable ? 'scrollable' : 'swipeable'}}
            </button>
        </a>    
      </div>
</template>

<script>
import {mapGetters} from 'vuex';
export default {
    name: 'NavBar',
    methods: {
        changeLayout () {
            this.$store.dispatch('application/changeLayout')
        }
    },
    computed: {
        ...mapGetters({
            isScrollable: 'application/isNewVersion'
        })
    }
}
</script>

<style scoped lang="scss">

</style>