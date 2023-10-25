<!-- 报道进度 -->

<template>
	<view>
		<view class="chartWrapper">			<!-- 波浪式柱形图 -->
			<canvas canvas-id="cKhHzZrIyITVcmeoKSHKAcaoaASuyZQI" id="cKhHzZrIyITVcmeoKSHKAcaoaASuyZQI" class="charts"
				@touchend="tap" />
		</view>
		<view class="charts_b">		<!-- 饼形图 -->
			<canvas canvas-id="pie" id="pie" class="charts_a" @touchend="tap_a" />
		</view>
	</view>
</template>

<script>
	import globalSetting from '@/common/json/globalSetting.json';
	import uCharts from '@/uni_modules/qiun-data-charts/js_sdk/u-charts/u-charts.js';
	var uChartsInstance = {};
	var uCharts_Instance = {};
	export default {
		data() {
			return {
				isNetworkBusy: true,
				cWidth: 750,
				cHeight: 500,

				c_Width: 750,
				c_Height: 500,
				sumCount: 0,
				dayCount: 0,
				allCountShould: 1000,
				NotCount: 0
			};
		},

		async onLoad() {
			uni.showToast({
				duration: globalSetting.TIME_OUT,
				icon: "loading",
			})
			//这里的 750 对应 css .charts 的 width
			this.cWidth = uni.upx2px(600);
			//这里的 500 对应 css .charts 的 height
			this.cHeight = uni.upx2px(500);
			await this.getServerData();

			//这里的 750 对应 css .charts 的 width
			this.c_Width = uni.upx2px(600);
			//这里的 500 对应 css .charts 的 height
			this.c_Height = uni.upx2px(500);
			this.getServer_Data();
			uni.hideToast();
		},

		onPullDownRefresh() {		//下拉刷新函数
			setTimeout(function () {
				uni.stopPullDownRefresh();
			}, 1000);
		},
		methods: {
			showPromptOfBusyNetwork() {		//繁忙刷新
				uni.showModal({
					showCancel: false,
					content: "网络繁忙，请稍后重试！",
				})
			},
			async getServerData() {			//获取数据
				await uni.request({
					url: globalSetting.API_SITE_INFO+"/getReportingProgress",
					method: "GET",
				}).then((data) => {
					var[err,res] = data;
					if (err){
						this.isNetworkBusy=true;
					}
					else{
						this.isNetworkBusy=false;
						this.sumCount = res.data.sumCount;
						this.dayCount = res.data.dayCount;
						this.NotCount = this.allCountShould - res.data.sumCount;
						console.log("未报到人数：" + this.NotCount);
					}
					if (this.isNetworkBusy==true){
						this.showPromptOfBusyNetwork();
					}
				})
				//模拟从服务器获取数据时的延时
				setTimeout(() => {
					//模拟服务器返回数据，如果数据格式和标准格式不同，需自行按下面的格式拼接
					let res = {
						series: [{
							data: [{
								"name": "总报到人数",
								"value": this.sumCount
							}, {
								"name": "当天报到人数",
								"value": this.dayCount
							}]
						}]
					};
					this.drawCharts('cKhHzZrIyITVcmeoKSHKAcaoaASuyZQI', res);
				}, 500);
			},

			drawCharts(id, data) {				//绘制图像
				const ctx = uni.createCanvasContext(id, this);
				uChartsInstance[id] = new uCharts({
					type: "mount",
					context: ctx,
					width: this.cWidth,
					height: this.cHeight,
					series: data.series,
					animation: true,
					timing: "easeOut",
					duration: 1000,
					rotate: false,
					rotateLock: false,
					background: "#FFFFFF",
					color: ["#1890FF", "#91CB74", "#FAC858", "#EE6666", "#73C0DE", "#3CA272", "#FC8452", "#9A60B4",
						"#ea7ccc"
					],
					padding: [15, 15, 0, 5],
					fontSize: 13,
					fontColor: "#666666",
					dataLabel: true,
					dataPointShape: true,
					dataPointShapeType: "solid",
					touchMoveLimit: 60,
					enableScroll: false,
					enableMarkLine: false,
					legend: {
						show: false,
						position: "top",
						float: "left",
						padding: 5,
						margin: 5,
						backgroundColor: "rgba(0,0,0,0)",
						borderColor: "rgba(0,0,0,0)",
						borderWidth: 0,
						fontSize: 13,
						fontColor: "#666666",
						lineHeight: 11,
						hiddenColor: "#CECECE",
						itemGap: 10
					},
					xAxis: {
						disableGrid: true,
						disabled: false,
						axisLine: true,
						axisLineColor: "#CCCCCC",
						calibration: false,
						fontColor: "#666666",
						fontSize: 16,
						rotateLabel: false,
						rotateAngle: 45,
						itemCount: 5,
						boundaryGap: "center",
						splitNumber: 5,
						gridColor: "#CCCCCC",
						gridType: "solid",
						dashLength: 4,
						gridEval: 1,
						scrollShow: false,
						scrollAlign: "left",
						scrollColor: "#A6A6A6",
						scrollBackgroundColor: "#EFEBEF",
						formatter: ""
					},
					yAxis: {
						data: [{
							min: 0
						}],
						disabled: true,
						disableGrid: true,
						splitNumber: 5,
						gridType: "solid",
						dashLength: 8,
						gridColor: "#CCCCCC",
						padding: 10,
						showTitle: false
					},
					extra: {
						mount: {
							type: "mount",
							widthRatio: 1.5,
							borderWidth: 1,
							barBorderCircle: false,
							linearType: "custom",
							linearOpacity: 1,
							colorStop: 0
						},
						tooltip: {
							showBox: true,
							showArrow: true,
							showCategory: false,
							borderWidth: 0,
							borderRadius: 0,
							borderColor: "#000000",
							borderOpacity: 0.7,
							bgColor: "#000000",
							bgOpacity: 0.7,
							gridType: "solid",
							dashLength: 4,
							gridColor: "#CCCCCC",
							fontColor: "#FFFFFF",
							splitLine: true,
							horizentalLine: false,
							xAxisLabel: false,
							yAxisLabel: false,
							labelBgColor: "#FFFFFF",
							labelBgOpacity: 0.7,
							labelFontColor: "#666666"
						},
						markLine: {
							type: "solid",
							dashLength: 4,
							data: []
						}
					}
				});
			},
			tap(e) {
				uChartsInstance[e.target.id].touchLegend(e);
				uChartsInstance[e.target.id].showToolTip(e);
			},

			// 饼图
			getServer_Data() {
				//模拟从服务器获取数据时的延时
				setTimeout(() => {
					//模拟服务器返回数据，如果数据格式和标准格式不同，需自行按下面的格式拼接
					let res = {
						series: [{
							data: [{
								"name": "已报到",
								"value": this.sumCount
							}, {
								"name": "未报到",
								"value": this.NotCount
							}]
						}]
					};
					this.draw_Charts('pie', res);
				}, 500);
			},

			draw_Charts(id, data) {			//绘制图像
				const ctx = uni.createCanvasContext(id, this);
				uCharts_Instance[id] = new uCharts({
					type: "pie",
					context: ctx,
					width: this.c_Width,
					height: this.c_Height,
					series: data.series,
					animation: true,
					timing: "easeOut",
					duration: 1000,
					rotate: false,
					rotateLock: false,
					background: "#FFFFFF",
					color: ["#ffbf70", "#1b8cee", "#1890FF", "#91CB74", "#FAC858", "#73C0DE", "#3CA272", "#FC8452",
						"#9A60B4"
					],
					padding: [5, 5, 5, 5],
					fontSize: 13,
					fontColor: "#666666",
					dataLabel: true,
					dataPointShape: true,
					dataPointShapeType: "solid",
					touchMoveLimit: 60,
					enableScroll: false,
					enableMarkLine: false,
					legend: {
						show: true,
						position: "bottom",
						float: "center",
						padding: 5,
						margin: 5,
						backgroundColor: "rgba(0,0,0,0)",
						borderColor: "rgba(0,0,0,0)",
						borderWidth: 0,
						fontSize: 16,
						fontColor: "#666666",
						lineHeight: 11,
						hiddenColor: "#CECECE",
						itemGap: 10
					},
					extra: {
						pie: {
							activeOpacity: 0.5,
							activeRadius: 10,
							offsetAngle: 0,
							labelWidth: 15,
							border: true,
							borderWidth: 3,
							borderColor: "#FFFFFF",
							customRadius: 0,
							linearType: "none"
						},
						tooltip: {
							showBox: true,
							showArrow: true,
							showCategory: false,
							borderWidth: 0,
							borderRadius: 0,
							borderColor: "#000000",
							borderOpacity: 0.7,
							bgColor: "#000000",
							bgOpacity: 0.7,
							gridType: "solid",
							dashLength: 4,
							gridColor: "#CCCCCC",
							fontColor: "#FFFFFF",
							splitLine: true,
							horizentalLine: false,
							xAxisLabel: false,
							yAxisLabel: false,
							labelBgColor: "#FFFFFF",
							labelBgOpacity: 0.7,
							labelFontColor: "#666666"
						}
					}
				});
			},
			tap_a(e) {
				uCharts_Instance[e.target.id].touchLegend(e);
				uCharts_Instance[e.target.id].showToolTip(e);
			}
		},

	};
</script>


<style lang="scss">
	.charts_b {			//饼形图样式
		margin: auto;
		margin-top: 50rpx;
		width: 600rpx;
		margin-top: 100rpx;
		background-color: rgba(204, 204, 204, 0.4);
		;
		border-radius: $uni-wrapper-radio;
		box-shadow: $uni-shadowBox;
	}
	.charts_a {			//柱形图样式

		margin-top: 50rpx;
		width: 600rpx;
		margin: auto;
		height: 500rpx;
	}
	.charts {
		margin-top: 50rpx;
		height: 500rpx;
		width: 600rpx;
	}

	.chartWrapper {
		margin: auto;
		margin-top: 100rpx;
		width: 600rpx;
		background-color: rgba(204, 204, 204, 0.4);
		;
		border-radius: $uni-wrapper-radio;
		box-shadow: $uni-shadowBox;
	}
</style>
