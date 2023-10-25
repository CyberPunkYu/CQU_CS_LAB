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
		
		<!-- 选择图片使用chooseImage所渲染在页面上的预览位置 -->
		<view class="picture">
			<image class="picture_a" :src="file_path"></image>
		</view>
		<!-- 上传照片的提交按钮 -->
		<view class="key">
			<u-button class="custom-style_a" shape="circle" size="medium" @click="choose_image">上传照片
			</u-button>
		</view>
		
		<!-- 下拉选择框 -->
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
		<u-button class="custom-style" :disabled="isSubmitting" :loading="isSubmitting" shape="circle" size="medium"
			type="primary" @click="submit">提交</u-button>
	</view>
</template>

<script>
	import globalSetting from '@/common/json/globalSetting.json'; //导入全局的配置变量
	export default {
		data() {
			return {
				imgArr: [], // 选择图片的图片地址存储数组
				file_path: '/static/defaultPic.png', // 设置的默认图片，便于明确图片的预览位置
				isfalse: false,  // boolen值判断是否表单录入信息成功
				
				// 下拉框定义的触发函数变量
				showSex: false,
				showOrigin: false,
				showClass: false,
				showMajor: false,
				isSubmitting: false, //提交按钮的loading判断
				
				// form表单的定义变量
				form: {
					name: '',  //姓名
					gender: '',  //性别
					age: '', //年龄
					native_place: '',  //籍贯
					major: '', //专业
					classnum: '' //班级
				},
				
				// 下拉框的选择数组
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
				
				// form表单的rules规则
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
							min: 2,
							max: 15,
							message: "姓名的长度为2~15位",
							trigger: ["change", "blur"],
						}
					],

					gender: [{
						required: true,
						message: '请选择你的性别',
						trigger: ['change', 'blur'],
					}],
					age: [{
							required: true,
							message: '请输入你的年龄',
							trigger: ['change', 'blur'],
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
						trigger: ['change', 'blur'],
					}, ],

					major: [{
						required: true,
						message: '请选择你的专业',
						trigger: ['change', 'blur'],
					}, ],

					classnum: [{
						required: true,
						message: '请选择你的班级',
						trigger: ['change', 'blur'],
					}, ]

				}
			};
		},


		onPullDownRefresh() { //停止页面的刷新
			setTimeout(function() {
				uni.stopPullDownRefresh();
			}, 1000);
		},

		methods: {
			
			// 信息录入失败的弹窗
			isFalse() {
				uni.showModal({
					content: '信息录入失败',
					confirmText: '确定',
					cancelText: '取消'
				});
			},
			
			// uniapp从本地选择上传图片功能
			choose_image() {
				var prev_imgPath=this.file_path;
				uni.chooseImage({
					count: 1, // 设置上传图片的数量为1
					sizeType: ['compressed'], // 定义上传图片的类型为可压缩的
					success: (res) => { // 如果上传成功则继续执行
						this.imgArr = res.tempFilePaths; // 图片的本地文件路径列表
						this.file_path = res.tempFilePaths[0]; //图片的路径地址
						const tempFiles = res.tempFiles; // 图片的本地文件列表，便于后面限制图片的上传大小
						let resSize = tempFiles[0].size; // 取出图片的大小
						if (resSize > 5242880) { // 设置，判断图片的大小不超过5MB
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
			
			// 判断表单是否为空
			isExistEmpty() {
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
			
			// 弹窗的封装函数
			showPrompt(text) {
				uni.showModal({
					showCancel: false,
					content: text,
				})
			},
			
			// 提交按钮所触发的函数
			submit() {
				this.isSubmitting = true;
				if (this.isExistEmpty() == true) {
					this.showPrompt("请完整填写信息");
					this.isSubmitting = false;
					uni.hideToast();
					return;
				}
				this.$refs.uForm.validate().then( // rules表单的判断规则，判断是否按照rules规则填写否则不能提交
					async res=>{
						if (this.file_path.length > 0) {
							this.sendInfo();
						} else {
							this.showPrompt("请选择照片");
							this.isSubmitting = false;
						}
					}
				).catch(
					errors => {
						this.isSubmitting=false;
						this.showPrompt("填写信息有误，请确认后重试");
						return;
					}
				);
			},
			// 把数据进行本地的缓存，提高通过服务器的数据传输的速率
			saveInfoToCache() {
				uni.setStorageSync("EASYCMP_AVATAR", this.file_path);
				uni.setStorageSync("EASYCMP_NAME", this.form.name);
				uni.setStorageSync("EASYCMP_GENDER", this.form.gender);
				uni.setStorageSync("EASYCMP_AGE", parseInt(this.form.age));
				uni.setStorageSync("EASYCMP_ORIGIN", this.form.native_place);
				uni.setStorageSync("EASYCMP_MAJOR", this.form.major);
				uni.setStorageSync("EASYCMP_CLASS", this.form.classnum);
			},
			
			// 录入信息的上传
			async sendInfo(){
				uni.uploadFile({
					url: globalSetting.API_SITE_STU + '/infoService', //仅为示例，非真实的接口地址
					filePath: this.file_path, // 文件路径
					name: 'image', //图片名称
					// 通过uploadFile上传的附加的formData的额外数据
					formData: {
						'name': this.form.name,
						'gender': this.form.gender,
						'age': parseInt(this.form.age),
						'origin': this.form.native_place,
						'major': this.form.major,
						'classnum': this.form.classnum,
						"ID": uni.getStorageSync("EASYCMP_ID"), // 解决多用户登录问题
					},
					timeout:globalSetting.TIME_OUT,
					success: (uploadFileRes) => {
						if (uploadFileRes.statusCode!=200){
							this.showPrompt("网络繁忙，请稍后重试！");
							this.isSubmitting=false;
							return;
						}
						this.isfalse = JSON.parse(uploadFileRes.data).uploadSucceed; // 因为uploadFile上传返回的数据为字符串类型，但是我们需要boolen所以需要数据格式的转换
						if (this.isfalse == true) {
							this.saveInfoToCache(); // loading缓存
							this.isSubmitting = false;
							uni.showToast({
								icon: "success",
								title: "录入成功",
								duration: 500,
							})
							setTimeout( // 录入成功进行页面的跳转
								function() {
									uni.switchTab({
										url: "/pages/index/navigation/navigation_homepage"
									})
								}, 500
							);
						}
					},
					fail:(err)=>{
						this.showPrompt("网络繁忙，请稍后重试！");
						this.isSubmitting = false;
					}
				});
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
		margin: auto;
		margin-bottom: 40rpx;
	}
	
	// 预览的图片
	.picture_a {
		width: 200rpx;
		height: 200rpx;
		margin: auto;
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
		margin: auto;
	}
	
	// 录入信息的提交
	.custom-style {
		margin-top: 200rpx;
		width: 250rpx;
		margin: auto;
	}
</style>
