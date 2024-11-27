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
  <section class="rec_table">
    <div>
      <h2>😀예.적금 추천 / 카드 추천 / 정책 추천</h2>
    </div>
    <div>
    <section v-if="RecFinPrdts && RecFinPrdts.recommendations.length">
      <span class="test">
        <h3>1. 상품명</h3>
        <ul>
          <span v-for="(recommendation, index) in RecFinPrdts.recommendations" :key="index">
            <strong>{{ recommendation.product_name }}</strong><br>
            금리: {{ recommendation.interest_rate }}%<br>
            회사명: {{ recommendation.company_name }}<br>
            예금 기간: {{ recommendation.save_term }}개월<br>
          </span>
        </ul>
      </span>
      <hr>
      <span class="test">
        <h3>2. 최고 지출 시간대</h3>
        <ul>
          <li v-for="(top3_hour, index) in RecFinPrdts.top3_hours_account" :key="index">
            계좌: {{ index+1 }}위  {{ top3_hour.hour }}시간 {{ top3_hour.total_spending / 10 }}원
          </li>
          <li v-for="(top3_hour, index) in RecFinPrdts.top3_hours_card" :key="index">
            카드: {{ index+1 }}위  {{ top3_hour.hour }}시간 {{ top3_hour.total_spending / 10 }}원
          </li>
        </ul>
      </span>
      <hr>
      <div class="test">
        <h3>3. 분석</h3>
        <ul>
          <li>월 통장_수입: {{ ((-1)*(RecFinPrdts.monthly_account_income / 10)).toLocaleString() }}원(₩)</li>
          <li>월 통장_지출: {{ (RecFinPrdts.monthly_account_expense / 10).toLocaleString() }}원(₩)</li>
          <li>월 카드_지출: {{ (RecFinPrdts.monthly_card_spending / 10).toLocaleString() }}원(₩)</li>
        </ul>
      </div>
      <div class="test">
        <h3>4. 위험 분석</h3>
        <ul>
          <li v-for="(risk, index) in RecFinPrdts.risks" :key="index">{{ risk }}</li>
        </ul>
      </div>
      <hr>
      <div>
        <img :src="'data:image/png;base64,' + RecFinPrdts.account_hour_graph" alt="Account Graph" style="width: 2114px;">
      </div>
      <div>
        <img :src="'data:image/png;base64,' + RecFinPrdts.card_hour_graph" alt="Card Graph" style="width: 2114px;">
      </div>
    </section>
    <section v-else>
      <button @click="analyzeFinPrdts">분석하기</button>
    </section>
    <hr>
  </div>

  <div>
    <hr>
    <h2>눈여겨볼 정책</h2>
    <section v-if="recPolicies">
      <ul class="policy-list">
  <li v-for="policy in recPolicies" :key="policy.support_id" class="policy-card">
    <div class="policy-content">
      <h3 class="policy-title">{{ policy.title }}</h3>
      <p class="policy-description">{{ policy.description }}</p>
      <ul class="policy-details">
        <li>📅 신청 기간: {{ policy.start_date }} ~ {{ policy.end_date }}</li>
        <li>🧑‍💼 모집 대상: {{ policy.start_age > 0 ? `${policy.start_age}세 이상` : '모든 연령대' }} 
          {{ policy.end_age > 0 ? `${policy.end_age}세 이하` : '' }}</li>
        <li>🏢 담당 기관: {{ policy.department }}</li>
        <li>🌍 지역: {{ policy.region }}</li>
        <li>📞 문의: {{ policy.contact }}</li>
      </ul>
      <a :href="policy.url" class="policy-button" target="_blank">자세히 보기</a>
    </div>
  </li>
</ul>
      <button @click="sendEmail(recPolicies)">send e-mail</button>
      <hr>
    </section>
    <section v-else>
      <button @click="analyzePolicies">분석하기</button>
    </section>
    <hr>
  </div>
</section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';
import PageBanner from '@/components/PageBanner.vue'

const RecFinPrdts = ref()
const rec_cards = ref()
const recPolicies = ref()
const store = useCounterStore()

const analyzeFinPrdts = function () {
  store.analyzeFinPrdts()
  .then((res) => {
    RecFinPrdts.value = res
  });
}

const analyzePolicies = function () {
  store.analyzePolicies()
  .then((res) => {
    recPolicies.value = res.recommended_supports
  });
}


const sendEmail = function (content) {
  store.sendEmail(content.policies)
}

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
.rec_table {
  padding-top:30px;
}

.policy-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  list-style: none;
  padding: 0;
  margin: 20px 0;
}

/* 개별 카드 스타일 */
.policy-card {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  transition: box-shadow 0.3s ease, transform 0.3s ease;
}

.policy-card:hover {
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  transform: translateY(-5px);
}

/* 카드 제목 스타일 */
.policy-title {
  font-size: 18px;
  font-weight: bold;
  margin: 0 0 10px;
  color: #333;
}

/* 카드 설명 스타일 */
.policy-description {
  font-size: 14px;
  color: #555;
  margin: 0 0 15px;
  line-height: 1.4;
}

/* 세부사항 리스트 */
.policy-details {
  font-size: 13px;
  color: #666;
  margin: 0 0 15px;
  padding: 0;
  list-style: none;
}

.policy-details li {
  margin-bottom: 5px;
}

/* 버튼 스타일 */
.policy-button {
  display: inline-block;
  background-color: #007bff;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  padding: 10px 15px;
  font-size: 14px;
  font-weight: bold;
  transition: background-color 0.3s ease;
  cursor: pointer;
}

.policy-button:hover {
  background-color: #0056b3;
}



li:hover {
  transform: translateY(-4px); /* 마우스 호버 시 살짝 띄우기 */
  background-color: #f1f5ff; /* 호버 시 배경색 변경 */
}

li strong {
  font-size: 1.2em; /* 제품명 강조 */
  color: #333; /* 진한 텍스트 색상 */
  margin-bottom: 8px;
  display: block;
}

li br {
  display: none; /* br 제거로 보기 좋게 */
}

li span {
  display: block; /* 한 줄에 하나씩 표시 */
  margin-bottom: 4px; /* 각 항목 간 간격 */
  font-size: 0.95em; /* 약간 작은 글씨 */
  color: #555; /* 부드러운 텍스트 색상 */
}

.test {
  width: 500px;
}
</style>