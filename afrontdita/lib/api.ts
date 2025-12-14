export async function getMerchants(): Promise<string[]> {
    try {
        const response = await fetch('http://localhost:7000/merchants', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            // If the API expects a body, we can add it here.
            // Based on "retrieves a list of merchants", it might not need one,
            // but usually POST implies some payload or action.
            // Since no payload was specified, we'll send an empty object or nothing.
            // We'll trust the user's instruction that it's a simple retrieval via POST.
        })

        if (!response.ok) {
            throw new Error('Failed to fetch merchants')
        }

        const data = await response.json()
        return data
    } catch (error) {
        console.error('Error fetching merchants:', error)
        return []
    }
}

export async function sendQuery(merchantId: string, message: string, context: string): Promise<string> {
    try {
        const response = await fetch('http://127.0.0.1:7000/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt_msg: message,
                context: context,
                merchant_id: merchantId,
            }),
        })

        if (!response.ok) {
            throw new Error('Failed to fetch query response')
        }

        const data = await response.json()
        return data.response
    } catch (error) {
        console.error('Error sending query:', error)
        return "I'm sorry, I couldn't process your request at the moment."
    }
}
