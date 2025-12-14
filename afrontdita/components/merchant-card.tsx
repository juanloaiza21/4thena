
"use client"

import { Card, CardContent } from "@/components/ui/card"
import { ChevronRight } from "lucide-react"

interface MerchantCardProps {
  merchantName: string
  onClick: () => void
}

export function MerchantCard({ merchantName, onClick }: MerchantCardProps) {
  // Generate a consistent color based on the name for the avatar background
  const getInitial = (name: string) => name.charAt(0).toUpperCase()

  return (
    <Card
      onClick={onClick}
      className="cursor-pointer hover:shadow-md transition-all duration-300 border-border group"
    >
      <CardContent className="p-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center text-primary font-semibold text-lg shrink-0">
            {getInitial(merchantName)}
          </div>
          <div>
            <h3 className="font-semibold text-lg text-foreground group-hover:text-primary transition-colors">
              {merchantName}
            </h3>
            {/*       <div className="text-xs text-muted-foreground">Volume</div> */}
            {/*       <div className="text-sm font-semibold text-foreground truncate">{merchant.stats.volume}</div> */}
            {/*     </div> */}
            {/*   </div> */}
            {/**/}
            {/*   <div className="flex items-center gap-2"> */}
            {/*     <TrendingUp className="h-4 w-4 text-primary shrink-0" /> */}
            {/*     <div className="min-w-0"> */}
            {/*       <div className="text-xs text-muted-foreground">Avg Ticket</div> */}
            {/*       <div className="text-sm font-semibold text-foreground truncate">{merchant.stats.avgTicket}</div> */}
            {/*     </div> */}
            {/*   </div> */}
            {/* </div> */}
          </div>

          <ChevronRight className="h-5 w-5 text-muted-foreground group-hover:text-primary group-hover:translate-x-1 transition-all shrink-0 mt-1" />
        </div>
      </CardContent>
    </Card>
  )
}
