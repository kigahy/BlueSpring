<template>
  <div class="page-banner">
    <h1>{{ title }}</h1>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

// props로 title과 description을 받습니다.
defineProps({
  title: {
    type: String,
    required: true,
  },
});
</script>

<style>
.page-banner {
  background-color: #f1d667; /* 춘식이 노란색 */
  color: white; /* 글자색 */
  display: flex; /* Flexbox 레이아웃 활성화 */
  align-items: center; /* 세로 가운데 정렬 */
  justify-content: center; /* 가로 가운데 정렬 */
  height: 120px; /* 배너 높이 */
  padding: 0; /* 내부 여백 제거 */

  border-bottom: 2px solid #ccae53; /* 하단 경계선 */
  box-sizing: border-box; /* 패딩 포함 크기 */
  text-align: center; /* 텍스트 가운데 정렬 */
}

.page-banner h1 {
  font-weight: bold;
  font-size: 2rem;
  margin: 0; /* 여백 제거 */
}

.page-banner p {
  font-size: 1.2rem;
  margin: 0; /* 여백 제거 */
}

.slide-down-enter-active, .slide-down-leave-active {
  transition: transform 2s ease-in-out;
}

.slide-down-enter, .slide-down-leave-to {
  transform: translateY(-110px);  /* 초기 위치 */
}
</style>
