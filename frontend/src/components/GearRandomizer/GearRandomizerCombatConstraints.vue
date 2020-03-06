<template>
    <div class="combat-stats ui stackable centered grid">
        <div class="ten wide column">
            <h4>Combat stats restrictions</h4>
            <form class="ui form grid">
              <div class="eight wide column">
                <div class="field">
                  <label>Attack</label>
                  <input
                    class="max-width-input"
                    v-model="form.att"
                    type="number"
                    name="attLevel"
                    placeholder="Attack level"
                    @input="checkValue('att', $event)"
                    @blur="checkValueOnBlur('att', $event)"
                  >
                </div>
                <div class="field">
                  <label>Strength</label>
                  <input
                    class="max-width-input"
                    v-model="form.str"
                    type="number"
                    name="strLevel"
                    placeholder="Strength level"
                    @input="checkValue('str', $event)"
                    @blur="checkValueOnBlur('str', $event)"
                  >
                </div>
                <div class="field">
                  <label>Defence</label>
                  <input
                    class="max-width-input"
                    v-model="form.def"
                    type="number"
                    name="defLevel"
                    placeholder="Defence level"
                    @input="checkValue('def', $event)"
                    @blur="checkValueOnBlur('def', $event)"
                  >
                </div>
              </div>
              <div class="eight wide column">
                <div class="field">
                  <label>Ranged</label>
                  <input
                    class="max-width-input"
                    v-model="form.ranged"
                    type="number"
                    name="rangedLevel"
                    placeholder="Ranged level"
                    @input="checkValue('ranged', $event)"
                    @blur="checkValueOnBlur('ranged', $event)"
                  >
                </div>
                <div class="field">
                  <label>Magic</label>
                  <input
                    class="max-width-input"
                    v-model="form.magic"
                    type="number"
                    name="magicLevel"
                    placeholder="Magic level"
                    @input="checkValue('magic', $event)"
                    @blur="checkValueOnBlur('magic', $event)"
                  >
                </div>
                <div class="field">
                  <label>Prayer</label>
                  <input
                    class="max-width-input"
                    v-model="form.prayer"
                    type="number"
                    name="prayerLevel"
                    placeholder="Prayer level"
                    @input="checkValue('prayer', $event)"
                    @blur="checkValueOnBlur('prayer', $event)"
                  >
                </div>
              </div>
            </form>
        </div>
        <div class="six wide column">
            <form class="ui form ">
                <div class="field">
                    <div class="ui checkbox">
                        <input
                        v-model="form.untradeables"
                        type="checkbox"
                        name="untradeables"
                        >
                        <label>Allow untradeables?</label>
                    </div>
                </div>
                <div class="field">
                    <label>Max slot price (10 000+)</label>
                    <input
                    v-model="form.maxPrice"
                    type="number"
                    name="maxPrice"
                    placeholder="Price"
                    @input="checkPrice('maxPrice', $event)"
                    @blur="checkValueOnBlur('maxPrice', $event)"
                    >
                </div>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    name: 'GearRandomizerCombatConstraints.vue',
    data () {
        return {
            form: {
                att: 99,
                str: 99,
                def: 99,
                magic: 99,
                ranged: 99,
                prayer: 99,
                untradeables: true,
                maxPrice: 100000
            }
        }
    },
    methods: {
        checkValue (lvl, e) {
            const value = e.target.valueAsNumber
            if (value > 99) {
                this.form[lvl] = 99
            }
            this.$emit('constraintsChanged', this.form)
        },
        checkPrice (price, e) {
            const value = e.target.valueAsNumber
            if (value < 10000) {
                this.form[price] = 10000
            }
            this.$emit('constraintsChanged', this.form)
        },
        checkValueOnBlur (lvl, e) {
            const value = e.target.valueAsNumber
            if (value < 1 || isNaN(value)) {
                this.form[lvl] = 1
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
.max-width-input {
  width: 60px;
}
.left-col-field {
  text-align: right;
  & label {
    float: left;
  }
}
</style>
