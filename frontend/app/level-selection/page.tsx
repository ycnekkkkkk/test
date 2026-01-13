'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { apiClient } from '@/lib/api'

const levels = [
  { value: 'beginner', label: 'Beginner', description: 'Mới bắt đầu học tiếng Anh' },
  { value: 'elementary', label: 'Elementary', description: 'Cơ bản' },
  { value: 'intermediate', label: 'Intermediate', description: 'Trung bình' },
  { value: 'upper_intermediate', label: 'Upper Intermediate', description: 'Khá' },
  { value: 'advanced', label: 'Advanced', description: 'Cao cấp' },
]

export default function LevelSelectionPage() {
  const router = useRouter()
  const [selectedLevel, setSelectedLevel] = useState<string>('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async () => {
    if (!selectedLevel) return

    setLoading(true)
    try {
      const session = await apiClient.createSession({ level: selectedLevel as any })
      router.push(`/phase-selection?sessionId=${session.id}`)
    } catch (error) {
      console.error('Error creating session:', error)
      alert('Có lỗi xảy ra. Vui lòng thử lại.')
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-center text-gray-800">
        Chọn trình độ hiện tại của bạn
      </h1>

      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="space-y-3">
          {levels.map((level) => (
            <label
              key={level.value}
              className={`block p-4 border-2 rounded-lg cursor-pointer transition ${
                selectedLevel === level.value
                  ? 'border-blue-600 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
            >
              <input
                type="radio"
                name="level"
                value={level.value}
                checked={selectedLevel === level.value}
                onChange={(e) => setSelectedLevel(e.target.value)}
                className="mr-3"
              />
              <span className="font-semibold text-lg">{level.label}</span>
              <span className="block text-sm text-gray-600 mt-1">{level.description}</span>
            </label>
          ))}
        </div>
      </div>

      <div className="text-center">
        <button
          onClick={handleSubmit}
          disabled={!selectedLevel || loading}
          className={`px-8 py-3 rounded-lg text-lg font-semibold transition ${
            selectedLevel && !loading
              ? 'bg-blue-600 text-white hover:bg-blue-700'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          }`}
        >
          {loading ? 'Đang xử lý...' : 'Tiếp tục →'}
        </button>
      </div>
    </div>
  )
}

