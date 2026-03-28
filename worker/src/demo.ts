import Anthropic from '@anthropic-ai/sdk';

// Rate limit: max requests per IP per hour
export const DEMO_RATE_LIMIT = 20;
const RATE_WINDOW_SECONDS = 3600;
const MAX_MESSAGES = 12; // max conversation turns
const MAX_TOKENS = 512; // per response

const SYSTEM_PROMPT = `You are Milo, an AI health coach built by Baseline. This is a live demo on the landing page. Run the real onboarding flow, not a generic chat.

## Your Opening (first message)

Lead with proof, then the goal menu. Keep it tight for a chat widget:

"Hey, I'm Milo. I'm a health coach that runs on your actual data.

We've helped people lose real weight, fix their sleep, catch conditions they didn't know they had, and build habits that stick. The results grow every day.

You pick one outcome, focus on it for 14 days, lock it in, then layer the next one.

Where would you want to start?

1. Sleep & Recovery
2. Body & Weight
3. Energy & Mind
4. Know My Numbers"

## Flow after they pick

**Step 1 - Branch down.** Based on their pick, offer 2-3 specific sub-goals. Example for Sleep: "Are you mainly looking to sleep better (more consistent, longer, wake up rested) or manage stress (calmer evenings, wind down)?"

**Step 2 - Diagnostic conversation.** Once you have their specific goal, ask about their current situation. One question at a time. This is a conversation, not a form. Find the first gap: the thing they're not doing that would make the biggest difference. Examples: "What time do you usually wake up? Is it consistent?" or "How much protein do you think you're getting daily?"

**Step 3 - Program pitch.** When you've found the gap, pitch ONE anchor habit for a 14-day block. Structure: reflect their situation back, name the one habit, give 1-2 supporting tips. Example: "Here's what I'd start you on: 6 AM wake time, every day, no exceptions. Two things that make it easier: bedtime by 10:30, and morning sunlight within 30 minutes. For 14 days, the only thing I'll ask you each morning is: did you get up at 6?"

**Step 4 - Transition to signup.** After the pitch: "That's what coaching with me looks like. Sign up below and we pick up right here. I'll text you tomorrow morning." Don't push. They just experienced the product.

## Rules

- 2-3 sentences per response. This is a chat widget, not WhatsApp.
- One question at a time. Never two questions in one message.
- No emojis.
- Connect things to the bigger picture. Poor sleep affects recovery, which affects training, which affects body comp. That kind of systems thinking is your edge.
- Use real numbers: "Most adults get 50-70% less protein than optimal." "Sleep under 6 hours doubles metabolic disease risk."
- Don't ask for PII (full name, email, phone, address).
- Don't diagnose conditions or prescribe medications.
- If they share something sensitive, acknowledge it warmly and note that a private coaching session after signup is the right place for that.
- Don't pretend you have their data. You don't. This is a demo.
- Your personality: the coach who reads the labs, notices patterns, and tells it straight. Smart friend who knows exercise science, not an AI assistant.`;

export async function handleDemoChat(
  client: Anthropic,
  request: Request,
  logs: KVNamespace,
  ip: string,
): Promise<Response> {
  // Rate limit check
  const rateKey = `demo-rate/${ip}/${Math.floor(Date.now() / (RATE_WINDOW_SECONDS * 1000))}`;
  const currentCount = parseInt((await logs.get(rateKey)) || '0');
  if (currentCount >= DEMO_RATE_LIMIT) {
    return Response.json(
      { error: 'Rate limit exceeded. Try again in a bit.' },
      { status: 429 },
    );
  }

  // Increment rate counter
  await logs.put(rateKey, String(currentCount + 1), {
    expirationTtl: RATE_WINDOW_SECONDS,
  });

  // Parse request
  let body: { messages: Array<{ role: string; content: string }> };
  try {
    body = await request.json() as typeof body;
  } catch {
    return Response.json({ error: 'Invalid JSON' }, { status: 400 });
  }

  if (!Array.isArray(body.messages) || body.messages.length === 0) {
    return Response.json({ error: 'messages array required' }, { status: 400 });
  }

  // Cap conversation length
  const messages = body.messages.slice(-MAX_MESSAGES).map((m) => ({
    role: m.role as 'user' | 'assistant',
    content: String(m.content).slice(0, 1000), // cap per-message length
  }));

  try {
    const start = Date.now();
    const response = await client.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: MAX_TOKENS,
      system: SYSTEM_PROMPT,
      messages,
    });

    const duration = Date.now() - start;
    const text =
      response.content[0]?.type === 'text' ? response.content[0].text : '';

    // Log for monitoring (no PII, just message count + duration)
    const logId = `demo/${Date.now()}-${crypto.randomUUID().slice(0, 8)}`;
    await logs.put(
      logId,
      JSON.stringify({
        ip_hash: await hashIP(ip),
        message_count: messages.length,
        duration_ms: duration,
        input_tokens: response.usage?.input_tokens,
        output_tokens: response.usage?.output_tokens,
        timestamp: new Date().toISOString(),
      }),
      { expirationTtl: 30 * 24 * 60 * 60 },
    );

    return Response.json({ reply: text, duration_ms: duration });
  } catch (err) {
    console.error('Demo chat error:', err);
    return Response.json(
      { error: 'Something went wrong. Try again.' },
      { status: 500 },
    );
  }
}

const SUMMARY_PROMPT = `Extract structured coaching context from this demo conversation. Return ONLY valid JSON, no markdown, no explanation.

Format:
{
  "domains": ["sleep", "labs", "nutrition", etc - health domains they mentioned or care about],
  "goals": ["lose weight", "sleep better", etc - what they want to achieve],
  "context": ["trains 3x/week", "has recent labs", etc - relevant facts they shared],
  "primary_concern": "one sentence summary of their main focus"
}

If the conversation is too short or off-topic, return: {"domains":[],"goals":[],"context":[],"primary_concern":""}`;

export async function handleDemoSummary(
  client: Anthropic,
  request: Request,
): Promise<Response> {
  let body: { messages: Array<{ role: string; content: string }> };
  try {
    body = (await request.json()) as typeof body;
  } catch {
    return Response.json({ error: 'Invalid JSON' }, { status: 400 });
  }

  if (!Array.isArray(body.messages) || body.messages.length < 2) {
    return Response.json({ summary: { domains: [], goals: [], context: [], primary_concern: '' } });
  }

  // Build transcript for extraction
  const transcript = body.messages
    .map((m) => `${m.role}: ${m.content}`)
    .join('\n');

  try {
    const response = await client.messages.create({
      model: 'claude-haiku-4-5-20251001',
      max_tokens: 256,
      messages: [
        { role: 'user', content: `${SUMMARY_PROMPT}\n\nConversation:\n${transcript}` },
      ],
    });

    let text = response.content[0]?.type === 'text' ? response.content[0].text : '{}';
    // Strip markdown code fences if present
    text = text.replace(/```json?\s*/g, '').replace(/```\s*/g, '').trim();
    const summary = JSON.parse(text);
    return Response.json({ summary });
  } catch (err) {
    console.error('Summary extraction error:', err);
    return Response.json({ summary: { domains: [], goals: [], context: [], primary_concern: '' } });
  }
}

// Hash IP for logging without storing raw IPs
async function hashIP(ip: string): Promise<string> {
  const encoder = new TextEncoder();
  const data = encoder.encode(ip + 'baseline-demo-salt');
  const hash = await crypto.subtle.digest('SHA-256', data);
  return Array.from(new Uint8Array(hash).slice(0, 8))
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('');
}
