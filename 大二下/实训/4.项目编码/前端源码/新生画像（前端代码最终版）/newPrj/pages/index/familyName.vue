<!-- 姓氏分布 -->

<template>
	<view>
		<view class="charts-box">			<!-- 词云图 -->
			<qiun-data-charts type="word" :chartData="wordData" />
		</view>
		<view class="tab">					<!-- 表格 -->
			<uni-table ref="table" emptyText="暂无更多数据">
				<uni-tr>
					<uni-th width="150" align="center">姓氏</uni-th>
					<uni-th width="150" align="center">频数</uni-th>
				</uni-tr>
				<uni-tr v-for="(item, index) in wordData.series" :key="index">
					<uni-td align="center">{{ item.name }}</uni-td>
					<uni-td align="center">{{ item.data}}</uni-td>
				</uni-tr>
			</uni-table>
		</view>
	</view>
</template>

<script>
	import globalSetting from '@/common/json/globalSetting.json';		//全局变量
	export default {
		data() {
			return {
				isNetworkBusy: true,		//网络繁忙标志位
				wordData: {				//词云数据

				},
			}
		},
		onPullDownRefresh() {			//下拉刷新
			console.log('refresh');
			setTimeout(function () {
				uni.stopPullDownRefresh();
			}, 1000);
		},
		async onLoad() {			//加载页面时请求数据
			uni.showToast({
				duration: globalSetting.TIME_OUT,
				icon: "loading",
			})
			await this.getServerData();
			uni.hideToast();
		},
		methods: {
			showPromptOfBusyNetwork() {		//模态提示框（网络繁忙）
				uni.showModal({
					showCancel: false,
					content: "网络繁忙，请稍后重试！",
				})
			},
			async getServerData() {			//从服务器获取数据
				await uni.request({
					url: globalSetting.API_SITE_INFO+"/getSurnameDistribution",
					method: "GET",
					timeout: globalSetting.TIME_OUT,
				}).then((data) => {
					var [err, res] = data;
					if (err) {			//不为空则网络存在问题
						this.isNetworkBusy = true;
					} else {
						this.isNetworkBusy = false;
						var resdata = {
							series: []
						};
						var textsize, totsum = 0;
						for (var item in res.data) {	//统计词频总数
							if (item == 15) {
								break;			//达到15个姓氏数量则跳出
							}
							totsum += Number(res.data[item][1]);
						}			
						for (var item in res.data) {
							if (item == 15) {
								break;			//达到15个姓氏数量则跳出
							}
							textsize = Math.max(300 * res.data[item][1] / totsum, 20);		//根据比例设计字体大小
							resdata.series.push({
								"name": res.data[item][0],
								"textSize": textsize,
								"data": res.data[item][1]
							});
						}
						this.wordData = JSON.parse(JSON.stringify(resdata));
					}
					if (this.isNetworkBusy == true) {
						this.showPromptOfBusyNetwork();			//网络繁忙提示框弹出
					}
				});
				return;
			}
		},
	}
</script>

<style lang="scss">
	.charts-box {			//词云图样式
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		width: 600rpx;
		margin: auto;
		margin-top: 50rpx;
		background-color: rgba(204, 204, 204, 0.4);
		border-radius: 30rpx;
		box-shadow: $uni-shadowBox;
	}
	.tab {					//表格样式
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		margin-top: 100rpx;
	}
</style>
