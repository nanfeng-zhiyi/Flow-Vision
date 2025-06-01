<template>
  <body style="height: 100%; margin: 0">
  <div ref="container" style="height: 100%" class="pannel"></div>
  <div class="left-up-tangle"></div>
  <div class="right-up-tangle"></div>
  <div class="left-bottom-tangle"></div>
  <div class="right-bottom-tangle"></div>
  </body>
</template>

<script setup>
  import * as echarts from 'echarts'
  import {onMounted, ref} from "vue";
  import axios from "axios";

  let option;
  let mChart = null
  const container = ref(null)
  let _rawData = null

  onMounted(() => {
    mChart = echarts.init(container.value, null, {
      renderer: 'canvas',
      useDirtyRect: false
    })
    window.addEventListener('resize', mChart.resize);
    axios.get("http://localhost:8001/test").then(res=>{
      _rawData = res.data
      renderChart()
    })
  })

  const renderChart = () => {
    console.log(_rawData)
    function run(_rawData) {
      const groups = [
        'Group_0', 'Group_1', 'Group_2', 'Group_3', 'Group_4', 'Group_5', 'Group_6',
      ];
      const datasetWithFilters = [];
      const seriesList = [];
      echarts.util.each(groups, function (group) {
        let datasetId = 'dataset_' + group;
        datasetWithFilters.push({
          id: datasetId,
          fromDatasetId: 'dataset_raw',
          transform: {
            type: 'filter',
            config: {
              and: [
                {dimension: 'Time', gte: 0},
                {dimension: 'Group', '=': group}
              ]
            }
          }
        });
        seriesList.push({
          type: 'line',
          datasetId: datasetId,
          showSymbol: false,
          name: group,
          endLabel: {
            show: true,
            formatter: function (params) {
              return params.value[1];
            },
            textStyle: {
              color: '#FFFFFF'
            }
          },
          labelLayout: {
            moveOverlap: 'shiftY'
          },
          emphasis: {
            focus: 'series'
          },
          encode: {
            x: 'Time',
            y: 'Predict',
            label: ['Group', 'Predict'],
            itemName: 'Time',
            tooltip: ['Predict'],
          }
        });
      });
      option = {
        animationDuration: 1000,
        dataset: [
          {
            id: 'dataset_raw',
            source: _rawData
          },
          ...datasetWithFilters
        ],
        title: {
          text: '未来2周内每小时车流量数据预测',
          left: 'center',
          textStyle:{
            color: '#FFFFFF',
            lineHeight: 30,
            fontWeight: 'normal'
          }
        },
        tooltip: {
          order: 'valueDesc',
          trigger: 'axis',
        },
        xAxis: {
          type: 'category',
          name: '小时',
          nameLocation: 'middle',
          axisLabel:{
            color: '#FFFFFF'
          }
        },
        yAxis: {
          name: '车流量',
          axisLabel:{
            color: '#FFFFFF',
          },
        },
        grid: {
          right: 80,
          top: 90,
          left: 70,

        },
        series: seriesList
      };
      mChart.setOption(option);
    }

    run(_rawData)

    if (option && typeof option === 'object') {
      mChart.setOption(option);
    }
  }
</script>

<style scoped lang="scss">
</style>