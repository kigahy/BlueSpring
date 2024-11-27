<template>
  <div>
    <div class="job-cards">
      <h1>채용 공고 모아보기</h1>
      <div v-if="Array.isArray(selectedJob)">
        <div v-for="job in selectedJob" :key="job.job_title" class="job-card">
          <h3>{{ job.job_title }}</h3>
          <p><strong>회사명:</strong> {{ job.company_name }}</p>
          <p><strong>대상 지역:</strong> {{ job.location }}</p>
          <p><strong>급여:</strong> {{ job.salary }}</p>
          <p><strong>고용 형태:</strong> {{ job.job_type }}</p>
          <p>
            <strong>공고 기간:</strong> {{ job.start_date }} ~
            {{ job.end_date }}
          </p>
          <p><strong>연관도 점수:</strong> {{ job.score }}</p>
          <div class="btn-container">
          <a :href="job.job_url" target="_blank" class="btn">공고 상세보기</a>
          <a :href="job.company_url" target="_blank" class="btn">회사정보 보기</a>
        </div>
        </div>
      </div>
      <!-- <div v-else>
        <h2>{{ selectedJob.job_title }}</h2>
        <p><strong>회사명:</strong> {{ selectedJob.companyName }}</p>
        나머지 정보 출력
      </div> -->
    </div>

    <div class="job-cards">
      <h1>청년 지원 모아보기</h1>
      <div v-if="Array.isArray(selectedSupport)">
        <div v-for="sup in selectedSupport" :key="sup.title" class="job-card">
          <h3>{{ sup.title }}</h3>
          <p><strong>담당 기관:</strong> {{ sup.department }}</p>
          <p><strong>대상 지역:</strong> {{ sup.region }}</p>
          <p><strong>상세 설명:</strong> {{ sup.description }}</p>
          <strong>대상 연령:</strong>
          <span v-if="sup.start_age === 0 && sup.end_age === 0">
            제한 없음
          </span>
          <span v-else>
            {{ sup.start_age }} ~
          {{ sup.end_age }}
          </span>
          
          <p>
            <strong>모집 기간:</strong> {{ sup.start_date }} ~
            {{ sup.end_date }}
          </p>
          <p><strong>연관도 점수:</strong> {{ sup.score }}</p>
          <div class="btn-container">
          <a :href="sup.url" target="_blank" class="btn">공고 상세보기</a>
        </div>
        </div>
      </div>
      <!-- <div v-else>
        <h2>{{ selectedSupport.title }}</h2>
        <p><strong>담당 기관:</strong> {{ selectedSupport.department }}</p>
      </div> -->
    </div>

  </div>
</template>

<script setup>
import { ref } from "vue";

const selectedJob = ref([]); // 채용 공고 리스트
const selectedSupport = ref([]); // 지원 정보 리스트

// 데이터 로드
import axios from "axios";
import { useCounterStore } from "@/stores/counter";
const counterStore = useCounterStore();

axios.get("http://127.0.0.1:8000/api/v1/recruits/", {
  headers: {
    Authorization: `Token ${counterStore.token}`,
  },
})
.then((response) => {
  selectedJob.value = response.data.recommended_jobs; // 데이터 저장
})
.catch((error) => {
  console.error("채용 정보 로드 실패:", error.response || error.message);
});

axios.get("http://127.0.0.1:8000/api/v1/recruits/supports/", {
  headers: {
    Authorization: `Token ${counterStore.token}`,
  },
})
.then((userResponse) => {
  selectedSupport.value = userResponse.data.recommended_supports; // 데이터 저장
})
.catch((error) => {
  console.error("지원 정보 로드 실패:", error.response || error.message);
});

import "@/assets/css/calendarinfo.css";
</script>

