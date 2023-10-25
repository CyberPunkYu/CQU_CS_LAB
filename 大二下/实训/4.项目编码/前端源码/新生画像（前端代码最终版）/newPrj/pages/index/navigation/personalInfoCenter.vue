<template>
	<view>
		<u-avatar class="imageStyle" :src="imgsrc"  size=200></u-avatar>		<!-- 头像设置 -->
		<u-cell-group>															<!-- 下面为uView的cell组件，依次为姓名，性别，年龄，籍贯，专业，班级，更改信息和修改密码 -->
			<u-cell title="姓名" :value="sName" size="large"></u-cell>
		</u-cell-group>
		<u-gap height="10rpx" bgColor="#e8e8e8"></u-gap>
		<u-cell-group>
			<u-cell title="性别" :value="sGender" size="large"></u-cell>
			<u-cell title="年龄" :value="nAge" size="large"></u-cell>
			<u-cell title="籍贯" :value="sOrigin" size="large"></u-cell>
		</u-cell-group>
		<u-gap height="10rpx" bgColor="#e8e8e8"></u-gap>
		<u-cell-group>
			<u-cell title="专业" :value="sMajor" size="large"></u-cell>
			<u-cell title="班级" :value="sClass+'班'" size="large"></u-cell>
		</u-cell-group>
		<u-gap height="10rpx" bgColor="#e8e8e8"></u-gap>
		<u-cell-group>
			<u-cell icon="list" title="更改信息" :isLink="true" arrow-direction="right" @click="navToEditInfo"></u-cell>
			<u-cell icon="lock" title="修改密码" :isLink="true" arrow-direction="right" @click="navToEditPwd"></u-cell>
		</u-cell-group>
	</view>
	
</template>

<script>
	import globalSetting from '@/common/json/globalSetting.json';			//引入全局变量
	export default{
		data(){
			return{
				imgsrc:"",	//头像路径
				sName:"",	//姓名
				sGender:"",	//性别
				nAge:null,	//年龄
				sOrigin:"",	//籍贯
				sClass:"",	//班级
				sMajor:"",	//专业
				isNetworkBusy:false,	//网络繁忙标志位
				isDataValid:true,		//数据有效标志位
			}
		},
		async onPullDownRefresh(){		//下拉刷新
			await this.sendRequest();	//发送请求，刷新数据
			setTimeout(function () {
				uni.stopPullDownRefresh();
			}, 1000);					//回弹刷新图标
			this.isExistExceptionAndPopWindow();	//弹出提示框
		},
		async onLoad(){
			this.cacheReadOrNetworkRequestInfo();	//加载信息
		},
		async onShow(){
			this.cacheReadOrNetworkRequestInfo();	//加载信息
		},
		methods:{
			async cacheReadOrNetworkRequestInfo(){	//加载信息，优化用户体验
				this.loadInfoFromCache();			//首先从本地缓存读取信息
				if (this.isExistEmpty()==false){	//本地有数据则直接返回
					return;
				}
				uni.showToast({							//弹出loading提示框
					icon:"loading",
					duration:globalSetting.TIME_OUT,
				});
				await this.sendRequest();//发起请求获取数据
				if (this.isDataValid==true){	//保存数据，便于下次直接读取，优化用户体验
					this.saveInfoToCache();
				}
				this.isExistExceptionAndPopWindow();	//异常状态提示框弹出
				uni.hideToast();				//隐藏提示框
			},
			isExistEmpty(){						//判断数据是否存在
				return(this.imgsrc=="" ||  this.sName=="" || this.sGender=="" || this.nAge=="" || this.sOrigin=="" || this.sMajor=="" || this.sClass=="");
			},
			loadInfoFromCache(){				//从本地读取数据
				this.imgsrc=uni.getStorageSync("EASYCMP_AVATAR");
				this.sName=uni.getStorageSync("EASYCMP_NAME");
				this.sGender=uni.getStorageSync("EASYCMP_GENDER");
				this.nAge=uni.getStorageSync("EASYCMP_AGE");
				this.sOrigin=uni.getStorageSync("EASYCMP_ORIGIN");
				this.sMajor=uni.getStorageSync("EASYCMP_MAJOR");
				this.sClass=uni.getStorageSync("EASYCMP_CLASS");
			},
			saveInfoToCache(){					//存储数据到本地
				uni.setStorageSync("EASYCMP_AVATAR",this.imgsrc);
				uni.setStorageSync("EASYCMP_NAME",this.sName);
				uni.setStorageSync("EASYCMP_GENDER",this.sGender);
				uni.setStorageSync("EASYCMP_AGE",this.nAge);
				uni.setStorageSync("EASYCMP_ORIGIN",this.sOrigin);
				uni.setStorageSync("EASYCMP_MAJOR",this.sMajor);
				uni.setStorageSync("EASYCMP_CLASS",this.sClass);
			},
			showPrompt(promptText){				//将模态提示框进一步封装，便于调用
				uni.showModal({
					showCancel:false,
					content:promptText,
				})
			},
			async sendRequest(){				//异步发送提示框，使用await进行类似于同步的操作
				await uni.request({
					    url: globalSetting.API_SITE_STU+'/getMessage', 
					    method:"POST",
						data:{
							ID:uni.getStorageSync("EASYCMP_ID"),		//提交表单
						},
						
					}).then(
						(data) => {
							var [err,res] = data;
							if (err!=null){								//err不为null说明网络有问题，设置标志位
								this.isNetworkBusy=true;
							}
							else{
								this.isNetworkBusy=false;
								try{									//防止数据为空，进行异常处理
									this.imgsrc = res.data.data[0].image;
									this.sName = res.data.data[0].name;
									this.sGender = res.data.data[0].gender;
									this.nAge = res.data.data[0].age;
									this.sOrigin = res.data.data[0].origin;
									this.sMajor = res.data.data[0].major;
									this.sClass = res.data.data[0].class;
									this.isDataValid=true;
								}
								catch(e){
									this.isDataValid=false;
								}
							}
						}
					)
			},
			
			navToEditInfo(){		//跳转到信息修改页面，但首先判断网络是否有异常，无异常才跳转，否则弹框提示用户
				if (this.isExistExceptionAndPopWindow()==true){
					return;
				}
				else{
					uni.navigateTo({
						url:"/pages/index/infoRevision",
					})
				}
			},
			navToEditPwd(){			//跳转到密码修改页面，但首先判断网络是否有异常，无异常才跳转，否则弹框提示用户
				if (this.isExistExceptionAndPopWindow()==true){
					return;
				}
				else{
					uni.navigateTo({
						url:"/pages/index/passwordEditing",
					})
				}
			},
			isExistExceptionAndPopWindow(){		//判断是否有异常，并且弹框提示用户，返回为true代表有异常，否则无异常
				if (this.isNetworkBusy==true){
					this.showPrompt("网络繁忙，请刷新重试！");
					return true;
				}
				else if (this.isDataValid==false){
					this.showPrompt("数据异常，请刷新重试！");
					return true;
				}
				return false;
			}
		}
	}
</script>

<style lang="scss">
	.imageStyle{				//头像样式设计
		display: block;
		margin: 0 auto;
		height: 350rpx;
		width: 250rpx;
		margin-top: 40rpx;
		margin-bottom: 40rpx;
	}
</style>