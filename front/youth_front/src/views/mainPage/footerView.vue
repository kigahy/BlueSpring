<template>
  <footer class="footer">
    <div class="footer-container">
      <!-- 회사 정보 -->
      <div class="footer-section company-info"> 
        <p class="footer-title">회사 정보</p>
        <p class="left">회사명: SSAFY.corp</p>
        <p class="left">주소: 부산광역시 강서구 녹산산업중로 333</p>
        <p class="left">전화: 010-4189-6639</p>
        <p class="left">이메일: lab.ssafy@ssafy.corp</p>
      </div>

      <!-- 메뉴 -->
      <div class="footer-section menu">
        <p class="footer-title">메뉴</p>
        <ul>
          <li><router-link to="/">문의하기</router-link></li>
          <li><router-link to="/">회사정보</router-link></li>
          <li><router-link to="/">서비스 소개</router-link></li>
          <li><router-link to="/">개인정보 처리방침</router-link></li>
        </ul>
      </div>

      <!-- Related Organization -->
      <div class="footer-section related-organization">
        <p class="footer-title">관련 기관</p>
        <ul>
          <li><router-link to="/">온통청년</router-link></li>
          <li><router-link to="/">금융감독원</router-link></li>
          <li><router-link to="/">사람인</router-link></li>
          <li><router-link to="/">전자공시시스템</router-link></li>
        </ul>
      </div>
    </div>

    <!-- 저작권 정보 -->
    <div class="footer-bottom">
      <p>&copy; 2024 SSAFY.corp. All rights reserved.</p>
    </div>
  </footer>
</template>

<script setup>
</script>

<style scoped>
.footer {
  background-color: #1a1a1a; /* 어두운 배경으로 고급스러움 강조 */
  color: #f5f5f5; /* 밝은 텍스트 색으로 가독성 확보 */
  padding-top: 30px;
  text-align: center;
  margin-top: 50px;
  font-family: 'Roboto', sans-serif;
  width: 2114px;
  height: 300px;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  padding: 0 20px;
}

.footer-section {
  flex: 1;
  margin: 15px;
}

.footer-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 12px;
  color: #00bcd4; /* 세련된 파란색 */
  text-transform: uppercase; /* 대문자로 강조 */
}

.footer-section ul {
  list-style: none;
  padding: 0;
}

.footer-section ul li {
  margin: 8px 0;
}

.footer-section ul li a {
  color: #f5f5f5;
  font-size: 1rem;
  text-decoration: none;
  transition: color 0.3s ease, transform 0.2s ease; /* 색상과 애니메이션 효과 */
}

.footer-section ul li a:hover {
  color: #00bcd4;
  transform: translateX(5px); /* 클릭 유도 효과 */
}

.footer-bottom {
  font-size: 17px;
  color: #888; /* 저작권 정보 색상 */
  text-align: center; /* 중앙 정렬 */
}
.footer-title {
  text-align: left;
}

.left {
  text-align: left;
}
</style>
