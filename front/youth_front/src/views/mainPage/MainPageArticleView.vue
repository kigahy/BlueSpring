<template>
  <div class="content-container">
    <!-- 탭 메뉴 -->
    <div class="tabs">
      <ul>
        <li>
          <a href="#" :class="{ active: activeTab === 'finance' }" 
             @click="changeTab('finance', $event)" class="tab-article">
             Finance
          </a>
        </li>
        <li>
          <a href="#" :class="{ active: activeTab === 'news' }" 
             @click="changeTab('news', $event)" class="tab-article">
             News
          </a>
        </li>
        <li>
          <a href="#" :class="{ active: activeTab === 'live-exchange-info' }" 
             @click="changeTab('live-exchange-info', $event)" class="tab-article">
             실시간 환율정보
          </a>
        </li>
      </ul>
    </div>
    <!-- 금융 섹션 -->
    <div v-if="activeTab === 'finance'" class="finance-section">
      <div class="finance-container">
        <!-- 추천 금융 상품 -->
        <div class="finance-product">
          <div class="finance-indicators">
            <table class="exchange-rates-table">
              <tr>
                <td class="currency-name">달러</td>
                <td>
                  <p :style="{color: usdFluc}" class="currency-value">
                    {{ usdKrw }}$/1000₩
                  </p>
                </td>
                <td class="currency-code">USD/KRW</td>
              </tr>
              <tr>
                <td class="currency-name">엔화</td>
                <td>
                  <p :style="{color: jpyFluc}" class="currency-value">
                    {{ jpyKrw }}¥/1000₩
                  </p>
                </td>
                <td class="currency-code">JPY/KRW</td>
              </tr>
              <tr>
                <td class="currency-name">위안화</td>
                <td>
                  <p :style="{color: cnyFluc}" class="currency-value">
                    {{ cnyKrw }}元/1000₩
                  </p>
                </td>
                <td class="currency-code">CNY/KRW</td>
              </tr>
              <tr>
                <td class="currency-name">유로화</td>
                <td>
                  <p :style="{color: eurFluc}" class="currency-value">
                    {{ eurKrw }}€/1000₩
                  </p>
                </td>
                <td class="currency-code">EUR/KRW</td>
              </tr>
            </table>
          </div>
          <MainPageFinanceView />
        </div>

        <div class="finance-video">
          <div v-for="video in financeVideos" :key="video.id" class="video-card">
            <div class="video-content">
              <div class="video">
                <!-- YouTube iframe -->
                <iframe :src="'https://www.youtube.com/embed/' + video.id" frameborder="0" allowfullscreen></iframe>
              </div>
              <!-- 영상 정보 -->
              <div class="video-info">
                <h4 class="video-title">{{ video.title }}</h4>
                <p>{{ video.description }}</p>
                <p class="video-details">업로드 날짜: {{ video.publishedAt }}</p>
              </div>
            </div>
          </div>
          <div class="source-info">이 영상은 금융감독원에서 제공한 자료로, 저작권은 금융감독원에 있으며, 
            해당 영상은 유튜브 API를 통해 제공됩니다. 금융감독원 공식 유튜브 채널에서 발표된 콘텐츠로, 
            금융 교육 및 정책 홍보를 목적으로 제작되었습니다. 본 영상에 사용된 모든 저작권 및 지식 재산권은 
            금융감독원에 있으며, 해당 영상의 사용과 재배포는 금융감독원의 공식 승인을 받아야 합니다. 자세한 
            사항은 금융감독원 공식 홈페이지(https://www.fss.or.kr)를 참조해 주시기 바랍니다."</div>
        </div>
      </div>
    </div>
    <div v-if="activeTab === 'live-exchange-info'" class="live-exchange-info-section">

    <!-- 실시간 환율 정보 섹션 -->
    <div v-if="activeTab === 'live-exchange-info'" class="live-exchange-info-section">
      <!-- 환율 선택 탭 -->
      <div class="tabs">
        <ul>
          <li v-for="currency in currencies" :key="currency.type">
            <a 
              href="#" 
              :class="{ active: selectedCurrency === currency.type }" 
              @click.prevent="selectCurrency(currency.type, $event)" 
              class="tab-article">
              {{ currency.label }}
            </a>
          </li>
        </ul>
        </div>

      <!-- 선택된 환율 정보 표시 -->
    <section class="exchange-tab">        
      <div class="exchange-rate-container">
        <iframe 
          :title="`실시간 ${selectedCurrency} 환율 정보`" 
          :src="`https://finance.naver.com/marketindex/exchangeDegreeCountQuote.naver?marketindexCd=FX_${selectedCurrency}KRW`" 
          id="exchangeDegreeCountQuote" 
          width="700px" 
          height="415px" 
          frameborder="0" 
          scrolling="no" 
          marginheight="0" 
          marginwidth="0" 
          style="height: 416px;">
        </iframe>
      </div>
      <div class="exchange-rate-container">
        <iframe 
          :title="`실시간 ${selectedCurrency} 고시회차별 시세`" 
          :src="`https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_${selectedCurrency}KRW`" 
          id="exchangeDailyQuote" 
          width="700px" 
          height="415px" 
          frameborder="0" 
          scrolling="no" 
          marginheight="0" 
          marginwidth="0" 
          style="height: 416px;">
        </iframe>
      </div>
          <!-- 환율 계산기 -->
        <div class="exchange-calculator">
          <form @submit.prevent="calculateExchange(selectedCurrency)">
            <span class="exchange-calculator-name">환율 계산기</span> 
            <button class="exchange-calculator-button">계산</button>
            <select v-model="selectedCurrency" class="select-currency">
              <option v-for="currency in currencies" :value="currency.type">{{ currency.label }}</option>
            </select>
            <input v-model.number="amount" 
            class="input-select-currency"
             type="number" 
             @input="resetCalculatedAmount" 
             placeholder="금액 입력 (₩)">
            <div v-if="calculatedAmount" class="result">
              {{ amount }}₩ → {{ calculatedAmount }} {{ selectedCurrency }}
            </div>
        </form>
        </div>
    </section>
    </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import MainPageFinanceView from '@/views/mainPage/MainPageFinanceView.vue';
import axios from 'axios';

const financeVideos = ref([]); // 금융감독원 유튜브 영상 저장
const CHANNEL_ID = 'UCjA-tHJ2xLwZRXzqXq0UaqA'; // 금융감독원 채널 ID
const activeTab = ref('finance');

const changeTab = function (tab, event) {
  event.preventDefault();
  activeTab.value = tab;
  if (tab === 'finance') {
    getExchange()
  }
}

const selectedCurrency = ref('USD') // 초기값: 달러
const currencies = [
  { type: 'USD', label: '달러(USD)' },
  { type: 'JPY', label: '엔화(JPY)' },
  { type: 'CNY', label: '위안화(CNY)' },
  { type: 'EUR', label: '유로화(EUR)' },
]
const selectCurrency = function (currencyType, event) {
  selectedCurrency.value = currencyType
}
const YOUTUBE_API_KEY = '1AIzaSyB7Ry2Ab5Kf9mC9etaPKea4s8pJqRnNvJI';
// AIzaSyBYx589z1Cpdb8LDVwRdrNqRKFpbPfqBHI
const fetchFinanceVideos = function () {
  axios({
    method: 'get',
    url: `https://www.googleapis.com/youtube/v3/search?key=${YOUTUBE_API_KEY}&channelId=${CHANNEL_ID}&part=snippet&type=video&order=date&maxResults=3`,
  })
  .then((res)=> {
    financeVideos.value = res.data.items.map((item) => ({
      id: item.id.videoId,
      title: item.snippet.title,
      description: item.snippet.description,
      thumbnail: item.snippet.thumbnails.high.url,
      publishedAt: item.snippet.publishedAt,
    }))    
  })
  .catch((err)=> {
    console.error('YouTube API 호출 실패:', err);
  })
}

const usdKrw = ref(null)
const usdFluc = ref(null)
const jpyKrw = ref(null)
const jpyFluc = ref(null)
const cnyKrw = ref(null)
const cnyFluc = ref(null)
const eurKrw = ref(null)
const eurFluc = ref(null)
// 환율계산기 관련
// 실시간 환율 iframe URL들
const exchangeIframeUrls = [
  'https://example.com/exchange1',
  'https://example.com/exchange2'
]

// 환율 데이터
const currencyData = ref([
  { CurrencyName: 'USD', name: '달러', rate: usdKrw.value, code: 'USD/KRW' },
  { CurrencyName: 'JPY', name: '엔화', rate: jpyKrw.value, code: 'JPY/KRW' },
  { CurrencyName: 'CNY', name: '위안화', rate: cnyKrw.value, code: 'CNY/KRW' },
  { CurrencyName: 'EUR', name: '유로화', rate: eurKrw.value, code: 'EUR/KRW' }
])

// 환율 계산기
const amount = ref(0)
const calculatedAmount = ref(null)

const getRateByCurrencyName = function(currencyName) {
  const currency = currencyData.value.find(c => c.CurrencyName === currencyName)  // CurrencyName이 일치하는 객체 찾기
  return currency ? currency.rate : 0  // 일치하는 객체가 있으면 rate 값 반환, 없으면 0 반환
}

const calculateExchange = (selectedCurrency) => {
  if (amount.value) {
    const rate = getRateByCurrencyName(selectedCurrency)
    calculatedAmount.value = ((amount.value / parseFloat(rate.replace(/,/g, '')))).toFixed(2)
  }
  else {
    amount.value = 0
    calculatedAmount.value = 0
  }
}
const resetCalculatedAmount = function () {
  calculatedAmount.value = null
} 
const getExchange = function () {
  axios({
    method: 'get',
    url: 'http://127.0.0.1:8000/api/v1/fin_products/main/dollar/',
  })
  .then((res) => {
    // 응답 데이터로 개별 환율 변수 업데이트
    usdKrw.value = res.data.usd;
    usdFluc.value = res.data.usd_fluc;
    jpyKrw.value = res.data.jpy;
    jpyFluc.value = res.data.jpy_fluc;
    cnyKrw.value = res.data.cny;
    cnyFluc.value = res.data.cny_fluc;
    eurKrw.value = res.data.eur;
    eurFluc.value = res.data.eur_fluc;

    // currencyData 업데이트
    currencyData.value = [
      { CurrencyName: 'USD', name: '달러', rate: usdKrw.value, code: 'USD/KRW' },
      { CurrencyName: 'JPY', name: '엔화', rate: jpyKrw.value, code: 'JPY/KRW' },
      { CurrencyName: 'CNY', name: '위안화', rate: cnyKrw.value, code: 'CNY/KRW' },
      { CurrencyName: 'EUR', name: '유로화', rate: eurKrw.value, code: 'EUR/KRW' }
    ]
  })
  .catch((err) => {
    console.log('환율정보 가져오기 실패', err);
  });
};

onMounted(() => {
  fetchFinanceVideos()
  getExchange()
})
</script>

<style scoped>
/* 기본 스타일 */
.content-container {
  font-family: Arial, sans-serif;
  width: 100%;
  padding: 20px 0px 20px 20px;
  border-radius: 8px;

}

.tab-article {
  color:#333333;
  text-decoration-line: none;
}

.tabs ul {
  display: flex;
  list-style: none;
  padding-left: 0;
}

.tabs li {
  margin: 0 10px;
}

.tabs a.active {
  color:#7c7c7c;
  font-weight: bold;
}

.news-section {
  margin-top: 20px;
}

.article {
  display: flex;
  margin-bottom: 20px;
}


.finance-section {
  min-height: 1000px;
  margin-top: 20px;
}

/* 금융 파트 섹션을 가로로 배치 */
.finance-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: space-between;
}

