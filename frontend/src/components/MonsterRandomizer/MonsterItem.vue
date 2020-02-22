<template>
    <div>
        Your monster is: <strong>{{monsterName}}</strong>
        <br/>
        <a :href="monsterWikiUrl" target="_blank">
        <img class="monster-image" :src="monsterImage" >
        </a>
    </div>    
</template>

<script>
export default {
    name: 'MonsterItem',
    props: {
        item: Object
    },
    computed: {
        monsterName () {
            return this.item.Name;
        },
        monsterImage () {
            return this.item.wiki_image_url;
        },
        monsterWikiUrl () {
            return this.item.wiki_url
        }
    }
}
</script>

<style scoped lang="scss">
.monster-image {
    height: 100px;
    width: auto;
}
</style>