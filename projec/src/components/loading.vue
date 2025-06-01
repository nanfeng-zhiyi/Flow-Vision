<template>
        <div ref="loadingcontainer" class="loading w-full h-full">
        <span>loading...</span> 
        </div>
</template>

<script setup>
import {ref } from 'vue';

const loadingcontainer = ref(null)

const props = defineProps({
  data: {
    type:Object,
    default: ()=>({isshow: true})
  }
})


// 隐藏加载遮罩
// loadingInstance.close();
// loadingInstance()

</script>

<style lang="scss" scoped>
.all{
  margin: 0;
  padding: 0;
  background-color: #34495e;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: "montserrat", sans-serif;
}

.loading {
  width: 200px;
  height: 200px;
  box-sizing: border-box;
  border-radius: 50%;
  border-top: 10px solid #e74c3c;
  position: relative;
  /* 添加动画 */
  animation: a1 2s linear infinite;
}

.loading::before,
.loading::after {
  content: "";
  width: 200px;
  height: 200px;
  /* background: red; */
  position: absolute;
  left: 0;
  top: -10px;
  box-sizing: border-box;
  border-radius: 50%;
}

.loading::before {
  border-top: 10px solid #e67e22;
  transform: rotate(120deg);
}
.loading::after {
  border-top: 10px solid #3498db;
  transform: rotate(240deg);
}

.loading span {
  position: absolute;
  width: 200px;
  height: 200px;
  color: #fff;
  text-align: center;
  line-height: 200px;
    /* 添加动画 */
  animation: a2 2s linear infinite;
}

/* 关键帧 */
@keyframes a1 { 
  to {
    transform: rotate(360deg);
  }
}
@keyframes a2 {
  to {
    transform: rotate(-360deg);
  }
}

</style>