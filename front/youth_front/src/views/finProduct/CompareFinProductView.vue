<template>
  <div>
    <hr>
    <h1>예적금 통합조회</h1>
    <form @submit.prevent="searchFinPrdts">
      <!-- 상품 이름 및 내용 검색 -->
      <div>
        <label>이름 및 내용</label>
        <input type="text" v-model="keyword" placeholder="키워드를 입력하세요" />
      </div>

      <!-- 상품 유형 선택 -->
      <div>
        <label>상품 유형</label>
        <select v-model="productType">
          <option>예금</option>
          <option>적금</option>
        </select>
      </div>

      <!-- 가입 기간 선택 -->
      <div>
        <label for="term">가입 기간: </label>
        <input type="text" v-model="min_term" placeholder="월 단위"/>개월
        ~
        <input type="text" v-model="max_term" placeholder="월 단위"/>개월
      </div>

      <!-- 이자 유형 -->
      <div>
        <label>금리유형</label>
        <select v-model="intr_rate_type">
          <option value="">전체</option>
          <option value="S">단리</option>
          <option value="M">복리</option>
        </select>
      </div>

      <!-- 적립 유형 -->
      <div>
        <label>적립 유형</label>
        <select v-model="cum_type">
          <option value="">전체</option>
          <option>자유적립식</option>
          <option>정액적립식</option>
        </select>
      </div>

      <!-- 제출 버튼 -->
      <button type="submit">검색</button> 
      <p v-show="!isClickable" style="color: red">상품 유형을 선택해 주세요.</p>
    </form>

    <hr>
    <hr>
    <div>
      <h2>검색 결과: {{ searchedPrdts?.length }}건</h2>
      <div v-if="totalPages > 1" class="pagination">
        <button @click="changePage(-1)" :disabled="currentPage === 1"><</button>
        <span style="font-size: 30px; margin-left: 20px; margin-right: 20px;">페이지 {{ currentPage }} / {{ totalPages }}</span>
        <button @click="changePage(+1)" :disabled="currentPage === totalPages">></button>
      </div>
    </div>
  </div>
  <hr>
  <ul v-if="totalPages > 1" class="product-list">
        <li v-for="prdt in paginatedResults" :key="prdt.name" class="product-card">
          <div class="product-content">
            <h3 class="product-title">{{ prdt.fin_prdt_nm }}</h3>
            <p class="product-details">세부사항: {{ prdt.etc_note }}</p>
            <p class="product-details">가입 기간: {{ prdt.save_trm }}개월</p>
            <p class="product-details">이자유형: {{ prdt.intr_rate_type_nm }}</p>
            <p class="product-details">최대금리: {{ prdt.intr_rate2 }}</p>
          </div>
        </li>
      </ul>
        <!-- 페이지네이션 -->
</template>

<script setup>
  import { ref, watch, onMounted, computed } from 'vue'
  import { useCounterStore } from '@/stores/counter'

  const store = useCounterStore()

  const keyword = ref('')
  const productType = ref('예금')
  const min_term = ref(12)
  const max_term = ref(36)
  const intr_rate_type = ref('S')
  const cum_type = ref('')
  const searchedPrdts = ref(null)

  const currentPage = ref(1)
  const itemsPerPage = 12 // 한 페이지당 10개씩 표시

  // 검색 결과 상태 감시
  watch(
    () => store.searchedFinPrdts,
    () => {
      searchedPrdts.value = store.searchedFinPrdts
    }
  )

  const totalPages = computed(() =>
    searchedPrdts.value ? Math.ceil(searchedPrdts.value.length / itemsPerPage) : 1
  )

  const paginatedResults = computed(() => {
    if (!searchedPrdts.value) return []
    const start = (currentPage.value - 1) * itemsPerPage
    const end = start + itemsPerPage
    return searchedPrdts.value.slice(start, end)
  })

  const changePage = (weight) => {
    if (currentPage.value == 1 && weight == -1) {
      currentPage.value = 1
    } 
    else if (currentPage.value == totalPages.value && weight == +1) {
      currentPage.value = totalPages.value
    }
    else {
      currentPage.value = currentPage.value + weight
    }
  }

  const isClickable = ref(true)
  const searchFinPrdts = function () {
    if (productType.value) {
      isClickable.value = true
      store.searchFinPrdts(
        keyword.value,
        productType.value,
        min_term.value,
        max_term.value,
        intr_rate_type.value,
        cum_type.value
      )
    } else {
      isClickable.value = false
    }
    currentPage.value = 1
  }

  const bannerVisible = ref(false)
  onMounted(() => {
    store.searchFinPrdts(
      keyword.value,
      productType.value,
      min_term.value,
      max_term.value,
      intr_rate_type.value,
      cum_type.value
    )
  })

</script>

<style scoped>
/* 폼 스타일 */
form {
  margin: 20px 0;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #f9f9f9;
}

form div {
  margin-bottom: 15px;
}

form label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

form input,
form select {
  width: 100%;
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* 버튼 스타일 */
button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px 15px;
  font-size: 16px;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

/* 검색 결과 스타일 */
ul {
  list-style-type: none;
  padding: 0;
}

li {
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

h2 {
  margin-top: 20px;
  color: #333;
}

.product-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); /* 카드 크기 */
  gap: 20px; /* 카드 간격 */
  list-style: none;
  padding: 0;
  margin: 20px 0;
}

/* 개별 카드 스타일 */
.product-card {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  padding: 20px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  width: 300px;
  height: 400px;
}

/* 카드 호버 효과 */
.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

/* 카드 내용 스타일 */
.product-content {
  text-align: left;
}

/* 제목 스타일 */
.product-title {
  font-size: 18px;
  font-weight: bold;
  margin: 0 0 10px;
  color: #333;
}
</style>
