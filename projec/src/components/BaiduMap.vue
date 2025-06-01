<template>
  <!-- <button>鸟</button> -->
  <div id="container"></div>
  <div class="btn" @click="goback">返回</div>
</template>

<script setup>
import { onMounted,ref,defineProps,defineEmits } from "vue";
const props = defineProps(['maplng','maplat'])
const emits = defineEmits(['goback'])
const map = ref(null)
const goback = ()=>{
  emits('goback',false)
}
onMounted(() => {
  map.value = new BMap.Map("container");
  // 创建点坐标
  var point = new BMap.Point(props.maplng, props.maplat);
  // 初始化地图，设置中心点坐标和地图级别
  map.value.centerAndZoom(point, 15);
  map.value.addControl(new BMap.NavigationControl());    
  map.value.addControl(new BMap.ScaleControl());    
  map.value.addControl(new BMap.OverviewMapControl());    
  map.value.addControl(new BMap.MapTypeControl());    
});
</script>
<style scoped lang="scss">
html {
  height: 100%;
}
body {
  height: 100%;
  margin: 0px;
  padding: 0px;
}
#container {
  width: 100vw;
  height: 100vh;
  box-sizing: border-box;
}
.btn{
  width: 100px;
  height: 30px;
  border: 1px solid #ccc;
  text-align: center;
  line-height: 30px;
  position: fixed;
  top: 60px;
  right: 40px;
  z-index: 999;
  background: rgba(240, 128, 128, 0.442);
  cursor: pointer;
}
</style>
