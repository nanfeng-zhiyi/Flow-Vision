<!-- 环形图 -->
<template>
  <div>
    <div>【主干道流量占比图】</div>
    <div ref="target" class="w-full h-full"></div>
  </div>
</template>
<script setup>
  import { ref, onMounted, watch } from 'vue'
  import * as echarts from 'echarts'

  const props = defineProps({
    data: {
      typeof: Object,
      required: true,
    }
  })

  // 1. 初始化 echarts 实例
  let mChart = null
  const target = ref(null)

  onMounted(() => {
    mChart = echarts.init(target.value)
    renderChart()
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

  const getSeriesData = () => {
    const series = []
    trafficVolumes.forEach((item, index) => {
      // 上层
      series.push({
        name: item[0].name,
        type: 'pie',
        clockWise: false,
        hoverAnimation: false,
        radius: [73 - index * 15 + '%', 68 - index * 15 + '%'],
        center: ['55%', '55%'],
        label: {
          show: false,
        },
        data: [
          {
            value: item[0].value,
            name: item[0].name
          }, {
            value: 1000,
            itemStyle: {
              color: 'rgba(0,0,0,0)',
              borderWidth: 0,
            },
            tooltip: {
              show: false
            },
            hoverAnimation: false
          }
        ]
      })
      // 底层
      series.push({
        name: item.map(item=>item.name),
        type: 'pie',
        silent: true,
        z: 1,
        clockWise: false,
        hoverAnimation: false,
        radius: [73 - index * 15 + '%', 68 - index * 15 + '%'],
        center: ['55%', '55%'],
        label: {
          show: false,
        },
        data: [
          {
            value: 7.5,
            itemStyle: {
              color: 'rgba(3,31,62)',
              borderWidth: 0,
            },
            tooltip: {
              show: false,
            },
            hoverAnimation: false
          }, {
            value: 2.5,
            itemStyle: {
              color: 'rgba(0,0,0,0)',
              borderWidth: 0,
            },
            tooltip: {
              show: false,
            },
            hoverAnimation: false
          }
        ]
      })
    })
    return series
  }

  // 2. 构建 option 配置对象 
  const renderChart = () => {
    const options = {
      // 图例配置
      timeline:{
        axisType: 'category',
        autoPlay: true,
        show:false,
        playInterval: 1000,
        data: trafficVolumes.map(item => item.name),
      },
      legend: {
        show: true,
        icon: 'circle',
        top: '14%',
        left: '60%',
        data: props.data.abnormals.map((item) => item.name),
        width: -5,
        itemWidth: 10,
        itemHeight: 10,
        itemGap: 6,
        textStyle: {
          fontSize: 12,
          lineHeight: 5,
          color: '#ffffff'
        }
      },
      // 提示层
      tooltip: {
        show: true,
        trigger: 'item',
        formatter: '{a}<br>{b}:{c}({d}%)'

      },
      // Y轴
      yAxis: [{
        type: 'category',
        inverse: true,
        axisLine: {
          show: false
        }
      }],
      // X轴
      xAxis: [{
        show: false
      }],
      // 核心配置 
      series: getSeriesData()
    }
    // 3. 通过 实例.setOptions(option)
    mChart.setOption(options)
  }

  watch(() => props.data, renderChart)

</script>
<style lang="scss" scoped>

</style>