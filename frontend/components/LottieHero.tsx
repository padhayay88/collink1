import React, { useEffect, useState } from 'react'
import Lottie, { LottieRefCurrentProps } from 'lottie-react'

export default function LottieHero() {
  const [animationData, setAnimationData] = useState<any | null>(null)

  useEffect(() => {
    let mounted = true
    fetch('/animations/hero.json')
      .then((res) => res.json())
      .then((data) => {
        if (mounted) setAnimationData(data)
      })
      .catch(() => {})
    return () => {
      mounted = false
    }
  }, [])

  if (!animationData) return null

  return (
    <div className="w-full flex items-center justify-center">
      <Lottie
        animationData={animationData}
        loop
        autoplay
        style={{ width: '100%', maxWidth: 360, height: 'auto' }}
      />
    </div>
  )
}
