<template>
	<view>
		<view class="charts-box">			<!-- 上面的条状统计图 -->
			<qiun-data-charts type="column" :chartData="chartData" :ontouch="false" :opts="opts1" />
		</view>
		<view class="charts-box_a">			<!-- 下面的环状统计图 -->
			<qiun-data-charts type="ring" :chartData="pieData" :opts="opts" />
		</view>
	</view>
</template>

<script>
	import globalSetting from '@/common/json/globalSetting.json';		//全局变量引入
	export default {
		data() {
			return {
				isNetworkBusy: true,					//网络状态标志位
				chartData: {},							//条状统计图数据
				pieData: {},							//环状统计图数据
				opts: {									//环状统计图设置
					"legend": {
						"show": true,
						"position": "bottom",
						"lineHeight": 25,
					},
				},
				opts1: {								//条状统计图设置
					"color": ['#5555ff']
				}
			}
		},

		onPullDownRefresh() {							//下拉刷新
			console.log('refresh');
			setTimeout(function () {
				uni.stopPullDownRefresh();
			}, 1000);
		},
		
		async onLoad() {			//加载时请求数据
			uni.showToast({
				duration: globalSetting.TIME_OUT,
				icon: "loading",
			})
			await this.getServerData();
			uni.hideToast();
		},
		methods: {
			showPromptOfBusyNetwork() {			//网络状态繁忙提示框弹出
				uni.showModal({
					showCancel: false,
					content: "网络繁忙，请稍后重试！",
				})
			},

			async getServerData() {			//获取数据
				await uni.request({
					url: globalSetting.API_SITE_INFO+'/getAgeDistribution',
					method: "GET",
					timeout: globalSetting.TIME_OUT, //超时时间在全局设置中
				}).then((data) => {
					var [err, res] = data;
					if (err) {					//err不为空则为true
						this.isNetworkBusy = true;
					} else {
						this.isNetworkBusy = false;
						var resdata = {			//拼接组合数据
							categories: ["16岁及以下", "17岁", "18岁", "19岁", "20岁及以上"],
							series: [{
								name: "年龄分布",
								data: [res.data.lqSixteen, res.data.seventeen, res.data.eighteen,
									res.data.nineteen, res.data.gqTwenty
								]
							}],
						};
						this.chartData = JSON.parse(JSON.stringify(resdata));
						resdata = {
							series: [{
									"name": "16岁及以下",
									"data": res.data.lqSixteen
								},
								{
									"name": "17岁",
									"data": res.data.seventeen
								},
								{
									"name": "18岁",
									"data": res.data.eighteen
								},
								{
									"name": "19岁",
									"data": res.data.nineteen
								},
								{
									"name": "20岁及以上",
									"data": res.data.gqTwenty
								},
							]
						};
						this.pieData = JSON.parse(JSON.stringify(resdata));
					}
					if (this.isNetworkBusy == true) {
						this.showPromptOfBusyNetwork();			//繁忙提示框
					}
				});
				return;
			},
			
		},
	}
</script>

<style lang="scss" scoped>
	.charts-box {		//条状统计图样式
		margin: auto;
		margin-top: 100rpx;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		background-color: rgba(204, 204, 204, 0.4);
		;
		border-radius: $uni-wrapper-radio;
		box-shadow: $uni-shadowBox;
		width: 600rpx;
	}

	.charts-box_a {		//环形统计图样式
		margin: auto;
		margin-top: 100rpx;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		background-color: rgba(204, 204, 204, 0.4);
		;
		border-radius: $uni-wrapper-radio;
		box-shadow: $uni-shadowBox;
		width: 600rpx;
	}
</style>
