<!-- 雷达图 -->
<template>
  <div>
    <div style="text-align: center; font-size: 18px; transform: translateY(-1vh)">高速主干拥堵量</div>
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

  const ydata = [
  // Imaginary data for 2019
  [
    { name: 'G4', value: 8.2 },
    { name: 'G2', value: 7.8 },
    { name: 'G15', value: 7.5 },
    { name: 'G25', value: 7.0 },
    { name: 'G30', value: 6.8 },
    { name: 'G42', value: 6.5 },
  ],
  // Imaginary data for 2020
  [
    { name: 'G4', value: 8.5 },
    { name: 'G3', value: 7.7 },
    { name: 'G5', value: 7.4 },
    { name: 'G6', value: 7.1 },
    { name: 'G2', value: 6.9 },
    { name: 'G60', value: 6.6 },
  ],
  // Imaginary data for 2021
  [
    { name: 'G4', value: 8.7 },
    { name: 'G30', value: 8.1 },
    { name: 'G25', value: 7.8 },
    { name: 'G42', value: 7.6 },
    { name: 'G50', value: 7.3 },
    { name: 'G55', value: 7.0 },
  ],
];


  // 1. 初始化 echarts 实例
  let mChart = null
  const target = ref(null)

  onMounted(() => {
    mChart = echarts.init(target.value)
    renderChart()
  })

  // 2. 构建 option 配置对象 
  const renderChart = () => {
    const options = {
      // 雷达图的坐标系配置
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
        data: Object.keys(ydata),
      },
      radar: {
        name: {
          textStyle: {
            color: '#05d5ff',
            fontSize: 14
          }
        },
        shape: 'polygon',
        center: ['50%', '50%'],
        radius: '80%',
        startAngle: 120,
        axisLine: {
          lineStyle: {
            color: 'rgba(211, 253, 250, 0.8)'
          }
        },
        splitLine: {
          show: true,
          lineStyle: {
            width: 1,
            color: 'rgba(5,213,255,.8)'
          }
        },
        indicator: ydata[0].map(item => ({
          name: item.name,
          max: 9
        })),
        splitArea: {
          show: false
        }
      },
      // 极坐标系配置
      polar: {
        center: ['50%', '50%'],
        radius: '0%'
      },
      // 角度轴
      angleAxis: {
        min: 0,
        interval: 5,
        clockwise: false
      },
      // 半径轴
      radiusAxis: {
        min: 0,
        interval: 20,
        splitLine: {
          show: false
        }
      },
    },
      options:[]
      // 核心配置
      // series: {
      //   type: 'radar',
      //   symbol: 'circle',
      //   symbolSize: 10,
      //   itemStyle: {
      //     normal: {
      //       color: '#05d5ff',
      //       opacity: 0.5
      //     }
      //   },
      //   areaStyle: {
      //     normal: {
      //       color: '#05d5ff',
      //       opacity: 0.5
      //     }
      //   },
      //   lineStyle: {
      //     width: 2,
      //     color: '#05d5ff',
      //   },
      //   label: {
      //     normal: {
      //       show: true,
      //       color: '#fff',
      //     }
      //   },
      //   data: [props.data.risks.map(item => item.value)]
      // }
    }
    ydata.map((item)=>{
     options.options.push({
        series: [
        {
        type: 'radar',
        symbol: 'circle',
        symbolSize: 10,
        itemStyle: {
          normal: {
            color: '#05d5ff',
            opacity: 0.5
          }
        },
        areaStyle: {
          normal: {
            color: '#05d5ff',
            opacity: 0.5
          }
        },
        lineStyle: {
          width: 2,
          color: '#05d5ff',
        },
        label: {
          normal: {
            show: true,
            color: '#fff',
          }
        },
        data: [item.map(item=>item.value)]
      }]
       })

      })
    // 3. 通过 实例.setOptions(option)
    mChart.setOption(options);
  }

  watch(() => props.data, renderChart)
  console.log(props.data)
  console.log("你好世界")
</script>
<style lang="scss" scoped>

</style>