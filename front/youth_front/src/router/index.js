import { createRouter, createWebHistory } from "vue-router";
// import NavBar from "@/components/NavBar.vue";
import MainPage from "@/views/mainPage/MainPage.vue";
import CompareFinProduct from "@/views/finProduct/CompareFinProductView.vue";
import Calendar from "@/views/calendar/Calendar.vue";
import CalendarInfo from '@/views/calendar/CalendarInfo.vue';
import CompanyInfo from "@/views/company/CompanyInfo.vue";
import ProductRecommend from "@/views/recommendation/ProductRecommend.vue";
import Profile from "@/views/profile/ProfileView.vue";
import UpdateProfileView from "@/views/profile/UpdateProfileView.vue";
import SignUpView from "@/views/logIn_signUp/SignUpView.vue";
import LogInView from "@/views/logIn_signUp/LogInView.vue";
import { useCounterStore } from '@/stores/counter'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "mainPage",
      component: MainPage,
      meta: {
        title: "대한민국 청년을 위한 맞춤 서비스, 작전명 청춘",
      },
    },
    {
      path:"/compareFinProduct",
      name: "compareFinProduct",
      component: CompareFinProduct,
      meta: {
        title: "Let's compare recent financial produts",
      },
    },
    {
      path: "/company-info",
      name: "companyInfo",
      component: CompanyInfo,
    },
    {
      path: "/calendar",
      name: "calendar",
      component: Calendar,
      meta: {
        title: "관심 분야, 나이, 지역, 학력에 따른 나만의 일정을 확인해 보아요.",

      },
    },
    {
      path: '/calendar-info/:job',
      name: 'calendarinfo',
      component: CalendarInfo,
      props: true, // job 데이터를 props로 전달
    },
    {
      path: "/product-recommend",
      name: "productRecommend",
      component: ProductRecommend,
      meta: {
        title: "거래 내역에 따른 금융 상품과 청년 지원 정책을 추천받아요.",
      },
    },
    {
      path: "/profile",
      name: "profile",
      component: Profile,
      meta: {
        title: "내 정보를 확인하고 관심사를 수정하여 다양한 서비스를 추천받아요.",
      },
    },
    {
      path: "/profile/update",
      name: "updateProfile",
      component: UpdateProfileView,
    },
    {
      path: "/signup",
      name: 'signup',
      component: SignUpView,
    },
    {
      path: "/login",
      name: "login",
      component: LogInView,
    },
  ],
});

router.beforeEach((to, from) => {
  const store = useCounterStore()
  // 만약 이동하는 목적지가 메인 페이지이면서
  // 현재 로그인 상태가 아니라면 로그인 페이지로 보냄
  if ((to.name === 'profile' || to.name === 'updateProfile') && !store.isLogin) {
    window.alert('로그인이 필요합니다.')
    return { name: 'login' }
  }

  // 만약 로그인 사용자가 회원가입 또는 로그인 페이지로 이동하려고 하면
  // 메인 페이지로 보냄
  if ((to.name === 'signup' || to.name === 'login') && (store.isLogin)) {
    window.alert('이미 로그인 되어있습니다.')
    return { name: 'mainPage' }
  }
})

export default router;
