import React, { useEffect, useState } from 'react'
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts'
import api, { TrendPoint } from '../lib/api'

interface TrendChartProps {
  collegeName: string
  exam: string
}

export default function TrendChart({ collegeName, exam }: TrendChartProps) {
  const [data, setData] = useState<TrendPoint[]>([])
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState<boolean>(false)

  useEffect(() => {
    let mounted = true
    setLoading(true)
    api.getRankTrends(collegeName, exam, 5)
      .then((res) => {
        if (!mounted) return
        const sorted = [...res.trends].sort((a, b) => a.year - b.year)
        setData(sorted)
      })
      .catch((e) => setError(e.message || 'Failed to load trends'))
      .finally(() => setLoading(false))
    return () => { mounted = false }
  }, [collegeName, exam])

  if (loading) {
    return <div className="text-sm text-gray-500">Loading trends…</div>
  }
  if (error) {
    return <div className="text-sm text-red-600">{error}</div>
  }
  if (!data.length) {
    return <div className="text-sm text-gray-500">No trend data</div>
  }

  return (
    <div className="w-full h-64">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="year" tick={{ fontSize: 12 }} />
          <YAxis tick={{ fontSize: 12 }} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="opening_rank" stroke="#4f46e5" name="Opening Rank" strokeWidth={2} dot={{ r: 2 }} />
          <Line type="monotone" dataKey="closing_rank" stroke="#9333ea" name="Closing Rank" strokeWidth={2} dot={{ r: 2 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}


