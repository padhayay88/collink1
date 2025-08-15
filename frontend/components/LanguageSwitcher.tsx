import React, { useEffect, useState } from 'react'

const languages = [
  { id: 'en', label: 'English' },
  { id: 'hi', label: 'हिन्दी' },
]

export default function LanguageSwitcher() {
  const [lang, setLang] = useState<string>('en')

  useEffect(() => {
    const saved = typeof window !== 'undefined' ? localStorage.getItem('lang') : null
    if (saved) setLang(saved)
  }, [])

  useEffect(() => {
    if (typeof window !== 'undefined') localStorage.setItem('lang', lang)
    document.documentElement.lang = lang
  }, [lang])

  return (
    <div className="inline-flex rounded-lg bg-gray-100 p-1">
      {languages.map((l) => (
        <button
          key={l.id}
          onClick={() => setLang(l.id)}
          className={`px-3 py-1.5 text-sm rounded-md ${lang === l.id ? 'bg-white shadow text-gray-900' : 'text-gray-600'}`}
        >
          {l.label}
        </button>
      ))}
    </div>
  )
}


