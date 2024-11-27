<template class="profile-template">
  <div>
    <!-- 춘식이컬러 페이지 배너 -->
    <transition
    name="slide-down"
    @before-enter="beforeEnter"
    @enter="enter"
    @leave="leave"
  >
    <PageBanner
      v-show="bannerVisible"
      :title="$route.meta.title"
      :description="$route.meta.description"
      class="page-banner"
    />
  </transition>    
    <!-- 프로필 데이터가 있으면 보여주기 -->
    <div v-if="profile && Object.keys(profile).length > 0" class="profile-container">
      <div class="profile-image-div">
        <!-- 프로필 이미지 선택 -->
        <div class="profile-image-section">
          <h3 class="profile-image-text">프로필 이미지</h3>
          <div class="image-picker">
            <img :src="profile.imageUrl || defaultImage" alt="Profile Image" class="profile-image" />
            <input type="file" accept="image/*" @change="handleImageChange" />
          </div>
        </div>
  
        <!-- 이모티콘 선택 -->
        <div class="emoji-section">
          <h3>이모티콘 선택</h3>
          <div class="emoji-container">
            <span v-for="(emoji, index) in emojis" :key="index" class="emoji" @click="selectEmoji(emoji)">
              {{ emoji }}
            </span>
          </div>
        </div>
      </div>
      <div class="profile-info">
        <!-- 프로필 정보 -->
        <p><strong>ID: </strong> {{ profile.username }}</p>
        <p><strong>닉네임: </strong> {{ profile.nick_name }}</p>
        <p><strong>이름: </strong> {{ profile.name }}</p>
        <p><strong>나이: </strong> {{ profile.age }}</p>
        <p><strong>성별: </strong> {{ profile.gender }}</p>
        <p><strong>전화번호: </strong> {{ profile.phone_number }}</p>
        <p><strong>이메일: </strong> {{ profile.email }}</p>
        <p><strong>직업: </strong> {{ profile.job }}</p>
        <p><strong>관심분야: </strong> {{ profile.interest }}</p>
        <p><strong>자산상태: </strong> {{ formatCurrency(profile.assets_amount) }} 원(₩)</p>
        <p><strong>연봉: </strong> {{ formatCurrency(profile.salary) }} 원(₩)</p>
        <p><strong>학력: </strong> {{ profile.education }}</p>
        <p><strong>지역: </strong> {{ profile.region }}</p>
      </div>

      <!-- 프로필 수정 버튼 -->
      <button class="update-button" @click="goToEditProfile">프로필 수정</button>
    </div>

    <!-- 프로필 데이터가 없으면 로딩 중 표시 -->
    <div v-else>
      <p>Loading profile...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useCounterStore } from '@/stores/counter'
import PageBanner from '@/components/PageBanner.vue'
import { useRouter } from 'vue-router'

// Pinia store 인스턴스 가져오기
const store = useCounterStore()
const router = useRouter()

