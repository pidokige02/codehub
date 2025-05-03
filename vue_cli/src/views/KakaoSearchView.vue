<template>
    <div>
      <h1>Kakao 책 검색</h1>
      <input v-model="query" type="text" placeholder="책 제목을 입력하세요" />
      <button @click="searchBook">검색</button>

      <div id="bookdata">
        <p v-if="error">{{ error }}</p>
        <div v-if="book">
          <strong>{{ book.title }}</strong><br />
          <img :src="book.thumbnail" alt="책 이미지" /><br />
          <p>{{ book.contents }}</p>
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
        book: null,
        error: ''
      }
    },
    methods: {
      async searchBook() {
        this.error = ''
        this.book = null

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
            this.book = response.data.documents[0]
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
