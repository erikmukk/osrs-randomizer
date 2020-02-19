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
        item: Array
    },
    computed: {
        monsterName () {
            return this.item[0].Name;
        },
        monsterImage () {
            return this.item[0].wiki_image_url;
        },
        monsterWikiUrl () {
            console.log(this.item[0].wiki_url)
            return this.item[0].wiki_url
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