<template>
    <div>
      <h1>Kakao 책 검색</h1>
      <input v-model="query" type="text" placeholder="책 제목을 입력하세요" />
      <button @click="searchBook">검색</button>

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
        error: ''
      }
    },
    methods: {
      async searchBook() {
        this.error = ''
        this.books = []

        if (!this.query) {
          this.error = '책 제목을 입력하세요.'
          return
        }

        try {
          const response = await axios.get('/kakao/api/book_search/', {
            params: { query: this.query }
          })

          if (response.data.documents.length === 0) {
            this.error = '검색 결과가 없습니다.'
          } else {
            this.books = response.data.documents
          }
        } catch (err) {
          this.error = '오류가 발생했습니다.'
          console.error(err)
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
  img {
    max-width: 200px;
  }
  </style>
