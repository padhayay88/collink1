import React, { useEffect, useState } from 'react'
import api from '../lib/api'

interface SaveCompareBarProps {
  userId: string
}

export default function SaveCompareBar({ userId }: SaveCompareBarProps) {
  const [saved, setSaved] = useState<string[]>([])

  const refresh = async () => {
    try {
      const res = await api.listSaved(userId)
      setSaved(res.colleges)
    } catch {}
  }

  useEffect(() => { refresh() }, [])

  return (
    <div className="fixed bottom-4 left-1/2 -translate-x-1/2 z-40">
      <div className="bg-white shadow-xl rounded-full px-5 py-3 flex items-center gap-4 border border-gray-200">
        <span className="text-sm text-gray-700 font-medium">Saved: {saved.length}</span>
        <button className="text-sm px-3 py-1.5 rounded-full bg-gray-100 hover:bg-gray-200" onClick={refresh}>Refresh</button>
        <button
          className="text-sm px-3 py-1.5 rounded-full bg-gradient-to-r from-blue-600 to-purple-600 text-white"
          onClick={async () => {
            if (saved.length < 2) return
            const res = await api.compareColleges(saved.slice(0, 4))
            alert(JSON.stringify(res.colleges, null, 2))
          }}
        >
          Compare
        </button>
      </div>
    </div>
  )
}


