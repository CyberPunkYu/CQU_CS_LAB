<template>
	<view>
		<view class="charts-box">
			<qiun-data-charts type="bar" :chartData="chartData" :ontouch="false" />
		</view>
		<view class="charts-box_a">
			<qiun-data-charts type="pie" :chartData="pieData" />
		</view>
	</view>
</template>

<script>
	import globalSetting from '@/common/json/globalSetting.json';
	export default {
		data() {
			return {
				isNetworkBusy: true,			//网络繁忙标志页
				chartData: {},
				pieData: {},
			}
		},

		async onLoad() {			//加载时获取数据
			uni.showToast({						
				duration: globalSetting.TIME_OUT,
				icon: "loading",
			})
			await this.getServerData();		
			uni.hideToast();
		},

		onPullDownRefresh() {			//下拉刷新，回弹图标
			console.log('refresh');
			setTimeout(function () {
				uni.stopPullDownRefresh();
			}, 1000);
		},
		methods: {
			showPromptOfBusyNetwork() {			//网络繁忙弹窗
				uni.showModal({
					showCancel: false,
					content: "网络繁忙，请稍后重试！",
				})
			},
			async getServerData() {			//获取服务器数据
				await uni.request({
					url: globalSetting.API_SITE_INFO+"/getMajorDistribution",
					method: "GET",
					timeout: globalSetting.TIME_OUT, 
				}).then((data) => {
					var [err, res] = data;
					if (err) {
						this.isNetworkBusy = true;			//err不为null则网络存在错误
						this.showPromptOfBusyNetwork();
					} else {								//组织图表数据
						this.isNetworkBusy = false;
						var resdata = {
							categories: ["大数据技术", "云计算技术运用", "物联网应用技术"],
							series: [{
								name: "已报到人数",
								data: [res.data.CSCountNow, res.data.ISCountNow, res.data
									.ITCountNow
								]
							}, {
								name: "总人数",
								data: [res.data.CSCountShould, res.data.ISCountShould, res.data
									.ITCountShould
								]
							}]
						};
						this.chartData = JSON.parse(JSON.stringify(resdata));
						resdata = {
							"series": [{
								    "name": "大数据技术",
									"data": res.data.CSCountNow
								},
								{
									"name": "云计算技术运用",
									"data": res.data.ISCountNow
								},
								{
									"name": "物联网应用技术",
									"data": res.data.ITCountNow
								},
							],
						};
						this.pieData = JSON.parse(JSON.stringify(resdata));
					}
				});
				return;
			},
		},
	}
</script>

<style lang="scss" scoped>
	.charts-box {
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
	.charts-box_a {
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
