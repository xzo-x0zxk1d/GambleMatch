import { NextResponse } from "next/server";
import store from "@/app/lib/store";

export async function GET() {
  return NextResponse.json(store.shop);
}
