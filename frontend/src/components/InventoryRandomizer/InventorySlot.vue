<template>
    <span v-if="addLinebreak" :class="className" :data-tooltip="item.name" data-position="bottom center">
    <img 
        class='svg-item' 
        :src="`data:image/jpeg;base64,${item.base64_icon}`" 
        alt="Equipment icon"
        >
    <br /></span>
    <span v-else :class="className" :data-tooltip="item.name" data-position="bottom center"><img 
        class='svg-item' 
        :src="`data:image/jpeg;base64,${item.base64_icon}`" 
        alt="Equipment icon"
        ></span>
</template>

<script>
export default {
    name: 'InventorySlot',
    props: {
        item: Object,
        index: Number
    },
    computed: {
        addLinebreak: function () {
            return (this.index + 1) % 4 === 0
        },
        className: function () {
            return `span-item row_${Math.ceil((this.index+1)/4)-1} item_${(this.index)%4}`
        }
    }
}
</script>

<style scoped lang="scss">
.span-item {
    text-align: center;
    &.row_0 {
        top: 15px;
    }
    &.row_1 {
        top: 50px;
    }
    &.row_2 {
        top: 85px;
    }
    &.row_3 {
        top: 120px;
    }
    &.row_4 {
        top: 155px;
    }
    &.row_5 {
        top: 190px;
    }
    &.row_6 {
        top: 223px;
    }
    &.item_0 {
        left: 20px;
    }
    &.item_1 {
        left: 65px;
    }
    &.item_2 {
        left: 110px;
    }
    &.item_3 {
        left: 155px;
    }
}
</style>