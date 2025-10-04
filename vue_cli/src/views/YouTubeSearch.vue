<template>
  <div class="youtube-search">
    <h2>YouTube 검색</h2>

    <!-- 검색 폼 -->
    <form @submit.prevent="getList()">
      <input
        type="text"
        v-model="query"
        placeholder="검색어 입력"
      />
      <button type="submit">가져오기</button>
    </form>

    <!-- 검색 결과 -->
    <div v-if="items.length === 0 && !loading" class="no-result">
      검색 결과가 없습니다.
    </div>

    <div v-else>
      <div v-for="item in items" :key="item.id.videoId" class="box">
        <p>
          <a :href="`https://youtu.be/${item.id.videoId}`" target="_blank">
            {{ item.snippet.title }}
          </a>
        </p>

        <!-- 썸네일 0~3 -->
        <img
          v-for="i in 4"
          :key="i"
          class="box"
          :src="`https://img.youtube.com/vi/${item.id.videoId}/${i-1}.jpg`"
          :alt="`thumbnail-${i-1}`"
        />

        <!-- default, hqdefault 썸네일 -->
        <img
          class="box"
          :src="`https://img.youtube.com/vi/${item.id.videoId}/default.jpg`"
          alt="default"
        />
        <img
          class="box"
          :src="`https://img.youtube.com/vi/${item.id.videoId}/hqdefault.jpg`"
          alt="hqdefault"
        />
      </div>
    </div>

    <!-- 페이지 네비게이션 -->
    <div class="pagination" v-if="prevPageToken || nextPageToken">
      <button v-if="prevPageToken" @click="getList(prevPageToken)">
        &lt;이전페이지&gt;
      </button>
      <button v-if="nextPageToken" @click="getList(nextPageToken)">
        &lt;다음페이지&gt;
      </button>
    </div>

    <!-- 로딩 표시 -->
    <div v-if="loading">로딩 중...</div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "YouTubeSearch",
  data() {
    return {
      query: "",
      items: [],
      prevPageToken: null,
      nextPageToken: null,
      loading: false,
    };
  },
  methods: {
    async getList(pageToken) {
      if (!this.query) {
        alert("검색어를 입력하세요.");
        return;
      }

      this.loading = true;
      this.items = [];
      this.prevPageToken = null;
      this.nextPageToken = null;

      try {
        let url = `/YouTube/api/search/?query=${encodeURIComponent(this.query)}`;
        if (pageToken) {
          url += `&pageToken=${pageToken}`;
        }

        const response = await axios.get(url);
        const jdata = response.data;

        if (!jdata.items) {
          this.items = [];
        } else {
          this.items = jdata.items;
        }

        this.prevPageToken = jdata.prevPageToken || null;
        this.nextPageToken = jdata.nextPageToken || null;
      } catch (error) {
        console.error(error);
        alert("서버 요청 중 오류가 발생했습니다.");
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.box {
  display: block;
  margin: 10px 0;
}
.pagination {
  margin-top: 10px;
}
</style>