.finance-product {
  flex: 1 1 33%; /* Allow each section to take up 33% of the container */
  box-sizing: border-box;
  border-radius: 8px;
  border: none;
  padding: 20px 20px 20px 20px;
  min-width: 900px;
}

.finance-video {
  flex: 1 1 33%; /* Allow each section to take up 33% of the container */
  box-sizing: border-box;
  border-radius: 8px;
  border: none;
  padding: 20px 20px 20px 20px;
  height: 1173.40px;

}

.finance-indicators {
  border: 1px;
  
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
}

.finance-indicators:hover {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* 부드러운 그림자 */
}

.finance-indicators table {
  width: 100%;
  text-align: center;
  font-size: 16px;
}

.finance-indicators table td {
  padding: 10px;
}

.video-content,
.video {
  width: 500px;
  height: 300px;
  border-radius: 8px;
}

.video {
  border: 1px solid;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 약간의 그림자 */
  border-color: rgba(140, 140, 240, 0.486);
}
.video-card {
  margin-bottom: 30px;
  width: 900px;
  height: 300px;
}


.video {
  padding-top: 50%;
  position: relative;
}

.video iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 8px;
}

.video-info {
  text-align: center;
  width: 400px;
  background-color: white;
  border-radius: 8px;
  border: 2px solid;
  justify-content: flex-start; /* 상단 정렬 */
  border: none;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1); /* 약간의 그림자 */
  padding-top: 20px;
  padding-left: 50px;
  padding-right: 50px;
  margin-left:35px;
}

