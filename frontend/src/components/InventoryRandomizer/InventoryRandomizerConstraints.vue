<template>
    <div class="combat-stats ui stackable centered grid">
        <form class="ui form">
            <div class="field">
                <label>Number of potions (0-{{remainingPots}})</label>
                <input 
                v-model="form.nrOfPots" 
                type="number" 
                name="nrOfPots" 
                placeholder="# potions"
                @blur="checkValueOnBlur('nrOfPots', $event)"
                >
            </div>
            <div class="field">
                <label>Number of food items (0-{{remainingFood}})</label>
                <input 
                v-model="form.nrOfFood" 
                type="number" 
                name="nrOfFood" 
                placeholder="# food"
                @blur="checkValueOnBlur('nrOfFood', $event)"
                >
            </div>
        </form>
    </div>    
    
</template>

<script>
export default {
    name: 'InventoryRandomizerConstraints',
    data () {
        return {
            form: {
                nrOfFood: 22,
                nrOfPots: 6
            }
        }
    },
    computed: {
        remainingPots () {
            return 28 - this.form.nrOfFood
        },
        remainingFood () {
            return 28 - this.form.nrOfPots
        }
    },
    methods: {
        checkValueOnBlur (type, e) {
            const value = e.target.valueAsNumber
            if (value < 1 || isNaN(value)) {
                this.form[type] = 0
            }
            let remaining = this.remainingPots;
            if (type === 'nrOfFood') {
                remaining = this.remainingFood
            }
            if (value > remaining) {
                this.form[type] = remaining
            }
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