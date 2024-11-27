<template>
  <div class="login-container" style="background-color: #ffffff;">
    <h1>Log In</h1>
    <form class="login-form" @submit.prevent="logIn">
      <div class="form-group">
        <label for="username">Username:</label>
        <input
          type="text"
          id="username"
          v-model.trim="username"
          placeholder="Enter your username"
        />
      </div>

      <div class="form-group">
        <label for="password">Password:</label>
        <input
          type="password"
          id="password"
          v-model.trim="password"
          placeholder="Enter your password"
        />
      </div>

      <input class="submit-btn" type="submit" value="Log In" />
    </form>
    <!-- 회원가입 페이지 버튼 -->
    <button class="signup-btn" @click="goToSignUpPage">[Sign Up]</button>
  </div>

</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')

const store = useCounterStore()
const router = useRouter()

const logIn = () => {
  const payload = {
    username: username.value,
    password: password.value,
  }
  store.logIn(payload)
}

const goToSignUpPage = () => {
  router.push({ name: 'signup' }) // 회원가입 페이지로 이동
}
</script>

<style scoped>
/* 전체 컨테이너 */
.login-container {
  width: 2114px;
  height: 500px;
  margin-top: 300px;
  margin-bottom: 300px;
  padding-left: 500px;
  padding-right: 500px;
  text-align: center;
  background-color: #ffffff;
}

/* 제목 */
h1 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

/* 폼 요소 */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
  text-align: left;
}

label {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 5px;
  color: #555;
}

input {
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 100%;
  box-sizing: border-box;
}

input:focus {
  border-color: #007BFF;
  outline: none;
  box-shadow: 0 0 4px rgba(0, 123, 255, 0.5);
}

/* 버튼 */
.submit-btn,
.signup-btn {
  padding: 10px 15px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
  margin-top: 10px;
}

.submit-btn {
  background-color: #007BFF;
  color: white;
}

.signup-btn {
  background-color: #6c757d;
  color: white;
}

.submit-btn:hover {
  background-color: #0056b3;
}

.signup-btn:hover {
  background-color: #5a6268;
}
</style>
