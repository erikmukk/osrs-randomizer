<template>
    <div v-if="!isEmpty" class="min-height">
        Your monster is: <strong>{{monsterName}}</strong>
        <span>
          <img v-if="poisonous" :src="poisonHitsplat" alt="Poison hitsplat"/>
        </span>
        <br/>
        <a :href="monsterWikiUrl" target="_blank">
        <img class="monster-image" :src="monsterImage" >
        </a>
    </div>
    <div v-else class="no-results min-height">
      <strong>No monsters found</strong>
    </div>
</template>

<script>
export default {
    name: 'MonsterItem',
    props: {
        item: Object,
        poisonous: Boolean
    },
    data () {
      return {
        poisonHitsplat: 'data:image/webp;base64,UklGRp4AAABXRUJQVlA4TJIAAAAvF4AFEB8gECBTYnRIETH/gWpwY9vW8dx/re+l1q9oLk5t1jZHk9ruPRlX6flzEBH9L4KVB6LwgWN+FiIi4hhROMLxufwwD+toschbcdm+xAF7KmeLEH0rigu+p6LUCSNFyYM3zMymp6K0yXtRlDqEsaK4WGj+P7m8KOwWghfCvGplPqqO/PD5hChx0SSIB3gfAQ=='
      }
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
        },
        isEmpty () {
          return Object.entries(this.item).length === 0
        }
    }
}
</script>

<style scoped lang="scss">
.monster-image {
    height: 100px;
    width: auto;
}
.no-results {
  color: red;
  font-size: 20px;
}
.min-height {
  min-height: 120px;
}
</style>
