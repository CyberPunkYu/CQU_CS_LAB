<template>
	<view>
		<view class="form-content">
			<!-- form表单 -->
			<u-form :model="form" ref="uForm" label-width="100" :labelStyle="{'font-size':'40rpx'}"
				labelPosition="left">
				<!-- 输入姓名 -->
				<u-form-item label="姓名" prop="name" borderBottom="true">
					<u-input v-model="form.name" border="false" inputAlign="center" fontSize="20px"
						placeholder="请输入你的姓名" />
				</u-form-item>
				<!-- 选择性别 -->
				<u-form-item label="性别" prop="gender" borderBottom="true" labelWidth="120" @click="showSex = true">
					<u-input v-model="form.gender" border="false" placeholder="请选择你的性别" inputAlign="center" disabled
						disabledColor="#FFFAFA" shape="circle"
						suffixIcon="arrow-right"
						fontSize="20px" />
				</u-form-item>
				<!-- 输入年龄 -->
				<u-form-item label="年龄" prop="age" borderBottom="true">
					<u-input v-model="form.age" border="false" placeholder="请输入你的年龄" inputAlign="center" type="number"
						maxlength=2
						fontSize="20px" />
				</u-form-item>
				<!-- 选择籍贯 -->
				<u-form-item label="籍贯" prop="native_place" borderBottom="true" labelWidth="120" @click="showOrigin = true">
					<u-input v-model="form.native_place" border="false" placeholder="请选择你的籍贯" inputAlign="center"
						disabled disabledColor="#FFFAFA" shape="circle" 
						suffixIcon="arrow-right"
						fontSize="20px" />
				</u-form-item>

				<u-form-item label="专业" prop="major" borderBottom="true" labelWidth="120" @click="showMajor = true">
					<u-input v-model="form.major" border="false" placeholder="请选择你的专业" inputAlign="center" disabled
						disabledColor="#FFFAFA" shape="circle"
						 suffixIcon="arrow-right"
						 fontSize="20px" />
				</u-form-item>

				<u-form-item label="班级" prop="classnum" borderBottom="true" labelWidth="120" @click="showClass = true">
					<u-input v-model="form.classnum" border="false" placeholder="请选择你的班级" inputAlign="center" disabled
						disabledColor="#FFFAFA" shape="circle"
						 suffixIcon="arrow-right"
						 fontSize="20px" />
				</u-form-item>
			</u-form>
		</view>

		<view class="picture">
			<image class="picture_a" :src="file_path"></image>
		</view>
		<!-- 上传照片 -->
		<view class="key">
			<u-button class="custom-style_a" shape="circle" size="medium" @click="choose_image">上传照片</u-button>
		</view>
		<!-- 选择性别 -->
		<u-action-sheet :show="showSex" :actions="actions_a" title="请选择性别" @close="showSex = false" @select="sexSelect">
		</u-action-sheet>
		<!-- 选择籍贯 -->
		<u-action-sheet :show="showOrigin" :actions="actions_b" title="请选择籍贯" @close="showOrigin = false"
			@select="originSelect">
		</u-action-sheet>
		<!-- 选择专业 -->
		<u-action-sheet :show="showMajor" :actions="actions_c" title="请选择专业" @close="showMajor = false"
			@select="majorSelect">
		</u-action-sheet>
		<!-- 选择班级 -->
		<u-action-sheet :show="showClass" :actions="actions_d" title="请选择班级" @close="showClass = false"
			@select="classSelect">
		</u-action-sheet>
		<!-- 提交按钮 -->
		<u-button class="custom-style" type="primary" throttleTime:10000 :disabled="isSubmitting" :loading="isSubmitting" shape="circle" size="medium"  @click="submit">提交</u-button>

	</view>
</template>

