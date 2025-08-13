import React, { useEffect, useState } from 'react'

export default function NearbyMap() {
  const [coords, setCoords] = useState<{ lat: number; lon: number } | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!navigator.geolocation) {
      setError('Geolocation not supported')
      return
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => setCoords({ lat: pos.coords.latitude, lon: pos.coords.longitude }),
      () => setError('Location permission denied')
    )
  }, [])

  const mapsUrl = coords
    ? `https://www.google.com/maps/search/?api=1&query=colleges&query_place_id=&center=${coords.lat},${coords.lon}`
    : 'https://www.google.com/maps/search/?api=1&query=colleges+near+me'

  return (
    <div className="bg-white rounded-2xl shadow-xl p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-lg font-semibold text-gray-900">Colleges Near You</h3>
        <a
          className="text-sm text-blue-600 hover:underline"
          href={mapsUrl}
          target="_blank"
          rel="noreferrer"
        >
          Open in Maps
        </a>
      </div>
      <div className="text-sm text-gray-600">
        {coords ? (
          <span>
            Showing results near {coords.lat.toFixed(3)}, {coords.lon.toFixed(3)}
          </span>
        ) : (
          <span>{error || 'Fetching your location…'}</span>
        )}
      </div>
    </div>
  )
}


