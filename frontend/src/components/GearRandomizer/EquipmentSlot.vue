<template>
    <div class="gear-square" :style="bgImage">
        <div v-if="item" :data-tooltip="item.Name" data-position="bottom center" @click.prevent=reroll>
            <img 
            class='svg-item' 
            v-if="svg !== ''" 
            :src="`data:image/jpeg;base64,${svg}`" 
            alt="Equipment icon"
            >
        </div>
    </div>
</template>

<script>
export default {
    name: 'EquipmentSlot',
    props: {
        image: String,
        svg: String,
        item: Object
    },
    data () {
        return {
            emptyIcon: 'https://i.imgur.com/yNwaJis.png'
        }
    },
    computed: {
        bgImage () {
            return this.svg === '' ? `background: url(${this.image}` : `background: url(${this.emptyIcon}`
        } 
    },
    methods: {
        reroll () {
            this.$emit('reroll', this.item.slot)
        }
    },
}
</script>

<style scoped lang="scss">
.gear-square {
    width: 36px;
    height: 36px;
}
.svg-item {
    left:2px;
    top: 2px;
}
</style>