<template>
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
  
  <div class="main-page">
    <hr />
    <MainPageBannerView />
    <MainPageArticleView class="MainPageArticleView" />
    <MainPageYouthPolicyView />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import PageBanner from '@/components/PageBanner.vue'
import MainPageBannerView from './MainPageBannerView.vue'
import MainPageYouthPolicyView from '@/views/mainPage/MainPageYouthPolicyView.vue'
import MainPageArticleView from '@/views/mainPage/MainPageArticleView.vue'

const bannerVisible = ref(false)

onMounted(() => {
  // 배너 표시
  setTimeout(() => {
    bannerVisible.value = true
  }, 1000) // 1초 후에 배너 표시

  // 배너가 3초 후에 사라지게 설정
  setTimeout(() => {
    bannerVisible.value = false
  }, 4000) // 배너가 3초간 표시된 뒤 사라짐
})

// 애니메이션 시작 전 설정
const beforeEnter = (el) => {
  el.style.transform = 'translateY(-110px)'
  el.style.opacity = '0'
}

// 애니메이션 실행
const enter = (el, done) => {
  el.offsetHeight // trigger reflow
  el.style.transition = 'transform 1s ease-in-out, opacity 1s ease-in-out'
  el.style.transform = 'translateY(0px)'
  el.style.opacity = '1'
  setTimeout(done, 1000) // 1초 후 애니메이션 종료
}

// 배너가 사라질 때의 애니메이션 설정
const leave = (el, done) => {
  el.style.transition = 'transform 1s ease-in-out, opacity 1s ease-in-out'
  el.style.transform = 'translateY(-110px)' // 위로 올라감
  el.style.opacity = '0' // 서서히 투명
  setTimeout(done, 1000) // 1초 후 애니메이션 종료
}
</script>

<style scoped>
.main-page {
  display: flex;
  flex-direction: column;  /* 자식 요소를 세로로 배치 */
  justify-content: flex-start; /* 상단 정렬 */
  align-items: center;     /* 수평 중앙 정렬 */
  min-height: 100vh;       /* 화면 높이가 최소 100vh */
  box-sizing: border-box;  /* 여백 및 패딩을 요소 크기에 포함 */
  width: 2114px;
}

h1 {
  font-size: 2rem;
  margin-bottom: 20px; /* 제목과 첫 번째 컴포넌트 사이 여백 */
}


</style>
