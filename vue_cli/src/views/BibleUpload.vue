<template>
    <div>
      <h2>성경 데이터 업로드</h2>

      <form @submit.prevent="handleUpload">
        <input type="file" @change="handleFileChange" required />
        <button type="submit">업로드</button>
      </form>

      <p v-if="message">{{ message }}</p>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
const selectedFile = ref(null)
const message = ref('')

const router = useRouter()

function handleFileChange(event) {
  selectedFile.value = event.target.files[0]
}
async function handleUpload() {
  if (!selectedFile.value) {
    message.value = '파일을 선택해주세요.'
    return
  }
  const formData = new FormData()
  formData.append('file', selectedFile.value)
  try {
      await axios.post('/bible/upload-api/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    message.value = '업로드 성공! 리디렉션 중...'
    // 네임드 라우터로 이동
    router.push({ name: 'BibleView', params: { book: 'Genesis', chapter: 1 } })

  } catch (error) {
    message.value = '업로드 실패: ' + (error.response?.data?.error || error.message)
  }
}
</script>
