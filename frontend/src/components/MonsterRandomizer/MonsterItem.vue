<template>
    <div v-if="!isEmpty" class="min-height">
        Your monster is:
        <br/>
        <strong>{{monsterName}}</strong>
        <span v-if="poisonous">
          <img :src="poisonHitsplat" alt="Poison hitsplat"/>
        </span>
        <span v-if="dragonfire">
          <img :src="dragonfireSign" alt="Dragonfire sign"/>
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
        poisonous: Boolean,
        dragonfire: Boolean
    },
    data () {
      return {
        poisonHitsplat: 'data:image/webp;base64,UklGRp4AAABXRUJQVlA4TJIAAAAvF4AFEB8gECBTYnRIETH/gWpwY9vW8dx/re+l1q9oLk5t1jZHk9ruPRlX6flzEBH9L4KVB6LwgWN+FiIi4hhROMLxufwwD+toschbcdm+xAF7KmeLEH0rigu+p6LUCSNFyYM3zMymp6K0yXtRlDqEsaK4WGj+P7m8KOwWghfCvGplPqqO/PD5hChx0SSIB3gfAQ==',
        dragonfireSign: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABsAAAAdCAMAAABsU+d6AAAA1VBMVEUAAAAAAAGsahapaBavaxaybRZiW1ugeRJaVFS1cBZfWVmPbBJnYF/AdhnUgRtYUVHRgBldVlZrZGRtZmamZha+dRnDeBllXl19dHS4cRa7cxbGehnJfBnLfRlNOglpYWGjZBKddhLOfxmuoqJ6Ww6BYQ5waGhJNwmgYhKZdBJ/dnbWgxu0qahDMQBQS0lTTEx+Xw6FZQ6dYBJyamqTbhJ1bGyWchKjexKwo6OxpaW1qqpTPwlDPz9NSEhVT0+JZw55cXB7c3LYhRuek5Oypqa6r669tLRNT4gNAAAAAXRSTlMAQObYZgAAAW5JREFUeNp10tdSwkAUBmC2l2w6qYAhBBAEkaKg2Ov7P5JLLmRBODO5yHz5N5OTv9HYD9DTOD3gbhgocPIBsErbdl4kkrv/ELx7nTgXGHWXsyMEb6nTsXNBYHM54ofngtRxWnaUJ1SOuk3qGgrS1PFasR0prAlBKF/+EFw5XqetUaCaqGtQ6vS0BQrXhPnzQUybHSRoR1De7OnicWdxEdImChAk7pNhTFsrUgJ9hghBOjOoZBOvHScKbTX5wtiMjrFJL44o+h6iysfUeNtlyT68lk3lzxA9+DxzpWFsM2nbkZxSOPU5oeaRJduMrQz7BN9zzolLzRhja7FSeFpx/oUpN2JzbQuRya3PHyDO/GQfux4wVtoR1Zu61xeVRqw/WLyOd38VV3pbQiojNh8MyvH6FlYVxxhTan53v9+/tSxLZzAhJCnAYfM0WaQeoY6LtNM8E9pUcKKB4C7SWBQn2wvAMAyC8EyzAQjPUa3m3S/Dsx6vZ/yMiQAAAABJRU5ErkJggg==',
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
