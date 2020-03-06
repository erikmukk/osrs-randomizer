<template>
    <div class="combat-stats ui stackable centered grid">
        <form class="ui form">
            <button class="ui secondary button" @click.prevent="resetConstraints">
                Reset constraints
            </button>
            <div class="grouped fields">
                <div class="field">
                    <div class="ui radio checkbox">
                        <input
                        v-model="form.monsterConstraint"
                        type="radio"
                        name="onlyBosses"
                        @change="checkboxChanged('onlyBosses', $event)"
                        value="bossesOnly"
                        >
                        <label>Bosses only?</label>
                    </div>
                </div>
                <div class="field">
                    <div class="ui radio checkbox">
                        <input
                        v-model="form.monsterConstraint"
                        type="radio"
                        name="slayerOnly"
                        value="slayerOnly"
                        @change="checkboxChanged('slayerOnly', $event)"
                        >
                        <label>Slayer monsters only?</label>
                    </div>
                </div>
            </div>
            <div class="inline field">
                <label>Maximum level</label>
                <input
                  class="max-width-input"
                  v-model="form.maxLvl"
                  type="number"
                  name="maxLvl"
                  placeholder="Maximum lvl"
                  @blur="checkValueOnBlur('maxLvl', $event)"
                >
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
                monsterConstraint: false,
                maxLvl: 9999
            }
        }
    },
    methods: {
        checkboxChanged (name, event) {
            this.$emit('constraintsChanged', this.form);
        },
        resetConstraints () {
            this.form.monsterConstraint = false;
            this.form.maxLvl = 9999;
            this.$emit('constraintsChanged', this.form);
        },
        checkValueOnBlur (type, e) {
            const value = e.target.valueAsNumber;
            if (value < 1 || isNaN(value)) {
                this.form[type] = 1;
            } else if (value > 9999) {
              this.form[type] = 9999
            }
            this.$emit('constraintsChanged', this.form);
        }
    },
    mounted () {
        this.$emit('constraintsChanged', this.form);
    }
}
</script>

<style scoped lang="scss">
form {
  text-align: left;
}
.max-width-input {
  max-width: 80px;
}
</style>
