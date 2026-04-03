import type { Metadata } from "next";
import "./globals.css";
import { Geist } from "next/font/google";
import { cn } from "@/lib/utils";

const geist = Geist({subsets:['latin'],variable:'--font-sans'});

export const metadata: Metadata = {
  title: "RM Team AI",
  description:
    "AI-powered recruitment marketing analytics for Indeed Flex",
};

function NavLink({
  href,
  children,
}: {
  href: string;
  children: React.ReactNode;
}) {
  return (
    <a
      href={href}
      className="text-sm font-medium text-gray-300 hover:text-white transition-colors"
    >
      {children}
    </a>
  );
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={cn("font-sans", geist.variable)}>
      <body className="bg-gray-50 text-gray-900 antialiased">
        <nav className="bg-gray-900 text-white">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="flex h-14 items-center justify-between">
              <a href="/" className="text-lg font-bold tracking-tight">
                RM Team AI
              </a>
              <div className="flex items-center gap-6">
                <NavLink href="/dashboard">Dashboard</NavLink>
                <NavLink href="/upload">Upload</NavLink>
                <NavLink href="/tools/utm-builder">UTM Builder</NavLink>
                <NavLink href="/tools/ad-copy">Ad Copy</NavLink>
                <NavLink href="/settings/integrations">Settings</NavLink>
              </div>
            </div>
          </div>
        </nav>
        <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
          {children}
        </main>
      </body>
    </html>
  );
}
