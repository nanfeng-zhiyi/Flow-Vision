<template>
  <!-- <body style="height: 100%; margin: 0"> -->
  <div ref="container" style="height: 100%" class="pannel" ></div>
  <div class="left-up-tangle"></div>
  <div class="right-up-tangle"></div>
  <div class="left-bottom-tangle"></div>
  <div class="right-bottom-tangle"></div>
  <!-- </body> -->
</template>

<script setup>
  import * as echarts from 'echarts'
  import {onMounted, ref} from "vue";

  let mChart = null
  
  const props = defineProps({
    data:{
      typedef: Object,
      require: true
    }
  })

  let province_name = ref(props.data[props.data.length - 1].province)
  // province_name.value = province_name.value.slice(0, -1);
  console.log(province_name.value)
  console.log(props.data)
  // 动态注册地图的位置
  console.log(province_name.value)
  let geoJson = require('@/assets/mapData/' + province_name.value + '.json')
  const container = ref(null)

  onMounted(() => {
    mChart = echarts.init(container.value, null, {
      renderer: 'canvas',
      useDirtyRect: false
    })
    renderChart()
  })

  function renderChart() {
    echarts.registerMap('maps', geoJson);
    mChart.setOption(
        ({
          title: {
            text: province_name.value + '道路里程显示',
            textStyle:{
              color:'white'
            },
            left: 'center',
            sublink:
                'http://zh.wikipedia.org/wiki/%E9%A6%99%E6%B8%AF%E8%A1%8C%E6%94%BF%E5%8D%80%E5%8A%83#cite_note-12'
          },
          toolbox: {
            show: true,
            orient: 'vertical',
            left: 'right',
            top: 'center',
            feature: {
              dataView: { readOnly: false },
              restore: {},
              saveAsImage: {}
            }
          },
          visualMap: {
            min: 800,
            max: 50000,
            text: ['High', 'Low'],
            textStyle:{
              color:'white'
            },
            realtime: false,
            calculable: true,
            inRange: {
              color: ['lightskyblue', 'yellow', 'orangered']
            }
          },
          series: [
            {
              name: province_name.value,
              type: 'map',
              map: 'maps',
              label: {
                show: false,
                textStyle:{
                  color:'white'
                },
                tooltip: {
                trigger: 'item', // 触发类型设置为数据项图形
                formatter: function (params) {
                        return params.name; // tooltip将仅显示区域名称
                   }
              }
            },
              data: props.data,
            }
          ]
        })
    );
  }
</script>

<style>
.pannel{
  border: 1px solid rgba(25,186,139,0.17);
  background-image: url('../assets/imgs/line.png');
  background-color: rgba(0,0,0,0.10);
  /* 通过伪类 */
}
/* .pannel::before{
    content: 45555555555555555555555555555;
    position: absolute;
    width: 20px;
    height: 20px;
    border-left: 2px solid #02a6b5;
    border-top: 2px solid #02a6b5;

} */
</style>