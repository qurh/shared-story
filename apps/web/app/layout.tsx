import type { Metadata } from "next";
import { Manrope, Noto_Serif_SC } from "next/font/google";
import "./globals.css";

const bodyFont = Manrope({
  subsets: ["latin"],
  variable: "--font-body"
});

const headingFont = Noto_Serif_SC({
  subsets: ["latin"],
  weight: ["500", "700"],
  variable: "--font-heading"
});

export const metadata: Metadata = {
  title: "shared-story",
  description: "Agent-first shared narrative content platform",
  keywords: ["shared-story", "AI", "story", "discussion", "agent"]
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN">
      <body className={`${bodyFont.variable} ${headingFont.variable}`}>{children}</body>
    </html>
  );
}
