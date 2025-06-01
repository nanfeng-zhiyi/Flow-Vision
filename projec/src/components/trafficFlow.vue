<template>
  <div>
    <div style="text-align: center; font-size: 18px">道路流量</div>
    <div ref="target" class="w-full h-full"></div>
  </div>
</template>

<script setup>
import {onMounted, ref} from "vue"
import * as echarts from 'echarts'

let mChart = null
let target = ref(null)
onMounted(() => {
  mChart = echarts.init(target.value)
  renderChart()
})

const trafficVolumes = [
  // Data for 2019
  [
    {name: 'G4', value: 5800, color: '#d95850'},
    {name: 'G2', value: 4700, color: '#d95850'},
    {name: 'G15', value: 3900, color: '#eb8146'},
    {name: 'G25', value: 3500, color: '#eb8146'},
    {name: 'G30', value: 3200, color: '#eb8146'},
    {name: 'G42', value: 3100, color: '#eb8146'},
    {name: 'G50', value: 2950, color: '#f2d643'},
    {name: 'G55', value: 2800, color: '#f2d643'},
    {name: 'G3', value: 2700, color: '#f2d643'},
    {name: 'G7', value: 2600, color: '#f2d643'}
  ],
  // Data for 2020
  [
    {name: 'G4', value: 6200, color: '#d95850'},
    {name: 'G2', value: 5100, color: '#d95850'},
    {name: 'G15', value: 4200, color: '#d95850'},
    {name: 'G25', value: 3800, color: '#eb8146'},
    {name: 'G30', value: 3400, color: '#eb8146'},
    {name: 'G42', value: 3300, color: '#eb8146'},
    {name: 'G50', value: 3050, color: '#eb8146'},
    {name: 'G55', value: 2900, color: '#f2d643'},
    {name: 'G3', value: 2750, color: '#f2d643'},
    {name: 'G7', value: 2650, color: '#f2d643'}
  ],
  // Data for 2021
  [
    {name: 'G4', value: 6700, color: '#d95850'},
    {name: 'G2', value: 5300, color: '#d95850'},
    {name: 'G15', value: 4300, color: '#d95850'},
    {name: 'G25', value: 3900, color: '#eb8146'},
    {name: 'G30', value: 3500, color: '#eb8146'},
    {name: 'G42', value: 3400, color: '#eb8146'},
    {name: 'G50', value: 3200, color: '#eb8146'},
    {name: 'G55', value: 3000, color: '#eb8146'},
    {name: 'G3', value: 2800, color: '#f2d643'},
    {name: 'G7', value: 2700, color: '#f2d643'}
  ]
];

const renderChart = () => {
  const option = {
    baseOption: {
      timeline: {
        show: false,
        axisType: 'category',
        // 时间轴自动播放
        autoPlay: true,
        // 播放时间间隔，单位毫秒
        playInterval: 3500,
        // 数据
        data: Object.keys(trafficVolumes),
      },
      grid: {
        top: 30,
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      xAxis: {
        type: 'category',
        data: [], // 需要填充数据
        axisLabel: {
          interval: 0,
          rotate: 30,
          color: '#6c757d' // 轴标签颜色
        },
        axisLine: {
          lineStyle: {
            color: '#ced4da' // 轴线颜色
          }
        },
      },
    },
    options: []
  }
  trafficVolumes.map((item) => {
    option.options.push({
      xAxis: {
        data: item.map(item => item.name)
      },
      series: [{
        type: 'bar',
        barWidth: '60%', // 柱图宽度
        data: item.map((item => ({
          name: item.name,
          value: item.value,
          itemStyle: {
            color: item.color, // 柱颜色
            barBorderRadius: 5, // 圆角
            shadowColor: 'rgba(0,0,0,0.3)', // 阴影
            shadowBluer: 5 // 阴影模糊
          }
        }))),
      }],
      yAxis: {
        type: 'value',
        splitLine: {
          lineStyle: {
            color: '#e9ecef' // 分割线颜色
          }
        },
        axisLabel: {
          formatter: (value) => `${(value / 1000).toFixed(0)}k`
        },

      }
    })
  })
  mChart.setOption(option)
}
</script>

<style lang="scss" scoped>

</style>