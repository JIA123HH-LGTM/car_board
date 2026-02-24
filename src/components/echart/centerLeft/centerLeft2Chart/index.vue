<template>
  <div>
    <div ref="chart" style="width: 290px; height: 450px"
         v-bind:key="cdata.category[0]"
         @mouseenter="startAction"
         @mouseleave="cancelAction">
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isHovered: true,
      myChart: null,
      timer: null,
      cdata: {
        category: [],    // carModel类型
        barData: []      // 销量数据
      }
    };
  },

  async mounted() {
    // 请求数据
    const res = await this.$http.get('myApp/centerLeft2/')
    this.$set(this.cdata, 'category', res.data.modelList)
    this.$set(this.cdata, 'barData', res.data.volumeList)
  },

  updated() {
    this.initChart()
    this.startDataUpdateInterval()
  },

  beforeDestroy() {
    // 清除定时器，防止内存泄漏
    if (this.timer) {
      clearInterval(this.timer)
    }
    if (this.myChart) {
      this.myChart.dispose()
    }
  },

  methods: {
    // 鼠标进入暂停滚动
    startAction() {
      this.isHovered = false
    },
    // 鼠标离开恢复滚动
    cancelAction() {
      this.isHovered = true
      this.startDataUpdateInterval()
    },

    // 初始化图表
    initChart() {
      this.myChart = this.$echarts.init(this.$refs.chart);

      const option = {
        // 提示框 - 鼠标悬停显示 carModel 类型和数量
        tooltip: {
          trigger: "axis",
          backgroundColor: "rgba(0,0,0,0.7)",
          borderColor: "#777",
          textStyle: {
            color: "#fff"
          },
          axisPointer: {
            type: "shadow"
          },
          // 自定义提示框内容
          formatter: function(params) {
            let result = `<div style="font-weight:bold;margin-bottom:5px;">${params[0].name}</div>`
            params.forEach(item => {
              result += `<div>
                <span style="display:inline-block;width:10px;height:10px;background:${item.color};border-radius:50%;margin-right:5px;"></span>
                ${item.seriesName}: <strong>${item.value.toLocaleString()}</strong>
              </div>`
            })
            return result
          }
        },

        // 数据缩放（隐藏滚动条，只保留功能）
        dataZoom: [
          {
            type: "slider",
            start: 0,
            end: 60,  // 默认显示前60%的数据
            show: false
          }
        ],

        // 网格
        grid: {
          left: "0%",
          right: "0%",
          bottom: "20%",
          top: "10%",
          containLabel: true
        },

        // X轴 - carModel类型
        xAxis: {
          type: 'category',
          data: this.cdata.category,
          axisLine: {
            lineStyle: {
              color: "#B4B4B4"
            }
          },
          axisLabel: {
            color: "#B4B4B4",
            interval: 0,      // 显示所有标签
            rotate: 30,       // 标签旋转30度，防止重叠
            fontSize: 11
          },
          axisTick: {
            alignWithLabel: true
          }
        },

        // Y轴 - 销量
        yAxis: {
          type: 'value',
          name: '销量（辆）',
          nameTextStyle: {
            color: "#B4B4B4"
          },
          splitLine: {
            lineStyle: {
              color: "rgba(255,255,255,0.1)"
            }
          },
          axisLine: {
            lineStyle: {
              color: "#B4B4B4"
            }
          },
          axisLabel: {
            color: "#B4B4B4",
            formatter: function(value) {
              if (value >= 10000) {
                return (value / 10000) + '万'
              }
              return value
            }
          }
        },

        // 数据系列
        series: [
          {
            name: "销售量",
            type: "bar",
            barWidth: 10,
            data: this.cdata.barData,
            // 渐变色柱子
            itemStyle: {
              borderRadius: [5, 5, 0, 0],
              color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: "#00d4ff" },   // 顶部颜色
                { offset: 1, color: "#0066cc" }    // 底部颜色
              ])
            },
            // 鼠标悬停时的高亮样式
            emphasis: {
              itemStyle: {
                color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: "#ff6b6b" },
                  { offset: 1, color: "#ee5a24" }
                ])
              }
            },
            // 标签显示在柱子上方
            label: {
              show: true,
              position: 'top',
              color: '#fff',
              fontSize: 10,
              formatter: function(params) {
                if (params.value >= 10000) {
                  return (params.value / 10000).toFixed(1) + '万'
                }
                return params.value
              }
            }
          }
        ]
      }

      this.myChart.setOption(option)
    },

    // 数据轮播：将第一个元素移到最后
    changeData(x) {
      var st = x[0]
      for(var i = 0;i<x.length-1;i++){
        x[i] = x[i+1]
      }
      x[x.length-1] = st
    },

    // 更新图表（轮播效果）
    updateBarChart() {
      if (this.isHovered === true && this.cdata.category.length > 0) {
        this.changeData(this.cdata.category)
        this.changeData(this.cdata.barData)

        this.myChart.setOption({
          xAxis: {
            data: this.cdata.category
          },
          series: [
            {
              data: this.cdata.barData
            }
          ]
        })
      }
    },

    // 启动定时轮播
    startDataUpdateInterval() {
      if (this.isHovered === true) {
        const interval = 3000  // 3秒切换一次
        clearInterval(this.timer)
        this.timer = setInterval(this.updateBarChart, interval)
      }
    }
  }
};
</script>

<style lang="scss" scoped>
</style>