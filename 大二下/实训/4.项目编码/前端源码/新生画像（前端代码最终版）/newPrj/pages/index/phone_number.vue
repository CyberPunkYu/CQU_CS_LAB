<template>
	<view class="container">
		<!-- 顶部面板 -->
		<!-- <view class="top--panel"> -->
		<!-- 顶部面板，可添加所需要放在页面顶部的内容代码。比如banner图 -->
		<!-- 		<view style="background-color: #ffaa00;text-align: center;font-size: 28rpx;padding: 10px 0;color: #fff;">
				<view>这里顶部内容占位区域，不需要则删除</view>
				<view>可添加需放在页面顶部的内容，比如banner图</view>
			</view>
		</view> -->
		<!-- 滚动区域 -->
		<view class="scroll-panel" id="scroll-panel">
			<view class="list-box">
				<view class="left">
					<scroll-view scroll-y="true" :style="{ height: scrollHeight + 'px' }"
						:scroll-into-view="leftIntoView">
						<view class="item" v-for="(item, index) in leftArray" :key="index"
							:class="{ active: index == leftIndex }" :id="'left-' + index" :data-index="index"
							@tap="leftTap">
							<u-text :text="item.name" 
							size="40rpx"
							align="center"></u-text>
							<!-- <u-gap height="2" bgColor="#bbb"></u-gap> -->
							<!-- {{ item.name }} -->
						</view>
						<!-- <view class="item_a"></view> -->
					</scroll-view>
				</view>
				<view class="main">
					<scroll-view scroll-y="true" :style="{ height: scrollHeight + 'px' }" @scroll="mainScroll"
						:scroll-into-view="scrollInto" scroll-with-animation="true">
						<view class="item main-item" v-for="(item, index) in mainArray" :key="index"
							:id="'item-' + index">
							<u-gap height="5" bgColor="#dfdfdf"></u-gap>
							<view class="title">
								<view>
									<u-text :text="item.name " color="#000000" 
									align="center"
									size="40rpx"></u-text>
									<!-- <u-gap height="20" bgColor="#bbb"></u-gap> -->
									<!-- <u-divider :dot="false"></u-divider> -->
								</view>
							</view>
							<view class="real_number" v-for="(item2,index2) in item.list" :key = "index2">
								<view class="right_number">
									<u-text :text ="item2.label +':\n '" 
									size="40rpx" lineHeight="80rpx"
									></u-text>
									<u-text :text = "item2.number + '\n'" size="30rpx"></u-text>
								</view>
							</view>
							<!-- <view class="goods" v-for="(item2, index2) in item.list" :key="index2"> -->
							<!-- 						<view>
									<view>第{{ index2 + 1 }}个商品标题</view>
									<view class="describe">第{{ index2 + 1 }}个商品的描述内容</view>
									<view class="money">第{{ index2 + 1 }}个商品的价格</view>
								</view> -->
							<!-- </view> -->
						</view>
						<!-- <view class="fill-last" :style="{ height: fillHeight + 'px' }"></view> -->
					</scroll-view>
				</view>
			</view>
		</view>
		<!-- 底部面板 -->
		<!-- <view class="bottom-panel"> -->
		<!-- 底部面板，可添加所需要放在页面底部的内容代码。比如购物车栏目 -->
		<!-- 			<view style="background-color: #ffaa00;text-align: center;font-size: 28rpx;padding: 10px 0;color: #fff;">
				<view>这里底部内容占位区域，不需要则删除</view>
			</view>
		</view> -->
	</view>
</template>

