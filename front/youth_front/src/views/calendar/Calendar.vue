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
  <div class="page-container">
    <div class="left-right-layout" id="left-right-layout">

    <div class="calendar-container">
    <div class="calendar-header">
      <h1>{{ nickName }} 님 맞춤 캘린더</h1>
      <button class="btn-add-event" @click="openAddEventModal">일정 추가</button>
    </div>
    <v-calendar v-model="focus" :attributes="events" :theme="theme">
      <template #day-content="{ day, attributes }">
        <div class="day-cell">
          <!-- 날짜 표시 -->
          <div class="day-number">{{ day.day }}</div>

          <!-- 이벤트 정보 반복 렌더링 -->
          <div v-for="attr in attributes" :key="attr.key">
            <!-- jobTitle 정보 -->
            <span
              v-if="attr.jobTitle"
              class="job-title-link"
              @click="openJobDetail(attr)"
              :class="{
                start: attr.type === 'start',
                end: attr.type === 'end',
              }"
            >
            {{ attr.jobTitle.length > 8 ? attr.jobTitle.slice(0, 8) + '...' : attr.jobTitle }}
            </span>

            <!-- eventTitle 정보 -->
            <span
              v-if="attr.eventTitle"
              class="job-title-link"
              @click="openViewEventModal(attr)"
              :class="{
                start: attr.type === 'start',
                end: attr.type === 'end',
              }"
            >
            {{ attr.eventTitle.length > 8 ? attr.eventTitle.slice(0, 8) + '...' : attr.eventTitle }}
            </span>

            <!-- suportTitle 정보 -->
            <span
              v-if="attr.title"
              class="job-title-link"
              @click="openSupportModal(attr)"
              :class="{
                start: attr.type === 'start',
                end: attr.type === 'end',
              }"
            >
            {{ attr.title.length > 8 ? attr.title.slice(0, 8) + '...' : attr.title }}
            </span>
          </div>
        </div>
      </template>
      <button class="btn-add-event" @click="openAddEventModal">
        일정 추가
      </button>
    </v-calendar>
  </div>

<!-- 상위 5개 채용공고 -->
<div class="right-side">
  <h2 id = top5title>Top 5 채용공고</h2>
  <div class="top-jobs">
  <ul>
    <li v-for="job in topJobs" :key="job.job_title">
      {{ job.job_title }} ({{ job.score }})
      <!-- URL이 있으면 버튼 클릭으로 해당 URL로 이동 -->
        <button id="top5button" @click="goToJob(job.job_url)">접수 상세</button>
    </li>
  </ul>
</div>


<!-- 상위 5개 지원정보 -->
<h2 id = top5title>Top 5 지원정보</h2>
<div class="top-supports">
  <ul>
    <li v-for="support in topSupports" :key="support.title">
      {{ support.title }} ({{ support.score }})
      
      <!-- URL이 존재하고 0이 아닌 경우 -->
      <template v-if="support.url && support.url !== '0'">
        <button id="top5button" @click="goToUrlSupport(support.url)">지원 상세</button>
      </template>
      
      <!-- URL이 없거나 0인 경우 -->
      <template v-else>
        <button id="top5button" @click="goToSupport(support.title)">검색 정보</button>
      </template>
      
    </li>
  </ul>
</div>
</div>
    </div>




    <!-- 새 일정 추가 모달 -->
    <div
      v-if="addEventModal"
      class="modal-overlay"
      @click.self="closeAddEventModal"
    >
      <div class="modal-content">
        <h2>새 일정 추가</h2>
        <form @submit.prevent="saveEvent">
          <label>
            일정명:
            <input type="text" v-model="newEvent.eventTitle" required />
          </label>
          <label>
            메모:
            <input type="text" v-model="newEvent.eventContent" />
          </label>
          <label>
            시작 날짜:
            <input type="date" v-model="newEvent.startDate" required />
          </label>
          <label>
            종료 날짜:
            <input type="date" v-model="newEvent.endDate" required />
          </label>
          <button type="submit" class="btn-save">저장</button>
          <button type="button" class="btn-cancel" @click="closeAddEventModal">
            취소
          </button>
        </form>
      </div>
    </div>

    <!-- 일정 업데이트 모달 -->
    <div
      v-if="updateEventModal"
      class="modal-overlay"
      @click.self="closeUpdateEventModal"
    >
      <div class="modal-content">
        <h2>새 일정 추가</h2>
        <form @submit.prevent="updateEvent">
          <label>
            일정명:
            <input type="text" v-model="updatedEvent.eventTitle" required />
          </label>
          <label>
            메모:
            <input type="text" v-model="updatedEvent.eventContent" />
          </label>
          <label>
            시작 날짜:
            <input type="date" v-model="updatedEvent.startDate" required />
          </label>
          <label>
            종료 날짜:
            <input type="date" v-model="updatedEvent.endDate" required />
          </label>
          <button type="submit" class="btn-save">업데이트</button>
          <button
            type="button"
            class="btn-cancel"
            @click="closeUpdateEventModal"
          >
            취소
          </button>
        </form>
      </div>
    </div>

   <!-- 지원정보 보기 모달 -->
