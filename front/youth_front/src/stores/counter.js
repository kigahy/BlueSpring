import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';
import { useRouter } from 'vue-router';

export const useCounterStore = defineStore('counter', () => {
  const API_URL = 'http://127.0.0.1:8000';
  const token = ref(localStorage.getItem('token') || null);  // Persist token in localStorage
  const router = useRouter();
  const profile = ref([])
  const searchedFinPrdts = ref([])

  // Computed property to check if the user is logged in
  const isLogin = computed(() => {
    return token.value !== null;
  });

  // DRF로 전체 프로필 요청을 보내는 함수
  const getProfile = function () {
    if (token.value) {
      axios({
        method: 'get',
        url: `${API_URL}/api/v1/accounts/profile/`,  // 실제 프로필 받을 경로
        headers: {
          Authorization: `Token ${token.value}`,  // 로그인된 사용자의 JWT 토큰을 헤더에 추가
        },
      })
        .then((res) => {
          profile.value = res.data;
        })
        .catch((err) => {
          console.error('Error fetching profile:', err);
          if (err.response && err.response.status === 401) {
            console.log('Unauthorized. Token may be expired or invalid.');
            // 토큰 만료 시 처리 (예: 로그인 페이지로 리다이렉션)
          } else if (err.response && err.response.status === 404) {
            console.log('Profile not found. Check the API endpoint.');
          } else {
            console.log('An error occurred while fetching the profile.');
          }
        });
    } else {
      console.log('User is not logged in');  // 로그인하지 않은 경우
      // 로그인 페이지로 리다이렉션하거나 로그인 창을 표시
    }
  };

  // 프로필 수정 함수
  const updateProfile = function () {
    if (token.value && profile.value) {
      axios({
        method: 'put',
        url: `${API_URL}/api/v1/accounts/profile/`,  // 실제 프로필 수정 경로
        headers: {
          Authorization: `Token ${token.value}`,  // 로그인된 사용자의 JWT 토큰을 헤더에 추가
        },
        data: profile.value,  // 수정된 프로필 데이터를 profile.value에서 가져옴
      })
        .then((res) => {
          profile.value = res.data;  // 수정된 프로필을 상태에 반영
        })
        .catch((err) => {
          console.error('Error updating profile:', err);
          if (err.response && err.response.status === 401) {
            console.log('Unauthorized. Token may be expired or invalid.');
            // 토큰 만료 시 처리 (예: 로그인 페이지로 리다이렉션)
          } else if (err.response && err.response.status === 400) {
            console.log('Bad Request. Invalid data.');
            // 잘못된 데이터 처리 (예: 입력값 검증)
          } else {
            console.log('An error occurred while updating the profile.');
          }
        });
    } else {
      console.log('User is not logged in or profile data is missing');  // 로그인하지 않았거나 프로필 데이터가 없음
    }
  };

  // 회원가입 요청 액션
  const signUp = function (payload) {
    const { username, password1, password2 } = payload;

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password2,
      },
    })
      .then((res) => {
        const password = password1;
        logIn({ username, password });
      })
      .catch((err) => {
        console.log(err);
      });
  };

  // 로그인 요청 액션
  const logIn = function (payload) {
    const { username, password } = payload;

    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password,
      },
    })
      .then((res) => {
        token.value = res.data.key;
        localStorage.setItem('token', res.data.key);  // Persist token in localStorage
        router.push({ name: 'mainPage' });
      })
      .catch((err) => {
        console.log(err);
      });
  };

  // 로그아웃 요청 액션
  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`,
    })
      .then((res) => {
        token.value = null;
        localStorage.removeItem('token');  // Remove token from localStorage
        router.push({ name: 'mainPage' });
      })
      .catch((err) => {
        console.log(err);
      });
  };

  // 조건에 따른 예적금 조회
  const searchFinPrdts = function (keyword, productType, min_term, max_term, intr_rate_type, cum_type) {
    axios({
      method: 'get',
      // url 수정해야함
      url: `${API_URL}/api/v1/fin_products/search_by_condition/`,
      params: {
        keyword: keyword,
        productType: productType,
        min_term: min_term,
        max_term: max_term,
        intr_rate_type: intr_rate_type,
        cum_type: cum_type,
      },
      })
    .then((res) => {
      searchedFinPrdts.value = res.data
    })
    .catch((err) => {
      console.log(err)
    })
  }
  
  // 추천 예적금
  const analyzeFinPrdts = function () {
    // 토큰 확인
    if (token.value) {
      return axios({
        method: 'get',
        // 요청보내는 url
        url: `${API_URL}/api/v1/fin_products/rec_fin_prdts/`, 
        // token 권한 확인을 위해 달아주는 headers
        headers: {
          Authorization: `Token ${token.value}`,  // 로그인된 사용자의 JWT 토큰을 헤더에 추가
        },
      })
        .then((res) => {
          return res.data
        })
        .catch((err) => {
          console.error('Error updating profile:', err);
          if (err.response && err.response.status === 401) {
            console.log('Unauthorized. Token may be expired or invalid.');
            // 토큰 만료 시 처리 (예: 로그인 페이지로 리다이렉션)
          } else if (err.response && err.response.status === 400) {
            console.log('Bad Request. Invalid data.');
            // 잘못된 데이터 처리 (예: 입력값 검증)
          } else {
            console.log('An error occurred.');
          }
        });
    } else {
      console.log('User is not logged in.');  // 로그인하지 않음
    }

  }
  // 추천 정책
  const analyzePolicies = function () {
    // 토큰 확인
    if (token.value) {
      return axios({
        method: 'get',
        // 요청보내는 url
        url: `${API_URL}/api/v1/recruits/supports/`, 
        // token 권한 확인을 위해 달아주는 headers
        headers: {
          Authorization: `Token ${token.value}`,  // 로그인된 사용자의 JWT 토큰을 헤더에 추가
        },
      })
        .then((res) => {
          return res.data
        })
        .catch((err) => {
          console.error('Error updating profile:', err);
          if (err.response && err.response.status === 401) {
            console.log('Unauthorized. Token may be expired or invalid.');
            // 토큰 만료 시 처리 (예: 로그인 페이지로 리다이렉션)
          } else if (err.response && err.response.status === 400) {
            console.log('Bad Request. Invalid data.');
            // 잘못된 데이터 처리 (예: 입력값 검증)
          } else {
            console.log('An error occurred.');
          }
        });
    } else {
      console.log('User is not logged in.');  // 로그인하지 않음
    }
  }

  // 메일 보내기
  const sendEmail = function (content) {
    if (token.value) {
      axios({
        method: 'POST',
        url: 'http://127.0.0.1:8000/api/v1/accounts/send_email/',
        headers: {
          Authorization: `Token ${token.value}`,  // 로그인된 사용자의 JWT 토큰을 헤더에 추가
        },
        data: {
          content: content,
        }
      })
        .then((res) => {
          console.log('Succes, send an E-mail.')
        })
        .catch((err) => {
          console.error('Error fetching profile:', err);
          if (err.response && err.response.status === 401) {
            console.log('Unauthorized. Token may be expired or invalid.');
            // 토큰 만료 시 처리 (예: 로그인 페이지로 리다이렉션)
          } else if (err.response && err.response.status === 404) {
            console.log('Profile not found. Check the API endpoint.');
          } else {
            console.log('An error occurred while fetching the profile.');
          }
        });
    } else {
      console.log('User is not logged in');  // 로그인하지 않은 경우
    }
  };
  return { 
    profile, API_URL, token, isLogin, searchedFinPrdts,
    signUp, logIn, logOut,
    getProfile, updateProfile,
    searchFinPrdts, 
    analyzeFinPrdts, analyzePolicies, 
    sendEmail,
  };
}, { persist: true });
