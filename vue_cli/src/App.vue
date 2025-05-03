<template>
  <div>
    <div class="navbar">
      <div class="menu">
        <router-link to="/">Home</router-link>

        <!-- <div class="dropdown">
          <router-link :to="{ name: 'BibleView', params: { book: 'Genesis', chapter: 1 } }">Bible</router-link>
          <div class="dropdown-content">
            <router-link to="/bible/upload">Upload</router-link>
          </div>
        </div> -->

        <div class="dropdown">
          <a href="#">Kakao</a>
          <div class="dropdown-content">
            <router-link to="/kakao/search/book">API Test</router-link>
          </div>
        </div>

        <router-link to="/about">About</router-link>
      </div>
    </div>

    <router-view />
  </div>
</template>

<script>
export default {
  name: 'MainLayout'
}
</script>

<style scoped>
@import "@/assets/css/main.css";

/* 필요한 경우 추가 스타일 작성 가능 */
</style>