<div
  v-if="supportDialog"
  class="modal-overlay"
  id="support-modal"
  @click.self="closeSupportModal"
>
  <div class="modal-content">
    <h2>{{ selectedSupport?.title }}</h2>
    <p><strong>상세:</strong> {{ selectedSupport?.description }}</p>
    <p><strong>담당 기관:</strong> {{ selectedSupport?.department }}</p>
    <p>
      <strong>대상 지역:</strong>
      <span v-if="selectedSupport?.region === '홈페이지 참조 바랍니다.'">
        제한 없음
      </span>
      <span v-else>
        {{ selectedSupport?.region }}
      </span>
    </p>
    <p>
      <strong>대상 연령:</strong>
      <span
        v-if="selectedSupport?.startAge === 0 && selectedSupport?.endAge === 0"
      >
        제한 없음
      </span>
      <span v-else>
        {{ selectedSupport?.startAge }} ~
        {{ selectedSupport?.endAge }}
      </span>
    </p>
    <p>
      <strong>공고 기간:</strong> {{ selectedSupport?.startDate }} ~
      {{ selectedSupport?.endDate }}
    </p>
    <p><strong>연관도 점수</strong> {{ selectedSupport?.score }}</p>
    <a :href="selectedSupport?.url" target="_blank" class="btn">공고 상세보기</a>
    <button @click="closeSupportModal" class="btn-close"></button>
  </div>
</div>

<!-- 채용공고 보기 모달 -->
<div v-if="dialog" class="modal-overlay" id="job-modal" @click.self="closeDialog">
  <div class="modal-content">
    <h2>{{ selectedJob?.jobTitle }}</h2>
    <p><strong>회사명:</strong> {{ selectedJob?.companyName }}</p>
    <p><strong>위치:</strong> {{ selectedJob?.location }}</p>
    <p><strong>급여:</strong> {{ selectedJob?.salary }}</p>
    <p><strong>고용 형태:</strong> {{ selectedJob?.jobType }}</p>
    <p>
      <strong>공고 기간:</strong> {{ selectedJob?.startDate }} ~
      {{ selectedJob?.endDate }}
    </p>
    <p><strong>연관도 점수:</strong> {{ selectedJob?.score }}</p>
    <a :href="selectedJob?.jobUrl" target="_blank" class="btn">공고 상세보기</a>
    <a :href="selectedJob?.companyUrl" target="_blank" class="btn">기업정보 보기</a>
    <button @click="closeDialog" class="btn-close"></button>
  </div>
</div>

<!-- 유저 일정 보기 모달 -->
<div
  v-if="viewEventModal"
  class="modal-overlay"
  id="event-modal"
  @click.self="closeViewEventModal"
>
  <div class="modal-content">
    <h2>{{ selectedEvent?.eventTitle }}</h2>
    <p><strong>메모:</strong> {{ selectedEvent?.eventContent }}</p>
    <p>
      <strong>일정 기간:</strong> {{ selectedEvent?.startDate }} ~
      {{ selectedEvent?.endDate }}
    </p>
    <!-- 삭제버튼 -->
    <button @click="deleteSelectedEvent" class="btn-delete">삭제</button>
    <!-- 수정버튼 -->
    <button @click="openUpdateEventModal" class="btn-update">수정</button>
    <button @click="closeViewEventModal" class="btn-close"></button>
  </div>
</div>
<CalendarInfo />

  </div>
</template>
<script setup>
import { onMounted, ref } from "vue";
import PageBanner from '@/components/PageBanner.vue'
import { useCounterStore } from "@/stores/counter";
import axios from "axios";

