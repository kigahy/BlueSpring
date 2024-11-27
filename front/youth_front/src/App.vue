<template>
  <div class="main-container">
    <!-- 네비게이션 바 -->
    <NavBar :is-logged-in="isLoggedIn" />

    <!-- 라우터 뷰 -->
    <RouterView />
  </div>

  <!-- 푸터뷰 -->
  <footerView />
</template>

<script setup>

import { ref, onMounted} from 'vue'
import footerView from '@/views/mainPage/footerView.vue'
import NavBar from '@/components/NavBar.vue'
import { RouterView } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()

const bannerVisible = ref(false)
const isLoggedIn = ref(false)

// 로그인 상태 확인
onMounted(() => {
  isLoggedIn.value = store.isLogin
  if (store.isLogin) {
    store.getProfile();
  }

});


// 검색 기능 예시
const search = (searchQuery) => {
  if (searchQuery) {
    console.log("검색어:", searchQuery)
    // 여기에 검색 로직을 추가하세요.
  }
}
</script>

<style>
.main-container {
  background-color: #fffbca;
  width: 2114px;
  /* height: 8000px; */
  position: relative;
}

NavBar {
  width: 100%;
  margin-bottom: 20px;
  background-color: white;
}

RouterView {
  width: 100%;
}

div {
  cursor: url('@/assets/cursor/choonsik_defualt.gif'), auto;
}
</style>