<template>
  <div>
    <div class="navbar">
      <div class="menu">
        <router-link to="/">Home</router-link>

        <div class="dropdown">
          <a href="#">Bible</a>
          <div class="dropdown-content">
            <router-link :to="{ name: 'BibleView', params: { book: '창세기', chapter: 1 } }">BibleView</router-link>
            <router-link to="/bible/upload">Upload</router-link>
          </div>
        </div>

        <div class="dropdown">
          <a href="#">Kakao</a>
          <div class="dropdown-content">
            <router-link to="/kakao/search/book">book query</router-link>
          </div>
        </div>

        <div class="dropdown">
          <a href="#">YouTube</a>
          <div class="dropdown-content">
            <router-link to="/YouTube/search/">API Test</router-link>
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