const counterStore = useCounterStore();
const events = ref([]); // 이벤트 데이터
const focus = ref(new Date()); // 현재 날짜
const dialog = ref(false); // 채용정보 모달 창 표시 여부
const supportDialog = ref(false); // 지원정보 모달 창 표시 여부
const selectedJob = ref(null); // 선택된 공고 상세 정보
const selectedSupport = ref(null); // 선택된 지원 상세 정보
const topJobs = ref([]);
const topSupports = ref([]);

// 배너관련 --------------------------------------
const bannerVisible = ref(false)
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
const theme = {
  dayCellWidth: "120px", // 균등한 너비
  dayCellHeight: "100px", // 균등한 높이
};
// ---------------------------------------------------

// 일정 추가 모달
const addEventModal = ref(false);
// 새 일정 데이터
const newEvent = ref({
  eventId: "",
  eventTitle: "",
  eventContent: "",
  startDate: "",
  endDate: "",
});

// 사용자 일정 저장
const saveEvent = () => {
  axios
    .post(
      "http://127.0.0.1:8000/api/v1/recruits/user-events/",
      {
        title: newEvent.value.eventTitle,
        content: newEvent.value.eventContent,
        start_date: newEvent.value.startDate,
        end_date: newEvent.value.endDate,
      },
      {
        headers: {
          Authorization: `Token ${counterStore.token}`,
        },
      }
    )
    .then((response) => {
      alert("일정이 성공적으로 추가되었습니다!");
      window.location.reload();
    })
    .catch((err) => {
      console.error("일정 저장 실패:", err.response || err.message);
      alert("일정 저장에 실패했습니다.");
    });
};

const loadEvents = () => {
  return axios
    .get("http://127.0.0.1:8000/api/v1/recruits/", {
      headers: {
        Authorization: `Token ${counterStore.token}`,
      },
    })
    .then((response) => {
      console.log(response.data);
      // 채용공고 데이터 처리
      const recruitEvents = response.data.recommended_jobs.flatMap((job) => [
        {
          key: `${job.job_title}-start`,
          dates: job.start_date,
          startDate: job.start_date,
          endDate: job.end_date,
          type: "start",
          jobTitle: job.job_title,
          companyName: job.company_name,
          score: job.score,
          jobType: job.job_type,
          salary: job.salary,
          location: job.location,
          jobUrl: job.job_url,
          companyUrl: job.company_url,
        },
        {
          key: `${job.job_title}-end`,
          dates: job.end_date,
          startDate: job.start_date,
          endDate: job.end_date,
          type: "end",
          jobTitle: job.job_title,
          companyName: job.company_name,
          score: job.score,
          jobType: job.job_type,
          salary: job.salary,
          location: job.location,
          jobUrl: job.job_url,
          companyUrl: job.company_url,
        },
      ]);
      events.value.push(...recruitEvents);

      // 채용공고 score 기준으로 상위 5개 항목 추출
      topJobs.value = response.data.recommended_jobs
      .sort((a, b) => b.score - a.score)  // score 내림차순 정렬
      .slice(0, 5);  // 상위 5개 항목

      // 사용자 일정 데이터 로드
      return axios
        .get("http://127.0.0.1:8000/api/v1/recruits/user-events/", {
          headers: {
            Authorization: `Token ${counterStore.token}`,
          },
        })
        .then((userResponse) => {
          const userEvents = userResponse.data.flatMap((event) => [
            {
              eventId: event.id,
              key: `custom-${event.id}-start`,
              dates: event.start_date, // 시작일 이벤트
              type: "start",
              eventTitle: event.title,
              eventContent: event.content,
              startDate: event.start_date,
              endDate: event.end_date,
            },
            {
              eventId: event.id,
              key: `custom-${event.id}-end`,
              dates: event.end_date, // 종료일 이벤트
              type: "end",
              eventTitle: event.title,
              eventContent: event.content,
              startDate: event.start_date,
              endDate: event.end_date,
            },
          ]);
          events.value.push(...userEvents);

          // 지원정보 로드
          return axios
            .get("http://127.0.0.1:8000/api/v1/recruits/supports/", {
              headers: {
                Authorization: `Token ${counterStore.token}`,
              },
            })
            .then((supportResponse) => {
              console.log(supportResponse.data);
              const supportEvents =
                supportResponse.data.recommended_supports.flatMap((sup) => [
                  {
                    supportId: sup.support_id,
                    key: `custom-${sup.support_id}-start`,
                    dates: sup.start_date,
                    title: sup.title,
                    description: sup.description,
                    content: sup.content,
                    scale: sup.scale,
                    type: "start",
                    startDate: sup.start_date,
                    endDate: sup.end_date,
                    startAge: sup.start_age,
                    endAge: sup.end_age,
                    department: sup.department,
                    contact: sup.contact,
                    region: sup.region,
                    url: sup.url,
                    score: sup.score,
                  },
                  {
                    supportId: sup.support_id,
                    key: `custom-${sup.support_id}-end`,
                    dates: sup.end_date,
                    title: sup.title,
                    description: sup.description,
                    content: sup.content,
                    scale: sup.scale,
                    type: "end",
                    startDate: sup.start_date,
                    endDate: sup.end_date,
                    startAge: sup.start_age,
                    endAge: sup.end_age,
                    department: sup.department,
                    contact: sup.contact,
                    region: sup.region,
                    url: sup.url,
                    score: sup.score,
                  },
                ]);
              events.value.push(...supportEvents);

              // 지원정보 score 기준으로 상위 5개 항목 추출
              topSupports.value = supportResponse.data.recommended_supports
                .sort((a, b) => b.score - a.score)  // score 내림차순 정렬
                .slice(0, 5);  // 상위 5개 항목

            })
            .catch((applicationError) => {
              console.error(
                "지원 정보 로드 실패:",
                applicationError.response || applicationError.message
              );
            });
        })
        .catch((userError) => {
          console.error(
            "사용자 일정 데이터 로드 실패:",
            userError.response || userError.message
          );
        });
    })
    .catch((recruitError) => {
      console.error(
        "채용공고 데이터 로드 실패:",
        recruitError.response || recruitError.message
      );
    });
};

