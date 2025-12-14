"use client"

import { useState, useEffect } from "react"
import { SearchPage } from "@/components/search-page"
import { ChatPage } from "@/components/chat-page"
import { getMerchants } from "@/lib/api"

export default function Home() {
  const [selectedMerchant, setSelectedMerchant] = useState<string | null>(null)
  const [merchants, setMerchants] = useState<string[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchMerchants = async () => {
      try {
        const data = await getMerchants()
        setMerchants(data)
      } catch (error) {
        console.error("Failed to load merchants", error)
      } finally {
        setIsLoading(false)
      }
    }

    fetchMerchants()
  }, [])

  const handleMerchantSelect = (merchantName: string) => {
    setSelectedMerchant(merchantName)
  }

  const handleBackToSearch = () => {
    setSelectedMerchant(null)
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="animate-pulse flex flex-col items-center">
          <div className="w-12 h-12 bg-primary/20 rounded-full mb-4"></div>
          <div className="text-muted-foreground">Loading...</div>
        </div>
      </div>
    )
  }

  return (
    <main className="min-h-screen bg-background">
      {!selectedMerchant ? (
        <SearchPage merchants={merchants} onMerchantSelect={handleMerchantSelect} />
      ) : (
        <ChatPage merchantName={selectedMerchant} onBack={handleBackToSearch} />
      )}
    </main>
  )
}
