<!-- 密码修改 -->

<template>
	<view class="form-content">
		<!-- form表单 -->
		<u-form :model="form" ref="uForm" label-width="70">
			<u-form-item label="原密码" prop="original_password" borderBottom="true">
				<u-input inputAlign="center" v-model="form.original_password" border="false" placeholder = "填写原密码" 
				maxlength=16
				type="password" 
				/>
			</u-form-item>
			<u-form-item label="新密码" prop="new_password" borderBottom="true" >
				<u-input inputAlign="center" v-model="form.new_password" border="false" placeholder = "填写新密码"
				 maxlength=16
				 type="password" 
				 />
			</u-form-item>
			<u-form-item label="确认密码" prop="check_password" borderBottom="true">
				<u-input inputAlign="center" v-model="form.check_password" border="true" placeholder = "再次填写确认"
				 maxlength=16
				 type="password"
				 />
			</u-form-item>
		</u-form>
		
		<!-- 提交按钮 -->
		<u-button class="custom-style" :disabled="isSubmitting" :loading="isSubmitting" shape="circle" size="medium" type="primary" @click="submitPwd">修改密码</u-button>
	</view>
</template>

<script>
	import globalSetting from '@/common/json/globalSetting.json';  // 设置全局变量
	export default {
		data() {
			return {
				isSubmitting:false, // loading的缓存
				isNetworkBusy:false, // 网络是否繁忙
				
				OldpwdCheck:false, // 旧密码是否正确
				OldnewCheck:false, // 新密码是否正确
				ChangeSuccess:false, //更改密码是否成功
				form: {
					original_password: '',
					new_password: '',
					check_password: ''
				},
				rules: {
					original_password: [{
						required: true,
						message: '请输入旧密码',
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
						min:6,
						max:16,
						message:"密码长度为6~16位",
						trigger: ["change", "blur"],
					}
					],
					new_password: [{
						required: true,
						message: '请输入新密码',
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
						min:6,
						max:16,
						message:"密码长度为6~16位",
						trigger: ["change", "blur"],
					}
					],
					check_password: [{
							required: true,
							message: '请确认新密码',
							trigger: ['change', 'blur'],
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
							min:6,
							max:16,
							message:"密码长度为6~16位",
							trigger: ["change", "blur"],
						}
					]
				}
			};
		},
		
		// 加载过程的设置动态标题
		onLoad() {
			uni.setNavigationBarTitle({
				title:"修改密码"
			})
		},
		
		// 下拉刷新
		onPullDownRefresh() {
			console.log('refresh');
			setTimeout(function () {
				uni.stopPullDownRefresh();
			}, 1000);
		},
		
		methods: {
			showPrompt(promptText){
				uni.showModal({
					showCancel:false,
					content:promptText,
				})
			},
			
			async submitPwd(){				//点击修改密码按钮后触发的函数
				this.isSubmitting=true;
				this.$refs.uForm.validate().then( // rules规则判定
					async res =>{
						if(this.isExistEmpty()==true){ // 判断信息是否为空
							this.isSubmitting=false;
							uni.hideToast();
							return;
						}
						await this.submitPwdRequest();
						if (this.isNetworkBusy==true){
							this.showPrompt("网络繁忙，请稍后重试！");
						}
						this.isSubmitting=false;
					}
				).catch(
					error => {
						this.isSubmitting=false;
						this.showPrompt("填写信息有误，请确认后重试");
						return;
					}
				)
			},
			
			// 判断信息录入是否为空
			isExistEmpty(){
				var oldpasswordIsEmpty=(this.form.original_password=="");
				var newpasswordIsEmpty=(this.form.new_password=="");
				var newpasswordIsEmpty_ok=(this.form.check_password=="");
				if (oldpasswordIsEmpty || newpasswordIsEmpty||newpasswordIsEmpty_ok){		//判断输入内容是否为空
					this.showPrompt('填写内容不能为空'); //判空
					return true;
				}
				return false;
			},
			
			// 修改密码与后端进行交互
			async submitPwdRequest(){				
				await this.sendRequest();	//发起请求
				if (this.OldpwdCheck==true&&this.OldnewCheck==true&&this.ChangeSuccess==true){					//允许修改
					uni.showToast({
						icon: "success",
						title: "修改成功",
						duration:500,
					})
					setTimeout(
						function(){ // 页面跳转
							uni.switchTab({
								url: "/pages/index/navigation/personalInfoCenter"
							})
						},500
					);
				}
				else if(this.OldpwdCheck==false&&this.OldnewCheck==false&&this.ChangeSuccess==false){										
					this.showPrompt('原密码不正确'); //旧密码输入错误
				}else if(this.OldpwdCheck==true&&this.OldnewCheck==true&&this.ChangeSuccess==false){
					this.showPrompt('两次填写的密码不一致'); //两次新密码不相同
				}else if(this.OldpwdCheck==true&&this.OldnewCheck==false&&this.ChangeSuccess==false){
					this.showPrompt('原密码不能与新密码相同');//新密码不能与旧密码相同
				}
			},
			
			// request请求传输数据
			async sendRequest(){
				await uni
					.request({
				    url: globalSetting.API_SITE_STU+'/changePassword',
					data: {
				        oldPassword:this.form.original_password,
						newPassword:this.form.new_password,
						repeatedPassword:this.form.check_password,
						ID:uni.getStorageSync("EASYCMP_ID"),		
				    },
					method:"POST",
					header:{
						"content-type":"application/json",
					},
					timeout:globalSetting.TIME_OUT,
				}).then((data)=>{
						console.log(data);
						var[err,res]=data;
						if (err!=null){
							this.isNetworkBusy=true;
						}
						else{
							this.isNetworkBusy=false;
							this.OldpwdCheck=res.data.oldpwdCheck;
							this.OldnewCheck=res.data.oldnewCheck;
							this.ChangeSuccess=res.data.changeSucceed;
						}
					});
				return;
			},
		},
		
		onReady() {
			this.$refs.uForm.setRules(this.rules);
		}
	};
</script>

<style scoped lang="scss">
	// form表单
	.form-content {
		width: 500rpx;
		height: 500rpx;
		margin: auto;
		margin-top: 150rpx;
		padding-left: 20px;
		padding-top: 30px;
		padding-right: 30px;
	}
	
	// 提交按钮
	.custom-style{
		margin-top: 200rpx;
		width: 250rpx;
	}
</style>