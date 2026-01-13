'use client'

import { useState, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { apiClient } from '@/lib/api'
import SpeechRecorder from '@/components/SpeechRecorder'
import InteractiveSpeaking from '@/components/InteractiveSpeaking'
import UnifiedSpeaking from '@/components/UnifiedSpeaking'

// Function to get audio playback rate based on level
function getAudioRate(level: string): number {
  const rateMap: { [key: string]: number } = {
    'beginner': 0.7,           // Chậm nhất cho người mới bắt đầu
    'elementary': 0.75,        // Chậm cho trình độ cơ bản
    'intermediate': 0.8,       // Trung bình
    'upper_intermediate': 0.85, // Hơi nhanh
    'advanced': 0.9,           // Gần tốc độ tự nhiên
  }
  return rateMap[level] || 0.8 // Default to intermediate if level not found
}

// Component for Listening Section with audio playback
function ListeningSection({ section, handleAnswerChange, level }: { section: any, handleAnswerChange: (key: string, value: string) => void, level: string }) {
  const [isPlaying, setIsPlaying] = useState(false)
  const [hasPlayed, setHasPlayed] = useState(false)
  const [currentUtterance, setCurrentUtterance] = useState<SpeechSynthesisUtterance | null>(null)

  const playAudio = () => {
    if (!section.audio_transcript) {
      alert('Không có audio transcript cho section này')
      return
    }

    // Chỉ cho phép nghe 1 lần
    if (hasPlayed) {
      return
    }

    if ('speechSynthesis' in window) {
      // Stop any current playback
      if (currentUtterance) {
        speechSynthesis.cancel()
      }

      const text = section.audio_transcript
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.lang = 'en-US'
      utterance.rate = getAudioRate(level) // Tốc độ phụ thuộc vào level
      utterance.pitch = 1.0

      utterance.onstart = () => setIsPlaying(true)
      utterance.onend = () => {
        setIsPlaying(false)
        setCurrentUtterance(null)
        setHasPlayed(true) // Đánh dấu đã nghe xong
      }
      utterance.onerror = () => {
        setIsPlaying(false)
        setCurrentUtterance(null)
        setHasPlayed(true) // Đánh dấu đã nghe (kể cả khi lỗi)
      }

      setCurrentUtterance(utterance)
      speechSynthesis.speak(utterance)
    } else {
      alert('Trình duyệt của bạn không hỗ trợ text-to-speech')
    }
  }

  const stopAudio = () => {
    if ('speechSynthesis' in window) {
      speechSynthesis.cancel()
      setIsPlaying(false)
      setCurrentUtterance(null)
      setHasPlayed(true) // Đánh dấu đã nghe (dù đã dừng)
    }
  }

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (currentUtterance) {
        speechSynthesis.cancel()
      }
    }
  }, [currentUtterance])

  return (
    <div className="mb-6 border-b pb-6 last:border-b-0">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-xl font-semibold">{section.title}</h3>
        {section.audio_transcript && (
          <button
            onClick={isPlaying ? stopAudio : playAudio}
            disabled={hasPlayed && !isPlaying}
            className={`px-4 py-2 rounded font-semibold transition ${hasPlayed && !isPlaying
                ? 'bg-gray-400 text-white cursor-not-allowed'
                : isPlaying
                  ? 'bg-red-600 text-white hover:bg-red-700'
                  : 'bg-green-600 text-white hover:bg-green-700'
              }`}
          >
            {isPlaying ? (
              <>
                <span className="inline-block w-2 h-2 bg-white rounded-full mr-2 animate-pulse"></span>
                Stop
              </>
            ) : hasPlayed ? (
              <>Already Played</>
            ) : (
              <>Listen to Section {section.id}</>
            )}
          </button>
        )}
      </div>
      <p className="text-gray-600 mb-4">{section.instructions}</p>
      {section.audio_transcript && (
        <div className="bg-yellow-50 border border-yellow-200 rounded p-3 mb-4">
          <p className="text-sm text-gray-700">
            <strong>Note:</strong> Click the "Listen to Section {section.id}" button above to play the audio. <strong>You can only listen once.</strong>
          </p>
        </div>
      )}
      <div className="space-y-4">
        {section.questions?.map((q: any) => (
          <div key={q.id} className="border-b pb-4">
            <div className="font-semibold mb-2">Câu {q.id}: {q.question}</div>
            {q.type === 'multiple_choice' && q.options ? (
              <div className="space-y-2">
                {q.options.map((opt: string, idx: number) => (
                  <label key={idx} className="flex items-center cursor-pointer">
                    <input
                      type="radio"
                      name={`listening_s${section.id}_q${q.id}`}
                      value={opt.split('.')[0].trim()}
                      onChange={(e) => handleAnswerChange(`listening_s${section.id}_q${q.id}`, e.target.value)}
                      className="mr-2"
                    />
                    <span>{opt}</span>
                  </label>
                ))}
              </div>
            ) : (
              <input
                type="text"
                className="w-full border rounded px-3 py-2 mt-2"
                placeholder="Nhập câu trả lời..."
                onChange={(e) => handleAnswerChange(`listening_s${section.id}_q${q.id}`, e.target.value)}
              />
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default function TestPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const sessionId = searchParams.get('sessionId')
  const phaseParam = searchParams.get('phase')

  const [session, setSession] = useState<any>(null)
  const phase = phaseParam ? parseInt(phaseParam) : 1
  const [content, setContent] = useState<any>(null)
  const [answers, setAnswers] = useState<any>({})
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    if (!sessionId) {
      router.push('/level-selection')
      return
    }

    const loadSession = async () => {
      if (!sessionId) return
      const currentPhase = phaseParam ? parseInt(phaseParam) : 1
      try {
        console.log(`Loading session ${sessionId} for phase ${currentPhase}`)
        const sessionData = await apiClient.getSession(parseInt(sessionId))
        setSession(sessionData)

        // Generate content if not exists
        if (currentPhase === 1 && !sessionData.phase1_content) {
          console.log('Generating phase 1 content...')
          await apiClient.generatePhase(parseInt(sessionId))
          const updated = await apiClient.getSession(parseInt(sessionId))
          setSession(updated)
          setContent(updated.phase1_content)
        } else if (currentPhase === 1 && sessionData.phase1_content) {
          console.log('Phase 1 content already exists, loading...')
          setContent(sessionData.phase1_content)
        } else if (currentPhase === 2 && !sessionData.phase2_content) {
          console.log('Generating phase 2 content...')
          await apiClient.generatePhase2(parseInt(sessionId))
          const updated = await apiClient.getSession(parseInt(sessionId))
          setSession(updated)
          setContent(updated.phase2_content)
        } else if (currentPhase === 2 && sessionData.phase2_content) {
          console.log('Phase 2 content already exists, loading...')
          setContent(sessionData.phase2_content)
        }

        setLoading(false)
      } catch (error) {
        console.error('Error loading session:', error)
        setLoading(false)
      }
    }

    // Reset state when phase changes
    setLoading(true)
    setContent(null)
    setAnswers({})
    setSubmitting(false)  // Reset submitting state when phase changes
    loadSession()
  }, [sessionId, phaseParam, router])

  const handleAnswerChange = (key: string, value: string) => {
    setAnswers({ ...answers, [key]: value })
  }

  const handleSubmit = async () => {
    if (!sessionId) return
    setSubmitting(true)

    try {
      if (phase === 1) {
        console.log('Submitting phase 1...')
        const result = await apiClient.submitPhase1(parseInt(sessionId), answers)
        console.log('Phase 1 submitted successfully:', result)
        // Reset submitting before navigation
        setSubmitting(false)
        // Move to phase 2
        router.push(`/test?sessionId=${sessionId}&phase=2`)
      } else {
        console.log('Submitting phase 2...')
        await apiClient.submitPhase2(parseInt(sessionId), answers)
        console.log('Phase 2 submitted, aggregating results...')
        // Aggregate and show results
        await apiClient.aggregateResults(parseInt(sessionId))
        setSubmitting(false)
        router.push(`/results?sessionId=${sessionId}`)
      }
    } catch (error: any) {
      console.error('Error submitting:', error)
      const errorMessage = error?.response?.data?.detail || error?.message || 'Có lỗi xảy ra. Vui lòng thử lại.'
      alert(errorMessage)
      setSubmitting(false)
    }
  }

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="text-xl">Đang tạo đề thi...</div>
      </div>
    )
  }

  if (!content) {
    return (
      <div className="text-center py-12">
        <div className="text-xl text-red-600">Không tìm thấy nội dung đề thi</div>
      </div>
    )
  }

  const isListeningSpeaking = session?.selected_phase === 'listening_speaking'
  const isPhase1 = phase === 1
  const showListening = (isListeningSpeaking && isPhase1) || (!isListeningSpeaking && !isPhase1)
  const showSpeaking = (isListeningSpeaking && isPhase1) || (!isListeningSpeaking && !isPhase1)
  const showReading = (!isListeningSpeaking && isPhase1) || (isListeningSpeaking && !isPhase1)
  const showWriting = (!isListeningSpeaking && isPhase1) || (isListeningSpeaking && !isPhase1)

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-blue-600 text-white p-4 rounded-lg mb-6">
        <h1 className="text-2xl font-bold">
          Phase {phase}: {isPhase1 ? (showListening ? 'Listening & Speaking' : 'Reading & Writing') : (showListening ? 'Listening & Speaking' : 'Reading & Writing')}
        </h1>
        <p className="text-blue-100 mt-1">Thời gian: 30 phút</p>
      </div>

      <div className="space-y-8">
        {/* Listening Section */}
        {showListening && content.listening && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold mb-4">Listening</h2>
            {content.listening.sections?.map((section: any) => (
              <ListeningSection
                key={section.id}
                section={section}
                handleAnswerChange={handleAnswerChange}
                level={session?.level || 'intermediate'}
              />
            ))}
          </div>
        )}

        {/* Reading Section */}
        {showReading && content.reading && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold mb-4">Reading</h2>
            {content.reading.passages?.map((passage: any) => (
              <div key={passage.id} className="mb-6">
                <h3 className="text-xl font-semibold mb-3">{passage.title}</h3>
                <div className="bg-gray-50 p-4 rounded mb-4 whitespace-pre-wrap">{passage.content}</div>
                <div className="space-y-4">
                  {passage.questions?.map((q: any) => (
                    <div key={q.id} className="border-b pb-4">
                      <div className="font-semibold mb-2">Câu {q.id}: {q.question}</div>
                      {q.type === 'multiple_choice' && q.options ? (
                        <div className="space-y-2">
                          {q.options.map((opt: string, idx: number) => (
                            <label key={idx} className="flex items-center cursor-pointer">
                              <input
                                type="radio"
                                name={`reading_p${passage.id}_q${q.id}`}
                                value={opt.split('.')[0].trim()}
                                onChange={(e) => handleAnswerChange(`reading_p${passage.id}_q${q.id}`, e.target.value)}
                                className="mr-2"
                              />
                              <span>{opt}</span>
                            </label>
                          ))}
                        </div>
                      ) : (
                        <input
                          type="text"
                          className="w-full border rounded px-3 py-2 mt-2"
                          placeholder="Nhập câu trả lời..."
                          onChange={(e) => handleAnswerChange(`reading_p${passage.id}_q${q.id}`, e.target.value)}
                        />
                      )}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Speaking Section - Unified */}
        {showSpeaking && content.speaking && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold mb-4">Speaking</h2>
            <UnifiedSpeaking
              part1={content.speaking.part1}
              part2={content.speaking.part2}
              part3={content.speaking.part3}
              onAnswer={(key, answer) => handleAnswerChange(key, answer)}
              answers={answers}
            />
          </div>
        )}

        {/* Writing Section */}
        {showWriting && content.writing && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold mb-4">Writing</h2>

            {/* Task 1 */}
            {content.writing.task1 && (
              <div className="mb-6">
                <h3 className="text-xl font-semibold mb-3">Task 1: {content.writing.task1.type}</h3>
                <div className="bg-gray-50 p-4 rounded mb-4">
                  <div className="font-semibold mb-2">Instructions:</div>
                  <div className="text-gray-700 mb-2">{content.writing.task1.instructions}</div>
                </div>
                {content.writing.task1.chart_description && (
                  <div className="bg-blue-50 border-2 border-blue-200 rounded-lg p-4 mb-4">
                    <div className="font-semibold text-blue-800 mb-2 flex items-center">
                      <span className="mr-2">📊</span>
                      Chart Description (Text Format)
                    </div>
                    <div className="text-gray-800 whitespace-pre-wrap bg-white p-3 rounded border border-blue-100">
                      {content.writing.task1.chart_description}
                    </div>
                    <div className="text-xs text-gray-600 mt-2 italic">
                      Note: This is a text description of the chart data. Use this information to write your response.
                    </div>
                  </div>
                )}
                <textarea
                  className="w-full border rounded px-3 py-2"
                  rows={8}
                  placeholder={`Viết ${content.writing.task1.word_count} từ...`}
                  onChange={(e) => handleAnswerChange('writing_task1', e.target.value)}
                />
                <div className="text-sm text-gray-500 mt-2">
                  Mục tiêu: {content.writing.task1.word_count} từ
                </div>
              </div>
            )}

            {/* Task 2 */}
            {content.writing.task2 && (
              <div className="mb-6">
                <h3 className="text-xl font-semibold mb-3">Task 2: Essay</h3>
                <div className="bg-gray-50 p-4 rounded mb-4">
                  <div className="font-semibold mb-2">Question:</div>
                  <div className="text-gray-700">{content.writing.task2.question}</div>
                </div>
                <textarea
                  className="w-full border rounded px-3 py-2"
                  rows={10}
                  placeholder={`Viết ${content.writing.task2.word_count} từ...`}
                  onChange={(e) => handleAnswerChange('writing_task2', e.target.value)}
                />
                <div className="text-sm text-gray-500 mt-2">
                  Mục tiêu: {content.writing.task2.word_count} từ
                </div>
              </div>
            )}
          </div>
        )}

        {/* Submit Button */}
        <div className="text-center py-6">
          <button
            onClick={handleSubmit}
            disabled={submitting}
            className={`px-8 py-3 rounded-lg text-lg font-semibold transition ${submitting
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-green-600 text-white hover:bg-green-700'
              }`}
          >
            {submitting ? 'Đang xử lý...' : phase === 1 ? 'Nộp bài và tiếp tục →' : 'Nộp bài và xem kết quả →'}
          </button>
        </div>
      </div>
    </div>
  )
}