const goToJob = (url) => {
    window.open(url, "_blank"); // 새 창에서 링크 열기
  };

// URL이 있을 경우 해당 URL로 이동하는 함수
const goToUrlSupport = (url) => {
  window.open(url, "_blank"); // 새 창에서 링크 열기
};
// 상위 5개 지원정보 이동 링크
const generateSupport = (title) => {
  const url = `https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifList.do?pageIndex=1&frameYn=&bizId=&dtlOpenYn=&plcyTpOpenTy=&srchWord=${title}&chargerOrgCdAll=&srchAge=&trgtJynEmp=&trgtJynEmp=&srchSortOrder=1&pageUnit=1#`;
  return url;
};
// 버튼 클릭 시 URL로 이동하는 함수
const goToSupport = (department) => {
  const url = generateSupport(department); // department로 URL 생성
  window.open(url, "_blank"); // 새 창에서 링크 열기
};



const nickName = ref(null)

// onMounted에서 데이터 로드
onMounted(() => {
  // 배너 표시
  setTimeout(() => {
    bannerVisible.value = true
  }, 1000) // 1초 후에 배너 표시

  // 배너가 3초 후에 사라지게 설정
  setTimeout(() => {
    bannerVisible.value = false
  }, 4000) // 배너가 3초간 표시된 뒤 사라짐

  loadEvents().then(() => {
    console.log("이벤트 로드 완료")
  })
  counterStore.getProfile()
  nickName.value = counterStore.profile.nick_name
});

// 채용공고 모달 열기 닫기
const openJobDetail = (job) => {
  selectedJob.value = job; // 선택된 공고 정보 설정
  dialog.value = true; // 모달 창 열기
};
const closeDialog = () => {
  dialog.value = false; // 모달 창 닫기
  selectedJob.value = null;
};

// 일정 추가 모달 열기 닫기
const openAddEventModal = () => {
  addEventModal.value = true;
};
const closeAddEventModal = () => {
  addEventModal.value = false;
  newEvent.value = {
    eventId: "",
    eventTitle: "",
    eventContent: "",
    startDate: "",
    endDate: "",
  };
};

// 지원정보 모달 열기 닫기
const openSupportModal = (sup) => {
  selectedSupport.value = sup;
  supportDialog.value = true;
};
const closeSupportModal = () => {
  supportDialog.value = false;
  selectedSupport.value = null;
};

