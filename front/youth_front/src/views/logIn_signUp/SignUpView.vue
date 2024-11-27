<template>
  <div class="sign-up">
    <div class="sign-up-second">
      <h1>Sign Up Page</h1>
      <form @submit.prevent="signUp">
        <label for="username">username : </label>
        <input type="text" id="username" v-model.trim="username"><br>
  
        <label for="password1">password : </label>
        <input type="password" id="password1" v-model.trim="password1"><br>
  
        <label for="password2">password confirmation : </label>
        <input type="password" id="password2" v-model.trim="password2">
        <div >
          <input type="submit" value="SignUp">
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'

const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)

const store = useCounterStore()

const signUp = function () {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value
  }
  store.signUp(payload)
}

</script>

<style>
.sign-up {
  background-color: white;
  width: 2114px;
  height: 950px;
}

.sign-up-second {
  font-size: 40px;
  position: relative;
  left: 900px;
  top: 300px;
}
</style>
