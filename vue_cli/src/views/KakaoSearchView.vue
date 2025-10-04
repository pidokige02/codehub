<template>
    <div>
      <h1>Kakao 책 검색</h1>
      <input v-model="query" type="text" placeholder="책 제목을 입력하세요" />
      <button @click="goPage(1)">검색</button>

      <div id="bookdata">
        <p v-if="error">{{ error }}</p>
        <!-- 여러 책 결과를 반복 렌더링 -->
        <div v-if="books.length > 0">
          <div v-for="(book, index) in books" :key="index" class="book-card">
            <strong>{{ book.title }}</strong><br />
            <img v-if="book.thumbnail" :src="book.thumbnail" alt="책 이미지" /><br />
            <p>{{ book.contents }}</p>
            <p><a :href="book.url" target="_blank">자세히 보기</a></p>
          </div>
        </div>

        <!-- 페이지네이션 -->
        <div class="pagination">
          <!-- 이전 버튼 -->
          <button :disabled="page === 1" @click="goPage(page - 1)">이전</button>

          <!-- 첫 페이지 -->
          <button v-if="startPage > 1" @click="goPage(1)">1</button>
          <span v-if="startPage > 2">…</span>

          <!-- 가운데 페이지들 -->
          <button
            v-for="p in visiblePages"
            :key="p"
            :class="{ active: p === page }"
            @click="goPage(p)"
          >
            {{ p }}
          </button>

          <!-- 마지막 페이지 -->
          <span v-if="endPage < maxPage - 1">…</span>
          <button v-if="endPage < maxPage" @click="goPage(maxPage)">{{ maxPage }}</button>

          <!-- 다음 버튼 -->
          <button :disabled="page === maxPage" @click="goPage(page + 1)">다음</button>
        </div>
      </div>
    </div>

  </template>

  <script>
  import axios from 'axios'

  export default {
    name: 'KakaoSearchView',
    data() {
      return {
        query: '',
        books: [],   // 단일 객체 대신 배열
        error: '',
        page: 1,          // 현재 페이지
        pageSize: 10,     // 한 페이지당 결과 수
        totalCount: 0,    // 총 결과 수
        maxPage: 1        // 총 페이지 수
      }
    },
    computed: {
      startPage() {
        const range = 5;
        return Math.max(1, this.page - Math.floor(range / 2));
      },
      endPage() {
        const range = 5;
        return Math.min(this.maxPage, this.startPage + range - 1);
      },
      visiblePages() {
        const pages = [];
        for (let i = this.startPage; i <= this.endPage; i++) {
          pages.push(i);
        }
        return pages;
      }
    },
    methods: {
      async searchBook(page = 1) {
        this.error = ''
        this.books = []
        this.page = page;

        if (!this.query) {
          this.error = '책 제목을 입력하세요.'
          return
        }

        try {
          const response = await axios.get('/kakao/api/book_search/', {
            params: { query: this.query, page: this.page, size: this.pageSize }
          })

          if (response.data.documents.length === 0) {
            this.error = '검색 결과가 없습니다.'
          } else {
            this.books = response.data.documents
            this.totalCount = response.data.meta.pageable_count || 0;
            this.maxPage = Math.ceil(this.totalCount / this.pageSize);
            console.log("jinha",this.totalCount, this.maxPage)
          }
        } catch (err) {
          this.error = '오류가 발생했습니다.'
          console.error(err)
        }
      },
      goPage(p) {
        if (typeof p === 'number' && p >= 1 && p <= this.maxPage) {
          this.searchBook(p)
        }
      }
    }
  }
  </script>

  <style scoped>
  input {
    margin-right: 8px;
    padding: 6px;
  }
  button {
    padding: 6px 12px;
  }
  #bookdata {
    margin-top: 20px;
  }
  .book-card {
    margin-bottom: 20px;
    border-bottom: 1px solid #ddd;
    padding-bottom: 10px;
  }
  img {
    max-width: 200px;
  }
  .pagination {
    margin-top: 20px;
  }
  button.active {
  background-color: #007bff;
  color: white;
  font-weight: bold;
  }
  </style>
