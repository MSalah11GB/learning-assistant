import type { ReactNode } from "react";
import { ClerkProvider } from "@clerk/nextjs";

import "./globals.css";

export const metadata = {
  title: "Learning Assistant",
  description: "Adaptive study assistant scaffold",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <ClerkProvider signInUrl="/login" signUpUrl="/signup" afterSignInUrl="/dashboard" afterSignUpUrl="/dashboard">
      <html lang="en">
        <body>{children}</body>
      </html>
    </ClerkProvider>
  );
}
