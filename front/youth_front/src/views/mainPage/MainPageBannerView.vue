<template>
  <div class="banner-container1">
    <!-- 배너 이미지 -->
    <div class="banner-image1">
      <img :src="banners[currentBannerIndex].imgSrc" alt="배너" />
      <!-- 왼쪽 화살표 버튼 -->
      <button class="arrow-button left" @click="changeBanner(-1)">&#60;</button>
      
      <!-- 오른쪽 화살표 버튼 -->
      <button class="arrow-button right" @click="changeBanner(1)">&#62;</button>
    </div>

    <!-- 로그인 박스 (프로필 카드 형태로 스타일링) -->
    <div class="login-box">
      <!-- 상단 이미지 -->
      <div class="login-box-image">
        <img src="@/assets/main/profile/li_chun_dance.gif" alt="로그인 배경 이미지" />
      </div>

      <h4>내게 필요한 민원/생활/혜택 정보를 확인하세요.</h4>
      <!-- 로그인 상태일 때 사용자 정보 표시 -->
      <div v-if="store.isLogin" class="user-info">
        <p>------------------------------------------</p>
        <p>닉네임: {{ store.profile?.nick_name || '' }}</p>
        <p>나이: {{ store.profile?.age || ''}}</p>
        <p>거주지: {{ store.profile?.region || ''}}</p>
        <a @click.prevent="logOut" class="logout-link">로그아웃</a>
        <a @click.prevent="goToUpdateProfile" class="update-profile-link">회원정보 수정</a>
      </div>

      <!-- 로그인 버튼과 비밀번호 찾기 버튼 -->
      <div v-else class="login-actions">
        <button @click.prevent="goToLoginPage" class="login-button">로그인</button>
        <a class="forgot-id-link" href="#">아이디 찾기</a> 
        <a class="forgot-password-link" href="#">비밀번호 찾기</a> 
        <a @click.prevent="goToSignUpPage" class="sign-in-link">회원가입</a> 
      </div>

    </div>
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue'; // ref를 임포트
  import { useRouter } from 'vue-router' // useRouter를 가져오기
  import { useCounterStore } from '@/stores/counter';
  
  // 배너 이미지 경로 (import 문법 사용)
  import testImg1 from '@/assets/main/Banner/1.png'
  import testImg2 from '@/assets/main/Banner/2.png'
  import testImg3 from '@/assets/main/Banner/3.png'

  const store = useCounterStore()
  const router = useRouter() // Router 객체 초기화
  const banners = [
    { imgSrc: testImg1 },
    { imgSrc: testImg2 },
    { imgSrc: testImg3 },
  ];

  const nickName = ref()
  const age = ref()
  const region = ref()


  // 현재 배너 인덱스를 ref로 반응형 변수로 설정
  const currentBannerIndex = ref(0);

  const logOut = () => {
  store.logOut()
}

// 배너를 변경하는 함수 (화살표 클릭 시)
  const changeBanner = (direction) => {
    currentBannerIndex.value = (currentBannerIndex.value + direction + banners.length) % banners.length;
  }

// 로그인 페이지 이동
const goToLoginPage = () => {
  router.push({ name: 'login' }) // store.router 대신 useRouter 사용
}

  // 회원가입 페이지 이동
  const goToSignUpPage = () => {
    router.push({ name: 'signup' }) // 라우터 네임이 'signUp'인 페이지로 이동
  }
</script>

<style scoped>
.banner-container1 {
  display: flex;
  justify-content: flex-start; /* 배너와 로그인 박스를 왼쪽 정렬 */
  align-items: center;
  min-width: 2114px;
  width: 2114px; /* 화면 너비에 맞게 설정 */
  height: 420px;  /* 고정된 높이 */
  padding-bottom: 20px;
}

