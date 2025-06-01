<!-- 横向柱状图 -->
<template>
  <div>
    <div style="text-align: center; font-size: 18px; transform: translateY(-1.5vh)">全国高速里程前六省份</div>
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
  

  const high_wayData = [
  [
    { name: '广东', value: 9003, color: '#D95850' },
    { name: '河北', value: 7280, color: '#F5B7BF' },
    { name: '四川', value: 7131, color: '#FED961' },
    { name: '湖南', value: 6725, color: '#DAE3F5' },
    { name: '河南', value: 6600, color: '#BFE3AA' },
    { name: '湖北', value: 6367, color: '#B16AF3'  }
  ],
   [
    { name: '广东', value: 9495, color: '#D95850'},
    { name: '河北', value: 7476, color: '#F5B7BF' },
    { name: '四川', value: 7523, color: '#FED961' },
    { name: '湖南', value: 6802, color: '#DAE3F5' },
    { name: '河南', value: 6967, color: '#BFE3AA' },
    { name: '湖北', value: 6860, color: '#B16AF3' }
  ],
 [
    { name: '广东', value: 10488, color: '#D95850' },
    { name: '河北', value: 7809, color: '#F5B7BF' },
    { name: '四川', value: 8140, color: '#FED961' },
    { name: '湖南', value: 6951, color: '#DAE3F5' },
    { name: '河南', value: 7100, color: '#BFE3AA' },
    { name: '湖北', value: 7230, color: '#B16AF3' }
  ]
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
        data: Object.keys(high_wayData),
      },
        xAxis: {
        show: false,
        type: 'value',
        max: function (value) { // 最大值 ，value 是X轴的数据
          return parseInt(value.max * 1.2)
        }
      },
      // y轴展示数据
      yAxis: {
        // 类别
        type: 'category',
        data: high_wayData[0].map((item) => item.name),
        inverse: true,
        // 轴线
        axisLine: {
          show: false
        },
        // 刻度
        axisTick: {
          show: false
        },
        // 文字
        axisLabel: {
          color: '#9eb1c8'
        }
      },
      // 图表绘制的位置，对应 上下左右
      grid: {
        top: 0,
        right: 10,
        bottom: 0,
        left: 15,
        containLabel: true
      },
      },
      options: []
    }
    high_wayData.map((item)=>{
       options.options.push({
         series:[
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
          showBackground: true,
          // 背景色
          backgroundStyle: {
            color: 'rgba(58,138,143,0.2)'
          },
          // 柱宽
          barWidth: 12,
          // 轴上文字
          label: {
            show: true,
            position: 'right',
            textStyle: {
              color: '#fff'
            }
          },
        }
         ]
       })
    })


    // 3. 通过 实例.setOptions(option)
    mChart.setOption(options);
  }

  watch(() => props.data, renderChart)
  console.log(props.data)

</script>
<style lang="scss" scoped>

</style>