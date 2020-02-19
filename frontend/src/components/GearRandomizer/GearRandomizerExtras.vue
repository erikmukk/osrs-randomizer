<template>
    <div>
        <form class="ui form">
            <div class="field">
                <label>Max attack level (1-99)</label>
                <input 
                v-model="form.att" 
                type="number" 
                name="attLevel" 
                placeholder="Attack level"
                @input="checkValue('att', $event)"
                @blur="checkValueOnBlur('att', $event)"
                >
            </div>
            <div class="field">
                <label>Max strength level (1-99)</label>
                <input 
                v-model="form.str" 
                type="number" 
                name="strLevel" 
                placeholder="Strength level"
                @input="checkValue('str', $event)"
                @blur="checkValueOnBlur('str', $event)"
                >
            </div>
            <div class="field">
                <label>Max defence level (1-99)</label>
                <input 
                v-model="form.def" 
                type="number" 
                name="defLevel" 
                placeholder="Defence level"
                @input="checkValue('def', $event)"
                @blur="checkValueOnBlur('def', $event)"
                >
            </div>
            <div class="field">
                <label>Max ranged level (1-99)</label>
                <input 
                v-model="form.ranged" 
                type="number" 
                name="rangedLevel" 
                placeholder="Ranged level"
                @input="checkValue('ranged', $event)"
                @blur="checkValueOnBlur('ranged', $event)"
                >
            </div>
            <div class="field">
                <label>Max magic level (1-99)</label>
                <input 
                v-model="form.magic" 
                type="number" 
                name="magicLevel" 
                placeholder="Magic level"
                @input="checkValue('magic', $event)"
                @blur="checkValueOnBlur('magic', $event)"
                >
            </div>
        </form>    
    </div>    
</template>

<script>
export default {
    name: 'GearRandomizerExtras',
    data () {
        return {
            form: {
                att: 99,
                str: 99,
                def: 99,
                magic: 99,
                ranged: 99
            }
        }
    },
    methods: {
        checkValue (lvl, e) {
            const value = e.target.valueAsNumber
            if (value > 99) {
                this.form[lvl] = 99
            }
            this.$emit('lvlChanged', this.form)
        },
        checkValueOnBlur (lvl, e) {
            const value = e.target.valueAsNumber
            if (value < 1 || isNaN(value)) {
                this.form[lvl] = 1
            }
            this.$emit('lvlChanged', this.form)
        }
    },
    mounted () {
        this.$emit('lvlChanged', this.form)
    }
}
</script>

<style scoped lang="scss">

</style>