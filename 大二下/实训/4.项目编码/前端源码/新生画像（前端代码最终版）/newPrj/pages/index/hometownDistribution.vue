<!-- 籍贯分布 -->
<template>
	<view>
		<view class="blank"></view>
		<qiun-data-charts 				
			  type="map"
			  class="mapFigure"
			  :opts="mapOpts"
			  :canvas2d="true"
			  :chartData="mapChartData"
			  tooltipFormat="tooltipFun" 
		/>				<!-- 地图 -->
		<scroll-view class="columnFigure" :scroll-x="true" :style="{height: columnFigureHeight+'px',marginTop: columnFigureMargin+'px',marginDown:columnFigureMargin+'px'}">
			  <view class="charts-box" :style="{height: columnFigureHeight+'px',width: columnCityNum*100+'rpx'}">
			    <qiun-data-charts 
					type="column"
					:opts="columnOpts"
					:chartData="columnChartData"
			    />
			  </view>
		</scroll-view>			<!-- 滚动柱状图 -->
	</view>
</template>

<script>
	import globalSetting from '@/common/json/globalSetting.json';
	import mapdata from '@/common/json/gui_zhou_province.json';
	import uCharts from '@/uni_modules/qiun-data-charts/js_sdk/u-charts/config-ucharts.js'
	var uChartsInstance = {};
	export default {
		data() {
			return {
				isNetworkBusy: true, // 网络繁忙问题
				// 城市及报道人数
				cityReportInfo:null,
				// 组件参数设置
				windowHeight:1500,
				columnFigureHeight:100,
				columnFigureMargin:100,
				columnCityNum:30,			//柱状图城市个数
				// 柱状图统计图表设置
				columnChartData: {},		//柱状图数据
				columnOpts: {				//柱状图样式设置
					color: ["#5555ff","#91CB74","#FAC858","#EE6666","#73C0DE","#3CA272","#FC8452","#9A60B4","#ea7ccc"],
					padding: [15,15,0,5],
					legend: {},
					xAxis: {
						disableGrid: true
					},
					yAxis: {
						data: [
							{
								min: 0
							}
						]
					},
					extra: {
						column: {
							type: "group",
							width: 30,
							activeBgColor: "#000000",
							activeBgOpacity: 0.08
						}
					},
				},
				// 地图统计图表设置
				mapChartData: {
					series:[]
				},
				mapOpts: {
					color: ["#1890FF","#91CB74","#FAC858","#EE6666","#73C0DE","#3CA272","#FC8452","#9A60B4","#ea7ccc"],
					padding: [0,0,0,0],
					dataLabel: false,
					extra: {
						map: {
							border: false,
							borderWidth: 1,
							borderColor: "#666666",
							fillOpacity: 0.6,
							activeBorderColor: "#F04864",
							activeFillColor: "#FACC14",
							activeFillOpacity: 1,
							mercator: true
						},
					},
				}
			}
		},
		
		async created() {		//组织图表，获取信息
			uni.showToast({
				duration:globalSetting.TIME_OUT,
				icon:"loading",
			})
			await this.getServerColumnData();		//获取统计图表信息
			await this.getServerMapData(); 
			uni.hideToast();
			uCharts.formatter.tooltipFun = (item, category, index, opts) => {
				return `${item.name}\n已报道: ${item.reportNum} 人`;
			}
		},
		
		onPullDownRefresh() {		//下拉刷新
			setTimeout(function () {
				uni.stopPullDownRefresh();
			}, 1000);
		},
		onLoad() {					//加载时高度自适应
			var sysInfo=uni.getSystemInfoSync();
			this.windowHeight=sysInfo.windowHeight;
			this.columnFigureHeight=sysInfo.windowHeight*0.4;
			this.columnFigureMargin=sysInfo.windowHeight*0.05;
		},
		methods: {
			showPromptOfBusyNetwork(){			//网络繁忙弹出提示
				uni.showModal({
					showCancel:false,
					content:"网络繁忙，请稍后重试！",
				})
			},
		    async getServerColumnData() {			//获取柱状图数据
				await uni.request({
					url: globalSetting.API_SITE_INFO+"/getOriginDistribution",
					method:"GET"
				}).then(
					(data)=>{
						var [err,res] = data;
						if (err){
							this.isNetworkBusy=true;
							this.showPromptOfBusyNetwork();
						}
						else{			
							this.isNetworkBusy=false;
							this.columnChartData=res.data;
							this.cityReportInfo=res.data;
						}
					}
				)
		    },
			
			getServerMapData() {					//获取地图数据
				let mapSeries=mapdata.features.map( (item)=>{
					item.reportNum=0;		//对应区县未找到则报道为0人
					for (var i=0;i<this.cityReportInfo.categories.length;i++){		//获取对应区县报道人数
						if(this.cityReportInfo.categories[i]==item.properties.name){
							item.reportNum=this.cityReportInfo.series[0].data[i];
						}
					}
					return item;
				})
				this.mapChartData.series=mapSeries;
			},
		}
	}
</script>

<style lang="scss">
	.titleFontStyle{
		font-size: 3ch;
		color: darkblue;
	}
	.blank{			//顶部空白栏
		width: 200rpx;
		height:100rpx;
	}
	.mapFigure{		//地图样式
		margin: auto;
		width: 600rpx;
		background-color: rgba(204, 204, 204, 0.4);;
		border-radius: $uni-wrapper-radio;
		box-shadow: $uni-shadowBox;
	}
	.columnFigure{		//柱状图背景
		margin: auto;
		width: 600rpx;
		background-color: rgba(204, 204, 204, 0.4);;
		border-radius: $uni-wrapper-radio;
		box-shadow: $uni-shadowBox;
	}
</style>