const viewEventModal = ref(false); // "일정 보기 모달" 열림 상태
const selectedEvent = ref(null); // 선택된 일정 정보

const openViewEventModal = (event) => {
  selectedEvent.value = {
    eventId: event.eventId,
    eventTitle: event.eventTitle || "제목 없음",
    eventContent: event.eventContent || "메모 없음",
    startDate: event.startDate || "",
    endDate: event.endDate || "",
  };
  viewEventModal.value = true; // 모달 열기
  console.log(event);
};

const closeViewEventModal = () => {
  viewEventModal.value = false; // 모달 닫기
  selectedEvent.value = null; // 데이터 초기화
};

const deleteSelectedEvent = () => {
  if (!selectedEvent.value) {
    alert("삭제할 일정이 선택되지 않았습니다.");
    return;
  }

  if (confirm("정말로 이 일정을 삭제하시겠습니까?")) {
    axios
      .delete("http://127.0.0.1:8000/api/v1/recruits/user-events/detail/", {
        headers: {
          Authorization: `Token ${counterStore.token}`, // 인증 토큰 전달
        },
        data: {
          // 삭제할 이벤트의 고유 데이터를 서버에 전달
          eventId: selectedEvent.value.eventId,
          eventTitle: selectedEvent.value.eventTitle,
          eventContent: selectedEvent.value.eventContent,
          startDate: selectedEvent.value.startDate,
          endDate: selectedEvent.value.endDate,
          eventId: selectedEvent.value.eventId,
        },
      })
      .then((res) => {
        alert("일정이 삭제되었습니다.");
        // 새로고침
        window.location.reload();
      })
      .catch((err) => {
        console.error("일정 삭제 실패:", err.response || err.message);
        window.location.reload();
      });
  }
};

// updateEventModal 열고 닫기
const updateEventModal = ref(false);
// 업데이트할 대상 이벤트 정보를 담을 객체
const updatedEvent = ref({
  eventId: "",
  eventTitle: "",
  eventContent: "",
  startDate: "",
  endDate: "",
});
// 업데이트 모달창 닫기
const closeUpdateEventModal = function () {
  // 값 초기화
  updatedEvent.value.eventId = "";
  updatedEvent.value.eventTitle = "";
  updatedEvent.value.eventContent = "";
  updatedEvent.value.startDate = "";
  updatedEvent.value.endDate = "";
  // 모달창 닫기
  updateEventModal.value = false;
};
// 일단, 업데이트 추가적으로 구현(구현핑아님)해놨음
const openUpdateEventModal = function () {
  // 새 모달창 띄우기
  updateEventModal.value = true;
  // 기존 이벤트의 값을 디폴트 값으로
  updatedEvent.value.eventId = selectedEvent.value.eventId;
  updatedEvent.value.eventTitle = selectedEvent.value.eventTitle;
  updatedEvent.value.eventContent = selectedEvent.value.eventContent;
  updatedEvent.value.startDate = selectedEvent.value.startDate;
  updatedEvent.value.endDate = selectedEvent.value.endDate;
  console.log(updatedEvent.value);
  // ViewEventModal 닫기
  closeViewEventModal();
  // UpdateEventModal 열기
  updateEventModal.value = true;
};
// 이벤트 업데이트 추가
const updateEvent = function () {
  if (!updatedEvent.value) {
    return console.log("업데이트 대상 이벤트를 찾을 수 없음.!!! Error.");
  } else {
    axios({
      method: "put",
      url: "http://127.0.0.1:8000/api/v1/recruits/user-events/detail/",
      headers: { Authorization: `Token ${counterStore.token}` },
      data: {
        // 업데이트할 이벤트의 고유 데이터를 서버에 전달
        eventId: updatedEvent.value.eventId,
        eventTitle: updatedEvent.value.eventTitle,
        eventContent: updatedEvent.value.eventContent,
        startDate: updatedEvent.value.startDate,
        endDate: updatedEvent.value.endDate,
        eventId: updatedEvent.value.eventId,
      },
    })
      .then((res) => {
        // 귀찮으니 새로고침으로 퉁
        window.location.reload();
      })
      .catch((err) => {
        console.error("일정 업데이트 실패:", err.response || err.error);
        window.location.reload();
      });
  }
};

import "@/assets/css/calendar.css";
import CalendarInfo from "@/views/calendar/CalendarInfo.vue";
</script>
