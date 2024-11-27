<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

// Pinia store 인스턴스 가져오기
const store = useCounterStore()
const router = useRouter()

// 프로필 데이터를 저장할 변수
const profile = ref({
  name: '', nick_name: '', age: '', gender: '', phone_number: '', email: '', job: '', 
  interest: '', assets_amount: '', salary: '', education: '', region: '', district: '',
})

// 지역구 목록
const regionsWithDistricts = {
  서울: ['강남구', '강북구', '송파구', '서초구', '관악구', '종로구', '마포구', '중구', '동대문구'],
  부산: ['해운대구', '수영구', '연제구', '동래구', '서구', '남구', '북구', '금정구', '기장군'],
  대구: ['중구', '동구', '서구', '남구', '북구', '달서구', '달성군'],
  인천: ['남동구', '서구', '계양구', '부평구', '미추홀구', '연수구', '강화군'],
  광주: ['서구', '남구', '북구', '동구', '광산구'],
  대전: ['서구', '유성구', '대덕구', '중구', '동구'],
  울산: ['남구', '동구', '북구', '중구', '울주군'],
  제주: ['제주시', '서귀포시'],
  세종: ['세종시']
}

// 지역 선택에 따른 지역구 변경 여부
const showDistrict = ref(true)
const districts = ref([])

// 지역이 변경될 때 호출되는 함수
const onRegionChange = () => {
  if (regionsWithDistricts[profile.value.region]) {
    showDistrict.value = true
    districts.value = regionsWithDistricts[profile.value.region]
    profile.value.district = ''  // 지역구 초기화
  } else {
    showDistrict.value = false
    profile.value.district = ''  // 지역구 초기화
  }
}