<script>
	import globalSetting from '@/common/json/globalSetting.json';
	export default {
		data() {
			return {
				imgArr: [],
				file_path: '/static/defaultPic.png',
				isfalse: false,

				showSex: false,
				showOrigin: false,
				showClass: false,
				showMajor: false,
				
				isSubmitting: false,
				isNetworkBusy:false,
				isDataVaild: true,
				
				form: {
					name: '',
					gender: '',
					age: '',
					native_place: '',
					major: '',
					classnum: ''
				},

				actions_a: [{
						name: '男',
					},
					{
						name: '女',
					},
				],

				actions_b: [{
						name: '贵州省外',
					},
					{
						name: '遵义市',
					},
					{
						name: '毕节市',
					},
					{
						name: '贵阳市',
					},
					{
						name: '六盘水市',
					},
					{
						name: '安顺市',
					},
					{
						name: '铜仁市',
					},
					{
						name: '黔西南布依族苗族自治州',
					},
					{
						name: '黔南布依族苗族自治州',
					},
					{
						name: '黔东南苗族侗族自治州',
					},
				],
				actions_c: [{
						name: '大数据技术',
					},
					{
						name: '云计算技术应用',
					},
					{
						name: '物联网应用技术'
					}
				],
				actions_d: [{
						name: '1',
					},
					{
						name: '2',
					},
					{
						name: '3',
					},
				],

				rules: {
					name: [{
							required: true,
							message: '请输入你的姓名',
							trigger: 'blur'
						},
						{
							validator: (rule, value, callback) => {
								return uni.$u.test.chinese(value);
							},
							message: "姓名必须为中文",
							trigger: ["change", "blur"],
						},
						{
							min:2,
							max:15,
							message:"姓名的长度为2~15位",
							trigger: ["change", "blur"],
						}
					],

					gender: [{
						required: true,
						message: '请选择你的性别',
						trigger: ['blur'],
					}],
					age: [{
						type:'number',
						required: true,
						message: '请输入你的年龄',
						trigger: 'blur',
					},
					 {
						 type:'number',
					 	validator: (rule, value, callback) => {
					 		return uni.$u.test.range(value,[12,80])
					 	},
					 	message: "年龄范围为12~80",
					 	trigger: ["change", "blur"],
					 },
					 ],

					native_place: [{
						required: true,
						message: '请选择你的籍贯',
						trigger: ['blur'],
					}, ],

					major: [{
						required: true,
						message: '请选择你的专业',
						trigger: ['blur'],
					}, ],

					classnum: [{
						required: true,
						message: '请选择你的班级',
						trigger: ['blur'],
					}, ]

				}
			};
		},
		
		// 页面的预加载
		async onLoad() {
			this.loadInfoFromCache();
			if (this.isExistEmpty()==true){
				uni.showToast({
					duration:globalSetting.TIME_OUT,
					icon:"loading"
				})
				this.getMsgFromNetwork();
				uni.hideToast();
			}
			this.exceptionPopWindow();
		},

		onPullDownRefresh() { // 下拉刷新
			this.loadInfoFromCache();
			if (this.isExistEmpty()==true){
				uni.showToast({
					duration:globalSetting.TIME_OUT,
					icon:"loading"
				})
				this.getMsgFromNetwork();
				uni.hideToast();
			}
			this.exceptionPopWindow();
			setTimeout(function () {
				uni.stopPullDownRefresh();
			}, 1000);
		},

		methods: {
			choose_image() { //更改信息的选择图片
				var prev_imgPath=this.file_path;
				uni.chooseImage({
					count: 1,
					sizeType: ['compressed'], //设置图片为可压缩的
					success: (res) => {
						this.imgArr = res.tempFilePaths;
						this.file_path = res.tempFilePaths[0];
						const tempFiles = res.tempFiles;
						let resSize = tempFiles[0].size;
						if (resSize > 5242880) {
							this.showPrompt("上传图片大小不能超过5MB");
							this.file_path=prev_imgPath;
							return;
						}
					}
				});
			},

			// 选择性别
			sexSelect(e) {
				this.form.gender = e.name
				this.$refs.uForm.validateField('gender')
			},
			// 选择籍贯
			originSelect(e) {
				this.form.native_place = e.name
				this.$refs.uForm.validateField('native_place')
			},
			// 选择专业
			majorSelect(e) {
				this.form.major = e.name
				this.$refs.uForm.validateField('major')
			},
			// 选择班级
			classSelect(e) {
				this.form.classnum = e.name
				this.$refs.uForm.validateField('classnum')
			},

			isExistEmpty(){
				var empty1 = (this.form.name == "");
				var empty2 = (this.form.gender == "");
				var empty3 = (this.form.age == "");
				var empty4 = (this.form.native_place == "");
				var empty5 = (this.form.major == "");
				var empty6 = (this.form.classnum == "");
				if (empty1 || empty2 || empty3 || empty4 || empty5 || empty6) {
					return true;
				}
				return false;
			},
			async submit() {
				this.isSubmitting = true;
				if (this.isExistEmpty()==true){ //判断信息是否为空
					this.showPrompt("信息未填写完整");
					this.isSubmitting=false;
					uni.hideToast();
					return;
				}
				this.$refs.uForm.validate().then( //rules规则的判定
					async res => {
						if (this.file_path.length > 0) {
							await this.sendUpdateMsg();
						}
						else {
							this.showPrompt("请上传照片");
							this.isSubmitting=false;
						}
					}).catch(
						errors => {
							this.isSubmitting=false;
							this.showPrompt("填写信息有误，请确认后重试");
							return;
						}
				)
			},
			// 更改信息的数据传输
			async sendUpdateMsg(){
				uni.uploadFile({
					url: globalSetting.API_SITE_STU+'/updateMessage', 
					filePath: this.file_path,
					name: 'image',
					formData: {
						'name': this.form.name,
						'gender': this.form.gender,
						'age': parseInt(this.form.age),
						'origin': this.form.native_place,
						'major': this.form.major,
						'classnum': this.form.classnum,
						'ID':uni.getStorageSync("EASYCMP_ID"),
					},
					timeout:globalSetting.TIME_OUT,
					success: (uploadFileRes) => {
						if (uploadFileRes.statusCode!=200){
							this.isNetworkBusy=true;
							this.isSubmitting=false;
							this.exceptionPopWindow();
							return;
						}
						this.isfalse = JSON.parse(uploadFileRes.data).updateSucceed;
						if (this.isfalse == true) {
							this.isNetworkBusy=false;
							this.isSubmitting=false;
							this.saveInfoToCache();
							uni.showToast({
								icon: "success",
								title: "修改成功",
								duration:500,
							})
							setTimeout(
								function(){
									uni.switchTab({ // 更改成功的页面跳转
										url: "/pages/index/navigation/personalInfoCenter"
									})
								},500
							);
						}
						else{
							this.isNetworkBusy=true; // 网络是否繁忙
							this.isSubmitting=false;
							this.exceptionPopWindow();
						}
					},
					fail:(err)=>{
						this.isNetworkBusy=true;
						this.isSubmitting=false;
						this.exceptionPopWindow();
					}
				});
			},
			
			// 更改信息的录入表单首先要request请求使表单数据的内容进行自动填充
			async getMsgFromNetwork(){
				await uni.request({
					url: globalSetting.API_SITE_STU+'/getMessage',
					method: "POST",
					data:{
						ID:uni.getStorageSync("EASYCMP_ID"),
					},
					timeout:globalSetting.TIME_OUT,
				}).then(
					(data) => {
						var [err, res] = data;
						if (err!=null){
							this.isNetworkBusy=true;
						}
						else{
							this.isNetworkBusy=false;
							try{
								this.file_path = res.data.data[0].image;
								this.form.name = res.data.data[0].name;
								this.form.gender = res.data.data[0].gender;
								this.form.age = res.data.data[0].age;
								this.form.native_place = res.data.data[0].origin;
								this.form.major = res.data.data[0].major;
								this.form.classnum = res.data.data[0].class;
								this.isDataVaild=true;
							}
							catch(e){
								this.isDataVaild=false;
							}
						}
					}
				)
			},
			
			// 数据缓存至本地
			saveInfoToCache(){
				uni.setStorageSync("EASYCMP_AVATAR",this.file_path);
				uni.setStorageSync("EASYCMP_NAME",this.form.name);
				uni.setStorageSync("EASYCMP_GENDER",this.form.gender);
				uni.setStorageSync("EASYCMP_AGE",parseInt(this.form.age));
				uni.setStorageSync("EASYCMP_ORIGIN",this.form.native_place);
				uni.setStorageSync("EASYCMP_MAJOR",this.form.major);
				uni.setStorageSync("EASYCMP_CLASS",this.form.classnum);
			},
			// 从本地缓存中读取数据
			loadInfoFromCache(){
				this.file_path=uni.getStorageSync("EASYCMP_AVATAR");
				this.form.name=uni.getStorageSync("EASYCMP_NAME");
				this.form.gender=uni.getStorageSync("EASYCMP_GENDER");
				this.form.age=uni.getStorageSync("EASYCMP_AGE");
				this.form.native_place=uni.getStorageSync("EASYCMP_ORIGIN");
				this.form.major=uni.getStorageSync("EASYCMP_MAJOR");
				this.form.classnum=uni.getStorageSync("EASYCMP_CLASS");
			},
			
			// 数据弹窗
			showPrompt(promptText){
				uni.showModal({
					showCancel:false,
					content:promptText,
				})
			},
			
			// 异常处理
			exceptionPopWindow(){
				if (this.isNetworkBusy==true){
					this.showPrompt("网络繁忙，请刷新重试！");
				}
				else if (this.isDataVaild==false){
					this.showPrompt("数据异常，请刷新重试！");
				}
			}
		},

		onReady() {
			this.$refs.uForm.setRules(this.rules);
		},
	};
</script>

<style scoped lang="scss">
	// form表单
	.form-content {
		width: 600rpx;
		height: 700rpx;
		padding: 30px;
		margin: auto;
		margin-bottom: 50rpx;
	}
	
	// 图片的预览位置
	.picture {
		width: 200rpx;
		height: 200rpx;
		margin-top: 50rpx;
		margin: auto;
		margin-bottom: 50rpx;
	}
	
	// 预览的图片
	.picture_a {
		width: 200rpx;
		height: 200rpx;
	}
	
	// 上传图片按钮
	.key {
		width: 200rpx;
		height: 100rpx;
		margin-bottom: 50rpx;
		margin: auto;
	}
	
	// u-botton上传图片
	.custom-style_a {
		width: 200rpx;
		background-color: #ffffff;
		border: 1px solid #bcbcbc;
		margin-bottom: 20rpx;
	}
	
	// 录入信息的提交
	.custom-style {
		margin-top: 200rpx;
		width: 250rpx;
		margin: auto;
	}
</style>