// profile을 ref로 선언하여 반응형 데이터로 만듦
const profile = ref({})
const bannerVisible = ref(false)
const emojis = ref([
  '😀', '😂', '😍', '😎', '😢', '😭', '😡', '🥳', '🥺', '😇', '😋', '😜', '🤩', '🥰', '😈',
  '😻', '🤪', '👻', '💀', '👑', '🌞', '🌛', '🌈', '🍀', '🌼', '🌸', '💐', '🌻', '🍓', '🍒',
  '🍉', '🍊', '🍋', '🍇', '🍍', '🍎', '🍏', '🍑', '🍒', '🍈', '🍉', '🥝', '🍊', '🍋', '🍌',
  '🍓', '🍔', '🍟', '🍕', '🍣', '🍤', '🍜', '🍲', '🍿', '🍩', '🍪', '🍫', '🍬', '🍭', '🍮',
  '🍯', '🍷', '🍸', '🍹', '🍺', '🥂', '🥃', '🍻', '🥤', '🍽', '🥄', '🍴', '🍕', '🍳', '🍔',
  '🥪', '🍡', '🍛', '🍚', '🍲', '🥣', '🥗', '🍝', '🍜', '🍢', '🍷', '🍸', '🍺', '🥂', '🥃',
  '🍻', '🥤', '🥑', '🥒', '🍅', '🥦', '🌽', '🍄', '🥬', '🥝', '🥑', '🥥', '🥒', '🍇', '🍓',
  '🍉', '🍊', '🍋', '🍍', '🍎', '🍏', '🍑', '🍒', '🍈', '🍓', '🍒', '🍍', '🍆', '🍑', '🍗',
  '🍖', '🍣', '🥗', '🍝', '🍛', '🍤', '🍨', '🍩', '🍪', '🍫', '🍬', '🍮', '🍡', '🥞', '🍔',
  '🍟', '🍕', '🍗', '🍖', '🍠', '🍢', '🍲', '🥣', '🥗', '🍜', '🍝', '🍗', '🍔', '🍟', '🍕',
  '🍖', '🍛', '🍣', '🍤', '🍱', '🍚', '🥘', '🍲', '🥣', '🥗', '🥧', '🥚', '🥐', '🥞', '🍪',
  '🍩', '🍫', '🍬', '🍭', '🍮', '🍷', '🍸', '🍹', '🍺', '🥂', '🥃', '🍻', '🥤', '🍷', '🥛',
  '🥤', '🥄', '🍴', '🍽', '🍴', '🥢', '🍱', '🍡', '🍢', '🍜', '🍝', '🍣', '🍤', '🍗', '🍖',
  '🍕', '🍔', '🥪', '🍟', '🍛', '🍚', '🍲', '🥗', '🥣', '🥗', '🍛', '🍝', '🍣', '🍤', '🍜',
  '🍢', '🍓', '🍇', '🍍', '🍉', '🍊', '🍋', '🍑', '🍎', '🍏', '🍒', '🍓', '🍈', '🍍', '🍒',
  '🍉', '🍊', '🍋', '🍋', '🍇', '🍑', '🍒', '🍍', '🍉', '🍇', '🍍', '🍑', '🍍', '🍇', '🍎',
  '🍋', '🍅', '🥝', '🍊', '🍓', '🍇', '🍏', '🍇', '🥝', '🍏', '🥑', '🥒', '🍇', '🍋', '🍒',
  '🍎', '🍍', '🥥', '🍑', '🍓', '🍒', '🍋', '🍋', '🍇', '🍍', '🍓', '🍑', '🍋', '🍇', '🍎'
])
const defaultImage = 'https://via.placeholder.com/150'

// 프로필 데이터를 불러오기 위해 컴포넌트 마운트 시에 호출
onMounted(() => {
  store.getProfile()
  // 배너 표시
  setTimeout(() => {
    bannerVisible.value = true
  }, 300)  // 300ms 후에 배너 표시 (애니메이션을 부드럽게 하기 위함)
})

// store의 profile이 변경되면 profile ref도 업데이트
watch(() => store.profile, (newProfile) => {
  profile.value = newProfile
})

// 프로필 수정 페이지로 이동하는 함수
const goToEditProfile = () => {
  router.push({ name: 'updateProfile' })
}

// 자산상태와 연봉 포맷팅 함수
const formatCurrency = (value) => {
  if (value === null || value === undefined) return '0'; // 값이 없을 경우 처리
  return new Intl.NumberFormat().format(value); // 천 단위로 구분
}

// 이미지 파일 변경 처리 함수
const handleImageChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      profile.value.imageUrl = e.target.result; // 이미지 URL을 프로필에 저장
    };
    reader.readAsDataURL(file);
  }
}

// 이모티콘 선택 함수
const selectEmoji = (emoji) => {
  profile.value.selectedEmoji = emoji; // 이모티콘 선택
  alert(`이모티콘 "${emoji}"을 선택했습니다!`); // 선택된 이모티콘을 사용자에게 알림
}

// 애니메이션 시작 전 설정
const beforeEnter = (el) => {
  el.style.transform = 'translateY(-110px)'
}

// 애니메이션 실행
const enter = (el, done) => {
  el.offsetHeight // trigger reflow
  el.style.transition = 'transform 0.5s ease-in-out'
  el.style.transform = 'translateY(0px)'
  done()
}
</script>

