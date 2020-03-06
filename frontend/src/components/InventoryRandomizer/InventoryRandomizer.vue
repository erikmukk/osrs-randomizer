<template>
    <div class="ui segment center aligned stackable grid custom">
        <div class="sixteen wide column no-margin">
            <h3>Step 3. Get an inventory setup</h3>
        </div>
        <div class="inventory-randomizer four wide column">
            <div>
                <Inventory :items="allItems" />
                <button class="ui secondary button" @click.prevent=randomize>
                    Randomize
                </button>
            </div>
            <div v-if="isLoading" class="loader-div">
                <div class="ui active inverted dimmer">
                    <div class="ui loader">
                        <br/>
                        <br/>
                        <br/>
                        {{loadingText}}
                    </div>
                </div>
            </div>
        </div>
        <div class="inventory-randomizer-extras nine wide column">
            <InventoryRandomizerConstraints @constraintsChanged="handleConstraintsChanged"/>
        </div>
    </div>
</template>

<script>
import Inventory from './Inventory';
import InventoryRandomizerConstraints from './InventoryRandomizerConstraints';
import {mapGetters} from 'vuex';

export default {
    name: 'InventoryRandomizer',
    components: {
        Inventory,
        InventoryRandomizerConstraints
    },
    data () {
        return {
            loadingText: '',
            inventoryConstraints: ''
        }
    },
    computed: {
        ...mapGetters({
            allItems: 'inventory/allItems',
            isLoading: 'inventory/isLoading',
            monsterIsPoisonous: 'monster/isPoisonous'
        })
    },
    methods: {
        randomize () {
            this.loadingText = 'Fetching new inventory for you'
            this.$store.dispatch('inventory/getAllInventory', this.inventoryConstraints)
        },
        handleConstraintsChanged (form) {
            this.inventoryConstraints = form;
        }
    },
}
</script>

<style scoped lang="scss">
.column {
  margin-bottom: 10px
}
.custom {
  background: #f6f6f4;
}
.inventory-randomizer {
  text-align: center;
  min-height: 191px;
  min-width: 240px
}
.inventory-randomizer-extras {
  text-align: center;
}
.ui.loader {
  min-width: 400px;
  max-width: 100%;
}
</style>
