export async function speechToText(audio: Blob): Promise<string> {
  const apiKey = import.meta.env.VITE_OPENAI_API_KEY;

  const fd = new FormData();
  fd.append("file", audio, "audio.webm");
  fd.append("model", "whisper-1"); // 🟦 MODEL STABIL VOCE
  fd.append("language", "ro"); // 🇷🇴 LIMBA ROMÂNĂ

  const res = await fetch("https://api.openai.com/v1/audio/transcriptions", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
    },
    body: fd,
  });

  if (!res.ok) {
    console.error(await res.text());
    throw new Error("STT failed");
  }

  const data = await res.json();
  return data.text;
}
