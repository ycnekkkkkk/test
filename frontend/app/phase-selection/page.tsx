'use client'

import { useState, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { apiClient } from '@/lib/api'

const phases = [
  {
    value: 'listening_speaking',
    label: 'Listening & Speaking',
    description: '30 phút - Phần nghe và nói',
    icon: '🎧',
  },
  {
    value: 'reading_writing',
    label: 'Reading & Writing',
    description: '30 phút - Phần đọc và viết',
    icon: '📚',
  },
]

export default function PhaseSelectionPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const sessionId = searchParams.get('sessionId')

  const [selectedPhase, setSelectedPhase] = useState<string>('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!sessionId) {
      router.push('/level-selection')
    }
  }, [sessionId, router])

  const handleSubmit = async () => {
    if (!selectedPhase || !sessionId) return

    setLoading(true)
    try {
      await apiClient.selectPhase(parseInt(sessionId), { phase: selectedPhase as any })
      router.push(`/test?sessionId=${sessionId}&phase=1`)
    } catch (error) {
      console.error('Error selecting phase:', error)
      alert('Có lỗi xảy ra. Vui lòng thử lại.')
      setLoading(false)
    }
  }

  if (!sessionId) {
    return null
  }

  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-center text-gray-800">
        Chọn phần làm trước
      </h1>
      <p className="text-center text-gray-600 mb-8">
        Bạn có thể chọn làm phần nào trước. Phần còn lại sẽ được tạo sau khi bạn hoàn thành phần này.
      </p>

      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {phases.map((phase) => (
            <label
              key={phase.value}
              className={`block p-6 border-2 rounded-lg cursor-pointer transition ${
                selectedPhase === phase.value
                  ? 'border-blue-600 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
            >
              <input
                type="radio"
                name="phase"
                value={phase.value}
                checked={selectedPhase === phase.value}
                onChange={(e) => setSelectedPhase(e.target.value)}
                className="sr-only"
              />
              <div className="text-center">
                <div className="text-4xl mb-3">{phase.icon}</div>
                <div className="font-semibold text-xl mb-2">{phase.label}</div>
                <div className="text-sm text-gray-600">{phase.description}</div>
              </div>
            </label>
          ))}
        </div>
      </div>

      <div className="text-center">
        <button
          onClick={handleSubmit}
          disabled={!selectedPhase || loading}
          className={`px-8 py-3 rounded-lg text-lg font-semibold transition ${
            selectedPhase && !loading
              ? 'bg-blue-600 text-white hover:bg-blue-700'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          }`}
        >
          {loading ? 'Đang xử lý...' : 'Bắt đầu làm bài →'}
        </button>
      </div>
    </div>
  )
}

