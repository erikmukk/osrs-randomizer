<template>
    <div class="ui segment center aligned stackable grid custom">
        <div class="sixteen wide column no-margin">
            <h3>Step 2. Get a monster to fight</h3>
        </div>
        <div class="monster-randomizer four wide column">
            <MonsterItem v-if="oneMonster" :item="oneMonster" :poisonous="isPoisonous" :dragonfire="isDragonfire" />
            <div v-else class="monster-placeholder"></div>
            <div>
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
        <div class="monster-randomizer-extras eight wide column">
            <MonsterRandomizerConstraints @constraintsChanged="handleConstraintsChanged"/>
        </div>
    </div>
</template>

<script>
import MonsterItem from '@/components/MonsterRandomizer/MonsterItem.vue';
import MonsterRandomizerConstraints from './MonsterRandomizerConstraints';
import {mapGetters} from 'vuex';

export default {
    name: 'MonsterRandomizer',
    components: {
        MonsterItem,
        MonsterRandomizerConstraints
    },
    data () {
        return {
            loadingText: '',
            monsterContstraints: ''
        }
    },
    computed: {
        ...mapGetters({
            oneMonster: 'monster/oneMonster',
            isLoading: 'monster/isLoading',
            isPoisonous: 'monster/isPoisonous',
            isDragonfire: 'monster/isDragonfire'
        })
    },
    methods: {
        randomize () {
            this.loadingText = 'Fetching a new monster for you';
            this.$store.dispatch('monster/getOneMonster', this.monsterContstraints)
        },
        handleConstraintsChanged (form) {
            this.monsterContstraints = form
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
  margin-bottom: 0;
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
.monster-placeholder {
    min-height: 120px
}
</style>
