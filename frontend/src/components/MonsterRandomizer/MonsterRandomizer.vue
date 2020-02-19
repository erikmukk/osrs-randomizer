<template>
    <div class="ui segment center aligned grid ">
        <div class="monster-randomizer four wide column">
            <strong>Get a random monster to fight!</strong>
            <MonsterItem v-if="currentMonster" :item="currentMonster" />
            <div>
                <button class="ui button primary" @click.prevent=randomize>
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
        <div class="monster-randomizer-extras six wide column">
            Monster randomizer constraints
        </div>    
    </div>
</template>

<script>
import MonsterItem from '@/components/MonsterRandomizer/MonsterItem.vue';

export default {
    name: 'MonsterRandomizer',
    components: {
        MonsterItem
    },
    data () {
        return {
            currentMonster: null,
            randomizerLoading: false,
            loadingText: '',
        }
    },
    methods: {
        resetCurrentMonster () {
            this.currentMonster = null;
            this.randomizerLoading = true;
            this.loadingText = 'Fetching a new monster for you';
        },
        randomize () {
            this.resetCurrentMonster();
            fetch('http://localhost:5000/one_monster')
            .then(resp => {
                return resp.json();
            })
            .then(resp => {
                this.currentMonster = resp;
            })
            .catch(err => {
                console.log(err)
            })
            .then(() => {
                this.randomizerLoading = false;
            })
        },
    },
}
</script>

<style scoped lang="scss">
.monster-randomizer {
  border: 1px solid black;
  text-align: center;
  min-height: 191px;
}
.monster-randomizer-extras {
  border: 1px solid black;
  text-align: center;
}
.ui.loader {
  min-width: 400px;
  max-width: 100%;
}
</style>