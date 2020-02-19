<template>
  <div class="home">
    <GearRandomizer />
    <MonsterRandomizer />
  </div>
</template>

<script>
// @ is an alias to /src
import GearRandomizer from '@/components/GearRandomizer/GearRandomizer.vue';
import MonsterRandomizer from '@/components/MonsterRandomizer/MonsterRandomizer.vue';

export default {
  name: 'Home',
  components: {
    GearRandomizer,
    MonsterRandomizer
  },
};
</script>
<style scoped>
.home {
  background-color: #e0e3dc !important;
}
</style>
