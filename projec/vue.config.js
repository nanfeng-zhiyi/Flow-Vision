const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave:false,
  // configureWebPack: {
  //   name: '道路交通数据可视化'
  // },
  devServer:{
    proxy:{
      '/baidu':{
        //代理的地址
        target:'https://api.map.baidu.com/',
        //路径重写，因为向真实的后台发送请求时，不需要加前缀
        pathRewrite:{
            //将地址中，/stu替换成空
            '^/baidu':''
        },
        '/test': {
           target: 'http://127.0.0.1:8001/test',
           changeOrigin: true,
           pathRewrite: {
            '/test': ''
           }
        }
    },
    },
  },

})
