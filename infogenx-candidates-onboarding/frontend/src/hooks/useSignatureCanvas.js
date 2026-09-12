import { useEffect, useRef, useState } from 'react'

function useSignatureCanvas() {
  const canvasRef = useRef(null)
  const [isSigned, setIsSigned] = useState(false)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const context = canvas.getContext('2d')
    context.lineWidth = 2.5
    context.lineCap = 'round'
    context.strokeStyle = '#00123C'

    let drawing = false

    const start = (event) => {
      drawing = true
      context.beginPath()
      const { x, y } = getEventPosition(event, canvas)
      context.moveTo(x, y)
    }

    const draw = (event) => {
      if (!drawing) return
      const { x, y } = getEventPosition(event, canvas)
      context.lineTo(x, y)
      context.stroke()
      setIsSigned(true)
    }

    const stop = () => {
      drawing = false
    }

    const getEventPosition = (event, canvasElement) => {
      const rect = canvasElement.getBoundingClientRect()
      const pointer = event.touches ? event.touches[0] : event
      return {
        x: pointer.clientX - rect.left,
        y: pointer.clientY - rect.top,
      }
    }

    canvas.addEventListener('mousedown', start)
    canvas.addEventListener('mousemove', draw)
    canvas.addEventListener('mouseup', stop)
    canvas.addEventListener('mouseleave', stop)
    canvas.addEventListener('touchstart', start, { passive: true })
    canvas.addEventListener('touchmove', draw, { passive: true })
    canvas.addEventListener('touchend', stop)

    return () => {
      canvas.removeEventListener('mousedown', start)
      canvas.removeEventListener('mousemove', draw)
      canvas.removeEventListener('mouseup', stop)
      canvas.removeEventListener('mouseleave', stop)
      canvas.removeEventListener('touchstart', start)
      canvas.removeEventListener('touchmove', draw)
      canvas.removeEventListener('touchend', stop)
    }
  }, [])

  const clearCanvas = () => {
    const canvas = canvasRef.current
    if (!canvas) return
    const context = canvas.getContext('2d')
    context.clearRect(0, 0, canvas.width, canvas.height)
    setIsSigned(false)
  }

  return { canvasRef, clearCanvas, isSigned }
}

export default useSignatureCanvas
