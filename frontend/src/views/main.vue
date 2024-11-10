<template>
 <header>
  <nav class="header_cont">
    <ul class="header_list_logo"><li class="header_list_logo_li"><img src="../img/Frame15.png" alt="logo"></li></ul>
    <ul class="header_list_logo_btnBar">
      <li class="header_list_logo_btnBar_li"><a href="#">Главное</a></li>
      <li class="header_list_logo_btnBar_li"><a href="#">Маниторинг</a></li>
      <li class="header_list_logo_btnBar_li"><a href="#">Аналитика</a></li>
      <li class="header_list_logo_btnBar_li"><a href="#">Проекты</a></li>
      <li class="header_list_logo_btnBar_li"><a href="#">Сервисы</a></li>
    </ul>
    <ul class="header_list_burger"><li class="header_list_burger_li"><img src="../img/burger.png" alt="burger"></li></ul>
  </nav>
 </header>

  <div class="text_cont">
    <div class="text">
      Карта-помощник: Городская застройка
    </div>
  </div>
  <main>
    <div class="main_header">
      <p class="main_header_text">Выберите место желаемой застройки:</p>
    </div>
    <div class="main_content">
      <div class="main_content_block1">
        <label class="file-upload">
          <p class="main_content_block1_text">Загрузить ваш файл</p>
          <img class="main_content_block1_img" src="../img/file.png" alt="">
          <input type="file" @change="handleFileChange" />
          <span class="file-name">{{ fileName }}</span>
        </label>
      </div>
      <div class="main_content_block2">
        <div class="main_content_block2_header">
          <p class="main_content_block2_header_text">Результат:</p>
          <img id="img" :src="imageSrc" alt="">
        </div>
      </div>
    </div>
    <div class="main_footer">
      <button class="main_footer_btn" @click="submitFile">Отправить</button>
    </div>
  </main>
</template>

<script>
export default {
  name: 'HomeView',
  data() {
    return {
      fileName: 'Файл не выбран',
      selectedFile: null,
      imageSrc: ''  // для хранения URL картинки, полученной от API
    };
  },
  methods: {
    handleFileChange(event) {
      const file = event.target.files[0];
      this.fileName = file ? file.name : 'Файл не выбран';
      this.selectedFile = file;
    },
    async submitFile() {
      if (!this.selectedFile) {
        alert('Пожалуйста, выберите файл перед отправкой.');
        return;
      }
      
      const formData = new FormData();
      formData.append('file', this.selectedFile);

      try {
        const response = await fetch('ЕБАНЫЙ_FLASK_API', {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          throw new Error('Ошибка при отправке файла');
        }

        const result = await response.json();
        
        // Предполагается, что API вернет путь к картинке
        if (result.imagePath) {
          this.imageSrc = require(`${result.imagePath}`);
        }
      } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при отправке файла.');
      }
    }
  }
};
</script>
<style >
.main_footer_btn{
  color: #FFF;
font-family: Inter;
font-size: 24px;
font-style: normal;
font-weight: 700;
line-height: normal;
  border: none;
  display: inline-flex;
padding: 18px 30px 18px 30px;
justify-content: flex-end;
align-items: center;
border-radius: 60px;
background: #62A744;
}
.main_footer{
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center ;
  margin-top: 50px;

}
.main_content_block2_header_text{
  margin: 0;
  text-align: end;
  color: #343449;
text-align: end;
font-family: Inter;
font-size: 25px;
font-style: normal;
font-weight: 700;
line-height: normal;
}
.main_content_block2_header{
  width: 100%;
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: end;;
}
.file-upload {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
}

.file-upload input[type="file"] {
  display: none;
}

.file-name {
  margin-top: 10px;
  font-size: 14px;
  color: #555;
}
.main_content_block2{
  width: 339px;
height: 508px;
border-radius: 40px;
border: 2px solid #343449;
background: rgba(255, 255, 255, 0.00);
}
.main_content_block1_text{
  color: #606060;
font-family: Inter;
font-size: 33px;
font-style: normal;
font-weight: 700;
line-height: normal;
margin-bottom: 31px;
}
.main_content_block1{
  margin-right: 207px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  
}
.main_content{
  display: flex;
  width: 100%;
  justify-content: center;
  align-items: center;
}
.main_header_text{
  width: 1167px;
height: 67px;
color: #343449;
font-family: Inter;
font-size: 45px;
font-style: normal;
font-weight: 700;
line-height: normal;
}
.main_header{
  height: 510px;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
main{
  margin-top: 80px;
width: 100%;
height: 1193px;
border-top-right-radius: 40px;
border-top-left-radius: 40px;
background: #fff;
}
.text_cont{
  margin-top: 160px;
  display: flex;
  justify-content: start;
  align-items: center;
  padding-left: 178px;

}
.text{
  width: 882px;
height: 176px;
flex-shrink: 0;
color: #FFF;
font-family: Inter;
font-size: 80px;
font-style: normal;
font-weight: 700;
line-height: normal;
}
ul{
  padding: 0;

}
.header_list_logo_btnBar_li{
  margin-right: 66px;
}
.header_list_logo_btnBar_li:last-child{
  margin-right: 0px;
}
.header_list_logo_btnBar{
  display: flex;
}
a{
  text-decoration: none;
  color: #fff;
}
.header_list_burger_li{
  position: relative;
  right: 5px;
}
li{
  cursor: pointer;
  list-style: none;
}
.header_cont{
  padding-left: 60px;
  padding-right: 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;;
  width: 1081px;
height: 81px;
flex-shrink: 0;
border-radius: 27px;
background: #62A744;
}
header{
  display: flex;
  width: 100%;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}
body{
  background: #343449;
  font-family: 'Inter', sans-serif;
}
</style>