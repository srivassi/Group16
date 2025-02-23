// app/page.tsx
import { SignedIn, SignedOut, RedirectToSignIn } from '@clerk/nextjs';
import Page from '@/app/components/landing/page';


export const metadata = {
  title: 'SentiMetrics',
  icons: {
    icon: '/vercel.svg',
  },
};

export default function HomePage() {
  return (
    <div>
      <SignedIn>
        <Page />
      </SignedIn>
      <SignedOut>
        <RedirectToSignIn />
      </SignedOut>
    </div>
  );
}
