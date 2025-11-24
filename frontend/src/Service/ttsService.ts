export async function textToSpeech(text: string): Promise<Blob> {
  const apiKey = import.meta.env.VITE_OPENAI_API_KEY;

  const res = await fetch("https://api.openai.com/v1/audio/speech", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model: "gpt-4o-mini-tts",
      voice: "alloy",
      input: text,
      format: "mp3",
    }),
  });

  if (!res.ok) throw new Error("TTS failed");

  return await res.blob();
}
