<template>
    <div class="ui segment center aligned stackable grid no-margin">
        <div class="sixteen wide column no-margin">
            <h3>Step 2. Get a monster to fight</h3>
        </div>
        <div class="monster-randomizer four wide column">
            <MonsterItem v-if="currentMonster" :item="currentMonster" />
            <div>
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
        <div class="monster-randomizer-extras eight wide column">
            <MonsterRandomizerConstraints @constraintsChanged="handleConstraintsChanged"/>
        </div>    
    </div>
</template>

<script>
import MonsterItem from '@/components/MonsterRandomizer/MonsterItem.vue';
import MonsterRandomizerConstraints from './MonsterRandomizerConstraints'

export default {
    name: 'MonsterRandomizer',
    components: {
        MonsterItem,
        MonsterRandomizerConstraints
    },
    data () {
        return {
            currentMonster: null,
            randomizerLoading: false,
            loadingText: '',
            monsterContstraints: ''
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
            fetch(`${process.env.VUE_APP_API_URL}?${this.makeQueryString()}`)
            .then(resp => {
                return resp.json();
            })
            .then(resp => {
                this.currentMonster = resp;
            })
            .catch(err => {
            })
            .then(() => {
                this.randomizerLoading = false;
            })
        },
        handleConstraintsChanged (form) {
            this.monsterContstraints = form
        },
        makeQueryString () {
            if (this.monsterContstraints !== '') {
                let qString = '&'
                Object.keys(this.monsterContstraints).map((key, index) => {
                qString += `${key}=${this.monsterContstraints[key]}&`
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
.monster-randomizer {
  text-align: center;
  min-height: 210px;
  min-width: 240px;
}
.monster-randomizer-extras {
  text-align: center;
}
.ui.loader {
  min-width: 400px;
  max-width: 100%;
}
</style>