<style scoped>
.profile-template {
  background-color: black; /* 배경색을 검정색으로 설정 */
  color: #ffe5ab; /* 텍스트 색상은 초록색 */
  font-family: 'Courier New', Courier, monospace; /* 고정 폭 글꼴로 설정 */
  font-size: 16px;
  padding: 20px;
  display: flex;
  justify-content: center; /* 가로 정렬 */
  align-items: center; /* 세로 정렬 */
  overflow: hidden;
}

/* 프로필 정보와 이미지 및 이모티콘을 나누는 섹션 */
.profile-sections {
  display: flex;
  flex-wrap: wrap; /* 작은 화면에서 두 섹션이 쌓이도록 */
  justify-content: space-between;
  width: 100%;
}

/* 왼쪽 섹션: 프로필 이미지와 이모티콘 */
.left-section {
  flex: 1 1 40%; /* 40% 크기로 설정 */
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-right: 20px;
}

/* 프로필 이미지 스타일 */
.profile-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background-color: #aaa; /* 프로필 이미지 색상, 실제 이미지는 따로 추가해야 함 */
  margin-bottom: 20px;
}

/* 이모티콘 컨테이너 */
.emojis-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(40px, 1fr)); /* 이모티콘 크기에 맞게 열 수 설정 */
  gap: 10px; /* 이모티콘 사이에 간격 추가 */
  max-width: 100%; /* 컨테이너의 최대 너비를 화면 크기에 맞게 설정 */
  margin-top: 20px;
  padding: 10px;
}

/* 이모티콘 스타일 */
.emojis-container span {
  font-size: 30px; /* 이모티콘 크기 설정 */
  text-align: center;
  cursor: pointer;
  transition: transform 0.2s ease-in-out, color 0.2s ease-in-out;
}

/* 이모티콘 hover 효과 */
.emojis-container span:hover {
  transform: scale(1.2); /* 이모티콘을 살짝 키워서 강조 */
  color: #ffcc00; /* hover 시 색상 변경 */
}

/* 오른쪽 섹션: 프로필 정보 */
.right-section {
  flex: 1 1 55%; /* 55% 크기로 설정 */
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding-left: 20px;
}

/* 프로필 데이터 스타일 */
div p {
  margin: 10px 0;
  font-size: 16px;
  color: #000000;
}

strong {
  color: #000000;
  font-weight: bold;
}

/* 제목 스타일 */
h1 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #000000;
}

/* 배너 스타일 */
.page-banner {
  background-color: #ffffff; /* 배경을 검정색으로 */
  color: #000000; /* 텍스트 색상을 초록색으로 */
  padding: 10px 20px;
  font-size: 20px;
  margin-bottom: 20px;
  text-align: center;
}

/* 버튼 스타일 */
button {
  background-color: black; /* 배경을 검정색으로 설정 */
  color: #ffffff; /* 텍스트 색상은 초록색 */
  padding: 10px 20px;
  font-size: 16px;
  text-transform: uppercase; /* 텍스트 대문자 */
  cursor: pointer;
  margin-top: 20px;
  transition: all 0.3s ease;
}

/* 버튼 hover 효과 */
button:hover {
  background-color: #00ff00; /* hover 시 배경색 초록색 */
  color: black; /* hover 시 텍스트 색상 검정색 */
  border: 2px solid black; /* hover 시 테두리 검정색 */
}

/* 로딩 메시지 스타일 */
.loading-message {
  font-size: 18px;
  color: #00ff00;
  text-align: center;
  margin-top: 40px;
}

.profile-image-div {
  height: 300px;
  width: 500px;
}

.emoji-section {
  padding: 60px;
  height: 500px;
  margin-left: 50px;
  z-index:9999;
}

.profile-info {
  position: relative;
  left: 1000px;
  bottom: -30px;
  z-index:0;
}

.image-picker {
  padding-left: 120px;
}

.profile-image-text {
  padding-left: 120px;  
}

.update-button {
  margin-left: 1200px;
  position: relative;
  bottom: 40px;
}
</style>

