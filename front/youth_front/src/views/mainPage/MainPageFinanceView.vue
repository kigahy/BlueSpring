<template>
  <div class="main-container">
    <!-- 예적금 섹션 -->
    <div class="fin-prdt-section">
      
      <!-- 예금상품 섹션 -->
      <div class="deposits">
        <h2>최근 출시된 예금상품</h2>
        <div class="product-grid">
          <div 
            v-for="product in depositPrdts" 
            :key="product.fin_prdt_cd" 
            class="product-item"
          >
            <div class="product-item-info">
              <div class="product-header">
                <h4>{{ product.fin_prdt_nm.split('(')[0].trim() }}</h4>
                <h4>({{ product.kor_co_nm }})</h4>
              </div>
            </div>
            <p class="product-code">상품 코드: {{ product.fin_prdt_cd }}</p>
            <!-- 모든 옵션을 토글하는 버튼 -->
            <p @click="toggleOptions" class="option-button">옵션 {{ visibleText }}</p>
            <div v-if="isOptionsVisible" class="options">
              <div v-for="option in product.options" :key="option.option_id">
                <p>저축 기간: {{ option.save_trm }}개월</p>
                <p>금리: {{ option.intr_rate }}%</p>
                <hr>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 적금상품 섹션 -->
      <div class="savings">
        <h2>최근 출시된 적금상품</h2>
        <div class="product-grid">
          <div 
            v-for="product in savingPrdts" 
            :key="product.fin_prdt_cd" 
            class="product-item"
          >
            <div class="product-item-info">
              <div class="product-header">
                <h4>{{ product.fin_prdt_nm.split('(')[0].trim() }}</h4>
                <h4>({{ product.kor_co_nm }})</h4>
              </div>
            </div>
            <p class="product-code">상품 코드: {{ product.fin_prdt_cd }}</p>
            <!-- 모든 옵션을 토글하는 버튼 -->
            <p @click="toggleOptions" class="option-button">옵션 {{ visibleText }}</p>
            <div v-if="isOptionsVisible" class="options">
              <div v-for="option in product.options" :key="option.option_id">
                <p>저축 기간: {{ option.save_trm }}개월</p>
                <p>금리: {{ option.intr_rate }}%</p>
                <hr>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

// Django 서버 API URL
const BASE_URL = 'http://127.0.0.1:8000/api/v1/fin_products/recent_prdt_main/';

// 상태 변수
const depositPrdts = ref([]);
const savingPrdts = ref([]);
const visibleOptions = ref(false); // 옵션이 보이는지 여부
const visibleText = ref('보기')
// 상품 옵션을 토글하는 함수
const toggleOptions = () => {
  if (visibleOptions.value) {
    visibleOptions.value = false
    visibleText.value = '닫기'
  }
  else {
    visibleOptions.value = true
    visibleText.value = '보기'
  }
};

// 상품의 옵션이 보이는지 확인하는 함수
const isOptionsVisible = computed(() => visibleOptions.value); // 옵션 보이기 상태

// 컴포넌트가 마운트될 때 API 호출
onMounted(() => {
  axios
    .get(BASE_URL)
    .then((response) => {
      // 데이터 추가: 예금상품과 적금상품 정보를 저장
      depositPrdts.value = response.data.deposits;
      savingPrdts.value = response.data.savings;
    })
    .catch((error) => {
      console.error('정책 데이터를 가져오는 중 오류 발생:', error);
    });
});
</script>

<style scoped>
/* 기본 스타일 */

body {
  font-family: 'Roboto', sans-serif;
  background-color: #f4f6f9;
  color: #333;
}

/* 메인 컨테이너 */
.main-container {
  margin-top: 30px;
  width: 100px;
}

/* 예적금 섹션 */
.fin-prdt-section {

  border-radius: 10px;
  padding: 20px;
  border: none;
  width: 1000px;
}

h2 {
  font-size: 1.6em;
  color: #2c3e50;
  margin-bottom: 20px;
  border-bottom: 2px solid #e0e0e0;
  padding-bottom: 10px;
}

/* 상품 그리드 */
.product-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

/* 개별 상품 항목 */
.product-item {
  display: grid;
  grid-template-rows: auto 1fr auto; /* 세로 방향으로 3개의 영역을 설정 */
  justify-items: center; /* 모든 자식 요소 중앙 정렬 */
  background-color: #ffffff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e5e5;
}

.product-item h4 {
  font-weight: bold;
}

.product-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.product-header {
  font-size: 1.1em;
  color: #34495e;
  margin-bottom: 15px;
}

.product-header h3 {
  margin-bottom: 10px;
  color: #2c3e50;
}

button {
  padding: 8px 16px;
  background-color: #2980b9;
  color: #fff;
  border: none;
  border-radius: 5px;
  font-size: 1em;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #1f5f82;
}

/* 옵션 스타일 */
.options {
  margin-top: 15px;
  background-color: #ecf0f1;
  padding: 15px;
  border-radius: 8px;
  height: 350px;
  width: 250px;
  text-align: center;
}

.options p {
  font-size: 1em;
  color: #7f8c8d;
  margin-bottom: 10px;
}

hr {
  border: 1px solid #ecf0f1;
  margin: 10px 0;
}

/* 적금 상품 섹션 */
.savings {
  margin-top: 50px;
}

.product-header h4 {
  text-align: center;   /* 텍스트 중앙 정렬 */
  word-wrap: break-word; /* 긴 단어가 줄 바꿈되도록 */
  word-break: break-word; /* 긴 단어가 화면을 넘지 않도록 줄 바꿈 */
}

.product-code {
  text-align: center;   /* 텍스트 왼쪽 정렬 */
  position: relative;
  top: 0px;
}

.option-button {
  position: relative;
  width: 100px;
  height: 30px;
  background-color: #fff29d;
  border-radius: 6px;
  text-align: center; /* 텍스트 가로 정렬 */
  color: #333333;
  font-weight: bold;

  line-height: 30px; /* 버튼 높이와 동일하게 설정 */
}


.option-button:hover {
  background-color: #FFDD00;
}

.product-item-info {
  height: 150px;
}
</style>
