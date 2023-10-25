<!-- 性别分布 -->

<template>
	<view class="content">
		<view class="charts-box">			<!-- 图表 -->
		    <qiun-data-charts type="pie" :chartData="pieData" :opts="ringOpts"/>
		</view>
		<view class="img">					<!-- 图片 -->
			<view class="img1">
				<img src="/static/male.png" width="200rpx"></img>
				<text class="text-area1">{{a}}</text>
			</view>
			<view class="img2">
				<img src="/static/female.png" width="200rpx"></img>
				<text class="text-area2">{{b}}</text>
			</view>
		</view>
	</view>
</template>

<script>
	import globalSetting from '@/common/json/globalSetting.json';
    export default {
		data() {
		    return {
				isNetworkBusy: true,		//网络繁忙标志位
				a:'',
				b:'',
				barData:{	
				},
		        pieData: {
		        },
				ringOpts:{
					title:{
						name:"男女占比",
					},
					subtitle:{
						name:"",
					},
					color:['#187ccf', '#ed90bb']
				},
		    }
		},
		async onLoad() {		//读取数据
			uni.showToast({
				duration:globalSetting.TIME_OUT,
				icon:"loading",
			})
		    await this.getServerData();
			uni.hideToast();
		},
		onPullDownRefresh() {	//下拉刷新
			console.log('refresh');
			setTimeout(function () {
				uni.stopPullDownRefresh();
			}, 1000);
		},
		methods: {
			showPromptOfBusyNetwork(){		//网络繁忙提示框
				uni.showModal({
					showCancel:false,
					content:"网络繁忙，请稍后重试！",
				})
			},
			async getServerData() {			//从服务器获取数据
				await uni.request({
				    url: globalSetting.API_SITE_INFO+"/getGenderDistribution",
					method:"GET",
					timeout:globalSetting.TIME_OUT,//5秒超时
					}).then((data)=>{
						var[err,res] = data;
						if (err){
							this.isNetworkBusy=true;		//err不为空说明网络存在问题
						}
						else{
							this.isNetworkBusy=false;
							var resdata={				//组织图表数据
								"series":[
									{"name":"男生已到比例","data":res.data.malePercent},
									{"name":"女生已到比例","data":res.data.femalePercent},
								]
							};
							this.barData=JSON.parse(JSON.stringify(resdata));
							resdata={
								"series":[
									{"name":"男生","data":res.data.maleCount},
									{"name":"女生","data":res.data.femaleCount},
								]
							};
							this.pieData=JSON.parse(JSON.stringify(resdata));
							this.a=res.data.maleCount;
							this.b=res.data.femaleCount;}
							if (this.isNetworkBusy==true){
								this.showPromptOfBusyNetwork();
							}
						});
						return;
		    },
		  },
    }
</script>

<style lang="scss">
	.content {				//整体样式
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		font-size: 70rpx;
		margin-bottom: 50rpx;
		background-image: src("/static/1.png");
	}
	.charts-box{		//图表背景样式
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		width: 600rpx;
		margin: auto;
		margin-top: 100rpx;
		background-color: rgba(204, 204, 204, 0.4);
		border-radius: 30rpx;
		box-shadow: $uni-shadowBox;
	}
	.img{				//外层样式
		display: flex;
		flex-direction: row;
		justify-content: center;
		align-items: center;
		margin-top: 50rpx;
	}
	.img1{				//图一样式
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}
	.img2{				//图二样式
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}
	.text-area1{		//男生数据样式
		width: 200rpx;
		font-size: 50rpx;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		margin-top: 30rpx;
		color: #187ccf;
	}
	.text-area2{		//女生数据样式
		width: 200rpx;
		font-size: 50rpx;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		margin-top: 30rpx;
		color: #ed90bb;
	}
</style>
