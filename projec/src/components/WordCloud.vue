<!-- 数据云图 -->
<template>
  <div>
    <div>【关键词条】</div>
    <div ref="target" class="w-full h-full"></div>
  </div>
</template>
<script setup>
  import { ref, onMounted, watch } from 'vue'
  import * as echarts from 'echarts'
  import 'echarts-wordcloud'

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

  const randomRGB = () => {
    const r = Math.floor(Math.random() * 255)
    const g = Math.floor(Math.random() * 255)
    const b = Math.floor(Math.random() * 255)
    return `rgb(${r},${g},${b})`
  }

  // 2. 构建 option 配置对象 
  const renderChart = () => {
    const options = {
      // 核心配置 
      series: [
        {
          type: 'wordCloud',
          sizeRange: [8, 46],
          rotationRange: [0, 0],
          gridSize: 0,
          layoutAnimation: true,
          textStyle: {
            color: randomRGB
          },
          data: props.data.datas,
          emphasis: {
            textStyle: {
              fontWeight: 'bold',
              color: '#000'
            }
          }
        }
      ]
    }
    // 3. 通过 实例.setOptions(option)
    mChart.setOption(options);
  }

  watch(() => props.data, renderChart)
</script>
<style lang="scss" scoped>

</style>