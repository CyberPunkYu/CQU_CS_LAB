<template>
	<view>
		<view class="gridBgWrapper" 		
		:style="{height: wrapperHeight+'px',
				marginTop: wrapperMargin+'px',
				marginBottom: wrapperMargin+'px'}" 
		@click="navToClub">			<!-- 图标背景方框，下面同理 -->
			<u-icon :style="{height: wrapperHeight+'px'}" name="tags" :size="46" color=#ffaa00
			label="社团信息" labelPos="bottom" labelColor=#000000 labelSize="23"></u-icon>
		</view>						<!-- icon图标，下面同理 -->
		<view class="gridBgWrapper" 
		:style="{height: wrapperHeight+'px',
				marginTop: wrapperMargin+'px',
				marginBottom: wrapperMargin+'px'}"
		@click="navToMap">
			<u-icon :style="{height: wrapperHeight+'px'}" name="map" :size="46" color=#45aa35
			label="校园地图" labelPos="bottom" labelColor=#000000 labelSize="23"></u-icon>
		</view>
		<view class="gridBgWrapper"
		:style="{height: wrapperHeight+'px',
				marginTop: wrapperMargin+'px',
				marginBottom: wrapperMargin+'px'}"
		@click="navToPhone">
			<u-icon :style="{height: wrapperHeight+'px'}" name="phone" :size="46" color=#1ea5ff 
			label="常用电话" labelPos="bottom" labelColor=#000000 labelSize="23"></u-icon>
		</view>
		<view class="gridBgWrapper" 
		:style="{height: wrapperHeight+'px',
				marginTop: wrapperMargin+'px',
				marginBottom: wrapperMargin+'px'}"
		@click="navToAttention">
			<u-icon :style="{height: wrapperHeight+'px'}" name="error-circle" :size="46" color=#ea0003 
			label="注意事项" labelPos="bottom" labelColor=#000000 labelSize="23"></u-icon>
		</view>
	</view>
</template>

<script>
	import globalSetting from '@/common/json/globalSetting.json';
	export default{
		data(){
			return{
				wrapperHeight:300,
				wrapperMargin:300,
			}
		},
		onPullDownRefresh() {
			console.log('refresh');
			setTimeout(function () {
				uni.stopPullDownRefresh();
			}, 1000);
		},
		onLoad(){
			var sysInfo = uni.getSystemInfoSync();					//高度自适应设置
			this.wrapperHeight=sysInfo.windowHeight*0.14;
			this.wrapperMargin=sysInfo.windowHeight*0.06;
			uni.setNavigationBarTitle({
				title: '校园'
			});
		},
		methods:{
			navToPersonalCenter(){									//底部导航栏，导航至个人中心
				uni.navigateTo({
					url:"/pages/index/navigation/personalInfoCenter",
				})
			},
			navToHomepage(){										//底部导航栏，导航至首页
				uni.navigateTo({
					url:"/pages/index/navigation/navigation_homepage",
				})
			},
			navToClub(){											//屏幕按钮，导航至社团信息
				uni.navigateTo({
					url:"/pages/index/clubListing",
				})
			},	
			navToAttention(){										//屏幕按钮，导航至注意事项
				uni.navigateTo({
					url:"/pages/index/warningList",
				})
			},
			navToMap(){										//屏幕按钮，导航至校园地图
				uni.navigateTo({
					url:"/pages/index/mapSearch",
				})
			},
			navToPhone(){										//屏幕按钮，导航至常用电话
				uni.navigateTo({
					url:"/pages/index/phone_number",
				})
			}
		}
	}
</script>

<style lang="scss">
	.gridBgWrapper{			
		width: 500rpx;
		margin: auto;
		background-image: linear-gradient(to bottom right, #f5f5f4, #fffffe);
		border-radius: 30rpx;
		box-shadow: $uni-shadowBox;
	}		//图标背景方框
</style>