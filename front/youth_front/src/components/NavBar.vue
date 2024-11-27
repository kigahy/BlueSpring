<template>
  <div>
    <nav class="navbar navbar-expand-lg bg-white" style="width: 2114px;">
      <div
        class="container-fluid d-flex justify-content-between align-items-center"
      >
        <!-- 로고 -->
        <img
          src="@/assets/main/banner/춘식.gif"
          alt="춘식읍따"
          class="choonsik"
        />
        <router-link :to="{ name: 'mainPage' }" class="navbar-brand"
          >작전명 청춘<span class="sik">식</span></router-link
        >

        <!-- 검색 바 -->
        <input
          type="text"
          placeholder="검색어를 입력하세요..."
          v-model="searchQuery"
          class="search-input"
          @keydown.enter="search"
        />
        <i class="fa fa-search" @click="search"></i>
        <!-- 메뉴 항목들 -->
        <div id="navbar-category" class="d-flex">
          <router-link :to="{ name: 'compareFinProduct' }" class="nav-link"
            >예금비교</router-link
          >
          <router-link :to="{ name: 'calendar' }" class="nav-link"
            >캘린더</router-link
          >
          <router-link :to="{ name: 'productRecommend' }" class="nav-link"
            >상품추천</router-link
          >
          <router-link :to="{ name: 'profile' }" class="nav-link"
            >내 프로필</router-link
          >
        </div>
      </div>
    </nav>

    <main>
      <!-- 본문 콘텐츠가 여기에 들어갑니다 -->
    </main>
  </div>
</template>
<script setup>
import { ref } from "vue";
const searchQuery = ref("");

const search = () => {
  if (searchQuery.value) {
    console.log("검색어:", searchQuery.value);
    // 검색 기능 로직을 추가
    searchQuery.value = "";
  }
};
</script>

<style scoped>
/* 춘식이 크기 조절 */
.choonsik {
  max-height: 15%; /* 네비게이션 바의 높이에 맞게 최대 크기 설정 */
  height: 80px; /* 비율을 유지하며 자동 크기 조절 */
  width: auto; /* 비율에 맞게 너비도 자동 조절 */
  margin-right: 20px;
}
.sik {
  color: rgba(255, 255, 255, 0.7);
}

/* 네비게이션 바 스타일 */
.navbar {
  background-color: #ffffff; /* 흰색 배경 */
  padding: 15px 20px; /* 더 큰 여백 */
  font-weight: bold; /* 글씨를 진하게 */
  border-bottom: solid 2px;
  border-color: rgba(219, 167, 55, 0.486);
  max-height: 100px;
  width: 2114px; /* 너비 고정 */
  margin: 0 auto; /* 가운데 정렬 */
  min-width: 1200px; /* 최소 너비 설정 */
  position: fixed;
  top: 0;
  left: 0;
  z-index: 9999;
}

/* 로고 스타일 */
.navbar-brand {
  font-size: 1.8rem; /* 브랜드 이름 크기 크게 */
  color: #333333; /* 진한 글씨 */
  text-decoration: none;
  font-weight: bold; /* 브랜드 글씨도 진하게 */
  margin-right: auto; /* 로고를 왼쪽에 배치 */
}

/* 네비게이션 메뉴 스타일 */
.nav-link {
  font-size: 1.2rem; /* 메뉴 항목 크기 크게 */
  color: #333333; /* 진한 글씨 */
  margin-left: 50px; /* 메뉴 항목 간 여백 */
  text-decoration: none; /* 링크 밑줄 제거 */
}

/* 메뉴 항목 호버 스타일 */
.nav-link:hover {
  color: #007bff; /* 메뉴 항목 호버 시 색상 변경 */
}

#navbar-category {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* 검색 입력란 스타일 */
.search-input {
  width: 35%;
  height: 45%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 20px;
  outline: none;
  margin-right: 10px; /* 버튼과의 간격 */
}

/* 검색 버튼 스타일 */
.search-button {
  padding: 10px 20px;
  font-size: 1rem;
  color: white;
  background-color: #4caf50;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.search-button:hover {
  background-color: #45a049;
}

i {
  font-size: 1.5rem; /* 아이콘 크기 조정 */
}

/* 네비게이션 바 상단 고정 */
.navbar {
  position: fixed; /* 화면 상단에 고정 */
  top: 0; /* 화면 상단에 배치 */
  left: 0; /* 화면 왼쪽에 배치 */
  width: 100%; /* 전체 너비 사용 */
  z-index: 9999; /* 다른 요소들보다 위에 표시되도록 설정 */
  background-color: #ffffff; /* 흰색 배경 */
  padding: 15px 20px; /* 네비게이션 바 안의 여백 */
}

/* body에 padding-top을 추가하여 네비게이션 바 높이만큼 여백을 추가 */
body {
  padding-top: 100px; /* 네비게이션 바의 정확한 높이에 맞춰 여백을 추가 */
}

/* main 태그 또는 콘텐츠 영역에 margin-top을 추가하여 네비게이션 바 높이만큼 밀기 */
main {
  margin-top: 100px; /* 네비게이션 바의 정확한 높이에 맞춰 여백을 추가 */
}
</style>