// 숫자를 3자리 단위로 포맷팅하는 함수
const formatNumber = (value) => {
  if (value === null || value === undefined) return ''
  return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

// 쉼표를 제거하고 숫자로 변환하는 함수
const parseNumber = (value) => {
  return parseInt(value.replace(/,/g, ''), 10) || 0
}

// 입력 값이 변경될 때 호출
const updateAssetsAmount = (event) => {
  profile.value.assets_amount = parseNumber(event.target.value)
}

const updateSalary = (event) => {
  profile.value.salary = parseNumber(event.target.value)
}

// 프로필 데이터 불러오기
onMounted(() => {
  store.getProfile()  // 프로필 데이터 로드
  profile.value.name = store.profile.name || ''
  profile.value.nick_name = store.profile.nick_name || ''
  profile.value.age = store.profile.age
  profile.value.gender = store.profile.gender || ''
  profile.value.phone_number = store.profile.phone_number || ''
  profile.value.email = store.profile.email || ''
  profile.value.job = store.profile.job || ''
  profile.value.interest = store.profile.interest || ''
  profile.value.assets_amount = store.profile.assets_amount || ''
  profile.value.salary = store.profile.salary || ''
  profile.value.education = store.profile.education || ''
  // region & district
  if (store.profile.region && store.profile.region.includes(' ')) {
    const [region, district] = store.profile.region.split(' ')
    profile.value.region = region
    profile.value.district = district
    districts.value = regionsWithDistricts[region]
  } else {
    profile.value.region = store.profile.region || ''
  }

})

// 프로필 수정 함수
const updateProfile = function () {
  // profile 데이터를 store로 반영
  store.profile.name = profile.value.name
  store.profile.nick_name = profile.value.nick_name
  store.profile.age = profile.value.age
  store.profile.gender = profile.value.gender
  store.profile.phone_number = profile.value.phone_number
  store.profile.email = profile.value.email
  store.profile.job = profile.value.job
  store.profile.interest = profile.value.interest
  store.profile.assets_amount = profile.value.assets_amount
  store.profile.salary = profile.value.salary
  store.profile.education = profile.value.education

  const updatedRegion = profile.value.region + ' ' + profile.value.district
  store.profile.region = updatedRegion  // 업데이트된 region과 district 반영
  store.profile.district = profile.value.district  // district도 함께 저장  

  store.updateProfile()
  router.push('/profile')  // 수정 완료 후 프로필 페이지로 이동
}
</script>

<template>
  <div>
    <!-- 프로필 수정 폼 -->
    <form @submit.prevent="updateProfile">
      <div>
        <label for="name">Name:</label>
        <input 
          type="text" 
          id="name" 
          v-model="profile.name" 
          placeholder="Enter your name" 
        />
      </div>

      <div>
        <label for="nick_name">Nickname:</label>
        <input 
          type="text" 
          id="nick_name" 
          v-model="profile.nick_name" 
          placeholder="Enter your nickname" 
        />
      </div>

      <div>
        <label for="age">Age(윤석열나이):</label>
        <input 
          type="number" 
          id="age" 
          min="10"
          v-model="profile.age" 
          placeholder="Enter your age" 
        />
      </div>

      <div>
        <label for="gender">Gender:</label>
        <select v-model="profile.gender" id="gender">
          <option value="">Select your gender</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
          <option value="Other">Other</option>
        </select>
      </div>

      <div>
        <label for="phone_number">Phone Number:</label>
        <input 
          type="text" 
          id="phone_number" 
          v-model="profile.phone_number" 
          placeholder="010-1234-5678"
        />
      </div>

      <div>
        <label for="email">Email:</label>
        <input 
          type="email" 
          id="email" 
          v-model="profile.email" 
          placeholder="Enter your email"
        />
      </div>

      <div>
        <label for="job">Job:</label>
        <input 
          type="text" 
          id="job" 
          v-model="profile.job" 
          placeholder="Enter your job"
        />
      </div>

      <div>
        <label for="interest">Interest:</label>
        <textarea 
          id="interest" 
          v-model="profile.interest" 
          placeholder="Enter your interests"
        ></textarea>
      </div>

      <div>
        <label for="assets_amount">Assets Amount:</label>
        <input 
          type="text" 
          id="assets_amount" 
          :value="formatNumber(profile.assets_amount)" 
          @input="updateAssetsAmount"
          placeholder="Enter your total assets"
        />
      </div>

      <!-- Salary -->
      <div>
        <label for="salary">Salary:</label>
        <input 
          type="text" 
          id="salary" 
          :value="formatNumber(profile.salary)" 
          @input="updateSalary"
          placeholder="Enter your monthly salary"
        />
      </div>

      <div>
        <label for="education">학력:</label>
        <select id="education" v-model="profile.education">
          <option value="">Select your education level</option>
          <option value="고졸 미만">고졸 미만</option>
          <option value="고교 재학">고교 재학</option>
          <option value="고졸 예정">고졸 예정</option>
          <option value="고교 졸업">고교 졸업</option>
          <option value="대학 재학">대학 재학</option>
          <option value="대졸 예정">대졸 예정</option>
          <option value="대학 졸업">대학 졸업</option>
          <option value="석·박사">석·박사</option>
        </select>
      </div>

      <div>
        <label for="region">Region:</label>
        <select id="region" v-model="profile.region" @change="onRegionChange">
          <option value="">Select your region</option>
          <option value="서울">서울</option>
          <option value="부산">부산</option>
          <option value="대구">대구</option>
          <option value="인천">인천</option>
          <option value="광주">광주</option>
          <option value="대전">대전</option>
          <option value="울산">울산</option>
          <option value="제주">제주</option>
          <option value="세종">세종</option>
        </select>
      </div>

      <div v-if="showDistrict">
        <label for="district">지역구:</label>
        <select id="district" v-model="profile.district">
          <option value="">Select your district</option>
          <option v-for="district in districts" :key="district" :value="district">{{ district }}</option>
        </select>
      </div>

      <button type="submit">Save Changes</button>
    </form>
  </div>
</template>


<style scoped>
/* 전체 폼 컨테이너 스타일 */
form {
  max-width: 500px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
  font-family: 'Arial', sans-serif;
}

/* 개별 입력 그룹 스타일 */
div {
  margin-bottom: 20px;
}

/* 입력 필드 레이블 */
label {
  display: block;
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 8px;
  color: #333333;
}

/* 텍스트 입력 필드 */
input[type="text"],
input[type="email"],
input[type="number"],
textarea,
select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #cccccc;
  border-radius: 5px;
  box-sizing: border-box;
  font-size: 14px;
  color: #333333;
  background-color: #f9f9f9;
  transition: border-color 0.2s ease-in-out, background-color 0.2s ease-in-out;
}

input:focus,
textarea:focus,
select:focus {
  border-color: #4CAF50;
  background-color: #ffffff;
  outline: none;
  box-shadow: 0 0 5px rgba(76, 175, 80, 0.5);
}

/* 텍스트 필드에 대한 플레이스홀더 스타일 */
input::placeholder,
textarea::placeholder {
  color: #aaaaaa;
  font-size: 12px;
}

/* 텍스트 영역 */
textarea {
  resize: none;
  height: 100px;
}

/* 버튼 스타일 */
button {
  width: 100%;
  padding: 12px 20px;
  font-size: 16px;
  font-weight: bold;
  color: white;
  background-color: #4CAF50;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
  transition: background-color 0.3s ease-in-out, transform 0.2s ease-in-out;
}

button:hover {
  background-color: #45a049;
  transform: translateY(-2px);
}

button:active {
  background-color: #3e8e41;
  transform: translateY(0);
}

/* 선택 메뉴 스타일 */
select {
  appearance: none;
  -moz-appearance: none;
  -webkit-appearance: none;
  background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 140 140'%3E%3Cpolygon points='0,0 140,0 70,80' fill='%23888888'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 10px;
}

/* 전체 폼 배경 색상 */
body {
  background-color: #f4f4f9;
  margin: 0;
  padding: 0;
  font-family: 'Arial', sans-serif;
}
</style>
