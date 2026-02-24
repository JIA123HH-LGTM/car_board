<template>
  <div id="bottomRight">
    <div class="bg-color-black">
      <div class="d-flex pt-2 pl-2">
        <span>
          <icon name="chart-area" class="text-icon"></icon>
        </span>
        <div class="d-flex">
          <span class="fs-xl text mx-2"><h1 style="font-size: 27px">汽车排行榜</h1></span>
          <div class="decoration2">
            <dv-decoration-2 :reverse="true" style="width:5px;height:6rem;" />
          </div>
        </div>
      </div>
      <div class="row_list">
        <div style="font-size: 20px;display: flex;padding-top: 10px">
            <div style="flex:1;text-align: center">销售排名</div>
            <div style="flex:1;text-align: center">图片</div>
            <div style="flex:1;text-align: right">汽车信息</div>
            <div style="flex:1;text-align: right">销售价格</div>
            <div style="flex:1;text-align: right">销售数量</div>
            <div style="flex:1;text-align: right">保修期限</div>
            <div style="flex:1;text-align: center">上市时间</div>
        </div>
        <ul class="car_rank" style="width: 100%;height: 420px;overflow: auto">
          <li
            v-for="car in carData"
            :key="car.rank"
            :class="{ 'active': hoverIndex === car.rank }"
            @mouseenter="hoverIndex = car.rank"
            @mouseleave="hoverIndex = null"
            @click="showImage(car)"
          >
            <div>{{car.rank}}</div>
            <div class="list_img">
              <img :src="car.carImg" style="height: 100%;width: 100%" alt="">
            </div>
            <div class="list_info">
              <p>{{car.carName}}</p>
              <p>{{car.manufacturer}}/{{car.brand}}</p>
            </div>
            <div class="list_price">{{car.price}}万元</div>
            <div class="list_volume">{{car.saleVolume}}辆</div>
            <div class="list_insure">{{car.insure}}</div>
            <div class="list_marketTime">{{car.marketTime}}</div>
          </li>
        </ul>
      </div>
    </div>

    <!-- 图片弹窗 -->
    <div v-if="showModal" class="modal" @click="closeModal">
      <div class="modal-content" @click.stop>
        <span class="close" @click="closeModal">&times;</span>
        <h3>{{ selectedCar.carName }}</h3>
        <img :src="selectedCar.carImg" alt="">
        <p>{{ selectedCar.manufacturer }} / {{ selectedCar.brand }}</p>
        <p>售价：{{ selectedCar.price }}万元 | 销量：{{ selectedCar.saleVolume }}辆</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  components: {},
  data(){
    return{
      carData: [],
      hoverIndex: null,      // 当前悬停的索引
      showModal: false,      // 是否显示弹窗
      selectedCar: {}        // 选中的车辆
    }
  },
  async mounted(){
    const res = await this.$http.get('myApp/bottomRight/')
    this.carData = res.data.carData
  },
  methods: {
    // 显示图片弹窗
    showImage(car) {
      this.selectedCar = car
      this.showModal = true
    },
    // 关闭弹窗
    closeModal() {
      this.showModal = false
      this.selectedCar = {}
    }
  }
};
</script>

<style lang="scss" scoped>
$box-height: 520px;
$box-width: 100%;

#bottomRight {
  padding: 14px 16px;
  height: $box-height;
  width: $box-width;
  border-radius: 5px;

  .bg-color-black {
    height: $box-height - 40px;
    border-radius: 10px;
  }

  .text {
    color: #c3cbde;
  }

  .decoration2 {
    position: absolute;
    right: 0.125rem;
  }

  .chart-box {
    margin-top: 16px;
    width: 170px;
    height: 170px;
    .active-ring-name {
      padding-top: 10px;
    }
  }

  .row_list {
    list-style: none;

    .car_rank::-webkit-scrollbar {
      width: 18px;
      height: 0;
    }

    .car_rank::-webkit-scrollbar-track {
      border-radius: 9px;
      border: none;
    }

    .car_rank::-webkit-scrollbar-thumb {
      background: #4a90e2;
      border-radius: 9px;
      border: 3px solid #1a1a2e;
      cursor: pointer;
      min-height: 30px;
    }

    .car_rank::-webkit-scrollbar-thumb:hover {
      background: #357abd;
    }

    .car_rank::-webkit-scrollbar-corner {
      background: transparent;
    }

    .car_rank li {
      display: grid;
      grid-template-columns: 100px 150px 180px 120px 120px 110px 100px;
      cursor: pointer;
      margin-left: 23px;
      text-align: center;
      line-height: 30px;
      padding: 5px 0;
      border-radius: 5px;
      transition: all 0.3s ease;  // 平滑过渡

      // 悬停高亮样式
      &:hover{
        background-color: rgba(74, 144, 226, 0.3);  // 半透明蓝色背景
        box-shadow: 0 0 10px rgba(74, 144, 226, 0.5);  // 发光效果
        transform: scale(1.02);  // 轻微放大
      }
    }

    .car_rank .list_img {
      width: 156px;
      height: 80px;
    }

    .car_rank .list_price,
    .car_rank .list_volume,
    .car_rank .list_insure,
    .car_rank .list_marketTime {
      line-height: 60px;
    }
  }

  // 弹窗样式
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;

    .modal-content {
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
      border: 2px solid #4a90e2;
      border-radius: 10px;
      padding: 20px;
      text-align: center;
      max-width: 600px;
      position: relative;
      box-shadow: 0 0 30px rgba(74, 144, 226, 0.5);

      h3 {
        color: #fff;
        margin-bottom: 15px;
        font-size: 24px;
      }

      img {
        max-width: 500px;
        max-height: 350px;
        border-radius: 8px;
        margin-bottom: 15px;
      }

      p {
        color: #c3cbde;
        margin: 5px 0;
        font-size: 16px;
      }

      .close {
        position: absolute;
        top: 10px;
        right: 15px;
        color: #fff;
        font-size: 30px;
        cursor: pointer;

        &:hover {
          color: #4a90e2;
        }
      }
    }
  }
}
</style>