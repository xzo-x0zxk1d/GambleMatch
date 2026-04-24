import { NextResponse } from "next/server";
import { discordFetch, MEDIA_CHANNEL } from "@/app/lib/discord";
import type { DiscordMessage } from "@/types/discord";
import type { MediaItem } from "@/types/discord";

const IMAGE_EXTS = /\.(png|jpe?g|gif|webp|avif)(\?.*)?$/i;

export async function GET() {
  try {
    const messages = await discordFetch<DiscordMessage[]>(
      `/channels/${MEDIA_CHANNEL}/messages?limit=100`
    );

    const items: MediaItem[] = [];

    for (const msg of messages) {
      // Attachments
      for (const att of msg.attachments ?? []) {
        const isImage =
          att.content_type?.startsWith("image/") ||
          IMAGE_EXTS.test(att.filename) ||
          IMAGE_EXTS.test(att.url);
        if (isImage) {
          items.push({
            id: att.id,
            url: att.url,
            proxy_url: att.proxy_url ?? att.url,
            author: msg.author,
            timestamp: msg.timestamp,
            width: att.width,
            height: att.height,
          });
        }
      }
      // Embeds with image
      for (const emb of msg.embeds ?? []) {
        if (emb.image?.url) {
          items.push({
            id: `${msg.id}_emb`,
            url: emb.image.url,
            proxy_url: emb.image.proxy_url ?? emb.image.url,
            author: msg.author,
            timestamp: msg.timestamp,
            width: emb.image.width,
            height: emb.image.height,
          });
        }
      }
    }

    return NextResponse.json(items);
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
