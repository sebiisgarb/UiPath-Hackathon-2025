export const parseAIReply = (text: string) => {
  return {
    airports: Array.from(text.matchAll(/\b([A-Z]{3})\b/g)).map((m) => m[1]),
    dates: Array.from(
      text.matchAll(/\b(\d{1,2}[-\/.]\d{1,2}[-\/.]\d{4})\b/g)
    ).map((m) => m[1]),
    travelers: (() => {
      const match = text.match(
        /\b(\d+)\s*(adulți|adulti|persoane|pers|oameni)\b/i
      );
      return match ? parseInt(match[1]) : null;
    })(),
    flightChoice: (() => {
      const match = text.match(/zbor\s*(\d+)/i);
      return match ? parseInt(match[1]) : null;
    })(),
    hotelChoice: (() => {
      const match = text.match(/hotel\s*(\d+)/i);
      return match ? parseInt(match[1]) : null;
    })(),
    budget: (() => {
      const match = text.match(/\b(\d{2,5})\s*(eur|euro|lei|ron)\b/i);
      return match ? { amount: match[1], currency: match[2] } : null;
    })(),
  };
};
