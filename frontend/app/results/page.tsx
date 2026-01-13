'use client'

import { useState, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { apiClient } from '@/lib/api'

export default function ResultsPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const sessionId = searchParams.get('sessionId')

  const [session, setSession] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!sessionId) {
      router.push('/')
      return
    }
    loadSession()
  }, [sessionId, router])

  const loadSession = async () => {
    if (!sessionId) return
    try {
      const sessionData = await apiClient.getSession(parseInt(sessionId))
      setSession(sessionData)
      setLoading(false)
    } catch (error) {
      console.error('Error loading session:', error)
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="text-xl">Đang tải kết quả...</div>
      </div>
    )
  }

  if (!session || !session.final_results) {
    return (
      <div className="max-w-3xl mx-auto text-center py-12">
        <div className="bg-white rounded-lg shadow-md p-8 mb-6">
          <div className="text-xl text-red-600 mb-4">Không tìm thấy kết quả</div>
          <button
            onClick={() => router.push('/')}
            className="px-8 py-3 bg-blue-600 text-white rounded-lg text-lg font-semibold hover:bg-blue-700 transition"
          >
            Về trang chủ
          </button>
        </div>
      </div>
    )
  }

  const results = session.final_results

  const getBandColor = (band: number) => {
    if (band >= 7) return 'bg-green-500'
    if (band >= 5.5) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  const BandCard = ({ title, band }: { title: string; band: number }) => {
    return (
      <div className="bg-white rounded-lg shadow-md p-6 text-center">
        <div className="text-gray-600 mb-3 text-sm font-medium uppercase tracking-wide">{title}</div>
        <div className={`${getBandColor(band)} text-white text-4xl font-bold rounded-full w-20 h-20 flex items-center justify-center mx-auto shadow-lg`}>
          {band.toFixed(1)}
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold mb-4 text-gray-800">Kết quả IELTS Test</h1>
        <p className="text-xl text-gray-600">
          Trình độ: <span className="font-semibold capitalize text-blue-600">{session.level}</span>
        </p>
      </div>

      {/* Overall Band Score */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-800 rounded-lg shadow-lg p-8 mb-8 text-white text-center">
        <div className="text-2xl mb-4 font-semibold">Overall Band Score</div>
        <div className="text-7xl font-bold mb-2">{results.overall?.toFixed(1) || '0.0'}</div>
        <div className="text-blue-100 text-lg">out of 9.0</div>
      </div>

      {/* Individual Bands Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <BandCard title="Listening" band={results.listening || 0} />
        <BandCard title="Reading" band={results.reading || 0} />
        <BandCard title="Writing" band={results.writing || 0} />
        <BandCard title="Speaking" band={results.speaking || 0} />
      </div>

      {/* Detailed Analysis Section */}
      {session.final_results?.detailed_analysis && (
        <div className="mt-8 space-y-6">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-6">Phân tích Chi tiết</h2>

          {/* IELTS Analysis */}
          {session.final_results.detailed_analysis.ielts_analysis && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-2xl font-bold mb-6 text-gray-800 border-b pb-3">Phân tích sâu theo khung IELTS</h3>

              {/* Reading Analysis */}
              {session.final_results.detailed_analysis.ielts_analysis.reading && (
                <div className="mb-6">
                  <h4 className="text-xl font-semibold mb-4 text-gray-700">📖 Reading (Đọc hiểu)</h4>
                  {session.final_results.detailed_analysis.ielts_analysis.reading.strengths && (
                    <div className="mb-4">
                      <div className="font-semibold text-green-700 mb-2">Điểm mạnh:</div>
                      <ul className="list-disc list-inside space-y-1 text-gray-700 ml-4">
                        {session.final_results.detailed_analysis.ielts_analysis.reading.strengths.map((s: string, i: number) => (
                          <li key={i}>{s}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {session.final_results.detailed_analysis.ielts_analysis.reading.weaknesses && (
                    <div className="mb-4">
                      <div className="font-semibold text-red-700 mb-2">Điểm yếu:</div>
                      <ul className="list-disc list-inside space-y-1 text-gray-700 ml-4">
                        {session.final_results.detailed_analysis.ielts_analysis.reading.weaknesses.map((w: string, i: number) => (
                          <li key={i}>{w}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {session.final_results.detailed_analysis.ielts_analysis.reading.question_type_analysis && (
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <div className="font-semibold mb-2 text-gray-700">Phân tích theo dạng câu hỏi:</div>
                      <div className="space-y-2 text-sm text-gray-600">
                        {Object.entries(session.final_results.detailed_analysis.ielts_analysis.reading.question_type_analysis).map(([type, analysis]: [string, any]) => (
                          <div key={type}>
                            <span className="font-medium capitalize">{type.replace(/_/g, ' ')}:</span> {analysis}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Listening Analysis */}
              {session.final_results.detailed_analysis.ielts_analysis.listening && (
                <div className="mb-6">
                  <h4 className="text-xl font-semibold mb-4 text-gray-700">🎧 Listening (Nghe hiểu)</h4>
                  {session.final_results.detailed_analysis.ielts_analysis.listening.strengths && (
                    <div className="mb-4">
                      <div className="font-semibold text-green-700 mb-2">Điểm mạnh:</div>
                      <ul className="list-disc list-inside space-y-1 text-gray-700 ml-4">
                        {session.final_results.detailed_analysis.ielts_analysis.listening.strengths.map((s: string, i: number) => (
                          <li key={i}>{s}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {session.final_results.detailed_analysis.ielts_analysis.listening.weaknesses && (
                    <div className="mb-4">
                      <div className="font-semibold text-red-700 mb-2">Điểm yếu:</div>
                      <ul className="list-disc list-inside space-y-1 text-gray-700 ml-4">
                        {session.final_results.detailed_analysis.ielts_analysis.listening.weaknesses.map((w: string, i: number) => (
                          <li key={i}>{w}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {session.final_results.detailed_analysis.ielts_analysis.listening.question_type_analysis && (
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <div className="font-semibold mb-2 text-gray-700">Phân tích theo dạng câu hỏi:</div>
                      <div className="space-y-2 text-sm text-gray-600">
                        {Object.entries(session.final_results.detailed_analysis.ielts_analysis.listening.question_type_analysis).map(([type, analysis]: [string, any]) => (
                          <div key={type}>
                            <span className="font-medium capitalize">{type.replace(/_/g, ' ')}:</span> {analysis}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Writing Analysis */}
              {session.final_results.detailed_analysis.ielts_analysis.writing && (
                <div className="mb-6">
                  <h4 className="text-xl font-semibold mb-4 text-gray-700">✍️ Writing (Viết)</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    {['task_achievement', 'coherence_cohesion', 'lexical_resource', 'grammatical_range'].map((criteria) => {
                      const critData = session.final_results.detailed_analysis.ielts_analysis.writing[criteria]
                      if (!critData) return null
                      return (
                        <div key={criteria} className="bg-gray-50 p-4 rounded-lg">
                          <div className="font-semibold mb-2 text-gray-700 capitalize">{criteria.replace(/_/g, ' ')}</div>
                          <div className="text-2xl font-bold text-blue-600 mb-2">{critData.score?.toFixed(1)}</div>
                          {critData.strengths && critData.strengths.length > 0 && (
                            <div className="text-sm text-green-700 mb-1">
                              <div className="font-medium">Mạnh:</div>
                              <ul className="list-disc list-inside ml-2">
                                {critData.strengths.map((s: string, i: number) => (
                                  <li key={i}>{s}</li>
                                ))}
                              </ul>
                            </div>
                          )}
                          {critData.weaknesses && critData.weaknesses.length > 0 && (
                            <div className="text-sm text-red-700">
                              <div className="font-medium">Yếu:</div>
                              <ul className="list-disc list-inside ml-2">
                                {critData.weaknesses.map((w: string, i: number) => (
                                  <li key={i}>{w}</li>
                                ))}
                              </ul>
                            </div>
                          )}
                        </div>
                      )
                    })}
                  </div>
                  {session.final_results.detailed_analysis.ielts_analysis.writing.overall_assessment && (
                    <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
                      <div className="font-semibold mb-1 text-gray-700">Đánh giá tổng quan:</div>
                      <div className="text-gray-700">{session.final_results.detailed_analysis.ielts_analysis.writing.overall_assessment}</div>
                    </div>
                  )}
                </div>
              )}

              {/* Speaking Analysis */}
              {session.final_results.detailed_analysis.ielts_analysis.speaking && (
                <div className="mb-6">
                  <h4 className="text-xl font-semibold mb-4 text-gray-700">🎤 Speaking (Nói)</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    {['fluency_coherence', 'lexical_resource', 'grammatical_range', 'pronunciation'].map((criteria) => {
                      const critData = session.final_results.detailed_analysis.ielts_analysis.speaking[criteria]
                      if (!critData) return null
                      return (
                        <div key={criteria} className="bg-gray-50 p-4 rounded-lg">
                          <div className="font-semibold mb-2 text-gray-700 capitalize">{criteria.replace(/_/g, ' ')}</div>
                          <div className="text-2xl font-bold text-blue-600 mb-2">{critData.score?.toFixed(1)}</div>
                          {critData.strengths && critData.strengths.length > 0 && (
                            <div className="text-sm text-green-700 mb-1">
                              <div className="font-medium">Mạnh:</div>
                              <ul className="list-disc list-inside ml-2">
                                {critData.strengths.map((s: string, i: number) => (
                                  <li key={i}>{s}</li>
                                ))}
                              </ul>
                            </div>
                          )}
                          {critData.weaknesses && critData.weaknesses.length > 0 && (
                            <div className="text-sm text-red-700">
                              <div className="font-medium">Yếu:</div>
                              <ul className="list-disc list-inside ml-2">
                                {critData.weaknesses.map((w: string, i: number) => (
                                  <li key={i}>{w}</li>
                                ))}
                              </ul>
                            </div>
                          )}
                        </div>
                      )
                    })}
                  </div>
                  {session.final_results.detailed_analysis.ielts_analysis.speaking.overall_assessment && (
                    <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
                      <div className="font-semibold mb-1 text-gray-700">Đánh giá tổng quan:</div>
                      <div className="text-gray-700">{session.final_results.detailed_analysis.ielts_analysis.speaking.overall_assessment}</div>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {/* Beyond IELTS Analysis */}
          {session.final_results.detailed_analysis.beyond_ielts && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-2xl font-bold mb-6 text-gray-800 border-b pb-3">Mở rộng ngoài IELTS</h3>

              {/* Reflex Level & Reception */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                {session.final_results.detailed_analysis.beyond_ielts.reflex_level && (
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <div className="font-semibold mb-2 text-gray-700">Năng lực phản xạ</div>
                    <div className="text-lg font-bold text-blue-600 capitalize">{session.final_results.detailed_analysis.beyond_ielts.reflex_level}</div>
                  </div>
                )}
                {session.final_results.detailed_analysis.beyond_ielts.reception_ability && (
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <div className="font-semibold mb-2 text-gray-700">Khả năng tiếp thu</div>
                    <div className="text-gray-700">{session.final_results.detailed_analysis.beyond_ielts.reception_ability}</div>
                  </div>
                )}
              </div>

              {/* Mother Tongue Influence */}
              {session.final_results.detailed_analysis.beyond_ielts.mother_tongue_influence && (
                <div className="mb-6">
                  <h4 className="text-xl font-semibold mb-4 text-gray-700">Ảnh hưởng của ngôn ngữ mẹ đẻ</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {Object.entries(session.final_results.detailed_analysis.beyond_ielts.mother_tongue_influence).map(([key, value]: [string, any]) => (
                      <div key={key} className="bg-gray-50 p-4 rounded-lg">
                        <div className="font-semibold mb-2 text-gray-700 capitalize">{key.replace(/_/g, ' ')}</div>
                        <div className="text-gray-700 text-sm">{value}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Grammar */}
              {session.final_results.detailed_analysis.beyond_ielts.grammar && (
                <div className="mb-6">
                  <h4 className="text-xl font-semibold mb-4 text-gray-700">Văn phạm</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {Object.entries(session.final_results.detailed_analysis.beyond_ielts.grammar).map(([key, value]: [string, any]) => (
                      <div key={key} className="bg-gray-50 p-4 rounded-lg">
                        <div className="font-semibold mb-2 text-gray-700 capitalize">{key.replace(/_/g, ' ')}</div>
                        <div className="text-gray-700 text-sm">{value}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Pronunciation */}
              {session.final_results.detailed_analysis.beyond_ielts.pronunciation && (
                <div className="mb-6">
                  <h4 className="text-xl font-semibold mb-4 text-gray-700">Phát âm</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {Object.entries(session.final_results.detailed_analysis.beyond_ielts.pronunciation).map(([key, value]: [string, any]) => (
                      <div key={key} className="bg-gray-50 p-4 rounded-lg">
                        <div className="font-semibold mb-2 text-gray-700 capitalize">{key.replace(/_/g, ' ')}</div>
                        <div className="text-gray-700 text-sm">{value}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Vocabulary */}
              {session.final_results.detailed_analysis.beyond_ielts.vocabulary && (
                <div className="mb-6">
                  <h4 className="text-xl font-semibold mb-4 text-gray-700">Từ vựng</h4>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {Object.entries(session.final_results.detailed_analysis.beyond_ielts.vocabulary).map(([key, value]: [string, any]) => (
                      <div key={key} className="bg-gray-50 p-4 rounded-lg">
                        <div className="font-semibold mb-2 text-gray-700 capitalize">{key.replace(/_/g, ' ')}</div>
                        <div className="text-gray-700 text-sm">{value}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Action Button */}
      <div className="text-center mt-8">
        <button
          onClick={() => router.push('/')}
          className="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 transition"
        >
          Làm bài test mới
        </button>
      </div>
    </div>
  )
}
