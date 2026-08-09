import { TelegramClient } from "teleproto";
import { StringSession } from "teleproto/sessions";

function required(name) {
  const value = process.env[name];
  if (!value) throw new Error(`Missing environment variable: ${name}`);
  return value;
}

async function readStdin() {
  let data = "";
  for await (const chunk of process.stdin) data += chunk;
  return JSON.parse(data || "{}");
}

function isoFromUnix(value) {
  if (!value) return null;
  return new Date(Number(value) * 1000).toISOString();
}

const task = await readStdin();
const apiId = Number(required("TELEGRAM_API_ID"));
const apiHash = required("TELEGRAM_API_HASH");
const sessionValue = required("TELEGRAM_STRING_SESSION");
const channels = (process.env.TELEGRAM_CHANNELS || "")
  .split(",")
  .map((x) => x.trim())
  .filter(Boolean);

if (!channels.length) {
  throw new Error("TELEGRAM_CHANNELS must contain at least one public/accessible channel");
}

const client = new TelegramClient(new StringSession(sessionValue), apiId, apiHash, {
  connectionRetries: 5,
});

await client.connect();

const query = (task.topics || []).filter(Boolean).join(" ") || task.question || "";
const maxItems = Math.max(1, Number(task.max_items || 50));
const perChannel = Math.max(1, Math.ceil(maxItems / channels.length));
const fromTs = task.date_from ? Date.parse(task.date_from) : null;
const toDate = task.date_to ? new Date(task.date_to) : undefined;
const out = [];

try {
  for (const channel of channels) {
    if (out.length >= maxItems) break;

    const messages = await client.getMessages(channel, {
      limit: perChannel,
      search: query || undefined,
      offsetDate: toDate,
    });

    for (const message of messages) {
      if (!message || !message.message) continue;
      const publishedAt = isoFromUnix(message.date);
      if (fromTs && publishedAt && Date.parse(publishedAt) < fromTs) continue;

      const username = channel.replace(/^https?:\/\/t\.me\//, "").replace(/^@/, "");
      const messageId = String(message.id);
      const publicUrl = /^[-\d]+$/.test(username)
        ? null
        : `https://t.me/${username}/${messageId}`;

      out.push({
        chat_id: String(channel),
        message_id: messageId,
        text: message.message,
        chat_title: String(channel),
        author: null,
        published_at: publishedAt,
        url: publicUrl,
        metadata: {
          transport: "teleproto",
          views: message.views ?? null,
          forwards: message.forwards ?? null,
          grouped_id: message.groupedId ? String(message.groupedId) : null,
          reply_to_msg_id: message.replyTo?.replyToMsgId ?? null,
        },
      });

      if (out.length >= maxItems) break;
    }
  }
} finally {
  await client.disconnect();
}

process.stdout.write(JSON.stringify(out));