.banner-image1 {
  flex: 5; /* 배너 이미지 부분에 5비율의 너비 할당 */
  height: 100%; /* 배너 이미지 높이 100% */
  overflow: hidden; /* 이미지가 컨테이너 밖으로 나가지 않도록 */
  position: relative; /* 배너 내부의 이미지가 화살표 버튼에 영향을 미치지 않도록 */
  margin-left: 20px; /* 좌측 마진 추가 */
  margin-right: 20px; /* 우측 마진 추가 */
  border-radius: 8px;
  border-style: solid;
  border: none;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* 부드러운 그림자 */
  width: 1630px;
}

img {
  object-fit: fill; /* 이미지의 비율을 무시하고 배너에 맞게 크기 조정 */
  width: 100%;  /* 배너 크기에 맞춰 이미지 너비 설정 */
  height: 100%; /* 배너 크기에 맞춰 이미지 높이 설정 */
  border-radius: 8px;
}

/* 화살표 버튼 스타일 */
.arrow-button {
  background-color: #fff29d;
  color: rgb(173, 135, 85);
  border: none;
  font-size: 1.2rem;
  padding: 5px 10px;
  cursor: pointer;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
}

.left {
  left: 0; /* 배너 이미지의 왼쪽 끝에 배치 */
}

.right {
  right: 0; /* 배너 이미지의 오른쪽 끝에 배치 */
}

.arrow-button:hover {
  background-color: #FFDD00
}

/* 로그인 박스 스타일 */
.login-box {
  flex: 1;
  height: 100%;
  padding: 20px;
  border: none;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-left: 20px;
  margin-right: 20px;
  min-width: 400px;
  position: relative; /* 로그인 박스 내에서 링크들 절대 위치 지정 */
}

.forgot-id-link,
.forgot-password-link,
.sign-in-link, 
.logout-link, 
.update-profile-link {
  font-size: 14px;
  position: absolute;  /* 로그인 박스를 기준으로 위치 절대 지정 */
  bottom: 10px;  /* 하단에 위치하도록 설정 */
  text-decoration: none;  /* 기본 밑줄 제거 */
  /* color: rgba(0, 0, 0, 0.479); */
  background-color: #fff29d; /* 테마 색상 */
  margin-left: 15px;
  width: 100px; /* 고정된 너비 */
  height: 40px; /* 고정된 높이 */
  border-radius: 6px;
  color: #333;
  font-weight: bold;
  text-align: center; /* 가로 중앙 정렬 */
  line-height: 40px; /* 세로 중앙 정렬 (height와 동일하게 설정) */
}
.login-box:hover {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* 부드러운 그림자 */
  /* transform: translateY(-5px); */
}

.forgot-id-link:hover,
.forgot-password-link:hover,
.sign-in-link:hover,
.logout-link:hover, 
.update-profile-link:hover {
  text-decoration: underline;  /* 마우스가 올라갔을 때만 밑줄 추가 */
}

.forgot-id-link,
.logout-link {
  left: 10px;  /* 가장 왼쪽에 배치 */
}

.forgot-password-link {
  left: calc(50% - 20px);  /* 왼쪽으로 20px 이동 */
  transform: translateX(-50%);
}

.sign-in-link,
.update-profile-link {
  right: 10px;  /* 가장 오른쪽에 배치 */
}

.user-info {
  text-align: center;
  padding-bottom: 20px;
}

.user-info p {
  margin: 5px 0;
}

.login-box-image {
  width: 200px;
  height: 200px; /* 상단의 30%에 이미지를 배치 */
  overflow: hidden;
}

.login-box-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.login-box h4 {
  margin-top: 20px;
  font-size: 1.2rem;
  text-align: center;
  color: black; /* 텍스트 색상 조정 */
}

.login-actions {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.login-button{
  height: 50px;
  width: 200px;
  font-size: 1rem;
  border-radius: 5px;
  border: 1px solid #ccc;
  cursor: pointer;
};  

hr {
  font-weight: bold;
  border: none;
  border-top: 2px solid black;
  margin: 10px 0;
  width: 80%;
  align-self: center; /* Keep this to center the hr */
  visibility: visible; /* Ensure visibility */
}
</style>
