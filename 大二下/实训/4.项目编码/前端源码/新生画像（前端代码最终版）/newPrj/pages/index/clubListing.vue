<template>
	<view>
		<u-list>
			<u-list-item
				v-for="(item, index) in clubList"
				:key="index"
			>			<!-- 使用v-for进行数据展示 -->
			<u-avatar class="avatarWrapper" :src=item.url size=130></u-avatar>		<!-- 头像 -->
			<scroll-view class="clubWrapper" :scroll-y="true">						<!-- 信息框,使用滚动视窗以便于存放更多信息,同时不影响用户观感-->
				<u-text 
				:text="' - 社团名称：'+item.name
					+'\n - 联系方式：'+item.tel
					+'\n - 社团介绍：'+item.intro">
				</u-text>
			</scroll-view>
			<u-divider :dot="false"></u-divider>									<!-- 分割线 -->
			</u-list-item>
		</u-list>
	</view>
</template>

<script>
	import globalSetting from '@/common/json/globalSetting.json';		//全局变量
	import clubList from '@/common/json/clubList.json';					//社团信息,以json格式存储在/common/json中
	export default{
		data(){
			return{
				clubList: clubList.clubList,							//社团信息,以列表形式提取
			}
		},
		onPullDownRefresh() {		//下拉刷新函数
			console.log('refresh');
			setTimeout(function () {
				uni.stopPullDownRefresh();
			}, 1000);
		},
		onLoad(){					//加载时弹出模态提示框
			this.showPrompt();
		},
		methods:{
			showPrompt(){
				uni.showModal({
					showCancel:false,
					content:"***温馨提示***\n下拉屏幕可查看更多社团\n下拉社团资料卡可查看更多信息",
				})
			},
		},
	}
</script>

<style lang="scss">
	.clubWrapper{			//社团信息卡样式
		width: 500rpx;
		height: 200rpx;
		margin: auto;
		margin-top: 20rpx;
		margin-bottom: 50rpx;
		background-color: rgba(204, 204, 204, 0.4);
		border-radius: 30rpx;
		box-shadow: $uni-shadowBox;
		padding: 20rpx;
        flex: auto;
        display: flex;
        flex-direction: column;
        justify-content: center;
	}
	.avatarWrapper{		//头像样式
		display: block;
		margin: 0 auto;
		width: 400rpx;
		margin-top: 40rpx;
	}
</style>