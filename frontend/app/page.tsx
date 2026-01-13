'use client'

import { useRouter } from 'next/navigation'

export default function Home() {
  const router = useRouter()

  return (
    <div className="max-w-4xl mx-auto text-center">
      <h1 className="text-4xl font-bold mb-6 text-gray-800">
        IELTS Test
      </h1>
      <p className="text-xl text-gray-600 mb-8">
        Đánh giá toàn diện 4 kỹ năng với AI
      </p>
      
      <div className="bg-white rounded-lg shadow-md p-8 mb-8">
        <h2 className="text-2xl font-semibold mb-4">Quy trình làm bài:</h2>
        <ol className="list-decimal list-inside text-left space-y-2 text-gray-700 max-w-2xl mx-auto">
          <li>Chọn trình độ hiện tại (Beginner → Advanced)</li>
          <li>Chọn phần làm trước: Listening & Speaking HOẶC Reading & Writing</li>
          <li>Hệ thống tạo đề cho phần đã chọn (30 phút)</li>
          <li>Làm bài và nộp phần 1</li>
          <li>Hệ thống tạo đề cho phần còn lại</li>
          <li>Làm bài và nộp phần 2</li>
          <li>Xem kết quả tổng hợp (4 kỹ năng + Overall Band)</li>
        </ol>
      </div>

      <button
        onClick={() => router.push('/level-selection')}
        className="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 transition"
      >
        Bắt đầu Test →
      </button>
    </div>
  )
}

