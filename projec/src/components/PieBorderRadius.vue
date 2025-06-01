<template>
  <div>
  <div style="text-align: center; font-size: 18px">道路流量占比</div>
  <!-- <div>【道路流量占比】</div> -->
  <div ref="container" class="w-full h-full" style="transform: translateY(-4vh)"></div>
  </div>
</template>

<script setup>
import * as echarts from 'echarts'
import {onMounted, ref} from "vue";

let option;
let mChart = null
const container = ref(null)

onMounted(() => {
  mChart = echarts.init(container.value, null, {
    renderer: 'canvas',
    useDirtyRect: false
  })
  renderChart()
  window.addEventListener('resize', mChart.resize);
})
const trafficVolumes = [
  // Data for 2019
[
    { name: 'G4', value: 5800 },
    { name: 'G2', value: 4700 },
    { name: 'G15', value: 3900 },
    { name: 'G25', value: 3500 },
    { name: 'G30', value: 3200 },
    { name: 'G42', value: 3100 },
    { name: 'G50', value: 2950 },
    { name: 'G55', value: 2800 },
    { name: 'G3', value: 2700 },
    { name: 'G7', value: 2600 }
  ],
  // Data for 2020
   [
    { name: 'G4', value: 6200 },
    { name: 'G2', value: 5100 },
    { name: 'G15', value: 4200 },
    { name: 'G25', value: 3800 },
    { name: 'G30', value: 3400 },
    { name: 'G42', value: 3300 },
    { name: 'G50', value: 3050 },
    { name: 'G55', value: 2900 },
    { name: 'G3', value: 2750 },
    { name: 'G7', value: 2650 }
  ],
  // Data for 2021
 [
    { name: 'G4', value: 6700 },
    { name: 'G2', value: 5300 },
    { name: 'G15', value: 4300 },
    { name: 'G25', value: 3900 },
    { name: 'G30', value: 3500 },
    { name: 'G42', value: 3400 },
    { name: 'G50', value: 3200 },
    { name: 'G55', value: 3000 },
    { name: 'G3', value: 2800 },
    { name: 'G7', value: 2700 }
  ]
];

const renderChart = () => {
  option = {
    baseOption:{
      timeline: {
        // 时间轴的配置
        show: false,
        axisType: 'category',
        // 时间轴自动播放
        autoPlay: true,
        // 播放时间间隔，单位毫秒
        playInterval: 3500,
        // 数据
        data: Object.keys(trafficVolumes),
      },
      tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      show: false,
      // textStyle:{
      //   color:'white'
      // }
    },
    },
    options:[]
    // series: [
    //   {
    //     name: 'Access From',
    //     type: 'pie',
    //     radius: '50%',
    //     data: [
    //       { value: 1048, name: 'Search Engine' },
    //       { value: 735, name: 'Direct' },
    //       { value: 580, name: 'Email' },
    //       { value: 484, name: 'Union Ads' },
    //       { value: 300, name: 'Video Ads' }
    //     ],
    //     emphasis: {
    //       itemStyle: {
    //         shadowBlur: 5,
    //         shadowOffsetX: 0,
    //         shadowColor: 'rgba(0, 0, 0, 0.5)'
    //       }
    //     }
    //   }
    // ]
    
  };
  trafficVolumes.map((item)=>{
       option.options.push({
          series: [
      {
        name: 'Access From',
        type: 'pie',
        radius: '50%',
        data: item.map(item=>({
          name: item.name,
          value: item.value,
          textStyle:{
            color:'white'
          }
        })),
        emphasis: {
          itemStyle: {
            shadowBlur: 5,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
       })
     })

  if (option && typeof option === 'object') {
    mChart.setOption(option);
  }

}
</script>

<style scoped lang="scss">

</style>