.video-info:hover {
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
}

.video-title {
  font-size: 18px;
  font-weight: bold;
}

.video-details {
  font-size: 14px;
  color: #777;
}

.video-card img {
  width: 100%;
  max-width: 500px;
  height: auto;
  border-radius: 8px;
  margin-bottom: 15px;
}

.exchange-tab {
  display: grid; /* CSS Grid 사용 */
  grid-template-columns: repeat(3, 1fr); /* 두 개의 동일한 열 */
  gap: 60px; /* 두 컨테이너 사이 간격 */
}

.exchange-rate-container {
  border: 1px solid #ddd; /* 컨테이너 경계 */
  border-radius: 8px;
  padding: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 약간의 그림자 */
  background-color: #fff;
  width: 730px;
}

.video-content {
  width: 900px;
  display: grid;
  grid-template-columns: 60% 35%; /* 비디오 영역 60%, 비디오 정보 영역 35% */
  gap: 20px; /* 각 요소 사이의 간격 */
}

.video {
  width: 557px;
  height: auto;
  position: relative;
}

.video-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

.video-details {
  font-size: 14px;
  color: #777;
  margin-top: auto; /* 하단에 정렬 */
}

.exchange-calculator {
  border: 1px solid #e3e3e3;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding-top:10px;
  padding-left: 10px;
  margin-right: 20px;
}

