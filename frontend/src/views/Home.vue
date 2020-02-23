<template>
  <div class="home ui stackable grid">
    <div class="sixteen wide column custom-padding">
      <GearRandomizer />
    </div>
    <div class="sixteen wide column custom-padding">
      <MonsterRandomizer />
    </div>
    <div class="sixteen wide column custom-padding">
      <InventoryRandomizer />
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import GearRandomizer from '@/components/GearRandomizer/GearRandomizer.vue';
import MonsterRandomizer from '@/components/MonsterRandomizer/MonsterRandomizer.vue';
import InventoryRandomizer from '@/components/InventoryRandomizer/InventoryRandomizer.vue';

export default {
  name: 'Home',
  components: {
    GearRandomizer,
    MonsterRandomizer,
    InventoryRandomizer
  },
};
</script>
<style scoped>
.custom-padding {
  padding: 0.1rem;
  margin: 0;
}
</style>
