<template>
    <div>
     <div ref="container" class="w-full h-full"></div>
      <div style="text-align: center; font-size: 15px; transform: translateY(-10vh)" >{{ props.name }}</div>
    </div>
 </template>
 
 <script setup>
   import * as echarts from 'echarts'
   import {onMounted, ref} from "vue";
 
   let mChart = null
   let option;
   const container = ref(null)
 
   const props = defineProps({
     name: {
       typeof: String,
       required: true,
     }
   })
 
   const flowData = [
       {name: '', value: 90},
       {name: '', value: 60},
       {name: '', value: 100}
   ]
 
   onMounted(() => {
     mChart = echarts.init(container.value, null, {
       renderer: 'canvas',
       useDirtyRect: false
     })
     renderChart()
     if (option && typeof option === 'object') {
       mChart.setOption(option);
     }
     window.addEventListener('resize', mChart.resize);
   })
   // const data = 
   const renderChart = () => {
     option = {
       baseOption:{
         timeline:{
         show: false,
         axisType: 'category',
         // 时间轴自动播放
         autoPlay: true,
         // 播放时间间隔，单位毫秒
         playInterval: 3500,
         // 数据
         data: Object.keys(flowData)
       },
         tooltip: {
         formatter: 'flow'
       },
       },
       options: []
     };
     flowData.map((item)=>{
       option.options.push({
         series: [
         {
           name: 'flow',
           min:0,
           max:250,
           type: 'gauge',
           legend: {
             textStyle:{
               color:"#8DB6DB"
             }
           },
           progress: {
             show: true
           },
           detail: {
             valueAnimation: true,
             formatter: '{value}'
           },
           data: [item],
           axisLabel:{
             fontSize: 0
           },
 
         }
       ]
       })
     })
     mChart.setOption(option)
   }
 </script>
 
 <style scoped lang="scss">
 
 </style>