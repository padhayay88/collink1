import { motion } from 'framer-motion'
import React from 'react'

/*
  Lightweight 3D-like animated backdrop using CSS 3D transforms + Framer Motion.
  - No external 3D libs, keeps bundle small
  - Works well behind hero content
*/

const floatingVariants = {
  initial: {
    opacity: 0,
    rotateX: -15,
    rotateY: 25,
    z: 0,
    scale: 0.9,
    y: 20,
    transitionEnd: { zIndex: 0 }
  },
  animate: {
    opacity: 0.75,
    rotateX: 15,
    rotateY: -25,
    z: 0,
    scale: 1,
    y: -20,
    transition: {
      duration: 6,
      ease: 'easeInOut',
      repeat: Infinity,
      repeatType: 'reverse' as const
    }
  }
} as const

function GlowSphere({ className, delay = 0 }: { className?: string; delay?: number }) {
  return (
    <motion.div
      className={`absolute rounded-full blur-2xl will-change-transform ${className || ''}`}
      variants={floatingVariants}
      initial="initial"
      animate={{ ...floatingVariants.animate, transition: { ...floatingVariants.animate.transition, delay } }}
      style={{
        transformStyle: 'preserve-3d',
        background:
          'radial-gradient(closest-side, rgba(255,255,255,0.8), rgba(255,255,255,0.15) 60%, rgba(255,255,255,0) 70%)'
      }}
    />
  )
}

function WireCube({ className, delay = 0 }: { className?: string; delay?: number }) {
  return (
    <motion.div
      className={`absolute will-change-transform ${className || ''}`}
      initial={{ opacity: 0, rotateX: 0, rotateY: 0, scale: 0.9 }}
      animate={{
        opacity: 0.9,
        rotateX: 360,
        rotateY: 360,
        scale: 1,
        transition: { duration: 20, delay, ease: 'linear', repeat: Infinity }
      }}
      style={{ transformStyle: 'preserve-3d' }}
    >
      <div className="absolute inset-0 rounded-xl border border-white/30" />
      <div className="absolute inset-2 rounded-xl border border-white/20" />
      <div className="absolute inset-4 rounded-xl border border-white/10" />
    </motion.div>
  )
}

export default function ThreeDBackdrop() {
  return (
    <div
      aria-hidden
      className="absolute inset-0 pointer-events-none [perspective:1000px]"
      style={{ contain: 'layout paint' }}
    >
      {/* Large soft glows */}
      <GlowSphere className="w-64 h-64 top-10 -left-8 bg-blue-400/30" delay={0.2} />
      <GlowSphere className="w-72 h-72 -bottom-8 right-10 bg-purple-400/30" delay={0.6} />
      <GlowSphere className="w-40 h-40 top-1/3 right-1/3 bg-cyan-300/30" delay={1.1} />

      {/* Rotating wireframe cubes */}
      <WireCube className="w-48 h-48 top-6 right-6" delay={0.3} />
      <WireCube className="w-56 h-56 bottom-8 left-10" delay={0.9} />
    </div>
  )
}
