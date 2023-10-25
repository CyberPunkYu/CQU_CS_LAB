<template>
	<view>
		<!-- 添加空格实现界面的优化 -->
		<view class="blank"></view> 
		<!-- 学校徽标 -->
		<view class="imageContent">
			<image style="width: 350rpx; height: 350rpx;" src="/static/schoolLogo.png" mode="scaleToFill"
				@error="imageError"></image>
		</view>
		<!-- 登录界面的背景图 -->
		<view>
			<image class="backgroundp" src="/static/bc2.png"></image>
		</view>
		<!-- 登录界面的中间提示文字 -->
		<view class="load">
			<text class="text">欢迎登录</text>
		</view>
		<!-- 登录的表单 -->
		<view class="form-content">
			<u-form :model="form" ref="uForm" label-width="50">
				<!-- 准考证号输入框，限制字体大小输入格式、长度；和提示的前置图标与提示输入的文字 -->
				<u-form-item prop="student_number">
					<u-input prefixIcon="account-fill" prefixIconStyle="font-size: 22px;color: #909399"
						v-model="form.student_number" clearable shape="circle" :adjustPosition="false"
						maxlength=9
						placeholder="请输入准考证号" />
				</u-form-item>
				<!-- 密码输入框 -->
				<u-form-item prop="student_password">
					<u-input prefixIcon="lock" type="password" prefixIconStyle="font-size: 22px;color: #909399"
						v-model="form.student_password" clearable shape="circle" :adjustPosition="false"
						maxlength=16
						placeholder="请输入密码" />
				</u-form-item>
				<!-- 提交按钮 -->
				<u-button class="custom-style" :disabled="isLogining" :loading="isLogining" shape="circle" size="medium"
					@click="loginRequest">登录</u-button>
				</u-button>
			</u-form>


		</view>
	</view>
</template>

