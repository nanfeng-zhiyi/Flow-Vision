<!-- 竖向柱状图 -->
<template>
  <div>
    <div style="text-align: center; font-size: 18px">核心主干道客货比</div>
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
  const passengerToGoodsRatios = [
  // Data for 2019
  [
    { name: 'G4', value: 8.2, color: '#dd6b66' },
    { name: 'G2', value: 7.8, color: '#eedd78' },
    { name: 'G15', value: 7.5, color: '#eedd78' },
    { name: 'G25', value: 7.0, color: '#eedd78' },
    { name: 'G30', value: 6.8, color: '#eedd78' },
    { name: 'G42', value: 6.5, color: '#eedd78' },
    { name: 'G50', value: 1.6, color: '#8dc1a9' },
    { name: 'G55', value: 1.5, color: '#8dc1a9' },
    { name: 'G3', value: 1.4, color: '#8dc1a9' },
    { name: 'G7', value: 1.3, color: '#8dc1a9' }
  ],
  // Data for 2020
  [
    { name: 'G4', value: 8.5, color: '#dd6b66' },
    { name: 'G3', value: 7.7, color: '#eedd78' },
    { name: 'G5', value: 7.4, color: '#eedd78' },
    { name: 'G6', value: 7.1, color: '#eedd78' },
    { name: 'G2', value: 6.9, color: '#eedd78' },
    { name: 'G60', value: 6.6, color: '#eedd78' },
    { name: 'G15', value: 2.2, color: '#8dc1a9' },
    { name: 'G25', value: 2.0, color: '#8dc1a9' },
    { name: 'G30', value: 1.9, color: '#8dc1a9' },
    { name: 'G42', value: 1.8, color: '#8dc1a9' }
  ],
  // Data for 2021
  [
    { name: 'G4', value: 8.7, color: '#dd6b66' },
    { name: 'G30', value: 8.1, color: '#dd6b66' },
    { name: 'G25', value: 7.8, color: '#eedd78' },
    { name: 'G42', value: 7.6, color: '#eedd78' },
    { name: 'G50', value: 7.3, color: '#eedd78' },
    { name: 'G55', value: 7.0, color: '#eedd78' },
    { name: 'G3', value: 1.6, color: '#8dc1a9' },
    { name: 'G2', value: 1.5, color: '#8dc1a9' },
    { name: 'G15', value: 1.4, color: '#8dc1a9' },
    { name: 'G5', value: 1.3, color: '#8dc1a9' }
  ]
];

console.log(passengerToGoodsRatios);

  // 2. 构建 option 配置对象 
  const renderChart = () => {
    const options = {
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
        data: Object.keys(passengerToGoodsRatios),
      },
      xAxis: {
        // 类别
        type: 'category',
        // data: props.data.servers.map((item) => item.name),
        // 文字
        axisLabel: {
          color: '#9eb1c8'
        }
      },
      // y轴展示数据
      yAxis: {
        show: false,
        type: 'value',
        max: function (value) { // 最大值 ，value 是X轴的数据
          return parseInt(value.max * 1.2)
        }
      },
      // 图表绘制的位置，对应 上下左右
      grid: {
        top: 16,
        right: 1,
        bottom: 46,
        left: 1,
      },
      // 核心配置 
      },
      options:[]
      // x轴展示数据

    }
    passengerToGoodsRatios.map((item=>{
       options.options.push(
         {
          series: [
        {
          // 柱
          type: 'bar',
          data: item.map((item) => ({
            name: item.name,
            value: item.value,
            itemStyle: {
              color: item.color, // 柱颜色
              barBorderRadius: 5, // 圆角
              shadowColor: 'rgba(0,0,0,0.3)', // 阴影
              shadowBluer: 5 // 阴影模糊
            },
          })),
          // 柱宽
          barWidth: 12,
          // 轴上文字
          label: {
            show: true,
            position: 'top',
            textStyle: {
              color: '#fff'
            },
            formatter: '{c}%'
          },
        },
      ],
      xAxis:{
        data: item.map(item=>item.name)
      }
         }
       )
    }))
    // 3. 通过 实例.setOptions(option)
    mChart.setOption(options);
  }

  watch(() => props.data, renderChart)
</script>
<style lang="scss" scoped>

</style>