<template>
  <div v-show="!showMap" id="main" @dblclick="back"></div>
  <BaiduMap v-if="showMap" :maplng="maplng" :maplat="maplat" @goback="showMap=$event"></BaiduMap>
  
</template>
<script setup>
import axios from "axios";
import BaiduMap from '../components/BaiduMap.vue'
import { provinces } from "../utils/provincesmap";
import { cityMap } from "../utils/citymap";
import { onMounted, ref } from "vue";
const chart = ref(null);
const showMap = ref(false)
const maplng = ref(0)
const maplat = ref(0)
//直辖市和特别行政区-只有二级地图，没有三级地图
const special = ["北京", "天津", "上海", "重庆", "香港", "澳门"];

let mapdata = [];

//初始化绘制全国地图配置
let option = {
  backgroundColor: "#000",
  title: {
    text: "中国地图",
    left: "center",
    textStyle: {
      color: "#fff",
      fontSize: 16,
      fontWeight: "normal",
      fontFamily: "Microsoft YaHei",
    },
    subtextStyle: {
      color: "#ccc",
      fontSize: 13,
      fontWeight: "normal",
      fontFamily: "Microsoft YaHei",
    },
  },
  tooltip: {
    trigger: "item",
    formatter: "{b}",
  },
  toolbox: {
    show: true,
    orient: "vertical",
    left: "right",
    top: "center",
    feature: {
      dataView: { readOnly: false },
      restore: {},
      saveAsImage: {},
    },
    iconStyle: {
      normal: {
        color: "#fff",
      },
    },
    emphasis:{
      areaColor: '#389bb7',
      borderWidth: 0,
    }
  },
  animationDuration: 1000,
  animationEasing: "cubicOut",
  animationDurationUpdate: 1000,
};

//绘制地图的方法
const renderMap = (map, data) => {
  option.title.subtext = map;
  option.series = [
    {
      name: map,
      type: "map",
      mapType: map,
      roam: false,
      nameMap: {
        china: "中国",
      },
      label: {
        normal: {
          show: true,
          textStyle: {
            color: "#999",
            fontSize: 13,
          },
        },
        symbolSize: 10,
        checkpointStyle: {
          borderColor: '#888',
          borderWidth: 2
        },
        emphasis: {
          show: true,
          textStyle: {
            color: "#fff",
            fontSize: 13,
          },
        },
      },
      itemStyle: {
        normal: {
          areaColor: {
                type: 'radial',
                x: 0.5,
                y: 0.5,
                r: 0.5,
                colorStops: [{
                  offset: 0,
                  color: 'rgba(147,235,248,0)',
                }, {
                  offset: 1,
                  color: 'rgba(147,235,248,.2)',
                }]
              },
          borderColor: "dodgerblue",
        },
        emphasis:{
          areaColor: '#389bb7',
          borderWidth: 0,
        }
      },
      data: data,
    },
  ];
  //渲染地图
  chart.value.setOption(option);
};

// 初始化中国地图
const loadChina = async () => {
  let { data } = await axios.get("/map/china.json");
  let d = [];
  for (var i = 0; i < data.features.length; i++) {
    d.push({
      name: data.features[i].properties.name,
    });
  }
  mapdata = d;
  //注册地图
  echarts.registerMap("china", data);
  //绘制地图
	renderMap('china',d);
};

const back = ()=>{
  renderMap('china',mapdata);
}

// 组件挂载完成
onMounted(() => {
  //地图容器
  chart.value = echarts.init(document.getElementById("main"));
  // 初始化中国地图
  loadChina();
  // 注册点击事件
  chart.value.on('click',async (params)=>{
    // 判断点击的是不是省份
    if(params.name in provinces){
      // 如果点击的是34个省、市、自治区，绘制选中地区的二级地图
      let {data} = await axios.get('/map/province/'+provinces[params.name]+'.json')
      // 注册省份地图数据
      echarts.registerMap(params.name, data);
      // 添加省份对应的城市数据
			var d = [];
			for( var i=0;i<data.features.length;i++ ){
				d.push({
					name:data.features[i].properties.name
				})
			}
      // 重新绘制地图
			renderMap(params.name,d);
    }else if(params.seriesName in provinces){
      if(special.indexOf( params.seriesName ) >=0){
        // 打开百度地图 
        let {data:{result:{location:{lat,lng}}}} = await axios.get('/baidu/geocoding/v3/',{
          params:{
            address:params.seriesName+params.name,
            ak:'CtDFZnPIhj7MjWLllGtFNyLpT4MpgGwv',
            output:'json'
          }
        })
        maplng.value = lng
        maplat.value = lat
        showMap.value = true
      }else{
        //显示县级地图
        let {data} = await axios.get('/map/city/'+cityMap[params.name]+'.json')
        // 注册城市地图数据
        echarts.registerMap(params.name, data);
        // 添加城市对应的区县数据
        var d = [];
				for( var i=0;i<data.features.length;i++ ){
					d.push({
						name:data.features[i].properties.name
					})
				}
        // 重新绘制地图
				renderMap(params.name,d);
      }
    }else{
      // 打开百度地图 
      let {data:{result:{location:{lat,lng}}}} = await axios.get('/baidu/geocoding/v3/',{
        params:{
          address:params.seriesName+params.name,
          ak:'sICFGuAAPisdVnB5Bx6ILAADGPnRDusH',
          output:'json'
        }
      })
      maplng.value = lng
      maplat.value = lat
      showMap.value = true
    }
  })
});
</script>
<style scoped lang="scss">
#main{
  width: 100vw;
  height: 100vh;
}
</style>