.exchange-rates-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.exchange-rates-table tr {
  border-bottom: 2px solid #eddbc8; /* 아래쪽 선 */
  border-bottom: px solid #b6a084;
}

.currency-name,
.currency-code {
  font-weight: bold;
  padding: 10px;
  font-size: 16px;
}

.currency-value {
  font-size: 16px;
  font-weight: normal;
  padding: 10px;
}

.currency-name {
  color: #333;
}

.currency-code {
  color: #666;
}

.currency-value {
  transition: color 0.3s ease-in-out;
}

/* Styling for the value fluctuations */
.currency-value {
  font-weight: bold;
}

.currency-value:hover {
  text-decoration: underline;
}

.select-currency {
  width: 400px;
  height: 40px;
  font-size: 20px; /* 글씨 크기 키우기 */
  font-family: 'Arial', sans-serif; /* 폰트 변경 */
  border: 1px solid #ccc; /* 테두리 색상 */
  background-color: #f9f9f9; /* 배경 색상 */
  border-radius: 8px;
  text-align: left;
  padding-left: 10px;
}

.input-select-currency {
  width: 400px;
  height: 40px;
  font-size: 20px; /* 글씨 크기 키우기 */
  font-family: 'Arial', sans-serif; /* 폰트 변경 */
  border: 1px solid #ccc; /* 테두리 색상 */
  border-radius: 8px;
  text-align: left;
  padding-left: 10px;
}

.exchange-calculator-name {
  font-size: 25px; /* 글씨 크기 키우기 */
  font-family: 'Arial', sans-serif; /* 폰트 변경 */
}

.exchange-calculator-button{
  position: relative;
  left: 180px;
  margin-bottom: 10px;
}

.source-info {
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1); /* 부드러운 그림자 */
  height: 130px;
  width: 993px;
  box-sizing: border-box;
  border-radius: 8px;
  border: none;
  font-size: 15px;
  padding: 20px;
  background-color: white;
}

.source-info:hover {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* 부드러운 그림자 */
}
</style>