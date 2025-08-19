import React, { useEffect, useState } from 'react'
import api from '../lib/api'
import { toast } from 'react-hot-toast'

interface SaveCompareBarProps {
  userId: string
}

export default function SaveCompareBar({ userId }: SaveCompareBarProps) {
  const [saved, setSaved] = useState<string[]>([])

  const refresh = async () => {
    try {
      const res = await api.listSaved(userId)
      setSaved(res.colleges)
      try {
        localStorage.setItem('saved.colleges', JSON.stringify(res.colleges))
      } catch {}
    } catch {}
  }

  useEffect(() => {
    // Initial load: try localStorage first for instant UI, then refresh from API
    try {
      const cached = localStorage.getItem('saved.colleges')
      if (cached) setSaved(JSON.parse(cached))
    } catch {}
    refresh()

    // Cross-tab sync
    const onStorage = (e: StorageEvent) => {
      if (e.key === 'saved.colleges' && e.newValue) {
        try {
          const list = JSON.parse(e.newValue)
          setSaved(list)
        } catch {}
      }
    }
    window.addEventListener('storage', onStorage)
    return () => window.removeEventListener('storage', onStorage)
  }, [])

  return (
    <div className="fixed bottom-4 left-1/2 -translate-x-1/2 z-40">
      <div className="bg-white shadow-xl rounded-full px-5 py-3 flex items-center gap-4 border border-gray-200">
        <span className="text-sm text-gray-700 font-medium">Saved: {saved.length}</span>
        <button className="text-sm px-3 py-1.5 rounded-full bg-gray-100 hover:bg-gray-200" onClick={refresh}>Refresh</button>
        <button
          className="text-sm px-3 py-1.5 rounded-full bg-gradient-to-r from-blue-600 to-purple-600 text-white"
          onClick={async () => {
            if (saved.length < 2) return
            const names = saved.slice(0, 4)
            const q = encodeURIComponent(names.join(','))
            const url = `/compare?colleges=${q}`
            window.open(url, '_blank')
            toast.success('Opened compare for saved colleges')
          }}
        >
          Compare
        </button>
      </div>
    </div>
  )
}