<script>
	import globalSetting from '@/common/json/globalSetting.json'; // 针对服务器的api，url,还有对于页面加载的时间延迟，设置全局变量，优化代码
	export default {
		data() {
			return {
				isLoginRequestCommited: false, // 是否可以登录
				isInfoRecorded: false, // 是否已经录入了信息
				isNetworkBusy: true, // 网络繁忙
				isLogining: false, // 加载提示
				
				// 通过v-model连接的输入变量
				form: {
					student_number: '',
					student_password: ''
				},
				// form表单的rules规则，即红色字体提示
				rules: {
					student_number: [{
						required: true,
						message: '请输入准考证号',
						trigger: ["change", "blur"],
					}, {
						pattern: /^[0-9a-zA-Z]*$/g, // 正则表达式限制输入只能是字母或则数字
						transform(value) {
							return String(value);
						},
						message: '只能包含字母或数字',
						trigger: ["change", "blur"],
					}, {
						max: 20,
						message: "准考证长度不能超过20",
						trigger: ["change", "blur"],
					}],
					student_password: [{
							required: true,
							message: '请输入密码',
							trigger: 'blur'
						},
						{
							pattern: /^[0-9a-zA-Z]*$/g,
							transform(value) {
								return String(value);
							},
							message: '只能包含字母或数字',
							trigger: ["change", "blur"],
						},
						{
							min: 6,
							max: 16,
							message: "密码长度为6~16位",
							trigger: ["change", "blur"],
						}
					]
				}
			};
		},
		
		// 页面加载的时候触发的函数
		onLoad() {
			uni.setNavigationBarTitle({ // 动态设置但前页面的标题
				title: "登录",
			})
			uni.preloadPage({ //预加载页面
				url:"/pages/index/navigation/navigation_homepage",
			})
			uni.preloadPage({
				url:"/pages/index/mapSearch",
			})
		},
		
		//停止当前页面的下拉刷新
		onPullDownRefresh() {
			setTimeout(function() {
				uni.stopPullDownRefresh();
			}, 1000);
		},
		
		methods: {
			//显示弹窗，封装为一个函数，优化代码结构
			showPrompt(text) {
				uni.showModal({
					content: text,
					showCancel: false,
				})
			},

			async loginRequest() { //点击登录后触发的函数
				this.isLogining = true; //加载提示
				
				this.$refs.uForm.validate().then( // form表单rules规则的判定语句，如果rules规则格式错误则不会执行登录功能
					async res => { // 同异步处理
						// 判断输入是否为空
						var userNameIsEmpty = (this.form.student_number == "");
						var passwordIsEmpty = (this.form.student_password == "");
						if (userNameIsEmpty || passwordIsEmpty) { //判断输入内容是否为空
							this.showPrompt("准考证号和密码不能为空！");
							this.isLogining = false;
							return;
						}
						
						await this.sendRequest(); //发起请求判断用户名和密码是否正确
						// 检测当前网路是否正常
						if (this.isNetworkBusy == true) {
							this.showPrompt("网络繁忙，请稍后重试");
						} else if (this.isLoginRequestCommited == true) { //允许登录
							uni.setStorageSync("EASYCMP_ID", this.form.student_number);			//ID缓存至本地，利于后期的优化
							this.removeInfoFromCache();											//清除数据，防止数据因本地缓存在后期造成冲突（如单机登录多号）
							uni.showToast({
								icon: "success",
								content: "登录成功",
							})
							if (this.isInfoRecorded == true) { //信息已录入
								uni.switchTab({
									url: "/pages/index/navigation/navigation_homepage"
								})
							} else { //信息未录入
								uni.navigateTo({
									url: "/pages/index/infoSubmission"
								})
							}
						} else { //拒绝登录
							this.showPrompt("用户名或密码错误，请检查重试");
						}
						this.isLogining = false; // 加载提示消失
						return;
					}
				).catch(
					error => {
						this.isLogining=false;
						this.showPrompt("填写信息有误，请确认后重试");
					}
				)
				
			},

			async sendRequest() { //TODO:超时判定
				var isLoginRequestCommited;
				await uni
					.request({
						url: globalSetting.API_SITE_STU + '/loginService', // 登录的url,这是设置了全局的API

						data: { // request传输的数据
							sUserName: this.form.student_number,
							sPassword: this.form.student_password, //TODO:MD5加密
						},
						method: "POST", // POST http网路请求
						timeout: globalSetting.TIME_OUT, // 全局变量的时间限制
					}).then((data) => { // 请求成功从后端返回的数据
						var [err, res] = data;
						if (err != null) { // data为一个数组，其中的0位是返回的错误信息，如果为null则表示网络正常
							this.isNetworkBusy = true;
						} else {
							this.isNetworkBusy = false;
							this.isLoginRequestCommited = res.data.isLoginRequestCommited; // 接受后端返回的数据，验证是否可以正常登录
							this.isInfoRecorded = res.data.isInformationRecorded; // 接受后端返回的数据，验证是否已经进行了录入信息
						}
					});
				return;
			},

			removeInfoFromCache() { //清除缓存，防止上一账号的信息通过缓存在个人中心加载到新号
				uni.removeStorageSync("EASYCMP_AVATAR");
				uni.removeStorageSync("EASYCMP_NAME");
				uni.removeStorageSync("EASYCMP_GENDER");
				uni.removeStorageSync("EASYCMP_AGE");
				uni.removeStorageSync("EASYCMP_ORIGIN");
				uni.removeStorageSync("EASYCMP_MAJOR");
				uni.removeStorageSync("EASYCMP_CLASS");
			},

		},
		// 必须要在onReady生命周期，因为onLoad生命周期组件可能尚未创建完毕
		onReady() {
			this.$refs.uForm.setRules(this.rules);
		}
	};
</script>

<style scoped lang="scss">
	//顶部的空格
	.blank {
		width: 50rpx;
		height: 50rpx;
		margin: auto;
		margin-bottom: 50rpx;
	}
	//学校的徽标
	.imageContent {
		margin: auto;
		margin-bottom: 50rpx;
		width: 350rpx;
		height: 350rpx;
	}
	
	// 页面背景中间的提示文字
	.text {
		font-size: 50rpx;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		margin-bottom: 50rpx;
	}
	
	// form表单
	.form-content {
		margin-top: 50rpx;
		width: 400rpx;
		height: 350rpx;
		margin: auto;
		padding: 30px;
		border: #e2e2e2 solid;
		border-radius: 25px;
	}
	
	// 提交按钮
	.custom-style {
		margin-top: 50rpx;
		color: #000000;
		width: 250rpx;
		background-color: #ffffff;
		border: 1px solid #bcbcbc;
	}
	
	// 登录页面的背景图
	.backgroundp {
		z-index: -1;
		width: 100%;
		height: 100%;
		position: fixed;
		top: 0;
	}
</style>
