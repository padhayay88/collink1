import React from 'react'

export function ListSkeleton({ count = 6 }: { count?: number }) {
  return (
    <div className="space-y-4">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="animate-pulse bg-white rounded-2xl shadow-md p-4">
          <div className="h-5 w-2/3 bg-gray-200 rounded mb-3" />
          <div className="h-4 w-1/2 bg-gray-100 rounded mb-2" />
          <div className="h-3 w-full bg-gray-100 rounded mb-2" />
          <div className="h-3 w-5/6 bg-gray-100 rounded" />
        </div>
      ))}
    </div>
  )
}

export function SummarySkeleton({ boxes = 6 }: { boxes?: number }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {Array.from({ length: boxes }).map((_, i) => (
        <div key={i} className="animate-pulse border rounded-xl p-4 bg-white">
          <div className="h-4 w-1/2 bg-gray-200 rounded mb-3" />
          <div className="h-3 w-1/3 bg-gray-100 rounded mb-2" />
          <div className="flex items-center gap-3">
            <div className="h-3 w-16 bg-gray-100 rounded" />
            <div className="h-3 w-16 bg-gray-100 rounded" />
            <div className="h-3 w-16 bg-gray-100 rounded" />
          </div>
        </div>
      ))}
    </div>
  )
}

// Compact skeletons suitable for AI recommendations list while loading
export function AIDenseSkeleton({ count = 6 }: { count?: number }) {
  return (
    <div className="space-y-4">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="animate-pulse bg-white rounded-xl shadow border border-gray-100 p-5">
          <div className="flex items-start justify-between mb-3">
            <div className="space-y-2 w-2/3">
              <div className="h-5 bg-gray-200 rounded w-3/4" />
              <div className="h-4 bg-gray-100 rounded w-1/2" />
            </div>
            <div className="h-8 w-24 bg-gray-200 rounded" />
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div className="h-10 bg-gray-100 rounded" />
            <div className="h-10 bg-gray-100 rounded" />
            <div className="h-10 bg-gray-100 rounded" />
          </div>
          <div className="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-2">
            <div className="h-7 bg-gray-100 rounded" />
            <div className="h-7 bg-gray-100 rounded" />
          </div>
        </div>
      ))}
    </div>
  )
}
