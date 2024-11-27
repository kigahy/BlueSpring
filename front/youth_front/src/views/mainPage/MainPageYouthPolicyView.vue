<template>
  <div class="main-container">

    <!-- 정책 섹션 -->
    <div class="policy-section">
      <div class="title">
        <h2>최근 중앙부처 정책</h2>
        <hr>
      </div>
      <div class="product-grid">
        <div v-for="policy in policies" :key="policy.bizId" class="product-item">
          <div class="product-header">
            <h3>{{ policy.polyBizSjnm }}</h3>
            <p>{{ policy.polyItcnCn }}</p>
          </div>
          <div class="options">
            <a
              :href="'https://youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifDtl.do?bizId=' + policy.bizId"
              target="_blank"
              rel="noopener noreferrer"
            >
              자세히 보기
            </a>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// Django 서버 API URL
const BASE_URL = 'http://127.0.0.1:8000/api/v1/policies/youth_policies_main/';

// 상태 변수
const policies = ref([]);

// 컴포넌트가 마운트될 때 API 호출
onMounted(() => {
  axios
    .get(BASE_URL)
    .then((response) => {
      // 데이터 추가: 정책 정보를 상태 변수에 저장
      if (response.data && response.data.youthPolicyList) {
        policies.value = response.data.youthPolicyList.youthPolicy.map((policy) => ({
          bizId: policy.bizId,
          polyBizSjnm: policy.polyBizSjnm,
          polyItcnCn: policy.polyItcnCn,
        }));
      }
    })
    .catch((error) => {
      console.error('정책 데이터를 가져오는 중 오류 발생:', error);
    });
});
</script>

<style scoped>
.main-container {
  padding: 20px;
  width: 2114px;
  height: 500px;
}

.policy-section {
  box-sizing: border-box;
  border-radius: 8px;
  border: none;
  margin-top: 20px;
  padding-left:20px;
  padding-right:20px;
}

.product-grid {
  display: grid; /* flex 대신 grid로 변경 */
  grid-template-columns: repeat(3, 1fr); /* 3개의 컬럼으로 설정 */
  gap: 20px;
}

.product-item {
  background-color: #fff; /* 배경을 흰색으로 설정 */
  padding: 20px;
  border-radius: 10px;
  box-sizing: border-box;
  width: 100%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* 깊이감을 주기 위해 그림자 추가 */
  transition: transform 0.3s ease, box-shadow 0.3s ease; /* 호버 시 애니메이션 */
}

.product-item:hover {
  transform: translateY(-5px); /* 마우스 오버 시 위로 살짝 올라가는 효과 */
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2); /* 호버 시 그림자 강도 증가 */
}

.product-header {
  margin-bottom: 15px;
}

.product-header h3 {
  font-size: 18px;
  margin-bottom: 8px;
  font-weight: bold;
  color: #333;
}

.product-header p {
  font-size: 14px;
  color: #777;
  margin-bottom: 15px;
  line-height: 1.5;
}


.options a {
  display: inline-block;
  padding: 10px 20px;
  color: #333;
  background-color: #fff29d; /* 버튼 색상 */
  text-decoration: none;
  font-weight: bold;
  border-radius: 6px;
  text-align: center;
  transition: background-color 0.3s ease;
  position: relative;
  left: 515px;
}

.options a:hover {
  background-color: #FFDD00; /* 호버 시 어두운 파랑색으로 변경 */
}

.title {
  padding-top: 15px;
}

</style>