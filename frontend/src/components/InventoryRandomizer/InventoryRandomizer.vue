<template>
    <div class="ui segment center aligned stackable grid no-margin custom-padding">
        <div class="sixteen wide column no-margin">
            <h3>Step 3. Get an inventory setup</h3>
        </div>
        <div class="inventory-randomizer four wide column">
            <div>
                <!--<template v-for="(item, index) in currentInv">
                    <img :key="index"
                        class='svg-item' 
                        :src="`data:image/jpeg;base64,${item.base64_icon}`" 
                        alt="Equipment icon"
                    >
                </template>-->
                <Inventory :items="currentInv" />  
                <button class="ui secondary button" @click.prevent=randomize>
                    Randomize
                </button>
            </div>
            <div v-if="randomizerLoading" class="loader-div">
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
        <div class="inventory-randomizer-extras eight wide column">
            <InventoryRandomizerConstraints @constraintsChanged="handleConstraintsChanged"/>
        </div>    
    </div>
</template>

<script>
import Inventory from './Inventory';
import InventoryRandomizerConstraints from './InventoryRandomizerConstraints'
export default {
    name: 'InventoryRandomizer',
    components: {
        Inventory,
        InventoryRandomizerConstraints
    },
    data () {
        return {
            currentInv: [],
            randomizerLoading: false,
            loadingText: '',
            inventoryConstraints: ''
        }
    },
    methods: {
        resetCurrentInv () {
            this.currentMonster = [];
            this.randomizerLoading = true;
            this.loadingText = 'Fetching new inventory for you';
        },
        randomize () {
            this.resetCurrentInv();
            fetch(`http://localhost:5000/full_inventory?${this.makeQueryString()}`)
            .then(resp => {
                return resp.json();
            })
            .then(resp => {
                this.currentInv = resp;
            })
            .catch(err => {
                console.log(err)
            })
            .then(() => {
                this.randomizerLoading = false;
            })
        },
        handleConstraintsChanged (form) {
            this.inventoryConstraints = form;
        },
        makeQueryString () {
            if (this.inventoryConstraints !== '') {
                let qString = '&'
                Object.keys(this.inventoryConstraints).map((key, index) => {
                qString += `${key}=${this.inventoryConstraints[key]}&`
                })
                return qString;
            }
            return ''
        }
    },
}
</script>

<style scoped lang="scss">
.column {
  margin-bottom: 10px
}
.no-margin {
  margin: 0 !important;
}
.custom-padding {
  padding: 0.1rem;
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