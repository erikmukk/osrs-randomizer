<template>
  <div class="ui segment center aligned grid">
    <div class="gear-randomizer four wide column">
      <strong>Your gear setup</strong>
      <br/>
      <br/>
      <div class="gear-model">
        <EquipmentSlot class="gear-slot" id="ammo" :image="ammo_img" :svg="ammo_svg" :item="ammo_item" @reroll=reroll />
        <EquipmentSlot class="gear-slot" id="body" :image="body_img" :svg="body_svg" :item="body_item" @reroll=reroll />
        <EquipmentSlot class="gear-slot" id="cape" :image="cape_img" :svg="cape_svg" :item="cape_item" @reroll=reroll />
        <EquipmentSlot class="gear-slot" id="feet" :image="feet_img" :svg="feet_svg" :item="feet_item" @reroll=reroll />
        <EquipmentSlot class="gear-slot" id="hands" :image="hands_img" :svg="hands_svg" :item="hands_item" @reroll=reroll />
        <EquipmentSlot class="gear-slot" id="head" :image="head_img" :svg="head_svg" :item="head_item" @reroll=reroll />
        <EquipmentSlot class="gear-slot" id="legs" :image="legs_img" :svg="legs_svg" :item="legs_item" @reroll=reroll />
        <EquipmentSlot class="gear-slot" id="neck" :image="neck_img" :svg="neck_svg" :item="neck_item" @reroll=reroll />
        <EquipmentSlot class="gear-slot" id="ring" :image="ring_img" :svg="ring_svg" :item="ring_item" @reroll=reroll />
        <EquipmentSlot class="gear-slot" id="shield" :image="shield_img" :svg="shield_svg" :item="shield_item" @reroll=reroll />
        <EquipmentSlot class="gear-slot" id="weapon" :image="weapon_img" :svg="weapon_svg" :item="weapon_item" @reroll=reroll />
      </div>
      <div>
      <button class="ui primary button randomize-button" @click.prevent=randomize>Randomize</button>
      </div>
      <div v-if="randomizerLoading" class="loader-div">
        <div class="ui active inverted dimmer">
          <div class="ui loader">
            <br/>
            <br/>
            <br/>
            {{loadingText}}
          </div>
        </div>
      </div>  
    </div>
    <div class="gear-randomizer-extras six wide column"> 
      <div class="ui grid">
        <div class="eight wide column">
          <GearRandomizerExtras @lvlChanged="handleLvLChanged" />
        </div> 
        <div class="eight wide column">
          Place for additional params
        </div> 
      </div>
    </div>
  </div>
</template>

<script>
import EquipmentSlot from '@/components/GearRandomizer/EquipmentSlot.vue';
import GearRandomizerExtras from '@/components/GearRandomizer/GearRandomizerExtras.vue'

