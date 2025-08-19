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
        {/* Head bobbing */}
        <motion.div
          initial={{ scale: 0.95, y: 0, rotate: 0 }}
          animate={{
            scale: [0.95, 1, 0.95],
            y: [0, -1.5, 0, 1.5, 0],
            rotate: [0, -1.2, 0, 1.2, 0],
          }}
          transition={{ repeat: Infinity, duration: 3.2, ease: 'easeInOut' }}
          className="relative w-9 h-9 rounded-full bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center text-white overflow-hidden"
        >
          {src ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={src} alt="Chatbot Avatar" className="w-full h-full object-cover" />
          ) : (
            <>
              <Bot className="w-5 h-5 opacity-90" />
              {/* Eyes (blink) */}
              <motion.div
                aria-hidden
                className="absolute inset-0 flex items-center justify-center"
                initial={{ opacity: 0.9 }}
                animate={{ opacity: [0.9, 1, 0.9] }}
                transition={{ repeat: Infinity, duration: 2.8, ease: 'easeInOut' }}
              >
                <div className="relative w-6 h-3">
                  <motion.span
                    className="absolute left-0 top-1/2 -translate-y-1/2 w-1.5 h-1.5 bg-white rounded-full shadow"
                    animate={{ scaleY: [1, 0.1, 1] }}
                    transition={{ repeat: Infinity, duration: 0.12, repeatDelay: 2.6 }}
                  />
                  <motion.span
                    className="absolute right-0 top-1/2 -translate-y-1/2 w-1.5 h-1.5 bg-white rounded-full shadow"
                    animate={{ scaleY: [1, 0.1, 1] }}
                    transition={{ repeat: Infinity, duration: 0.12, repeatDelay: 2.6, delay: 0.02 }}
                  />
                </div>
              </motion.div>
              {/* Mouth pulse */}
              <motion.div
                aria-hidden
                className="absolute bottom-[6px] w-3 h-[2px] rounded-full bg-white/80"
                animate={{ scaleX: [0.6, 1, 0.6] }}
                transition={{ repeat: Infinity, duration: 2.4, ease: 'easeInOut' }}
              />
            </>
          )}
        </motion.div>
      </div>
    </div>
  )
}
