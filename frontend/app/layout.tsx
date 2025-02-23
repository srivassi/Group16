import type { Metadata } from 'next';
import { ClerkProvider, SignedIn, SignedOut, UserButton, SignInButton, SignUpButton } from '@clerk/nextjs';
import Link from "next/link";
import './globals.css';

export const metadata: Metadata = {
  title: 'SentiMetrics',
  description: 'A HackIreland project',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body className="bg-gradient-to-b from-white to-gray-100 font-[Poppins]">
          {/* Header */}
          <header className="flex justify-between items-center p-4 gap-4 h-16 bg-white shadow-md">
            <h1 className="text-xl font-bold text-[#202A41] cursor-pointer">
              <Link href="/">SentiMetrics</Link>
            </h1>
            <div>
              <SignedOut>
                <SignInButton />
                <SignUpButton />
              </SignedOut>
              <SignedIn>
                <UserButton />
              </SignedIn>
            </div>
          </header>

          {/* Main Content */}
          <main className="min-h-screen">{children}</main>

          {/* Footer */}
          <footer className="relative w-full bg-gray-800 text-[#E3E7EA] p-4 mt-10 flex justify-center items-center">
            <nav className="flex space-x-4">
              <a href="/about" className="hover:underline">About</a>
              <a href="https://github.com/srivassi/Group16" target="_blank" rel="noopener noreferrer" className="hover:underline">Look Under the Hood</a>
            </nav>
          </footer>
        </body>
      </html>
    </ClerkProvider>
  );
}
