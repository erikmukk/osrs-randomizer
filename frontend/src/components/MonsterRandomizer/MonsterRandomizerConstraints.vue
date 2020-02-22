<template>
    <div class="combat-stats ui stackable centered grid">
        <form class="ui form">
            <div class="ui checkbox">
                <input 
                v-model="form.onlyBosses" 
                type="checkbox" 
                name="onlyBosses" 
                @change="checkboxChanged('onlyBosses', $event)"
                >
                <label>Bosses only?</label>
            </div>
        </form>
    </div>    
</template>

<script>
export default {
    name: 'MonsterRandomizerConstraints',
    data () {
        return {
            form: {
                onlyBosses: false
            }
        }
    },
    methods: {
        checkboxChanged (name, event) {
            this.$emit('constraintsChanged', this.form)
        }
    },
    mounted () {
        this.$emit('constraintsChanged', this.form)
    }
}
</script>

<style scoped lang="scss">

</style>