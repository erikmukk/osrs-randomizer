<template>
    <div>
        <div class="inventory">
            <template v-for="(item, index) in items">
                <InventorySlot :key="index" :item="item" :index="index" :class="rowIndex(index)"  />
            </template>
        </div>
    </div>    
</template>

<script>
import InventorySlot from './InventorySlot'
export default {
    name: "Inventory",
    components: {
        InventorySlot
    },
    props: {
        items: Array
    },
    methods: {
        rowIndex (index) {
            return `class_${Math.ceil((index + 1) / 4)}`
        }
    }
}
</script>

<style scoped lang="scss">
.class_1 {
    position: absolute;
}
.class_2 {
    position: absolute;
}
.class_3 {
    position: absolute;
}
.class_4 {
    position: absolute;
}
.class_5 {
    position: absolute;
}
.class_6 {
    position: absolute;
}
.class_7 {
    position: absolute;
}
.inventory {
    background: url('https://i.imgur.com/UombFb0.png') no-repeat;
    position: relative;
    display: inline-block;
    height: 271px;
    width: 198px;
    
}
</style>