<!-- 导航页面 -->

<template>
	<view>
		<image class="imgSty" src="/static/globalBgImg2.png"></image>		<!-- 背景图片 -->
		<u-swiper
				:list="imageList"
				indicator
				indicatorMode="line"
				circular
		></u-swiper>		<!-- 轮播图 -->
		<view class="gridBgWrapper">		<!-- 灰色透明方框背景 -->
			<u-grid class="gridWrapper" :style="{height: wrapperHeight+'px',marginTop: wrapperMargin+'px'}" col=2 :border="true">		<!-- 使用uView的宫格布局，两列 -->
				<u-grid-item :style="{height: buttonHeight+'px'}" >		<!-- 报道进度 -->
					<u-icon name="hourglass-half-fill" :size="46" color=#ff381e 
					@click="reportProgressNavigation" 
					label="报道进度" labelPos="bottom" labelColor=#000000></u-icon>
				</u-grid-item>
				<u-grid-item :style="{height: buttonHeight+'px'}" >		<!-- 性别分布 -->
					<u-icon name="/static/gender.png" :size="46" 
					@click="genderDistributionNavigation" 
					label="性别分布" labelPos="bottom" labelColor=#000000></u-icon>
					<view class="grid-text"></view>
				</u-grid-item>
				<u-grid-item :style="{height: buttonHeight+'px'}" >		<!-- 年龄分布 -->
					<u-icon name="calendar" :size="46" color=#ffa914 
					@click="ageDistributionNavigation"
					label="年龄分布" labelPos="bottom" labelColor=#000000></u-icon>
				</u-grid-item>
				<u-grid-item :style="{height: buttonHeight+'px'}" >		<!-- 专业分布 -->
					<u-icon name="order" :size="46" color=#ef03ff 
					@click="majorityDistributionNavigation"
					label="专业分布" labelPos="bottom" labelColor=#000000></u-icon>
				</u-grid-item>
				<u-grid-item :style="{height: buttonHeight+'px'}">		<!-- 籍贯分布 -->
					<u-icon name="home" :size="46" color=#338bff 
					@click="hometownDistributionNavigation"
					label="籍贯分布" labelPos="bottom" labelColor=#000000></u-icon>
				</u-grid-item>
				<u-grid-item :style="{height: buttonHeight+'px'}" >		<!-- 姓氏统计 -->
					<u-icon name="/static/familyname.png" :size="46" color=#aa007f 
					@click="familyNavigation" 
					label="姓氏统计" labelPos="bottom" labelColor=#000000></u-icon>
				</u-grid-item>
			</u-grid>
		</view>
	</view>
</template>

<script>
	import globalSetting from '@/common/json/globalSetting.json';		//全局变量引入
	export default {
		data() {
			return {
				imageList:[
					"/static/swiper1.jpg",
					"/static/swiper2.png",
					"/static/swiper3.jpg",
				],					//轮播图列表
				windowHeight: 1650,		//自适应高度参数，下同
				topImageHeight: 900,	
				wrapperHeight:900,
				wrapperMargin:200,
				buttonHeight:300,
			}
		},
		onPullDownRefresh() {			//下拉刷新函数(回退刷新图标)
			console.log('refresh');
			setTimeout(function () {
				uni.stopPullDownRefresh();
			}, 1000);
		},
		onLoad() {
			var sysInfo = uni.getSystemInfoSync();		//动态获取页面高度
			this.windowHeight=sysInfo.windowHeight;
			this.topImageHeight=this.windowHeight*0.25;
			this.wrapperHeight=this.windowHeight*0.60;
			this.buttonHeight=this.wrapperHeight/3;
			this.wrapperMargin=(this.windowHeight-this.topImageHeight-this.wrapperHeight)/3;
		},
		methods: {
			reportProgressNavigation(){				//导航至报道进度页面
				uni.navigateTo({
					url:"/pages/index/reportProgress",
				})
			},
			genderDistributionNavigation(){			//导航至性别分布页面
				uni.navigateTo({
					url:"/pages/index/genderDistribution",
				})
			},
			ageDistributionNavigation(){			//导航至年龄分布页面
				uni.navigateTo({
					url:"/pages/index/ageDistribution",
				})
			},
			majorityDistributionNavigation(){		//导航至专业分布页面
				uni.navigateTo({
					url:"/pages/index/majorDistribution",
				})
			},
			hometownDistributionNavigation(){		//导航至籍贯分布页面
				uni.navigateTo({
					url:"/pages/index/hometownDistribution",
				})
			},
			familyNavigation(){						//导航至籍贯分布页面		
				uni.navigateTo({
					url:"/pages/index/familyName",
				})
			},
		}
	}
</script>

<style lang="scss">
	.gridWrapper{							//宫格布局整体设置
		width: 600rpx;
		margin: auto;
	}
	.gridBgWrapper{							//背景方框设置
		width: 600rpx;
		margin: auto;
		background-color: rgba(204, 204, 204, 0.2);
		border-radius: 30rpx;
		// box-shadow: $uni-shadowBox;
	}
	.imgSty{								//背景图片
		z-index:-1; 
		width:100%; 
		height:100%; 
		position: fixed; 
		top:0; 
	}
</style>