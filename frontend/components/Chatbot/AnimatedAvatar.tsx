import { motion } from 'framer-motion'
import { Bot } from 'lucide-react'

export default function AnimatedAvatar({ src }: { src?: string }) {
  return (
    <div className="relative w-12 h-12">
      {/* Animated gradient ring */}
      <motion.div
        className="absolute inset-0 rounded-full bg-gradient-to-tr from-blue-500 via-purple-500 to-pink-500"
        animate={{ rotate: 360 }}
        transition={{ repeat: Infinity, duration: 6, ease: 'linear' }}
        style={{ filter: 'blur(6px)', opacity: 0.6 }}
      />
      <div className="absolute inset-[3px] rounded-full bg-white flex items-center justify-center shadow-md">
        <motion.div
          initial={{ scale: 0.95 }}
          animate={{ scale: [0.95, 1, 0.95] }}
          transition={{ repeat: Infinity, duration: 2.2, ease: 'easeInOut' }}
          className="w-9 h-9 rounded-full bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center text-white overflow-hidden"
        >
          {src ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={src} alt="Chatbot Avatar" className="w-full h-full object-cover" />
          ) : (
            <Bot className="w-5 h-5" />
          )}
        </motion.div>
      </div>
    </div>
  )
}