<script>
	import globalSetting from '@/common/json/globalSetting.json';
	import left_list from '@/common/json/left_list.json'
	import right_list from '@/common/json/right_list.json'
	export default {
		data() {
			return {
				left_list: left_list.left_list,
				right_list: right_list.right_list,

				scrollHeight: 400,
				scrollTopSize: 0,
				fillHeight: 0, // 填充高度，用于最后一项低于滚动区域时使用
				leftArray: [],
				mainArray: [],
				topArr: [],
				leftIndex: 0,
				scrollInto: ''
			};
		},
		computed: {
			/* 计算左侧滚动位置定位 */
			leftIntoView() {
				return `left-${this.leftIndex > 3 ? this.leftIndex - 3 : 0}`;
			}
		},
		onPullDownRefresh() {
			console.log('refresh');
			setTimeout(function () {
				uni.stopPullDownRefresh();
			}, 1000);
		},
		mounted() {
			/* 等待DOM挂载完成 */
			this.$nextTick(() => {
				/* 在非H5平台，nextTick回调后有概率获取到错误的元素高度，则添加200ms的延迟来减少BUG的产生 */
				setTimeout(() => {
					/* 等待滚动区域初始化完成 */
					this.initScrollView().then(() => {
						/* 获取列表数据，你的代码从此处开始 */
						this.getListData();
					});
				}, 200);
			});
		},
		methods: {
			/* 初始化滚动区域 */
			initScrollView() {
				return new Promise((resolve, reject) => {
					let view = uni.createSelectorQuery().select('#scroll-panel');
					view.boundingClientRect(res => {
						this.scrollTopSize = res.top;
						this.scrollHeight = res.height;
						this.$nextTick(() => {
							resolve();
						});
					}).exec();
				});
			},
			/* 获取列表数据 */
			getListData() {
				// Promise 为 ES6 新增的API ，有疑问的请自行学习该方法的使用。
				new Promise((resolve, reject) => {
					/* 因无真实数据，当前方法模拟数据。正式项目中将此处替换为 数据请求即可 */
					uni.showLoading();
					setTimeout(() => {
						let [left, main] = [
							[],
							[]
						];
						left = this.left_list;
						main = this.right_list;
						// 将请求接口返回的数据传递给 Promise 对象的 then 函数。
						resolve({
							left,
							main
						});
					}, 1000);
				}).then(res => {
					uni.hideLoading();
					this.leftArray = res.left;
					this.mainArray = res.main;

					// DOM 挂载后 再调用 getElementTop 获取高度的方法。
					this.$nextTick(() => {
						this.getElementTop();
					});
				});
			},

			/* 获取元素顶部信息 */
			getElementTop() {
				new Promise((resolve, reject) => {
					let view = uni.createSelectorQuery().selectAll('.main-item');
					view.boundingClientRect(data => {
						resolve(data);
					}).exec();
				}).then(res => {
					let topArr = res.map(item => {
						return item.top - this.scrollTopSize; /* 减去滚动容器距离顶部的距离 */
					});
					this.topArr = topArr;

					/* 获取最后一项的高度，设置填充高度。判断和填充时做了 +-20 的操作，是为了滚动时更好的定位 */
					let last = res[res.length - 1].height;
					if (last - 20 < this.scrollHeight) {
						this.fillHeight = this.scrollHeight - last + 20;
					}
				});
			},
			/* 主区域滚动监听 */
			mainScroll(e) {
				let top = e.detail.scrollTop;
				let index = 0;
				/* 查找当前滚动距离 */
				for (let i = this.topArr.length - 1; i >= 0; i--) {
					/* 在部分安卓设备上，因手机逻辑分辨率与rpx单位计算不是整数，滚动距离与有误差，增加2px来完善该问题 */
					if (top + 2 >= this.topArr[i]) {
						index = i;
						break;
					}
				}
				this.leftIndex = index < 0 ? 0 : index;
			},
			/* 左侧导航点击 */
			leftTap(e) {
				let index = e.currentTarget.dataset.index;
				this.scrollInto = `item-${index}`;
			}
		}
	};
</script>

<style lang="scss">
	page,
	.container {
		height: 100%;
	}

	/* 容器 */
	.container {
		display: flex; // 弹性盒子布局
		flex-direction: column; //主轴为垂直方向，起点在上沿
		flex-wrap: wrap; // 是否换行
		justify-content: center;  // 对其方式
		align-items: auto; 
		align-content: flex-start;
		
		&>view {
			width: 100%;
		}

		.scroll-panel {
			flex-grow: 1;
			height: 0;
			overflow: hidden;
		}

		.bottom-panel {
			padding-bottom: 0;
			padding-bottom: constant(safe-area-inset-bottom);
			padding-bottom: env(safe-area-inset-bottom);
		}
	}

	.list-box {
		display: flex;
		flex-direction: row;
		flex-wrap: nowrap;
		justify-content: flex-start;
		align-items: flex-start;
		align-content: flex-start;
		font-size: 40rpx;

		.left {
			width: 250rpx;
			background-color: #f5f5f5;
			line-height: 80rpx;
			box-sizing: border-box;
			font-size: 40rpx;

			.item {
				position: relative;

				&:not(:first-child) {
					margin-top: 1px;

					&::after {
						content: '';
						display: block;
						height: 0;
						border-top: #d6d6d6 solid 1px;
						width: 620upx;
						position: absolute;
						top: -1px;
						right: 0;
						transform: scaleY(0.5);
						/* 1px像素 */
					}
				}

				&.active {
					color: #42b983;
					background-color: #fff;
				}
			}

			.fill-last {
				height: 0;
				width: 100%;
				background: none;
			}
		}

		.main {
			background-color: #ffffff;
			width: 0;
			flex-grow: 1;
			box-sizing: border-box;
			border: #DCDCDC solid;

			.title {
				line-height: 64rpx;
				font-size: 24rpx;
				font-weight: bold;
				color: #666;
				background-color: #ffffff;
				position: sticky;
				top: 0;
				z-index: 19;
			}

			.item {
				border: #FFFAFA solid;
				border-bottom: #eee solid 1px;
			}
		}
	}
</style>
