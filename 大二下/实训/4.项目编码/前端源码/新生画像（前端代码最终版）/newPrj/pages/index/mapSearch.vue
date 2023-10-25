<template>
	<view class="content" >
		<view class="map_a">
			<image class="img" src="/static/huxi.jpg" @click="clickImg1"></image>
		</view>
		<!-- <image class="img" src="/static/huxi.jpg" @click="clickImg1"></image> -->
		<view class="map_b">
			<image class="img" src="/static/huxipic.png" @click="clickImg2"></image>
		</view>
		<!-- <image class="img" src="/static/huxipic.png" @click="clickImg2"></image> -->
	</view>
</template>

<script>
	import globalSetting from '@/common/json/globalSetting.json';
	export default {
		onPullDownRefresh() {		//下拉刷新，进行回弹
			console.log('refresh');
			setTimeout(function () {
				uni.stopPullDownRefresh();
			}, 1000);
		},
		methods: {
			clickImg1() {
				uni.previewImage({
					urls: ["/static/huxi.jpg"], //需要预览的图片http链接列表，多张的时候，url直接写在后面就行了
					current: '', // 当前显示图片的http链接，默认是第一个
					success: function(res) {},
					fail: function(res) {},
					complete: function(res) {},
				})
			},
			
			clickImg2() {
				uni.previewImage({
					urls: ["/static/huxipic.png"], //需要预览的图片http链接列表，多张的时候，url直接写在后面就行了
					current: '', // 当前显示图片的http链接，默认是第一个
					success: function(res) {},
					fail: function(res) {},
					complete: function(res) {},
				})
			},
		}
	}
</script>

<style>
	.content {		//外部视窗样式
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		width: 600rpx;
		margin: auto;
	}
	.map_a{			//第一个地图的样式
		margin: auto;
		width: 600rpx;
		border-radius: $uni-wrapper-radio;
		box-shadow: $uni-shadowBox;

	}
	.img {			//图像样式
		width: 600rpx;
		margin: auto;
		margin-top: 100rpx;
		margin-left: auto;
		margin-right: auto;
		outline:#5555ff ;
		outline-width: 25rpx;
		outline-style: groove;
	}
</style>
