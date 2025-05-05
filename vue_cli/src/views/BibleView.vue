<template>
  <div>
    <!-- 제목 -->
    <h2 class="bible-title">{{ book }} {{ chapter }}장 [{{ version_code }}]</h2>

    <!-- 성경 구절 목록 -->
    <ul class="bible-verses">
      <li v-for="verse in verses" :key="verse.verse">
        <strong>{{ verse.verse }}.</strong> {{ verse.text }}
      </li>
    </ul>

    <!-- 장 이동 네비게이션 -->
    <div class="chapter-navigation">
      <button v-if="chapter > 1" @click="goToChapter(chapter - 1)" class="nav-button">이전</button>

      <span class="page-numbers">
        <span v-for="num in totalChapters" :key="num">
          <span v-if="num === '...'" class="ellipsis">...</span>
          <strong v-else-if="num === chapter" class="current-page">{{ num }}</strong>
          <a v-else @click="goToChapter(num)" class="page-link">{{ num }}</a>
        </span>
      </span>

      <button v-if="chapter < totalChapters[totalChapters.length - 1]" @click="goToChapter(chapter + 1)" class="nav-button">다음</button>
    </div>

    <!-- 성경 선택 UI -->
    <div class="bible-selector">
      <select v-model="selectedVersion">
        <option v-for="version in versions" :key="version.code" :value="version.code">
          {{ version.name }}
        </option>
      </select>

      <select v-model="selectedBook">
        <option v-for="bookOption in books" :key="bookOption" :value="bookOption">
          {{ bookOption }}
        </option>
      </select>

      <input type="number" v-model.number="selectedChapter" :min="1" :max="maxChapter" />

      <button @click="goToSelected">읽기</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import '@/assets/css/bible_list.css'

// 라우터 인스턴스
const route = useRoute()
const router = useRouter()

// reactive 변수
const book = ref(route.params.book)
const chapter = ref(parseInt(route.params.chapter))
const versionCode = ref(route.query.version_code )

const selectedBook = ref(book.value)
const selectedChapter = ref(chapter.value)
const selectedVersion = ref(versionCode.value)

const verses = ref([])
const books = ref([])
const versions = ref([])
const version_code = ref("")
const totalChapters = ref([])
const maxChapter = ref(150) // 예시값 (실제 API 값으로 대체)

// API 호출 함수 (중복 제거용)
async function fetchBibleData() {
  book.value = route.params.book
  chapter.value = parseInt(route.params.chapter)
  versionCode.value = route.query.version_code

  const response = await axios.get(`/bible/apiview/${book.value}/${chapter.value}/`, {
    params: { version_code: versionCode.value }
  })
  const data = response.data

  verses.value = data.verses
  books.value = data.books
  versions.value = data.versions
  version_code.value = data.version_code
  totalChapters.value = data.total_chapters
  maxChapter.value = Array.isArray(data.total_chapters)
    ? Math.max(...data.total_chapters.filter(n => typeof n === 'number'))
    : 1

  selectedVersion.value = data.versions.some(v => v.code === versionCode.value)
    ? versionCode.value
    : data.version_code || data.versions[0]?.code || ''
}

// 최초 진입 시 호출
onMounted(() => {
  fetchBibleData()
})


// 라우트 변경 감지 (예: chapter 바뀔 때)
watch(() => route.fullPath, () => {
  fetchBibleData()
})

// 버튼 클릭 시 라우팅
function goToChapter(newChapter) {
  console.log ("Jinha1", book.value, newChapter, versionCode.value)
  router.push({
    name: 'BibleView',
    params: { book: book.value, chapter: newChapter },
    query: { version_code: versionCode.value }
  })
}

function goToSelected() {
  console.log ("Jinha2", selectedBook.value, selectedChapter.value, selectedVersion.value )
  router.push({
    name: 'BibleView',
    params: {
      book: selectedBook.value,
      chapter: selectedChapter.value
    },
    query: { version_code: selectedVersion.value }
  })
}
</script>
