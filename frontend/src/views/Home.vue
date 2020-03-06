<template>
  <div class="home ui stackable grid">
    <div v-if="!isNewVersion" class="sixteen wide column">
      <div class="sixteen wide column">
        <GearRandomizer />
      </div>
      <div class="sixteen wide column">
        <MonsterRandomizer />
      </div>
      <div class="sixteen wide column">
        <InventoryRandomizer />
      </div>
    </div>  
    <div v-else class="sixteen wide column">
      <carousel 
        :perPage=1 
      >
        <slide>
          <GearRandomizer />
        </slide>
        <slide>
          <MonsterRandomizer />
        </slide>
        <slide>
          <InventoryRandomizer />
        </slide>
      </carousel>  
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import GearRandomizer from '@/components/GearRandomizer/GearRandomizer.vue';
import MonsterRandomizer from '@/components/MonsterRandomizer/MonsterRandomizer.vue';
import InventoryRandomizer from '@/components/InventoryRandomizer/InventoryRandomizer.vue';
import {mapGetters} from 'vuex';
import {Carousel, Slide} from 'vue-carousel';

export default {
  name: 'Home',
  components: {
    GearRandomizer,
    MonsterRandomizer,
    InventoryRandomizer,
    Slide,
    Carousel
  },
  computed: {
    ...mapGetters({
      isNewVersion: 'application/isNewVersion'
    })
  }
};
</script>
<style scoped>
.VueCarousel {
  width: inherit
}
</style>