export default {
  name: 'GearRandomizer',
  components: {
    EquipmentSlot,
    GearRandomizerExtras
  },
  data () {
    return {
      ammo_img: 'https://i.imgur.com/r7jVJCd.png',
      body_img: 'https://i.imgur.com/1AQRpRe.png',
      cape_img: 'https://i.imgur.com/UCOnj2K.png',
      feet_img: 'https://i.imgur.com/IqE5e6m.png',
      hands_img: 'https://i.imgur.com/1dEk8Qy.png',
      head_img: 'https://i.imgur.com/0MLEcDT.png',
      legs_img: 'https://i.imgur.com/mgr1lfU.png',
      neck_img: 'https://i.imgur.com/qpWuL49.png',
      ring_img: 'https://i.imgur.com/aWocZG8.png',
      shield_img: 'https://i.imgur.com/1iMnkRD.png',
      weapon_img: 'https://i.imgur.com/TnPm0hi.png',
      bg_img: 'https://i.imgur.com/JgjetaQ.png',
      ammo_svg : '',
      body_svg: '',
      cape_svg: '',
      feet_svg: '',
      hands_svg: '',
      head_svg: '',
      legs_svg: '',
      neck_svg: '',
      ring_svg: '',
      shield_svg: '',
      weapon_svg:'',
      ammo_item : null,
      body_item: null,
      cape_item: null,
      feet_item: null,
      hands_item: null,
      head_item: null,
      legs_item: null,
      neck_item: null,
      ring_item: null,
      shield_item: null,
      weapon_item:null,
      randomizerLoading: false,
      loadingText: '',
      gearConstraints: ''
    }
  },
  methods: {
    handleLvLChanged (form) {
      this.gearConstraints = form;
    },
    setItem (equipmentItem) {
      switch (equipmentItem.slot) {
        case 'ammo':
          this.ammo_svg = equipmentItem.base64_icon;
          this.ammo_item = equipmentItem;
          break;
        case 'body':  
           this.body_svg = equipmentItem.base64_icon;
           this.body_item = equipmentItem;
           break;
        case 'cape':
          this.cape_svg = equipmentItem.base64_icon;
          this.cape_item = equipmentItem;
          break;
        case 'feet':
          this.feet_svg = equipmentItem.base64_icon;
          this.feet_item = equipmentItem;
          break;
        case 'hands':
          this.hands_svg = equipmentItem.base64_icon;
          this.hands_item = equipmentItem;
          break;
        case 'head':
          this.head_svg = equipmentItem.base64_icon;
          this.head_item = equipmentItem;
          break;
        case 'legs':
          this.legs_svg = equipmentItem.base64_icon;
          this.legs_item = equipmentItem;
          break;
        case 'neck':
          this.neck_svg = equipmentItem.base64_icon;
          this.neck_item = equipmentItem;
          break;
        case 'ring':
          this.ring_svg = equipmentItem.base64_icon;
          this.ring_item = equipmentItem;
          break;
        case 'shield':
          this.shield_svg = equipmentItem.base64_icon;
          this.shield_item = equipmentItem;
          break;
        case 'weapon':
        case '2h':  
          this.weapon_svg = equipmentItem.base64_icon;  
          this.weapon_item = equipmentItem;
          break;
      }
    },
    reroll (slot) {
      this.loadingText = `Looking for a new item for '${slot}' slot`
      this.randomizerLoading = true
      fetch(`http://localhost:5000/one_in_slot?slot=${slot}${this.makeQueryString()}`)
      .then(resp => {
        return resp.json();
      })
      .then(resp => {
        const equipmentItem = resp[0];
        this.setItem(equipmentItem);
      })
      .catch(err => {
        console.log(err)
      })
      .then(() => {
        this.randomizerLoading = false
      })
    },
    randomize () {
      this.resetSvg();
      this.loadingText = 'Randomizing your gear setup'
      this.randomizerLoading = true;
      fetch(`http://localhost:5000/full_gear?${this.makeQueryString()}`)
      .then(resp => {
        return resp.json();
      })
      .then(resp => {
        resp.forEach(item => {
          const equipmentItem = item[0];
          this.setItem(equipmentItem);
        })
      })
      .catch(err => {
        console.log(err);
      })
      .then(() => {
       this.randomizerLoading = false;
      })
    },
    resetSvg () {
      this.ammo_svg = '';
      this.body_svg = '';
      this.cape_svg = '';
      this.feet_svg = '';
      this.hands_svg = '';
      this.head_svg = '';
      this.legs_svg = '';
      this.neck_svg = '';
      this.ring_svg = '';
      this.shield_svg = '';
      this.weapon_svg ='';
      this.ammo_item = null;
      this.body_item = null;
      this.cape_item = null;
      this.feet_item = null;
      this.hands_item = null;
      this.head_item = null;
      this.legs_item = null;
      this.neck_item = null;
      this.ring_item = null;
      this.shield_item = null;
      this.weapon_item =null;
    },
    makeQueryString () {
      if (this.gearConstraints !== '') {
        let qString = '&'
        Object.keys(this.gearConstraints).map((key, index) => {
          qString += `${key}=${this.gearConstraints[key]}&`
        })
        return qString;
      }
      return ''
    }
  },
};
</script>

<style scoped lang="scss">
.randomize-button {
  margin-top: 10px;
}
.ui.loader {
  min-width: 400px;
  max-width: 100%;
}
.gear-randomizer {
  border: 1px solid black;
  text-align: center;
}
.gear-randomizer-extras {
  border: 1px solid black;
  text-align: center;
}
.gear-model {
  position: relative;
  display: inline-block;
  background: url('https://i.imgur.com/JgjetaQ.png') no-repeat;
  height: 194px;
  width: 148px;
}
.gear-slot {
  position: absolute;
  cursor: pointer;
}
#ammo {
  top: 39px;
  left: 97px;
}
#body {
  top: 78px;
  left: 56px;
}
#cape {
  top: 39px;
  left: 15px;
}
#feet {
  top: 158px;
  left: 56px;
}
#hands {
  top: 158px;
  left: 0px;
}
#head {
  left: 56px;
}
#legs {
  top: 118px;
  left: 56px;
}
#neck {
  top: 39px;
  left: 56px;
}
#ring {
  top: 158px;
  left: 112px;
}
#shield {
  top: 78px;
  left: 112px;
}
#weapon {
  top: 78px;
  left: 0px;
}
</style>
